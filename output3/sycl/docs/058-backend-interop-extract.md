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
