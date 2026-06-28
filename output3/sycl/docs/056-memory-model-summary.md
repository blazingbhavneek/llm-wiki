For the code to work correctly, the following three conditions must hold:

1. The atomic operations must use memory orders at least as strict as those shown, to guarantee that the correct fences are generated.

2. The elected leader of each work-group in the NDrange must make progress independently of the leaders in other work-groups, to avoid a single work-item spinning in the loop from starving other work-items that have yet to increment the counter.

3. The device must be capable of executing all workgroups in the ND-range simultaneously, with strong forward progress guarantees, in order to ensure that the elected leaders of every work-group in the NDrange eventually reach the latch.

```cpp
struct device_latch {
  explicit device_latch(size_t num_groups)
    : counter(0), expected(num_groups) {}

  template <int Dimensions>
  void arrive_and_wait(nd_item<Dimensions>& it) {
    auto grp = it.get_group();
    group_barrier(grp);
    // Elect one work-item per work-group to be involved in
    // the synchronization. All other work-items wait at the
    // barrier after the branch.
    if (grp.leader()) {
      atomic_ref<size_t, memory_order::acq_rel,
                            memory_scope::device,
                            access::address_space::global_space>
        atomic_counter(counter);

      // Signal arrival at the barrier.
      // Previous writes should be visible to all work-items
      // on the device.
      atomic_counter++;

      // Wait for all work-groups to arrive.
      // Synchronize with previous releases by all
      // work-items on the device.
      while (atomic_counter.load() != expected) {
      }
    }
    group_barrier(grp);
  }

  size_t counter;
  size_t expected;
};
```

```cpp
// Allocate a one-time-use device_latch in USM
void* ptr = sycl::malloc_shared(sizeof(device_latch), q);
device_latch* latch = new (ptr) device_latch(num_groups);
q.submit([&](handler& h) {
    h.parallel_for(R, [=](nd_item<1> it) {
        // Every work-item writes a 1 to its location
        data[it.get_global_linear_id()] = 1;

        // Every work-item waits for all writes
        latch->arrive_and_wait(it);

        // Every work-item sums the values it can see
        size_t sum = 0;
        for (int i = 0; i < num_groups * items_per_group;
            ++i) {
            sum += data[i];
        }
        sums[it.get_global_linear_id()] = sum;
    });
}).wait();
free(ptr, q);
```

## Figure 19-19. Using the device-wide latch from Figure 19-18

Although this code is not guaranteed to be portable, we have included it here to highlight two key points: (1) SYCL is expressive enough to enable device-specific tuning, sometimes at the expense of portability; and (2) SYCL already contains the building blocks necessary to implement higherlevel synchronization routines, which may be included in a future version of the language.

## Summary

This chapter provided a high-level introduction to memory model and atomic classes. Understanding how to use (and how not to use!) these classes is key to developing correct, portable, and efficient parallel programs.

Memory models are an overwhelmingly complex topic, and our focus here has been on establishing a base for writing real applications. If more information is desired, there are several websites, books, and talks dedicated to memory models referenced in the following.

## For More Information

• A. Williams, C++ Concurrency in Action: Practical Multithreading, Manning, 2012, 978-1933988771

H. Sutter, “atomic<> Weapons: The C++ Memory Model and Modern Hardware”, herbsutter.com/2013/02/11/ atomic-weapons-the-c-memory-model-and-modernhardware/

• H-J. Boehm, “Temporarily discourage memory\_order\_ consume,” wg21.link/p0371

• C++ Reference, “std::atomic,” en.cppreference.com/w/ cpp/atomic/atomic

• C++ Reference, “std::atomic\_ref,” en.cppreference. com/w/cpp/atomic/atomic\_ref

![](images/eb25c4dc421aa99b063ef16ab200d09a3ecc9b4b638e50b13e30567547398e15.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
