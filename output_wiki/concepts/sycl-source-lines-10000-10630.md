# sycl Source Lines 10000-10630

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L10000-L10630

Citation: [sycl:L10000-L10630]

````text
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

# Backend Interoperability

In this chapter we will learn about backend interoperability, a SYCL feature that can incrementally add SYCL to an application that is already using other data parallel techniques or APIs.

We will also learn how backend interoperability can be used by expert programmers familiar with low-level APIs to “peek behind the curtain” and use underlying data parallel APIs from SYCL programs directly. This provides direct access to API-specific features, when necessary, while retaining the portability and ease-of-use benefits of SYCL otherwise.

## What Is Backend Interoperability?

So far in this book we have referred to SYCL programs running on SYCL devices, but in practice many SYCL implementations build upon lowerlevel APIs such as OpenCL, Level Zero, CUDA, or others to access the parallel hardware in a system. When a SYCL implementation is built upon a lower-level API, we refer to the target API as a SYCL backend. Figure 20-1 shows the relationship between SYCL backends, platforms, and devices. Most SYCL implementations can run SYCL programs on multiple SYCL backends simultaneously to utilize all the parallel hardware in a system.

![](images/35ad5ab35b3289cff4bf75d2d64bb6f2e07c5032e67ae38cecfd069564145b5b.jpg)  
Figure 20-1. Relationship between SYCL backends, platforms, and devices

We can query the SYCL backends in a system by first querying the SYCL platforms and then querying the SYCL backend associated with each platform, as shown in Figure 20-2. The output from this program will depend on the number and type of SYCL devices in a system. If the same device is supported by different SYCL backends, it may enumerate as a SYCL device for each backend.

![](images/0bd2905f5bee855a13f10b18703df88c473c3fc98cec185d8a0fc08166e2c524.jpg)  
Figure 20-2. Querying the SYCL backend for a SYCL platform

The associated backend can be queried for most SYCL objects, not just for SYCL platforms. For example, we can also query the associated backend for a SYCL device, a SYCL context, or a SYCL queue.

Backend interoperability lets us use knowledge of the associated backend to interact with and manipulate underlying native backend objects that represent SYCL objects for the associated backend.

## When Is Backend Interoperability Useful?

Many SYCL programmers will never need to use backend interoperability. In fact, using backend interoperability may be undesirable; backend interoperability will frequently either make a program more complex because it requires multiple code paths for multiple SYCL backends, or it will make a program less portable because it will restrict execution to devices with a single associated backend.

Still, backend interoperability is a useful tool to have in our toolbox to solve some specific problems. In this section we will explore several common use cases where backend interoperability is useful.

## BACKEND INTEROPERABILITY IS LIKE AN INLINE ASSEMBLER

A useful mental model for backend interoperability is that backend interoperability is to SYCL as inline assembler is to C++ host code: backend interoperability is not necessary for learning SYCL or being productive with SYCL, and backend interoperability is often undesirable because it increases complexity or decreases portability. Nevertheless, it is a useful tool to have in our toolbox to solve specific problems.

## Adding SYCL to an Existing Codebase

The SYCL programs in this book are designed to teach specific SYCL concepts so they are intentionally straightforward and short. By contrast, most real-world software is large and complex, consisting of thousands or millions of lines of code, perhaps developed by many people over many years. Even if we wanted to do so, completely rewriting a large application to use SYCL may not be feasible.

One of the key benefits provided by backend interoperability is the ability to incrementally add SYCL to an existing codebase that is already using a low-level API, by creating SYCL objects from native backend objects for that API. For example, let’s say we have a large OpenCL application that creates an OpenCL context and OpenCL memory objects. Backend interoperability has templated functions like make\_context and make\_buffer which let us seamlessly create SYCL objects from these OpenCL objects. After creating SYCL objects from the OpenCL objects, they can be used by SYCL queues and SYCL kernels just like any other SYCL object, as shown in Figure 20-3.

```cpp
// Create SYCL objects from the native backend objects.
context c =
    make_context<backend::opencl>(openclContext);
device d = make_device<backend::opencl>(openclDevice);
buffer data_buf =
    make_buffer<backend::opencl, int>(openclBuffer, c);

// Now use the SYCL objects to create a queue and submit
// a kernel.
queue q{c, d};

q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};
    h.parallel_for(size, [=](id<1> i) {
        data_acc[i] = data_acc[i] + 1;
    });
}).wait();
```

Figure 20-3. Creating SYCL objects from OpenCL objects

The SYCL 2020 specification only defines interoperability with OpenCL backends, but SYCL implementations may provide interoperability with other backends via extensions. Figure 20-4 shows how SYCL objects may be created from Level Zero objects using the sycl\_ext\_oneapi\_backend\_ level\_zero extension.

