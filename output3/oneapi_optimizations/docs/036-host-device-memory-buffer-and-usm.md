## References

1. Matrix Multiplication Performance

2. Matrix Multiplication

## Host/Device Memory, Buffer and USM

Accelerators have access to a rich memory hierarchy. Utilizing the right level in the hierarchy is critical to getting the best performance.

In this section we cover topics related to declaration, movement, and access to the memory hierarchy.

The API allows sharing of memory objects across different device processes. Since each process has its own virtual address space, there is no guarantee that the same virtual address will be available when the memory object is shared in new process. There are a set of APIs that make it easier to share the memory objects.

To learn more about using the oneAPI Level Zero API for memory sharing, see Inter-Process Communication in the Level Zero Specification.

• Unified Shared Memory Allocations

• Performance Impact of USM and Buffers

• Avoiding Moving Data Back and Forth between Host and Device

• Optimizing Data Transfers

• Avoiding Declaring Buffers in a Loop

• Buffer Accessor Modes

## Unified Shared Memory Allocations

Unified Shared Memory (USM) allows a program to use C/C++ pointers for memory access. There are three ways to allocate memory in SYCL:

## malloc\_device:

• Allocation can only be accessed by the specified device but not by other devices in the context nor by host.

• The data stays on the device all the time and thus is the fastest choice for kernel execution.

• Explicit copy is needed to transfer data to the host or other devices in the context.

## malloc\_host:

• Allocation can be accessed by the host and any other device in the context.

• The data stays on the host all the time and is accessed via PCI from the devices.

• No explicit copy is needed for synchronizing of the data with the host or devices.

## malloc\_shared:

• Allocation can be accessed by the host and the specified device only.

• The data can migrate (operated by the Level-Zero driver) between the host and the device for faster access.

• No explicit copy is necessary for synchronizing between the host and the device, but it is needed for other devices in the context.

The three kinds of memory allocations and their characteristics are summarized in the table below.

Memory allocation types and characteristics

<table><tr><td>Memory allocation types</td><td>Description</td><td>Host accessible</td><td>Device accessible</td><td>Location</td></tr><tr><td>host</td><td>allocated in host memory</td><td>yes</td><td>yes, remotely through PCIe or fabric link</td><td>host</td></tr><tr><td>device</td><td>allocated in device memory</td><td>no</td><td>yes</td><td>device</td></tr><tr><td>shared</td><td>allocated shared between host and device</td><td>yes</td><td>yes</td><td>dynamically migrate between host and device</td></tr></table>

In a multi-stack, multi-C-slice GPU environment, it is important to note that device and shared USM allocations are associated with the root device. Hence, they are accessible by all the stacks and C-slices on the same device. A program should use root device for malloc\_device and malloc\_shared allocations to avoid confusion.

## OpenMP USM Allocation API

To align with SYCL USM model, we added three new OpenMP APIs as Intel extensions for users to perform memory allocations based on application, memory size and performance requirements. Their semantics and performance characteristics are detailed in the following subsections.

## Host Memory Allocation

This host allocation is easier to use than device allocations since we do not have to manually copy data between the host and the device. Host allocations are allocations in host memory that are accessible on both the host and the device. These allocations, while accessible on the device, cannot migrate to the device’s attached memory. Instead, offloading regions that read from or write to this memory do it remotely through either PCIe bus or fabric link. This tradeoff between convenience and performance is something that we must take into consideration. Despite the higher access costs that host allocations can incur, there are still valid reasons to use them. Examples include rarely accessed data or large data sets that cannot fit inside device attached memory. The API to perform host memory allocation is:

```txt
extern void *omp_target_alloc_host(size_t size, int device_num)
```

## Device Memory Allocation

This kind of allocation is what users need in order to have a pointer into a device’s attached memory, such as (G)DDR, or HBM on the device. Device allocations can be read from or written to by offloading regions running on a device, but they cannot be directly accessed from code executing on the host. Trying to access a device allocation on the host can result in either incorrect data or a program crashing. The API to perform device memory allocation is:

```c
extern void *omp_target_alloc_device(size_t size, int device_num)
```

## Shared Memory Allocation

Like host allocations, shared allocations are accessible on both the host and the device. The difference between them is that shared allocations are free to migrate between host memory and device attached memory, automatically, without our intervention. If an allocation has migrated to the device, any offloading region executing on that device accessing it will do so with greater performance than remotely accessing it from the host. However, shared allocations do not give us all the benefits without any drawbacks such as page migration cost and ping-pong effects:

extern void \*omp\_target\_alloc\_shared(size\_t size, int device\_num)

USM Support for omp\_target\_alloc API

The OpenMP API for target memory allocation maps to:

```c
extern void *omp_target_alloc_device(size_t size, int device_num)
```

## Performance Impact of USM and Buffers

SYCL offers several choices for managing memory on the device. This section discusses the performance tradeoffs, briefly introducing the concepts. For an in-depth explanation, see Data Parallel C++.

As with other language features, the specification defines the behavior but not the implementation, so performance characteristics can change between software versions and devices. This guide provide best practices.

Buffers. A buffer is a container for data that can be accessed from a device and the host. The SYCL runtime manages memory by providing APIs for allocating, reading, and writing memory. The runtime is responsible for moving data between host and device, and synchronizing access to the data.
