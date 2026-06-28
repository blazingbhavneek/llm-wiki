## Atomic Operations in Global and Local Address Spaces

The standard C++ memory model assumes that applications execute on a single device with a single address space. Neither of these assumptions holds for SYCL applications: different parts of the application execute on different devices (i.e., a host device and one or more accelerator devices); each device has multiple address spaces (i.e., private, local, and global); and the global address space of each device may or may not be disjoint (depending on USM support).

When using atomics in the global address space, again, care must be taken because global updates are much slower than local.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
int main() {
    constexpr int N = 256 * 256;
    constexpr int M = 512;
    int total = 0;
    int *a = static_cast<int *>(malloc(sizeof(int) * N));
    for (int i = 0; i < N; i++)
        a[i] = 1;
    sycl::queue q({sycl::property::queue::enable_profiling()});
    sycl::buffer<int> buf(&total, 1);
    sycl::buffer<int> bufa(a, N);
    auto e = q.submit([&](sycl::handler &h) {
        sycl::accessor acc(buf, h);
        sycl::accessor acc_a(bufa, h, sycl::read_only);
        h.parallel_for(sycl::nd_range<1>(N, M), [=](auto it) {
            auto i = it.get_global_id();
            sycl::atomic_ref<int, sycl::memory_order_relaxed,
                    sycl::memory_scope_device,
                    sycl::access::address_space::global_space>
                atomic_op(acc[0]);
            atomic_op += acc_a[i];
        });
    });
    sycl::host_accessor h_a(buf);
    std::cout << "Reduction Sum : " << h_a[0] << "\n";
    std::cout
        << "Kernel Execution Time of Global Atomics Ref: "
        << e.get_profiling_info<sycl::info::event_profiling::command_end>() -
            e.get_profiling_info<sycl::info::event_profiling::command_start>()
        << "\n";
    return 0;
}
```

It is possible to refactor your code to use local memory space as the following example demonstrates.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
int main() {
  constexpr int N = 256 * 256;
  constexpr int M = 512;
  constexpr int NUM_WG = N / M;
  int total = 0;
  int *a = static_cast<int *>(malloc(sizeof(int) * N));
  for (int i = 0; i < N; i++)
    a[i] = 1;
  sycl::queue q({sycl::property::queue::enable_profiling()});
  sycl::buffer<int> global(&total, 1);
  sycl::buffer<int> buta(a, N);
```

```cpp
auto e1 = q.submit([&](sycl::handler &h) {
    sycl::accessor b(global, h);
    sycl::accessor acc_a(bufa, h, sycl::read_only);
    auto acc = sycl::local_accessor<int, 1>(NUM_WG, h);
    h.parallel_for(sycl::nd_range<1>(N, M), [=](auto it) {
        auto i = it.get_global_id(0);
        auto group_id = it.get_group(0);
        sycl::atomic_ref<int, sycl::memory_order_relaxed,
                sycl::memory_scope_device,
                sycl::access::address_space::local_space>
            atomic_op(acc[group_id]);
        sycl::atomic_ref<int, sycl::memory_order_relaxed,
                sycl::memory_scope_device,
                sycl::access::address_space::global_space>
            atomic_op_global(b[0]);
        atomic_op += acc_a[i];
        it.barrier(sycl::access::fence_space::local_space);
        if (it.get_local_id() == 0)
            atomic_op_global += acc[group_id];
    });
});
sycl::host_accessor h_global(global);
std::cout << "Reduction Sum : " << h_global[0] << "\n";
int total_time =
    (e1.get_profiling_info<sycl::info::event_profiling::command_end>() -
        e1.get_profiling_info<sycl::info::event_profiling::command_start>());
std::cout << "Kernel Execution Time of Local Atomics : " << total_time
            << "\n";
return 0;
}
```

## Atomic Operations on USM Data

On discrete GPU,

• Atomic operations on host allocated USM (sycl::malloc\_host) are not supported.

• Concurrent accesses from host and device to shared USM location (sycl::malloc\_shared) are not supported.

We recommend using device allocated USM (sycl::malloc\_device) memory for atomics and device algorithms with atomic operations.

## Memory Scope of Atomic Operations

Memory scope of atomic operations allows you to avoid data races.

To learn more about the sycl::memory\_scope parameter see the Memory scope section of the SYCL specification.

To learn more about the memory model, see the Memory Model and Atomics chapter of the DPC++ book.

## Local Barriers vs Global Atomics

Atomics allow multiple work-items in the kernel to work on shared resources. Barriers allow synchronization among the work-items in a work-group. It is possible to achieve the functionality of global atomics through judicious use of kernel launches and local barriers. Depending on the architecture and the amount of data involved, one or the other can have better performance.

In the following example, we try to sum a relatively small number of elements in a vector. This task is can be achieved in different ways. The first kernel shown below does this using only one work-item which walks through all elements of the vector and sums them up.

```cpp
q.submit([&](auto &h) {
    sycl::accessor buf_acc(buf, h, sycl::read_only);
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
    h.parallel_for(data_size, [=](auto index) {
        int glob_id = index[0];
        if (glob_id == 0) {
            int sum = 0;
            for (size_t i = 0; i < N; i++)
                sum += buf_acc[i];
            sum_acc[0] = sum;
        }
    });
});
```

In the kernel shown below, the same problem is solved using global atomics, where every work-item updates a global variable with the value it needs to accumulate. Although there is a lot of parallelism here, the contention on the global variable is quite high and in most cases its performance will not be very good.

```rust
q.submit([&](auto &h) {
    sycl::accessor buf_acc(buf, h, sycl::read_only);
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(data_size, [=](auto index) {
        size_t glob_id = index[0];
        auto v = sycl::atomic_ref<int, sycl::memory_order::relaxed,
                             sycl::memory_scope::device,
                             sycl::access::address_space::global_space>(
            sum_acc[0]);
        v.fetch_add(buf_acc[glob_id]);
    });
});
```

In the following kernel, every work-item is responsible for accumulating multiple elements of the vector. This accumulation is done in parallel and then updated into an array that is shared among all work-items of the work-group. At this point all work-items of the work-group do a tree reduction using barriers to synchronize among themselves to reduce intermediate results in shared memory to the final result. This kernel explicitly created exactly one work-group and distributes the responsibility of all elements in the vector to the workitems in the work-group. Although it is not using the full capability of the machine in terms of the number of threads, sometimes this amount of parallelism is enough for small problem sizes.

```cpp
Timer timer;
q.submit([&](auto &h) {
    sycl::accessor buf_acc(buf, h, sycl::read_only);
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
    sycl::local_accessor<int, 1> scratch(work_group_size, h);
    h.parallel_for(sycl::nd_range<1>{work_group_size, work_group_size},
        [=](sycl::nd_item<1> item) {
        size_t loc_id = item.get_local_id(0);
        int sum = 0;
        for (size_t i = loc_id; i < data_size;
            i += num_work_items)
            sum += buf_acc[i];
        scratch[loc_id] = sum;
        for (size_t i = work_group_size / 2; i > 0; i >>= 1) {
            item.barrier(sycl::access::fence_space::local_space);
            if (loc_id < i)
                scratch[loc_id] += scratch[loc_id + i];
```

```txt
}
    if (loc_id == 0)
        sum_acc[0] = scratch[0];
});
```

The performance of these three kernels varies quite a bit among various platforms, and developers need to pick the technique that suits their application and hardware.
