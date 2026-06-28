## Submitting Kernels to Multiple Queues

Queues provide a channel to submit kernels for execution on an accelerator. Queues also hold a context that describes the state of the device. This state includes the contents of buffers and any memory needed to execute the kernels. The runtime keeps track of the current device context and avoids unnecessary memory transfers between host and device. Therefore, it is better to submit and launch kernels from one context together, as opposed to interleaving the kernel submissions in different contexts.

The following example submits 30 independent kernels that use the same buffers as input to compute the result into different output buffers. All these kernels are completely independent and can potentially execute concurrently and out of order. The kernels are submitted to three queues, and the execution of each kernel will incur different costs depending on the how the queues are created.

```cpp
int VectorAdd(sycl::queue &q1, sycl::queue &q2, sycl::queue &q3,
        const IntArray &a, const IntArray &b) {

    sycl::buffer a_buf(a);
```

```cpp
sycl::buffer b_buf(b);
sycl::buffer<int> *sum_buf[3 * iter];
for (size_t i = 0; i < (3 * iter); i++)
    sum_buf[i] = new sycl::buffer<int>(256);

size_t num_groups = 1;
size_t wg_size = 256;
auto start = std::chrono::steady_clock::now();
for (int i = 0; i < iter; i++) {
    q1.submit([&](auto &h) {
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        auto sum_acc = sum_buf[3 * i]->get_access<sycl::access::mode::write>(h);

        h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) {
            size_t loc_id = index.get_local_id();
            sum_acc[loc_id] = 0;
            for (size_t i = loc_id; i < array_size; i += wg_size) {
                sum_acc[loc_id] += a_acc[i] + b_acc[i];
            }
        });
    });
    q2.submit([&](auto &h) {
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        auto sum_acc =
            sum_buf[3 * i + 1]->get_access<sycl::access::mode::write>(h);

        h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) {
            size_t loc_id = index.get_local_id();
            sum_acc[loc_id] = 0;
            for (size_t i = loc_id; i < array_size; i += wg_size) {
                sum_acc[loc_id] += a'acc[i] + b_acc[i];
            }
        });
    });
    q3.submit([&](auto &h) {
        sycl::accessor a_acc(a_buf, h, sycl::read_only);
        sycl::accessor b_acc(b_buf, h, sycl::read_only);
        auto sum_acc =
            sum_buf[3 * i + 2]->get_access<sycl::access::mode::write>(h);

        h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
            [=](sycl::nd_item<1> index) {
            size_t loc_id = index.get_local_id();
            sum_acc[loc_id] = 0;
            for (size_t i = loc_id; i < array_size; i += wg_size) {
                sum_acc[loc_id] += a.acc[i] + b.acc[i];
            }
        });
    });
}
q1.wait();
q2.wait();
q3.wait();
auto end = std::chrono::steady_clock::now();
```

```cpp
std::cout << "Vector add completed on device - took " << (end - start).count()
        << " u-secs\n";
// check results
for (size_t i = 0; i < (3 * iter); i++)
    delete sum_buf[i];
return ((end - start).count());
} // end VectorAdd
```

Submitting the kernels to the same queue gives the best performance because all the kernels are able to just transfer the needed inputs once at the beginning and do all their computations.

```javascript
VectorAdd(q, q, q, a, b);
```

If the kernels are submitted to different queues that share the same context, the performance is similar to submitting it to one queue. The issue to note here is that when a kernel is submitted to a new queue with a different context, the JIT process compiles the kernel to the new device associated with the context. If this JIT compilation time is discounted, the actual execution of the kernels is similar.

```txt
sycl::queue q1(sycl::default_selector_v);
sycl::queue q2(q1.get_context(), sycl::default_selector_v);
sycl::queue q3(q1.get_context(), sycl::default_selector_v);
VectorAdd(q1, q2, q3, a, b);
```

If the kernels are submitted to three different queues that have three different contexts, performance degrades because at kernel invocation, the runtime needs to transfer all input buffers to the accelerator every time. In addition, the kernels will be JITed for each of the contexts.

```txt
sycl::queue q4(sycl::default_selector_v);
sycl::queue q5(sycl::default_selector_v);
sycl::queue q6(sycl::default_selector_v);
VectorAdd(q4, q5, q6, a, b);
```

If for some reason you need to use different queues, the problem can be alleviated by creating the queues with shared context. This will prevent the need to transfer the input buffers, but the memory footprint of the kernels will increase because all the output buffers have to be resident at the same time in the context, whereas earlier the same memory on the device could be used for the output buffers. Another thing to remember is the issue of memory-to-compute ratio in the kernels. In the example above, the compute requirement of the kernel is low so the overall execution is dominated by the memory transfers. When the compute is high, these transfers do not contribute much to the overall execution time.

This is illustrated in the example below, where the amount of computation in the kernel is increased a thousand-fold and so the runtime will be different.

```cpp
int VectorAdd(sycl::queue &q1, sycl::queue &q2, sycl::queue &q3,
        const IntArray &a, const IntArray &b) {

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer<int> *sum_buf[3 * iter];
    for (size_t i = 0; i < (3 * iter); i++)
        sum_buf[i] = new sycl::buffer<int>(256);

    size_t num_groups = 1;
    size_t wg_size = 256;
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
        q1.submit([&](auto &h) {
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            auto sum_acc = sum_buf[3 * i]->get_access<sycl::access::mode::write>(h);

            h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
```

```cpp
[=](sycl::nd_item<1> index) {
    size_t loc_id = index.get_local_id();
    sum_acc[loc_id] = 0;
    for (int j = 0; j < 1000; j++)
        for (size_t i = loc_id; i < array_size; i += wg_size) {
            sum_acc[loc_id] += a_acc[i] + b_acc[i];
        }
    });
});
q2.submit([&](auto &h) {
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    auto sum_acc =
        sum_buf[3 * i + 1]->get_access<sycl::access::mode::write>(h);

    h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
        [=](sycl::nd_item<1> index) {
        size_t loc_id = index.get_local_id();
        sum_acc[loc_id] = 0;
        for (int j = 0; j < 1000; j++)
            for (size_t i = loc_id; i < array_size; i += wg_size) {
                sum_acc[loc_id] += a_acc[i] + b_acc[i];
            }
        });
});
q3.submit([&](auto &h) {
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    auto sum_acc =
        sum_buf[3 * i + 2]->get_access<sycl::access::mode::write>(h);

    h.parallel_for(sycl::nd_range<1>(num_groups * wg_size, wg_size),
        [=](sycl::nd_item<1> index) {
        size_t loc_id = index.get_local_id();
        sum_acc[loc_id] = 0;
        for (int j = 0; j < 1000; j++)
            for (size_t i = loc_id; ii < array_size; i += wg_size) {
                sum_acc[loc_id] += a_acc[i] + b_acc[i];
            }
        });
});
}
q1.wait();
q2.wait();
q3.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add completed on device - took " << (end - start).count()
       << " u-secs\n";
// check results
for (size_t i = 0; i < (3 * iter); i++)
    delete sum_buf[i];
return ((end - start).count());
} // end VectorAdd
```