```cpp
// Create SYCL objects from the native backend objects.
device d = make_device<backend::ext_oneapi_level_zero>(
    level0Device);
context c =
    make_context<backend::ext_oneapi_level_zero>(
        {level0Context,
            {d},
            ext::oneapi::level_zero::ownership::keep});
buffer data_buf =
    make_buffer<backend::ext_oneapi_level_zero, int>(
        {level0Ptr,
            ext::oneapi::level_zero::ownership::keep},
            c);

// Now use the SYCL objects to create a queue and submit
// a kernel.
queue q{c, d};

q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};
    h.parallel_for(size, [=](id<1> i) {
        data_acc[i] = data_acc[i] + 1;
    });
}).wait();
```

## Figure 20-4. Creating SYCL objects from Level Zero objects

Notice that the parameters that are passed to create the SYCL objects are slightly different for the Level Zero backend. This will generally be true for any supported backend interoperability because each backend may require different information to properly create the SYCL object. Otherwise, the same make\_device, make\_context, and make\_buffer functions are used for both OpenCL and Level Zero backend interoperability.

Notice also that ownership is handled differently by each backend. For the OpenCL backend, the SYCL implementation uses the reference counting provided by OpenCL to manage the lifetimes of the native backend objects. For the Level Zero backend, the SYCL implementation must be explicitly told whether it should take ownership of the native backend object, or whether our application will keep ownership. If the SYCL implementation takes ownership of the native backend object, then the native backend object will be destroyed when the SYCL object is destroyed; otherwise, our application is responsible for freeing the native backend object directly.

## Using Existing Libraries with SYCL

Backend interoperability can also be used to extract native backend objects from SYCL objects. This can be useful to use existing low-level libraries or other helper functions with our SYCL applications. There are two methods to do this: the first uses get\_native free functions to get native backend objects from SYCL objects. The second uses a host\_task and an interop\_handle to get native backend objects from SYCL objects from code that is scheduled by the SYCL runtime.

## Getting Backend Objects with Free Functions

For example, let’s say we have an optimized OpenCL library that we would like to use with our SYCL application. We can call the backend interoperability get\_native functions to get native OpenCL objects from our SYCL objects, which can then be used with the OpenCL library. For simplicity, the code in Figure 20-5 just performs a query and allocates some memory with the native OpenCL objects, but they could also be used to perform more complicated operations like creating command queues, compiling programs, and executing kernels.

```cpp
CHAPTER 20 BACKEND IN

cl_device_id openclDevice =
    get_native Ci backend::opencl>(d);
cl_context openclContext = get_native Ci backend::opencl>(c);

// Query the device name from OpenCL:
size_t sz = 0;
clGetDeviceInfo(openclDevice, CL_DEVICE_NAME, 0, nullptr,
        &sz);
std::string openclDeviceName(sz, ' ');
clGetDeviceInfo(openclDevice, CL_DEVICE_NAME, sz,
        &openclDeviceName[0], nullptr);
std::cout << "Device name from OpenCL is: "
       << openclDeviceName << "\n";

// Allocate some memory from OpenCL:
cl_mem openclBuffer = clCreateBuffer(
    openclContext, 0, sizeof(int), nullptr, nullptr);

// Clean up OpenCL objects when done:
clReleaseDevice(openclDevice);
clReleaseContext(openclContext);
clReleaseMemObject(openclBuffer);
```

## Figure 20-5. Extracting OpenCL objects from SYCL objects using get\_native free functions

The same get\_native functions are also added for the Level Zero backend as part of the sycl\_ext\_oneapi\_backend\_level\_zero extension, as shown in Figure 20-6.

```txt
CHAPTER 20 BACKEND INTEROPERABILITY
```

```cpp
ze_device_handle_t level0Device =
    get_native Ci backend::ext_oneapi_level_zero>(d);
ze_context_handle_t level0Context =
    get_native Ci backend::ext_oneapi_level_zero>(c);

// Query the device name from Level Zero:
ze_device_properties_t level0DeviceProps = {};
level0DeviceProps.stype =
    ZE_STRUCTURE_TYPE_DEVICE_PROPERTIES;

zeDeviceGetProperties(level0Device, &level0DeviceProps);

std::cout << "Device name from SYCL is: "
        << d.get_info<info::device::name>() << "\n";
std::cout << "Device name from Level Zero is: "
        << level0DeviceProps.name << "\n";

// Allocate some memory from Level Zero:
void* level0Ptr = nullptr;
ze_host_mem_alloc_desc_t level0HostAllocDesc = {};
level0HostAllocDesc.stype =
    ZE_STRUCTURE_TYPE_HOST_MEM_ALLOC_DESC;
zeMemAllocHost(level0Context, &level0HostAllocDesc,
           sizeof(int), 0, &level0Ptr);

// Clean up Level Zero objects when done:
zeMemFree(level0Context, level0Ptr);
```

