
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
