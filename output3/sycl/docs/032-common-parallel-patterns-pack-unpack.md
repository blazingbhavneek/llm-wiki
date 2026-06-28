## Map

Owing to its simplicity, the map pattern can be implemented directly as a basic parallel kernel. The code shown in Figure 14-15 shows such an implementation, using the map pattern to compute the square root of each input element in a range.

```txt
// Compute the square root of each input value
q.parallel_for(N, [=](id<1> i) {
  output[i] = sqrt(input[i]);
}).wait();
```

Figure 14-15. Implementing the map pattern in a data-parallel kernel

## Stencil

Implementing a stencil directly as a multidimensional basic data-parallel kernel with multidimensional buffers, as shown in Figure 14-16, is straightforward and easy to understand.

```lisp
q.submit([&](handler& h) {
  accessor input{input_buf, h};
  accessor output{output_buf, h};

  // Compute the average of each cell and its immediate
  // neighbors
  h.parallel_for(stencil_range, [=](id<2> idx) {
    int i = idx[0] + 1;
    int j = idx[1] + 1;

    float self = input[i][j];
    float north = input[i - 1][j];
    float east = input[i][j + 1];
    float south = input[i + 1][j];
    float west = input[i][j - 1];
    output[i][j] =
      (self + north + east + south + west) / 5.0f;
  });
});
```

Figure 14-16. Implementing the stencil pattern in a data-parallel kernel

However, this expression of the stencil pattern is very naïve and should not be expected to perform very well. As mentioned earlier in the chapter, it is well known that leveraging locality (via spatial or temporal blocking) is required to avoid repeated reads of the same data from memory. A simple example of spatial blocking, using work-group local memory, is shown in Figure 14-17.

## Chapter 14 Common Parallel Patterns

```lisp
q.submit([&](handler& h) {
  accessor input{input_buf, h};
  accessor output{output_buf, h};

  constexpr size_t B = 4;
  range<2> local_range(B, B);
  range<2> tile_size =
    local_range +
      range<2>(2, 2);  // Includes boundary cells
  auto tile = local_accessor<float, 2>(tile_size, h);

  // Compute the average of each cell and its immediate
  // neighbors
  h.parallel_for(
    nd_range<2>(stencil_range, local_range),
    [=](nd_item<2> it) {
      // Load this tile into work-group local memory
      id<2> lid = it.get_local_id();
      range<2> lrange = it.get_local_range();
      for (int ti = lid[0]; ti < B + 2;
        ti += lrange[0]) {
        int gi = ti + B * it.get_group(0);
        for (int tj = lid[1]; tj < B + 2;
          tj += lrange[1]) {
          int gj = tj + B * it.get_group(1);
          tile[ti][tj] = input[gi][gj];
        }
      }
      group_barrier(it.get_group());

      // Compute the stencil using values from local
      // memory
      int gi = it.get_global_id(0) + 1;
      int gj = it.get_global_id(1) + 1;

      int ti = it.get_local_id(0) + 1;
      int tj = it.get_local_id(1) + 1;

      float self = tile[ti][tj];
      float north = tile[ti - 1][tj];
      float east = tile[ti][tj + 1];
      float south = tile[ti + 1][tj];
      float west = tile[ti][tj - 1];
      output[gi][gj] =
        (self + north + east + south + west) / 5.0f;
    });
});
```

Figure 14-17. Implementing the stencil pattern in an ND-range kernel, using work-group local memory

Selecting the best optimizations for a given stencil requires compiletime introspection of block size, the neighborhood, and the stencil function itself, requiring a much more sophisticated approach than discussed here.

## Reduction

It is possible to implement reduction kernels in SYCL by leveraging language features that provide synchronization and communication capabilities between work-items (e.g., atomic operations, work-group and sub-group functions, sub-group “shuffles”). The kernels in Figure 14-18 and Figure 14-19 show two possible reduction implementations: a naïve reduction using a basic parallel\_for and an atomic operation for every work-item, and a slightly smarter reduction that exploits locality using an ND-range parallel\_for and a work-group reduce function, respectively. We revisit these atomic operations in more detail in Chapter 19.

```rust
q.parallel_for(N, [=](id<1> i) {
    atomic_ref<int, memory_order::relaxed,
            memory_scope::system,
            access::address_space::global_space>(
        *sum) += data[i];
}).wait();
```

Figure 14-18. Implementing a naïve reduction expressed as a data-parallel kernel

```cpp
q.parallel_for(nd_range<1>{N, B}, [=](nd_item<1> it) {
    int i = it.get_global_id(0);
    auto grp = it.get_group();
    int group_sum =
        reduce_over_group(grp, data[i], plus<>());
    if (grp.leader()) {
        atomic_ref<int, memory_order::relaxed,
            memory_scope::system,
            access::address_space::global_space>(
                *sum) += group_sum;
    }
}).wait();
```

