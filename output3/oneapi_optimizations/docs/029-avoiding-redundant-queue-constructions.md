
## Avoiding Redundant Queue Constructions

To execute kernels on a device, the user must create a queue, which references an associated context, platform, and device. These may be chosen automatically, or specified by the user.

A context is constructed, either directly by the user or implicitly when creating a queue, to hold all the runtime information required by the SYCL runtime and the SYCL backend to operate on a device. When a queue is created with no context specified, a new context is implicitly constructed using the default constructor. In general, creating a new context is a heavy duty operation due to the need for JIT compiling the program every time a kernel is submitted to a queue with a new context. For good performance one should use as few contexts as possible in their application.

In the following example, a queue is created inside the loop and the kernel is submitted to this new queue. This will essentially invoke the JIT compiler for every iteration of the loop.

```cpp
int reductionMultipleQMultipleC(std::vector<int> &data, int iter) {
    const size_t data_size = data.size();
    int sum = 0;

    int work_group_size = 512;
    int num_work_items = work_group_size;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr Due};

    sycl::buffer<int> buf(data.data(), data_size, props);
    sycl::buffer<int> sum_buf(&sum, 1, props);

    sycl::queue q1{sycl::default_selector_v, exception_handler};
    // initialize data on the device
    q1.submit([&](auto &h) {
        sycl::accessor buf_acc(buf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(data_size, [=](auto index) { buf_acc[index] = 1; });
    });

    double elapsed = 0;
    for (int i = 0; i < iter; i++) {
        sycl::queue q2{sycl::default_selector_v, exception_handler};
        if (i == 0)
            std::cout << q2.get_device().get_info<sycl::info::device::name>() << "\n";
        // reductionMultipleQMultipleC main begin
        Timer timer;
        q2.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
            sycl::local_accessor<int, 1> scratch(work_group_size, h);
            h.parallel_for(sycl::nd_range<1>{num_work_items, work_group_size},
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
                    }
                    if (loc_id == 0)
                        sum_acc[0] = scratch[0];
                });
            });
        // reductionMultipleQMultipleC main end
        q2.wait();
        sycl::host_accessor h_acc(sum_buf);
```

```cpp
sum = h_acc[0];
elapsed += timer.Elapsed();
}
elapsed = elapsed / iter;
if (sum == sum_expected)
    std::cout << "SUCCESS: Time reductionMultipleQMultipleC = " << elapsed
        << "s"
        << " sum = " << sum << "\n";
else
    std::cout << "ERROR: reductionMultipleQMultipleC Expected " << sum_expected
        << " but got " << sum << "\n";
return sum;
} // end reductionMultipleQMultipleC
```

The above program can be rewritten by moving the queue declaration outside the loop, which improves performance quite dramatically.

```cpp
int reductionSingleQ(std::vector<int> &data, int iter) {
    const size_t data_size = data.size();
    int sum = 0;

    int work_group_size = 512;
    int num_work_items = work_group_size;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()};

    sycl::buffer<int> buf(data.data(), data_size, props);
    sycl::buffer<int> sum_buf(&sum, 1, props);
    sycl::queue q{sycl::default_selector_v, exception_handler};
    std::cout << q.get_device().get_info<sycl::info::device::name>() << "\n";

    // initialize data on the device
    q.submit([&](auto &h) {
        sycl::accessor buf_acc(buf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(data_size, [=](auto index) { buf_acc[index] = 1; });
    });

    double elapsed = 0;
    for (int i = 0; i < iter; i++) {
        // reductionIntBarrier main begin
        Timer timer;
        q.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
            sycl::local_accessor<int, 1> scratch(work_group_size, h);
            h.parallel_for(sycl::nd_range<1>{num_work_items, work_group_size},
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
                    }
                    if (loc_id == 0)
```

```cpp
sum_acc[0] = scratch[0];
});
});
// reductionSingleQ main end
q.wait();
sycl::host_accessor h_acc(sum_buf);
sum = h_acc[0];
elapsed += timer.Elapsed();
}
elapsed = elapsed / iter;
if (sum == sum_expected)
    std::cout << "SUCCESS: Time reductionSingleQ = " << elapsed << "s"
        << " sum = " << sum << "\n";
else
    std::cout << "ERROR: reductionSingleQ Expected " << sum_expected
        << " but got " << sum << "\n";
return sum;
} // end reductionSingleQ
```

In case you need to create multiple queues, try to share the contexts among the queues. This will improve the performance. The above kernel is rewritten as shown below where the new queues created inside the loop and the queue outside the loop share the context. In this case the performance is same as the one with one queue.

```cpp
int reductionMultipleQSingleC(std::vector<int> &data, int iter) {
    const size_t data_size = data.size();
    int sum = 0;

    int work_group_size = 512;
    int num_work_items = work_group_size;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr Due};

    sycl::buffer<int> buf(data.data(), data_size, props);
    sycl::buffer<int> sum_buf(&sum, 1, props);

    sycl::queue q1{sycl::default_selector_v, exception_handler};
    // initialize data on the device
    q1.submit([&](auto &h) {
        sycl::accessor buf_acc(buf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(data_size, [=](auto index) { buf_acc[index] = 1; });
    });

    double elapsed = 0;
    for (int i = 0; i < iter; i++) {
        sycl::queue q2{q1.get_context(), sycl::default_selector_v,
            exception_handler};
        if (i == 0)
            std::cout << q2.get_device().get_info<sycl::info::device::name>() << "\n";
        // reductionMultipleQSingleC main begin
        Timer timer;
        q2.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
            sycl::local_accessor<int, 1> scratch(work_group_size, h);
            h.parallel_for(sycl::nd_range<1>{num_work_items, work_group_size},
                [=](sycl::nd_item<1> item) {
                size_t loc_id = item.get_local_id(0);
                int sum = 0;
```

```cpp
for (size_t i = loc_id; i < data_size;
    i += num_work_items)
    sum += buf_acc[i];
    scratch[loc_id] = sum;
    for (size_t i = work_group_size / 2; i > 0; i >>= 1) {
        item.barrier(sycl::access::fence_space::local_space);
        if (loc_id < i)
            scratch[loc_id] += scratch[loc_id + i];
    }
    if (loc_id == 0)
        sum_acc[0] = scratch[0];
    });
});
// reductionMultipleQSingleC main end
q2.wait();
sycl::host_accessor h_acc(sum_buf);
sum = h_acc[0];
elapsed += timer.Elapsed();
}
elapsed = elapsed / iter;
if (sum == sum_expected)
    std::cout << "SUCCESS: Time reductionMultipleQSingleContext = " << elapsed
        << "s"
        << " sum = " << sum << "\n";
else
    std::cout << "ERROR: reductionMultipleQSingleContext Expected "
        << sum_expected << " but got " << sum << "\n";
return sum;
} // end reductionMultipleQSingleC
```
