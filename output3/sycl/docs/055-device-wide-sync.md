## Computing a Histogram

The code in Figure 19-17 demonstrates how to use relaxed atomics in conjunction with work-group barriers to compute a histogram. The kernel is split by the barriers into three phases, each with their own atomicity requirements. Remember that the barrier acts both as a synchronization point and an acquire-release fence—this ensures that any reads and writes in one phase are visible to all work-items in the work-group in later phases.

The first phase sets the contents of some work-group local memory to zero. The work-items in each work-group update independent locations in work-group local memory by design—race conditions cannot occur, and no atomicity is required.

The second phase accumulates partial histogram results in local memory. Work-items in the same work-group may update the same locations in work-group local memory, but synchronization can be deferred until the end of the phase—we can satisfy the atomicity requirements using memory\_order::relaxed and memory\_ scope::work\_group.

The third phase contributes the partial histogram results to the total stored in global memory. Work-items in the same work-group are guaranteed to read from independent locations in work-group local memory, but may update the same locations in global memory—we no longer require atomicity for the work-group local memory and can satisfy the atomicity requirements for global memory using memory\_ order::relaxed and memory\_scope::system as before.

## Chapt er 19 Memory Model and At omics

```cpp
q.submit([&](handler& h) {
    auto local = local_accessor<uint32_t, 1>{B, h};
    h.parallel_for(
        nd_range<1>{num_groups * num_items, num_items},
        [=](nd_item<1> it) {
            auto grp = it.get_group();

            // Phase 1: Work-items co-operate to zero local
            // memory
            for (int32_t b = it.get_local_id(0); b < B;
                b += it.get_local_range(0)) {
                local[b] = 0;
            }
            group_barrier(grp);  // Wait for all to be zeroed

            // Phase 2: Work-groups each compute a chunk of
            // the input. Work-items co-operate to compute
            // histogram in local memory
            const auto [group_start, group_end] =
                distribute_range(grp, N);
            for (int i = group_start + it.get_local_id(0);
                i < group_end; i += it.get_local_range(0)) {
                int32_t b = input[i] % B;
                atomic_ref<uint32_t, memory_order::relaxed,
                    memory_scope::work_group,
                    access::address_space::local_space>(local[b])++;
            }
            group_barrier(
                grp);  // Wait for all local histogram
                // updates to complete

            // Phase 3: Work-items co-operate to update
            // global memory
            for (int32_t b = it.get_local_id(0); b < B;
                b += it.get_local_range(0)) {
                atomic_ref<uint32_t, memory_order::relaxed, memory_scope::system,
                    access::address_space::global_space>(histogram[b]) +=
                    local[b];
            }
        });
}).wait();
```

Figure 19-17. Computing a histogram using atomic references in different memory spaces

## Implementing Device-Wide Synchronization

Back in Chapter 4, we warned against writing kernels that attempt to synchronize work-items across work-groups. However, we fully expect several readers of this chapter will be itching to implement their own device-wide synchronization routines atop of atomic operations and that our warnings will be ignored.

## Device-wide synchronization is currently not portable and is best left to expert programmers. Future versions of SYCL will address this.

The code discussed in this section is dangerous and should not be expected to work on all devices, because of potential differences in device hardware features and SYCL implementations. The memory ordering guarantees provided by atomics are orthogonal to forward progress guarantees, and, at the time of writing, work-group scheduling in SYCL is completely implementation-defined. Formalizing the concepts and terminology required to describe SYCL’s ND-range execution model and the forward progress guarantees associated with work-items, sub-groups, and work-groups is currently an area of active academic research—future versions of SYCL are expected to build on this work to provide additional scheduling queries and controls. For now, these topics should be considered expert-only.

Figure 19-18 shows a simple implementation of a device-wide latch (a single-use barrier), and Figure 19-19 shows a simple example of its usage. Each work-group elects a single work-item to signal arrival of the group at the latch and await the arrival of other groups using a naïve spin-loop, while the other work-items wait for the elected work-item using a workgroup barrier. It is this spin-loop that makes device-wide synchronization unsafe; if any work-groups have not yet begun executing or the currently executing work-groups are not scheduled fairly, the code may deadlock.

## Relying on memory order alone to implement synchronization primitives may lead to deadlocks in the absence of sufficiently strong forward progress guarantees!