Figure 14-19. Implementing a naïve reduction expressed as an ND-range kernel

There are numerous other ways to write reduction kernels, and different devices will likely prefer different implementations, owing to differences in hardware support for atomic operations, work-group local memory size, global memory size, the availability of fast device-wide barriers, or even the availability of dedicated reduction instructions. On some architectures, it may even be faster (or necessary!) to perform a tree reduction using log (N) separate kernel calls.

We strongly recommend that manual implementations of reductions should only be considered for cases that are not supported by the SYCL reduction library or when fine-tuning a kernel for the capabilities of a specific device—and even then, only after being 100% sure that SYCL’s built-in reductions are underperforming!

## Scan

As we saw earlier in this chapter, implementing a parallel scan requires multiple sweeps over the data, with synchronization occurring between each sweep. Since SYCL does not provide a mechanism for synchronizing all work-items in an ND-range, a direct implementation of a device-wide scan must use multiple kernels that communicate partial results through global memory.

The code, shown in Figures 14-20, 14-21, and 14-22, demonstrates an inclusive scan implemented using several kernels. The first kernel distributes the input values across work-groups, computing work-group local scans in work-group local memory (note that we could have used the work-group inclusive\_scan function instead). The second kernel computes a local scan using a single work-group, this time over the final value from each block. The third kernel combines these intermediate results to finalize the prefix sum. These three kernels correspond to the three layers of the diagram in Figure 14-5.

```lisp
// Phase 1: Compute local scans over input blocks
q.submit([&](handler& h) {
    auto local = local_accessor<int32_t, 1>(L, h);
    h.parallel_for(nd_range<1>(N, L), [=](nd_item<1> it) {
        int i = it.get_global_id(0);
        int li = it.get_local_id(0);

        // Copy input to local memory
        local[li] = input[i];
        group_barrier(it.get_group());

        // Perform inclusive scan in local memory
        for (int32_t d = 0; d <= log2((float)L) - 1; ++d) {
            uint32_t stride = (1 << d);
            int32_t update =
                (li >= stride) ? local[li - stride] : 0;
            group_barrier(it.get_group());
            local[li] += update;
            group_barrier(it.get_group());
        }

        // Write the result for each item to the output
        // buffer Write the last result from this block to
        // the temporary buffer
        output[i] = local[li];
        if (li == it.get_local_range()[0] - 1) {
            tmp[it.get_group(0)] = local[li];
        }
    });
}).wait();
```

## Chapter 14 Common Parallel Patterns

```txt
// Phase 2: Compute scan over partial results
q.submit([&](handler& h) {
    auto local = local_accessor<int32_t, 1>(G, h);
    h.parallel_for(nd_range<1>(G, G), [=](nd_item<1> it) {
        int i = it.get_global_id(0);
        int li = it.get_local_id(0);

        // Copy input to local memory
        local[li] = tmp[i];
        group_barrier(it.get_group());

        // Perform inclusive scan in local memory
        for (int32_t d = 0; d <= log2((float)G) - 1; ++d) {
            uint32_t stride = (1 << d);
            int32_t update =
                (li >= stride) ? local[li - stride] : 0;
            group_barrier(it.get_group());
            local[li] += update;
            group_barrier(it.get_group());
        }

        // Overwrite result from each work-item in the
        // temporary buffer
        tmp[i] = local[li];
    });
}).wait();
```

Figure 14-21. Phase 2 for implementing a global inclusive scan in an ND-range kernel: scanning across the results of each work-group

```txt
// Phase 3: Update local scans using partial results
q.parallel_for(nd_range<1>(N, L), [=](nd_item<1> it) {
    int g = it.get_group(0);
    if (g > 0) {
        int i = it.get_global_id(0);
        output[i] += tmp[g - 1];
    }
}).wait();
```

Figure 14-22. Phase 3 (final) for implementing a global inclusive scan in an ND-range kernel

Figure 14-20 and Figure 14-21 are very similar; the only differences are the size of the range and how the input and output values are handled. A real-life implementation of this pattern could use a single function taking different arguments to implement these two phases, and they are only presented as distinct code here for pedagogical reasons.

## Pack and Unpack

Pack and unpack are also known as gather and scatter operations. These operations handle differences in how data is arranged in memory and how we wish to present it to the compute resources.

## Pack

Since pack depends on an exclusive scan, implementing a pack that applies to all elements of an ND-range must also take place via global memory and over the course of several kernel enqueues. However, there is a common use case for pack that does not require the operation to be applied over all elements of an ND-range—namely, applying a pack only across items in a specific work-group or sub-group.

