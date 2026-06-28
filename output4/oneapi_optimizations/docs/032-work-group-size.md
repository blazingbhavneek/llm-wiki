
## Considerations for Selecting Work-Group Size

In SYCL you can select the work-group size for nd\_range kernels. The size of work-group has important implications for utilization of the compute resources, vector lanes, and communication among the workitems. The work-items in the same work-group may have access to hardware resources like shared local memory and hardware synchronization capabilities that will allow them to run and communicate more efficiently than work-items across work-groups. So in general you should pick the maximum work-group size supported by the accelerator. The maximum work-group size can be queried by the call device::get\_info<cl::sycl::info::device::max\_work\_group\_size>().

To illustrate the impact of the choice of work-group size, consider the following reduction kernel, which goes through a large vector to add all the elements in it. The function that runs the kernels takes in the workgroup-size and sub-group-size as arguments, which lets you run experiments with different values. The performance difference can be seen from the timings reported when the kernel is called with different values for work-group size.

```cpp
void reduction(sycl::queue &q, std::vector<int> &data, std::vector<int> &flush,
        int iter, int work_group_size) {
    const size_t data_size = data.size();
    const size_t flush_size = flush.size();
    int sum = 0;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
    // int vec_size =
    // q.get_device().get_info<sycl::info::device::native_vector_width_int>();
    int num_work_items = data_size / work_group_size;
    sycl::buffer<int> buf(data.data(), data_size, props);
    sycl::buffer<int> flush_buf(flush.data(), flush_size, props);
    sycl::buffer<int> sum_buf(&sum, 1, props);

    init_data(q, buf, data_size);

    double elapsed = 0;
    for (int i = 0; i < iter; i++) {
        q.submit([&](auto &h) {
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(1, [=](auto index) { sum_acc[index] = 0; });
        });
        // flush the cache
        q.submit([&](auto &h) {
            sycl::accessor flush_acc(flush_buf, h, sycl::write_only, sycl::no_init);
            h.parallel_for(flush_size, [=](auto index) { flush_acc[index] = 1; });
        });

        Timer timer;
        // reductionMapToHWVector main begin
        q.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::local_accessor<int, 1> scratch(work_group_size, h);
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);
```

```cpp
h.parallel_for(
    sycl::nd_range<1>(num_work_items, work_group_size),
    [=](sycl::nd_item<1> item) [[intel::reqd_sub_group_size(16)]] {
        auto v =
            sycl::atomic_ref<int, sycl::memory_order::relaxed,
                sycl::memory_scope::device,
                sycl::access::address_space::global_space>(
                    sum_acc[0]);
        int sum = 0;
        int glob_id = item.get_global_id();
        int loc_id = item.get_local_id();
        for (unsigned int i = glob_id; i < data_size; i += num_work_items
            sum += buf_acc[i];
        scratch[loc_id] = sum;

        for (int i = work_group_size / 2; i > 0; i >>= 1) {
            item.barrier(sycl::access::fence_space::local_space);
            if (loc_id < i)
                scratch[loc_id] += scratch[loc_id + i];
        }

        if (loc_id == 0)
            v.fetch_add(scratch[0]);
    });
});
q.wait();
elapsed += timer.Elapsed();
sycl::host_accessor h_acc(sum_buf);
sum = h_acc[0];
}
elapsed = elapsed / iter;
std::string msg = "with work-groups=" + std::to_string(work_group_size);
check_result(elapsed, msg, sum);
// reduction end
```

In the code below, the above kernel is called with two different values: 2\*vec-size and the maximum possible work-group size supported by the accelerator. The performance of the kernel when work-group size is equal to 2\*vec-size will be lower than when the work-group size is the maximum possible value.

```rust
int vec_size = 16;
int work_group_size = vec_size;
reduction(q, data, extra, 16, work_group_size);
work_group_size =
    q.get_device().get_info<sycl::info::device::max_work_group_size>();
reduction(q, data, extra, 16, work_group_size);
```

In situations where there are no barriers nor atomics used, the work-group size will not impact the performance. To illustrate this, consider the following vec\_copy kernel where there are no atomics or barriers.

```cpp
void vec_copy(sycl::queue &q, std::vector<int> &src, std::vector<int> &dst,
        std::vector<int> &flush, int iter, int work_group_size) {
    const size_t data_size = src.size();
    const size_t flush_size = flush.size();

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
    int num_work_items = data_size;
    double elapsed = 0;
    {
```

```cpp
sycl::buffer<int> src_buf(src.data(), data_size, props);
sycl::buffer<int> dst_buf(dst.data(), data_size, props);
sycl::buffer<int> flush_buf.flush.data(), flush_size, props);

for (int i = 0; i < iter; i++) {
    // flush the cache
    q.submit([&](auto &h) {
        sycl::accessor flush_acc_flush_buf, h, sycl::write_only, sycl::no_init);
        h.parallel_for.flush_size, [=](auto index) { flush_acc[index] = 1; });
    });

    Timer timer;
    q.submit([&](auto &h) {
        sycl::accessor src_acc(src_buf, h, sycl::read_only);
        sycl::accessor dst_acc(dst_buf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(sycl::nd_range<1>(num_work_items, work_group_size),
            [=](sycl::nd_item<1> item)
                [[intel::reqd_sub_group_size(16)]] {
                    int glob_id = item.get_global_id();
                    dst_acc[glob_id] = src_acc[glob_id];
                });
    });
    q.wait();
    elapsed += timer.Elapsed();
}
elapsed = elapsed / iter;
std::string msg = "with work-group-size=" + std::to_string(work_group_size);
check_result(elapsed, msg, dst);
// vec_copy end
```

In the code below, the above kernel is called with different work-group sizes. All the above calls to the kerne will have similar run times which indicates that there is no impact of work-group size on performance. The reason for this is that the threads created within a work-group and threads from different work-groups behave in a similar manner from the scheduling and resourcing point of view when there are no barriers nor shared memory in the work-groups.

```c
int vec_size = 16;
int work_group_size = vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 2 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 4 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 8 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
work_group_size = 16 * vec_size;
vec_copy(q, src, dst, extra, 16, work_group_size);
```

In some accelerators, a minimum sub-group size is needed to obtain good performance due to the way in which threads are scheduled among the processing elements. In such a situation you may see a big performance difference when the number of sub-groups is less than the minimum. The call to the kernel on line 3 above has only one sub-group, while the call on line 5 has two sub-groups. There will be a significant performance difference in the timings for these two kernel invocations on an accelerator that performs scheduling of of two sub-groups at a time.