Figure 20-6. Extracting Level Zero objects from SYCL objects using get\_native free functions

## Getting Backend Objects via an Interop Handle

Using the get\_native free functions is an effective way to get backendspecific objects for large sections of code that will use backend APIs directly. In many cases, though, we only want to perform a specific operation in the SYCL task graph using a backend API. In these cases, we can perform the backend-specific operation using a SYCL host\_task with a special interop\_handle parameter. The interop\_handle represents the state of the SYCL runtime when the host task is invoked and provides access to native backend objects representing the SYCL queue, device, context, and any buffers that were captured for the host task.

Figure 20-7 shows how to use the interop\_handle to get native OpenCL objects from a host\_task that is scheduled by the SYCL runtime. For simplicity, this sample also only performs some queries using the native OpenCL objects, but real application code would commonly enqueue a kernel or call into a library using the native OpenCL objects. Because these operations are performed from a host task, they will be properly scheduled with any other operations in the SYCL queue.

```cpp
q.submit([&](handler& h) {
  accessor a{b, h};
  h.host_task([=](interop_handle ih) {
    // Get the OpenCL device from the interop handle:
    auto openclDevice =
        ih.get_native_device<backend::opencl>();

    // Query the device name from the OpenCL device:
    size_t sz = 0;
    clGetDeviceInfo(openclDevice, CL_DEVICE_NAME, 0,
                      nullptr, &sz);
    std::string openclDeviceName(sz, ' ');
    clGetDeviceInfo(openclDevice, CL_DEVICE_NAME, sz,
                      &openclDeviceName[0], nullptr);
    std::cout << "Device name from OpenCL is: "
           << openclDeviceName << "\n";

    // Get the OpenCL buffer from the interop handle:
    auto openclMem =
        ih.get_native_mem<frontend::opencl>(a)[0];

    // Query the size of the OpenCL buffer:
    clGetMemObjectInfo(openclMem, CL_MEM_SIZE, sizeof(sz),
                    &sz, nullptr);
    std::cout << "Buffer size from OpenCL is: " << sz
           << " bytes\n";
  });
});
```

Figure 20-7. Extracting OpenCL objects from SYCL objects using an interop\_handle

Notice that when getting native OpenCL objects for our accessor, the get\_native\_mem member function of the interop\_handle returns a vector of cl\_mem memory objects. This is a requirement in the SYCL 2020 specification, where the return type of member functions of the interop\_ handle must match the get\_native free functions, but for the interop\_ handle usage we can simply use the first element of the vector.

As with the get\_native free functions, similar functionality may also be provided for other SYCL backends via extensions. Figure 20-8 shows how to perform similar operations with the Level Zero backend using the sycl\_ext\_oneapi\_backend\_level\_zero extension.

```cpp
q.submit([&](handler& h) {
  accessor a{b, h};
  h.host_task([=](interop_handle ih) {
    // Get the Level Zero device from the interop handle:
    auto level0Device = ih.get_native_device<
      backend::ext_oneapi_level_zero>();

    // Query the device name from Level Zero:
    ze_device_properties_t level0DeviceProps = {};
    level0DeviceProps.stype =
      ZE_STRUCTURE_TYPE_DEVICE_PROPERTIES;
    zeDeviceGetProperties(level0Device,
                       &level0DeviceProps);
    std::cout << "Device name from Level Zero is: "
          << level0DeviceProps.name << "\n";

    // Get the Level Zero context and memory allocation
    // from the interop handle:
    auto level0Context = ih.get_native_context<
      backend::ext_oneapi_level_zero>();
    auto ptr =
      ih.get_native_mem posterior::ext_oneapi_level_zero>(
        a);

    // Query the size of the memory allocation:
    size_t sz = 0;
    zeMemGetAddressRange(level0Context, ptr, nullptr,
                       &sz);
    std::cout << "Buffer size from Level Zero is: " << sz
          << " bytes\n";
  });
});
```

Figure 20-8. Extracting OpenCL objects from SYCL objects using an interop\_handle

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

## Backend Interoperability Hints and Tips

This section describes practical hints and tips to effectively use backend interoperability.

## Choosing a Device for a Specific Backend

The first requirement to properly use backend interoperability is to choose a SYCL device associated with the required SYCL backend. There are several ways to accomplish this.