The snippet in Figure 14-23 shows how to implement a group pack operation on top of an exclusive scan.

```txt
uint32_t index =
    exclusive_scan(g, (uint32_t)predicate, plus<>());
if (predicate) dst[index] = value;
```

Figure 14-23. Implementing a group pack operation on top of an exclusive scan

The code in Figure 14-24 demonstrates how such a pack operation could be used in a kernel to build a list of elements which require some additional postprocessing (in a future kernel). The example shown is based on a real kernel from molecular dynamics simulations: the work-items in the sub-group assigned to particle i cooperate to identify all other particles within a fixed distance of i, and only the particles in this “neighbor list” will be used to calculate the force acting on each particle.

```lisp
range<2> global(N, 8);
range<2> local(1, 8);
q.parallel_for(nd_range<2>(global, local), [=](nd_item<2>
            it) {
    int i = it.get_global_id(0);
    sub_group sg = it.get_sub_group();
    int sglid = sg.get_local_id()[0];
    int sgrange = sg.get_local_range()[0];

    uint32_t k = 0;
    for (int j = sglid; j < N; j += sgrange) {
        // Compute distance between i and neighbor j
        float r = distance(position[i], position[j]);

        // Pack neighbors that require
        // post-processing into a list
        uint32_t pack = (i != j) and (r <= CUTOFF);
        uint32_t offset =
            exclusive_scan_over_group(sg, pack, plus<>());
        if (pack) {
            neighbors[i * MAX_K + k + offset] = j;
        }

        // Keep track of how many neighbors have been
        // packed so far
        k += reduce_over_group(sg, pack, plus<>());
    }
    num_neighbors[i] =
        reduce_over_group(sg, k, maximum<>());
}).wait();
```

Figure 14-24. Using a sub-group pack operation to build a list of elements needing additional postprocessing

Note that the pack pattern never reorders elements—the elements that are packed into the output array appear in the same order as they did in the input. This property of pack is important and enables us to use pack functionality to implement other more abstract parallel algorithms (such as std::copy\_if and std::stable\_partition). However, there are other parallel algorithms that can be implemented on top of pack functionality where maintaining order is not required (such as std::partition).

## Unpack

As with pack, we can implement unpack using scan. Figure 14-25 shows how to implement a sub-group unpack operation on top of an exclusive scan.

```txt
uint32_t index =
    exclusive_scan(sg, (uint32_t)predicate, plus<>());
return (predicate) ? new_value[index] : original_value;
```

Figure 14-25. Implementing a sub-group unpack operation on top of an exclusive scan

The code in Figure 14-26 demonstrates how such a sub-group unpack operation could be used to improve load balancing in a kernel with divergent control flow (in this case, computing the Mandelbrot set). Each work-item is assigned a separate pixel to compute and iterates until convergence or a maximum number of iterations is reached. An unpack operation is then used to replace completed pixels with new pixels.

```cpp
// Keep iterating as long as one work-item has work to do
while (any_of_group(sg, i < Nx)) {
    uint32_t converged = next_iteration(
        params, i, j, count, cr, ci, zr, zi, mandelbrot);
    if (any_of_group(sg, converged)) {
        // Replace pixels that have converged using an
        // unpack. Pixels that haven't converged are not
        // replaced.
        uint32_t index = exclusive_scan_over_group(
            sg, converged, plus<>());
        i = (converged) ? iq + index : i;
        iq += reduce_over_group(sg, converged, plus<Play));

        // Reset the iterator variables for the new i
        if (converged) {
            reset(params, i, j, count, cr, ci, zr, zi);
        }
    }
}
```

Figure 14-26. Using a sub-group unpack operation to improve load balancing for kernels with divergent control flow

The degree to which an approach like this improves efficiency (and decreases execution time) is highly application- and input-dependent, since checking for completion and executing the unpack operation both introduce some overhead! Successfully using this pattern in realistic applications will therefore require some fine-tuning based on the amount of divergence present and the computation being performed (e.g., introducing a heuristic to execute the unpack operation only if the number of active work-items falls below some threshold).

## Summary

This chapter has demonstrated how to implement some of the most common parallel patterns using SYCL features, including built-in functions and libraries.

The SYCL ecosystem is still developing, and we expect to uncover new best practices for these patterns as developers gain more experience with the language and from the development of production-grade applications and libraries.

## For More Information

Structured Parallel Programming: Patterns for Efficient Computation by Michael McCool, Arch Robison, and James Reinders, © 2012, published by Morgan Kaufmann, ISBN 978-0-124-15993-8.

Algorithms library, C++ Reference, https://en.cppreference.com/w/cpp/algorithm.

![](images/260a6d3244a08f11cf46bb54dc803cc4a5d0b254c490a04894c32f0d2ad60bae.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
