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

## Programming Intel® XMX Using SYCL Joint Matrix Extension

Joint matrix is a new SYCL extension for matrix hardware programming. This unifies targets like Intel<sup>®</sup> Advanced Matrix Extensions (Intel<sup>®</sup> AMX) for CPUs, Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions (Intel<sup>®</sup> XMX) for GPUs, and NVIDIA\* Tensor Cores. In general, frameworks like TensorFlow and libraries like Intel<sup>®</sup> oneAPI Deep Neural Network Library(oneDNN) are the answer for many types of AI users and applications. However, for users who want to build their own neural networks applications, these libraries and frameworks become high-level because users cannot do custom optimizations, and heavyweight because the size of the library is large. Moreover, new operations are introduced and changing in machine learning domain for which frameworks and libraries do not provide timely and performing solutions. For such cases, joint matrix has a lower-level of abstraction than the frameworks to provide performance, productivity, and fusion capabilities but at the same time offers portability by using one code to target different matrix hardware.

## The detailed specification of this extension can be found here

The joint matrix extensions consists of a new type joint\_matrix, explicit memory operations joint\_matrix\_load and joint\_matrix\_store, joint\_matrix\_fill for matrix initialization, joint\_matrix\_mad for the actual multiply and add operations, and joint\_matrix\_apply for element wise operations.

In the code below, the kernel makes use of the joint matrix interface by declaring 3 joint\_matrix matrices: tA, tB, tC and computes the operation tC += tA \* tB. DPAS (Dot Product and Accumulate Systolic) is the name of the elementary operations done in Intel<sup>®</sup> XMX. For more examples that use joint\_matrix, please refer to the Intel llvm-test-suite repo.

In order for this example to run successfully on Intel<sup>®</sup> XMX, The GPU must have Intel<sup>®</sup> XMX hardware. There is no emulation or fall back strategy in the joint matrix implementation.

```cpp
size_t NDRangeM = M / TM;
size_t NDRangeN = N / TN;
size_t sg_size = get_sg_size<kernel_name>(q);
q.submit([&](sycl::handler &cgh) {
    cgh.parallel_for<kernel_name>(
        sycl::nd_range<2>({NDRangeM, NDRangeN * sg_size}, {1, 1 * sg_size}),
        [=](sycl::nd_item<2> spmd_item)

        {
            // The joint matrix API has to be accessed by all the workitems in a
            // subgroup these functions will be called once by the subgroup no
            // code divergence between the workitems
            const auto global_idx = spmd_item.get_global_id(0);
            const auto global_idy = spmd_item.get_global_id(1);
            const auto sg_startx = global_idx - spmd_item.get_local_id(0);
            const auto sg_starty = global_idy - spmd_item.get_local_id(1);

            sycl::sub_group sg = spmd_item.get_sub_group();
            auto pA = sycl::address_space_cast<
                sycl::access::address_space::global_space,
                sycl::access::decorated::no>(A);
            auto pB = sycl::address_space_cast<
                sycl::access::address_space::global_space,
                sycl::access::decorated::no>(B);
            auto pC = sycl::address_space_cast<
                sycl::access::address_space::global_space,
                sycl::access::decorated::no>(C);
            sycl::ext::oneapi::experimental::matrix::joint_matrix<
                sycl::sub_group, Ta, use::a, TM, TK, layout::row_major>
                sub_a;
            sycl::ext::oneapi::experimental::matrix::joint_matrix<
                sycl::sub_group, Tb, use::b, TK, TN, layout::row_major>
                sub_b;
            sycl::ext::oneapi::experimental::matrix::joint_matrix<
                sycl::sub_group, Tc, use::accumulator, TM, TN>
                sub_c;

            joint_matrix_fill(sg, sub_c, C_INIT);
            for (size_t k = 0; k < K / TK; k += 1) {
                joint_matrix_load(sg, sub_a, pA + (sg_startx * TM) * K + k * TK,
                    K);
                joint_matrix_load(sg, sub_b,
                    pB + (k * TK) * N + sg_starty / sg_size * TN, N);
                joint_matrix_mad(sg, sub_c, sub_a, sub_b, sub_c);
            }
            joint_matrix_apply(sg, sub_c, [=](Tc &x) { x *= ALPHA; });
            joint_matrix_store(
                sg, sub_c, pC + (sg_startx * TM) * N + sg_starty / sg_size * TN,
                    N, layout::row_major);
        }); // parallel for
    }).wait();
```

The example uses the device matrix descriptor that can be queried using get\_info API to query the different shapes supported by different GPU and CPU generations.

```cpp
std::vector<sycl::ext::oneapi::experimental::matrix::combination>
    combinations = q.get_device()
        .get_info<sycl::ext::oneapi::experimental::info::
            device::matrix_combinations>();

bool passed = true;
for (unsigned int i = 0; i < combinations.size(); i++) {
    if (combinations[i].nsize == 0) { // Intel AMX
        passed &=
            test<int8_t, int8_t, int32_t, 16, 16, 64, class amx_int_16x16x64>();
        passed &= test<bfloat16, bfloat16, float, 16, 16, 32,
            class amx_bf16_16x16x32>();
        break;
    }

    if (combinations[i].nsize == 16) { // architecture::intel_gpu_pvc
        passed &=
            test<int8_t, int8_t, int32_t, 8, 16, 32, class pvc_int_8x16x32>();
        passed &=
            test<bfloat16, bfloat16, float, 8, 16, 16, class pvc_bf16_8x16x16>();
        break;
    }

    if (combinations[i].nsize == 8) { // architecture::intel_gpu_dg2*
        passed &= test<int8_t, int8_t, int32_t, 8, 8, 32, class dg2_int_8x8x32>();
        passed &=
            test<bfloat16, bfloat16, float, 8, 8, 16, class dg2_bf16_8x16x16>();
        break;
    }
}
```