The first is to integrate the required SYCL backend into existing custom device selection logic, by querying the associated backend while scoring each device. If our application is already using custom device selection logic, this should be a straightforward addition. This mechanism is also portable because it uses only standard SYCL queries.

For applications that do not already use custom device selection logic, we can write a short C++ lambda expression to iterate over all devices to find a device with the requested backend, as shown in Figure 20-11. Because this version of find\_device does not request a specific device type, it is effectively a replacement for the standard default\_selector\_v.

```cpp
#include <iostream>
#include <sycl/sycl.hpp>
using namespace sycl;

int main() {
    auto find_device = [](backend b,
                          info::device_type t =
                          info::device_type::all) {
        for (auto d : device::get_devices(t)) {
            if (d.get_backend() == b) {
                return d;
            }
        }
        throw sycl::exception(errc::runtime,
                          "Could not find a device with "
                          "the requested backend!");
    };

    try {
        device d{find_device-backend::opencl});
        std::cout << "Found an OpenCL SYCL device: "
                          << d.get_info<info::device::name>() << "\n";
    } catch (const sycl::exception &e) {
        std::cout << "No OpenCL SYCL devices were found.\n";
    }

    try {
        device d{find_device-backend::ext_oneapi_level_zero});
        std::cout << "Found a Level Zero SYCL device: "
                          << d.get_info<info::device::name>() << "\n";
    } catch (const sycl::exception &e) {
        std::cout << "No Level Zero SYCL devices were found.\n";
    }

    return 0;
}
```  
Figure 20-11. Finding a SYCL device with a specific backend

Finally, for fast prototyping some SYCL implementations can use external mechanisms, such as environment variables, to influence the SYCL devices they enumerate. As an example, the DPC++ SYCL runtime can use the ONEAPI\_DEVICE\_SELECTOR environment variable to limit enumerated devices to specific device types or associated device backends (refer to Chapter 13). This is not an ideal solution for production code

because it requires external configuration, but it is a useful mechanism for prototype code to ensure that an application is using a specific device from a specific backend.

## Be Careful About Contexts!

Recall from Chapters 6 and 13 that many SYCL objects, such as kernels and USM allocations, are generally not accessible by a SYCL context if they were created in a different SYCL context. This is still true when using backend interoperability; therefore, a backend-specific context created using a backend API generally will not have access to objects created in a different SYCL context (and vice versa) even if the SYCL context is associated with the same backend.

To safely share objects between SYCL and a backend, we should always either create our SYCL context from a native backend context using make\_context, or we should get a native backend context from a SYCL context using get\_native.

Always create a SYCL context from a native backend context or get a native backend context from a SYCL context to safely share objects between SYCL and a backend!

## Access Low-Level API-Specific Features

Occasionally a cutting-edge feature will be available in a low-level API before it is available in SYCL, even as a SYCL extension. Some features may even be so backend-specific or so device-specific that they will never be exposed through SYCL. For example, some native backend APIs may provide access to queues with specific properties or unique kernel instructions for specific accelerator hardware. Although we hope and expect these cases to be rare, when these types of features exist, we may still gain access to them using backend interoperability.

## Support for Other Backends

The examples in this chapter demonstrated backend interoperability with OpenCL and Level Zero backends, but SYCL is a growing ecosystem and SYCL implementations are regularly adding support for additional backends and devices. For example, several SYCL implementations supporting CUDA and HIP backends already have some support for interoperability with these backends. Check the documentation for a SYCL implementation to determine which SYCL backends are supported and whether they support backend interoperability!

## Summary

In this chapter, we discovered how each SYCL object is associated with an underlying SYCL backend and how to query the SYCL backends in a system. We described how backend interoperability provides a mechanism for our SYCL application to directly interact with an underlying backend API. We discussed how this enables us to incrementally add SYCL to an application that is directly using a backend API, or to reuse libraries or utility functions written specifically for a backend API. We also discussed how backend interoperability reduces application portability, by restricting which SYCL devices the application will run on.

We specifically explored how backend interoperability for kernels provides similar functionality in SYCL 2020 that was present in earlier versions of SYCL. We examined how an online compiler extension can enable the use of some source languages for kernels, even if they are not directly understood by some SYCL backends.

## Chapter 20 Backend Interoperabi lity

Finally, we reviewed practical hints and tips to effectively use backend interoperability in our programs, such as how to choose a SYCL device for a specific SYCL backend, how to set up a SYCL context for backend interoperability, and how backend interoperability can provide access to features even if they have not been added to SYCL.

![](images/5a33a92a6019c42eaae871e4ad3660c775f08d99947a920f6697e9b18e9a7473.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
