
## Shared Local Memory

Often work-items need to share data and communicate with each other. On one hand, all work-items in all work-groups can access global memory, so data sharing and communication can occur through global memory. However, due to its lower bandwidth and higher latency, sharing and communication through global memory is less efficient. On the other hand, work-items in a sub-group executing simultaneously in a vector engine (VE) thread can share data and communicate with each other very efficiently, but the number of work-items in a sub-group is usually small and the scope of data sharing and communication is very limited. Memory with higher bandwidth and lower latency accessible to a bigger scope of work-items is very desirable for data sharing communication among work-items. The shared local memory (SLM) in Intel<sup>®</sup> GPUs is designed for this purpose.

Each X<sup>e</sup>-core of Intel GPUs has its own SLM. Access to the SLM is limited to the VEs in the X<sup>e</sup>-core or workitems in the same work-group scheduled to execute on the VEs of the same X<sup>e</sup>-core. It is local to a X<sup>e</sup>-core (or work-group) and shared by VEs in the same X<sup>e</sup>-core (or work-items in the same work-group), so it is called SLM. Because it is on-chip in each X<sup>e</sup>-core, the SLM has much higher bandwidth and much lower latency than global memory. Because it is accessible to all work-items in a work-group, the SLM can accommodate data sharing and communication among hundreds of work-items, depending on the workgroup size.

It is often helpful to think of SLM as a work-group managed cache. When a work-group starts, work-items in the work-group can explicitly load data from global memory into SLM. The data stays in SLM during the lifetime of the work-group for faster access. Before the work-group finishes, the data in the SLM can be explicitly written back to the global memory by the work-items. After the work-group completes execution, the data in SLM is also gone and invalid. Data consistency between the SLM and the global memory is the program’s responsibility. Properly using SLM can make a significant performance difference.

## Shared Local Memory Size and Work-group Size

Because it is on-chip, the SLM has limited size. How much memory is available to a work-group is devicedependent and can be obtained by querying the device, e.g.:

```cpp
std::cout << "Local Memory Size: "
          << q.get_device().get_info<sycl::info::device::local_mem_size>()
          << std::endl;
```

The output may look like:

```txt
Local Memory Size: 65536
```

The unit of the size is a byte. So this GPU device has 65,536 bytes or 64KB SLM for each work-group.

It is important to know the maximum SLM size a work-group can have. In a lot of cases, the total size of SLM available to a work-group is a non-constant function of the number of work-items in the work-group. The maximum SLM size can limit the total number of work-items in a group, i.e. work-group size. For example, if the maximum SLM size is 64KB and each work-item needs 512 bytes of SLM, the maximum work-group size cannot exceed 128.

## Bank Conflicts

The SLM is divided into equally sized memory banks that can be accessed simultaneously for high bandwidth. The total number of banks is device-dependent. At the time of writing, 64 consecutive bytes are stored in 16 consecutive banks at 4-byte (32-bit) granularity. Requests for access to different banks can be serviced in parallel, but requests to different addresses in the same bank cause a bank conflict and are serialized. Bank conflicts adversely affect performance. Consider this example:

```cpp
constexpr int N = 32;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([&](auto &h) {
    sycl::local_accessor<int, 1> slm(sycl::range(32 * 64), h);
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
        [=](sycl::nd_item<1> it) {
            int i = it.get_global_linear_id();
            int j = it.get_local_linear_id();

            slm[j * 16] = 0;
            it.barrier(sycl::access::fence_space::local_space);

            for (int m = 0; m < 1024 * 1024; m++) {
                slm[j * 16] += i * m;
                it.barrier(sycl::access::fence_space::local_space);
            }

            data[i] = slm[j * 16];
        });
});
```

If the number of banks is 16, all work-items in the above example will read from and write to different addresses in the same bank. The memory bandwidth is 1/16 of full bandwidth.

The next example instead does not have SLM bank conflicts and achieves full memory bandwidth because every work-item reads from and writes to different addresses in different banks.

```cpp
constexpr int N = 32;
int *data = sycl::malloc_shared<int>(N, q);

auto e = q.submit([&](auto &h) {
    sycl::local_accessor<int, 1> slm(sycl::range(32 * 64), h);
```

```cpp
h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
    [=](sycl::nd_item<1> it) {
        int i = it.get_global_linear_id();
        int j = it.get_local_linear_id();

        slm[j] = 0;
        it.barrier(sycl::access::fence_space::local_space);

        for (int m = 0; m < 1024 * 1024; m++) {
            slm[j] += i * m;
            it.barrier(sycl::access::fence_space::local_space);
        }

        data[i] = slm[j];
    });
});
```
