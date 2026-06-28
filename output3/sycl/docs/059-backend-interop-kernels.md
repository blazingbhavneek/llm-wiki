## Using Backend Interoperability for Kernels

This section describes how to use backend interoperability to compile kernels and manipulate kernel bundles. This is an area that was significantly redesigned in SYCL 2020 to increase robustness and to add the flexibility that is required to support different SYCL backends.

Earlier versions of SYCL supported two interoperability mechanisms for kernels. The first mechanism enabled creation of a kernel from an API-defined handle. The second enabled creation of a kernel from an APIdefined source or intermediate representation, such as OpenCL C source or SPIR-V intermediate representation. These two mechanisms still exist in SYCL 2020, though the syntax for both mechanisms has been updated and now uses backend interoperability.

## Interoperability with API-Defined Kernel Objects

With this form of interoperability, the kernel objects themselves are created using the low-level API and then imported into SYCL using backend interoperability. The code in Figure 20-9 shows how get an OpenCL context from a SYCL context, how to create an OpenCL kernel using this OpenCL context, and then how to create and use a SYCL kernel from the OpenCL kernel object.

```txt
CHAPTER 20 BACKEND INTEROPERABILITY

// Get the native OpenCL context from the SYCL context:
auto openclContext = get_native出生:opencl>(c);
const char* kernelSource =
    R"CLC(
        kernel void add(global int* data) {
            int index = get_global_id(0);
            data[index] = data[index] + 1;
        }
    )CLC";
// Create an OpenCL kernel using this context:
cl_program p = clCreateProgramWithSource(
    openclContext, 1, &kernelSource, nullptr, nullptr);
clBuildProgram(p, 0, nullptr, nullptr, nullptr,
                    nullptr);
cl_kernel k = clCreateKernel(p, "add", nullptr);

// Create a SYCL kernel from the OpenCL kernel:
auto sk = make_kernel出生:opencl>(k, c);

// Use the OpenCL kernel with a SYCL queue:
q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};

    h.set_args(data_acc);
    h.parallel_for(size, sk);
});

// Clean up OpenCL objects when done:
clReleaseContext(openclContext);
clReleaseProgram(p);
clReleaseKernel(k);
```

## Figure 20-9. Kernel created from an OpenCL kernel object

Because the SYCL compiler does not have visibility into a SYCL kernel that was created using the low-level API directly, any kernel arguments must explicitly be passed using the set\_arg() or set\_args() interface. Additionally, the SYCL runtime and the low-level API kernel must agree on a convention to pass objects as kernel arguments. This convention should be described as part of the backend interoperability specification. In this example, the accessor data\_acc is passed as the global pointer kernel argument data.

The SYCL 2020 standard leaves the precise semantics of set\_arg() and set\_args() interfaces to be defined by each SYCL backend specification. This allows flexibility but is another way how the code using backend interoperability that we write is likely to be specific to the backends we target.

## Interoperability with Non-SYCL Source Languages

With this form of interoperability, the contents of the kernel are described as source code or as an intermediate representation that is not defined by SYCL. This form of interoperability allows reuse of kernel libraries written in other source languages or use of domain-specific languages (DSLs) that generate code in an intermediate representation.

Previous versions of SYCL included functions like build\_with\_source to directly create a SYCL program from an API-defined source language but this functionality was removed in SYCL 2020. When a backend directly supports an API-defined source language, such as the OpenCL C kernel used by the OpenCL backend in Figure 20-9, this removal is not a problem, but what should we do if a backend does not directly support a specific source language?

## Chapter 20 Backend Interoperabi lity

Some SYCL implementations may provide an explicit online compiler to compile from a source language that cannot be used directly by a backend to a different format supported by a backend. Figure 20-10 shows how to use the experimental sycl\_ext\_intel\_online\_compiler extension to compile from OpenCL C source, which is not supported by the Level Zero backend, to SPIR-V intermediate representation, which is supported by the Level Zero backend. Using this method, a kernel can be used by any backend so long as it can be compiled by the online compiler into a format supported by the backend.

## CAUTION, EXPERIMENTAL EXTENSION!

The sycl\_ext\_intel\_online\_compiler extension is an experimental extension, so it is subject to change or removal! We have included it in this book because it provides a way to achieve similar functionality as the previous SYCL build\_with\_source function and because it is a convenient way to demonstrate how domain-specific languages may interface with SYCL backends to execute kernels.

```txt
// Compile OpenCL C kernel source to SPIR-V intermediate
// representation using the online compiler:
const char* kernelSource =
    R"CLC(
        kernel void add(global int* data) {
            int index = get_global_id(0);
            data[index] = data[index] + 1;
        }
    )CLC";
online_compiler<source_language::opencl_c> compiler(d);
std::vector<byte> spirv =
    compiler.compile(kernelSource);

// Get the native Level Zero context and device:
auto level0Context =
    get_native Ci backend::ext_oneapi_level_zero>(c);
auto level0Device =
    get_native Ci backend::ext_oneapi_level_zero>(d);

// Create a Level Zero kernel using this context:
ze_module_handle_t level0Module = nullptr;
ze_module_desc_t moduleDesc = {};
moduleDesc.stype = ZE_STRUCTURE_TYPE_MODULE_DESC;
moduleDesc.format = ZE_MODULE_FORMAT_IL_SPIRV;
moduleDesc.inputSize = spirv.size();
moduleDesc.pInputModule = spirv.data();
zeModuleCreate(level0Context, level0Device, &moduleDesc,
                    &level0Module, nullptr);

ze_kernel_handle_t level0Kernel = nullptr;
ze_kernel_desc_t kernelDesc = {};
kernelDesc.stype = ZE_STRUCTURE_TYPE_KERNEL_DESC;
kernelDesc.pKernelName = "add";
zeKernelCreate(level0Module, &kernelDesc,
                    &level0Kernel);

// Create a SYCL kernel from the Level Zero kernel:
auto skb =
    make_kernel_bundle Ci backend::ext_oneapi_level_zero,
                        bundle_state::executable>(
        {level0Module}, c);
auto Sk = make_kernel Ci backend::ext_oneapi_level_zero>(
    {skb, level0Kernel}, c);

// Use the Level Zero kernel with a SYCL queue:
q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};

    h.set_args(data_acc);
    h.parallel_for(size, sk);
});
```

Figure 20-10. Kernel created using SPIR-V and the online compiler

In this example, the kernel source string is represented as a C++ raw string literal in the same file as the SYCL host API calls, but there is no requirement that this is the case, and some applications may read the kernel source string from a file or even generate it just-in-time.

As before, because the SYCL compiler does not have visibility into a SYCL kernel written in an API-defined source language, any kernel arguments must explicitly be passed using the set\_arg() or set\_args() interface.
