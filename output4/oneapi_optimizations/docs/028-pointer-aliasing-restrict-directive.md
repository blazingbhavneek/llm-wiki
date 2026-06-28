
## Pointer Aliasing and the Restrict Directive

Kernels typically operate on arrays of elements that are provided as pointer arguments. When the compiler cannot determine whether these pointers alias each other, it will conservatively assume that they do, in which case it will not reorder operations on these pointers. Consider the following vector-add example, where each iteration of the loop has two loads and one store.

```cpp
size_t VectorAdd(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
  sycl::range num_items{a.size()};

  sycl::buffer a_buf(a);
```

```cpp
sycl::buffer b_buf(b);
sycl::buffer sum_buf(sum.data(), num_items);

auto start = std::chrono::steady_clock::now();
for (int i = 0; i < iter; i++) {
    auto e = q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(num_items,
                [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add completed on device - took " << (end - start).count()
       << " u-secs\n";
return ((end - start).count());
} // end VectorAdd
```

In this case, the programmer leaves all the choices about vector length and the number of work-groups to the compiler. In most cases the compiler does a pretty good job of selecting these parameters to get good performance. In some situations it may be better to explicitly choose the number of work-groups and workgroup sizes to get good performance and provide hints to the compiler to get better-performing code.

The kernel below is written to process multiple elements of the array per work-item and explicitly chooses the number of work-groups and work-group size. The intel::kernel\_args\_restrict on line 25 tells the compiler that the buffer accessors in this kernel do not alias each other. This will allow the compiler to hoist the loads and stores, thereby providing more time for the instructions to complete and getting better instruction scheduling. The pragma on line 27 directs the compiler to unroll the loop by a factor of two.

```cpp
size_t VectorAdd2(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    // size_t num_groups =
    // q.get_device().get_info<sycl::info::device::max_compute_units>();
    // wg_size =
    // q.get_device().get_info<sycl::info::device::max_work_group_size>();
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(
                    16)]] [[intel::kernel_args_restrict]] {
```

```cpp
size_t loc_id = index.get_local_id();
// unroll with a directive
#pragma unroll(2)
    for (size_t i = loc_id; i < mysize; i += wg_size) {
        sum_acc[i] = a_acc[i] + b_acc[i];
    }
});
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add2 completed on device - took "
       << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd2
```

The kernel below illustrates manually unrolling of the loop instead of the compiler directive (the compiler may or may not honor the directive depending on its internal heuristic cost model). The advantage of unrolling is that fewer instructions are executed because the loop does not have to iterate as many times, thereby saving on the compare and branch instructions.

```cpp
size_t VectorAdd3(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index)
                [[intel::reqd_sub_group_size(16)]] {
                    // Manual unrolling
                    size_t loc_id = index.get_local_id();
                    for (size_t i = loc_id; i < mysize; i += 32) {
                        sum_acc[i] = a_acc[i] + b_acc[i];
                        sum_acc[i + 16] = a_acc[i + 16] + b_acc[i + 16];
                    }
                });
            });
        }
        q.wait();
        auto end = std::chrono::steady_clock::now();
        std::cout << "Vector add3 completed on device - took "
               << (end - start).count() << " u-secs\n";
        return ((end - start).count());
    } // end VectorAdd3
```

The kernel below shows how to reorder the loads and stores so that all loads are issued before any operations on them are done. Typically, there can be many outstanding loads for every thread in the GPU. It is always better to issue the loads before any operations on them are done. This will allow the loads to complete before the data are actually needed for computation.

```cpp
size_t VectorAdd4(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
                [=](sycl::nd_item<1> index)
                [[intel::reqd_sub_group_size(16)]] {
                    // Manual unrolling
                    size_t loc_id = index.get_local_id();
                    for (size_t i = loc_id; i < mysize; i += 32) {
                        int t1 = a_acc[i];
                        int t2 = b_acc[i];
                        int t3 = a_acc[i + 16];
                        int t4 = b_acc[i + 16];
                        sum_acc[i] = t1 + t2;
                        sum_acc[i + 16] = t3 + t4;
                    }
                });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add4 completed on device - took "
              << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd4
```

The following kernel has a restrict directive, which provides a hint to the compiler that there is no aliasing among the vectors accessed inside the loop and the compiler can hoist the load over the store just like it was done manually in the previous example.

```cpp
size_t VectorAdd5(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    size_t num_groups = 1;
    size_t wg_size = 16;
    auto start = std::chrono::steady_clock::now();
```

```cpp
for (int i = 0; i < iter; i++) {
    q.submit([&](auto &h) {
        // Input accessors
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        // Output accessor
        sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) [[intel::reqd_sub_group_size(
                16)]] [[intel::kernel_args_restrict]] {
            // compiler needs to hoist the loads
            size_t loc_id = index.get_local_id();
            for (size_t i = loc_id; i < mysize; i += 32) {
                sum_acc[i] = a_acc[i] + b_acc[i];
                sum_acc[i + 16] = a_acc[i + 16] + b_acc[i + 16];
            }
        });
    });
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add5 completed on device - took "
           << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd5
```