In order to get optimal performance on Intel<sup>®</sup> XMX, the GEMM kernel has to be written in a way that keeps feeding Intel<sup>®</sup> XMX with data it needs to perform the maximum multiply and adds operations/cycle. Some of these tuning techniques are the following:

• One sub-group can perform multiple DPAS operations.

• Blocking for cache locality should be made on the three\`\` i\`\`, j, and k dimensions. Blocking on the first two dimensions is included in the global range of the kernel. The k-level cache blocking is done within the kernel body. e.g. by choosing block factors of 256x256x32, global range results in:

```txt
range<2> global{M / 256, N / 256 * SG_SIZE};
```

Then, by choosing one sub - group to perform 64x32x32 elements, local range results in:

```javascript
range<2> local{256 / 64, 256 / 32 * SG_SIZE};
```

• Large register file per thread gives the best results for the GEMM kernel. This can be explicitly specified in the compilation command as follows:

```batch
icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc -options -ze-opt-large-register-file" joint-matrix.cpp
```

## Doing I/O in the Kernel

Print statement is the most fundamental capability needed for looking at the results of a program. In accelerators, printing is surprisingly hard and also fairly expensive in terms of overhead.

SYCL\* provides some capabilities to help make this task similar to standard I/O C/C++ programs, but there are some quirks you need to understand because of the way accelerators work. File I/O is not possible from SYCL\* kernels.

SYCL\* provides the stream class to let you print information to the console from within kernels, providing an easy way to debug simple issues without resorting to a debugger. The stream class provides functionality that is very similar to the C++ STL ostream class, and its usage is similar to the STL class. Below we describe how to use SYCL stream class to output information from within an enqueued kernel.

To use the class we must first instantiate it. The signature of the stream constructor is as follows:

```c
stream(size_t BufferSize, size_t MaxStatementSize, handler &CGH);
```

The constructor takes three parameters:

• BufferSize: the total number of characters that may be printed over the entire kernel range • MaxStatementSize: the maximum number of characters in any one call to the stream class • CGH: reference to the sycl::handler parameter in the sycl::queue::submit call

Usage is very similar to that of the C++ STL ostream std::cout class. The message or data that needs to be printed is sent to the SYCL stream instance via the appropriate operator<< method. SYCL provides implementations for all the built-in data types (such as int, char and float) as well as some common classes (such as sycl::nd\_range and sycl::group).

Here is an example usage of a SYCL stream instance:

```cpp
void out1() {
    constexpr int N = 16;
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(N, [=](sycl::item<1> it) {
            int id = it[0];
            /* Send the identifier to a stream to be printed on the console */
            str << "ID=" << id << sycl::endl;
        });
    }).wait();
} // end out1
```

The use of sycl::endl is analogous to the use of the C++ STL std::endlostream reference–it serves to insert a new line as well as flush the stream.

Compiling and executing the above kernel gives the following output:

Care must be taken in choosing the appropriate BufferSize and MaxStatementSize parameters. Insufficient sizes may cause statements to either not be printed, or to be printed with less information than expected. Consider the following kernel:

```cpp
void out2() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 4, cgh);
```

```cpp
cgh.parallel_for(1, [=](sycl::item<1>) {
    str << "ABC" << sycl::endl;      // Print statement 1
    str << "ABCDEFG" << sycl::endl; // Print statement 2
});
}).wait();
} // end out2
```

Compiling and running this kernel gives the following output:

```txt
ABC
```

The first statement was successfully printed out since the number of characters to be printed is 4 (including the newline introduced by sycl::endl) and the maximum statement size (as specified by the MaxStatementSize parameter to the sycl::stream constructor) is also 4. However, only the newline from the second statement is printed.

The following kernel shows the impact of increasing the allowed maximum character size:

```cpp
void out3() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 10, cgh);
        cgh.parallel_for(1, [=](sycl::item<1>) {
            str << "ABC" << sycl::endl;      // Print statement 1
            str << "ABCDEFG" << sycl::endl; // Print statement 2
        });
    }).wait();
} // end out3
```

Compiling and running the above kernel gives the expected output:

```txt
ABC
ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

The examples above used simple kernels with a single work item. More realistic kernels will typically include multiple work items. In these cases, no guarantee is made as to the specific order of the statements printed to the console and you should expect statements from different work items to be interleaved. Consider the following kernel:

```cpp
void out4() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(sycl::nd_range<1>(32, 4), [=](sycl::nd_item<1> it) {
            int id = it.get_global_id();
            str << "ID=" << id << sycl::endl;
        });
    }).wait();
} // end out4
```

One run can produce the following output.

```txt
ID=29
ID=30
ID=31
```

When this program is run again, we might get the output in a totally different order, depending on the order the threads are executed.

The output from sycl::stream is printed after the kernel has completed execution. In most cases this is of no consequence. However, should the kernel fault or throw an exception, no statement will be printed. To illustrate this, consider the following kernel, which raises an exception:

```cpp
void out5() {
    int *m = NULL;
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(sycl::nd_range<1>(32, 4), [=](sycl::nd_item<1> it) {
            int id = it.get_global_id();
            str << "ID=" << id << sycl::endl;
            if (id == 31)
                *m = id;
        });
    }).wait();
} // end out5
```

Compiling and executing the above code generates a segmentation fault due the write to a null pointer.

```txt
Segmentation fault (core dumped)
```

None of the print statements are actually printed to the console. Instead, you will see an error message about a segmentation fault. This is unlike traditional C/C++ streams.
