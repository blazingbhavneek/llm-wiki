## 14.4. Reserving a Virtual Address Range

Since with Virtual Memory Management the notions of address and memory are distinct, applications must carve out an address range that can hold the memory allocations made by cuMemCreate. The address range reserved must be at least as large as the sum of the sizes of all the physical memory allocations the user plans to place in them.

Applications can reserve a virtual address range by passing appropriate parameters to cuMemAddressReserve. The address range obtained will not have any device or host physical memory associated with it. The reserved virtual address range can be mapped to memory chunks belonging to any device in the system, thus providing the application a continuous VA range backed and mapped by memory belonging to diferent devices. Applications are expected to return the virtual address range back to CUDA using cuMemAddressFree. Users must ensure that the entire VA range is unmapped before calling cuMemAddressFree. These functions are conceptually similar to mmap/munmap (on Linux) or VirtualAlloc/VirtualFree (on Windows) functions. The following code snippet illustrates the usage for the function:

```txt
CUdeviceptr ptr;
// `ptr` holds the returned start of virtual address range reserved.
CUresult result = cuMemAddressReserve(&ptr, size, 0, 0, 0); // alignment = 0 for
    default alignment
```

## 14.5. Virtual Aliasing Support

The Virtual Memory Management APIs provide a way to create multiple virtual memory mappings or “proxies” to the same allocation using multiple calls to cuMemMap with diferent virtual addresses, socalled virtual aliasing. Unless otherwise noted in the PTX ISA, writes to one proxy of the allocation are considered inconsistent and incoherent with any other proxy of the same memory until the writing device operation (grid launch, memcpy, memset, and so on) completes. Grids present on the GPU prior to a writing device operation but reading after the writing device operation completes are also considered to have inconsistent and incoherent proxies.

For example, the following snippet is considered undefined, assuming device pointers A and B are virtual aliases of the same memory allocation:

```txt
__global__ void foo(char *A, char *B) {
  *A = 0x1;
  printf("%d\n", *B);    // Undefined behavior!  *B can take on either
// the previous value or some value in-between.
}
```

The following is defined behavior, assuming these two kernels are ordered monotonically (by streams or events).

```txt
__global__ void foo1(char *A) {
    *A = 0x1;
}

__global__ void foo2(char *B) {
    printf("%d\n", *B);      // *B == *A == 0x1 assuming foo2 waits for foo1
// to complete before launching
```

(continues on next page)

(continued from previous page)

```txt
}
cudaMemcpyAsync(B, input, size, stream1);    // Aliases are allowed at
// operation boundaries
foo1<<<1,1,0,stream1>>>(A);                  // allowing foo1 to access A.
cudaEventRecord(event, stream1);
cudaStreamWaitEvent(stream2, event);
foo2<<<1,1,0,stream2>>>(B);
cudaStreamWaitEvent(stream3, event);
cudaMemcpyAsync(output, B, size, stream3);   // Both launches of foo2 and
                                // cudaMemcpy (which both
                                // read) wait for foo1 (which writes)
                                // to complete before proceeding
```

If accessing same allocation through diferent “proxies” is required in the same kernel a fence.proxy. alias can be used between the two accesses. The above example can thus be made legal with inline PTX assembly:

```lisp
__global__ void foo(char *A, char *B) {
    *A = 0x1;
    asm volatile ("fence.proxy.alias;" ::: "memory");
    printf("%d\n", *B);      // *B == *A == 0x1
}
```

## 14.6. Mapping Memory

The allocated physical memory and the carved out virtual address space from the previous two sections represent the memory and address distinction introduced by the Virtual Memory Management APIs. For the allocated memory to be useable, the user must first place the memory in the address space. The address range obtained from cuMemAddressReserve and the physical allocation obtained from cuMemCreate or cuMemImportFromShareableHandle must be associated with each other by using cuMemMap.

Users can associate allocations from multiple devices to reside in contiguous virtual address ranges as long as they have carved out enough address space. In order to decouple the physical allocation and the address range, users must unmap the address of the mapping by using cuMemUnmap. Users can map and unmap memory to the same address range as many times as they want, as long as they ensure that they don’t attempt to create mappings on VA range reservations that are already mapped. The following code snippet illustrates the usage for the function:

```javascript
CUdeviceptr ptr;
// `ptr`: address in the address range previously reserved by cuMemAddressReserve.
// `allocHandle`: CUmemGenericAllocationHandle obtained by a previous call to
    →cuMemCreate.
CUresult result = cuMemMap(ptr, size, 0, allocHandle, 0);
```

## 14.7. Controlling Access Rights

The Virtual Memory Management APIs enable applications to explicitly protect their VA ranges with access control mechanisms. Mapping the allocation to a region of the address range using cuMemMap does not make the address accessible, and would result in a program crash if accessed by a CUDA kernel. Users must specifically select access control using the cuMemSetAccess function, which allows or restricts access for specific devices to a mapped address range. The following code snippet illustrates the usage for the function:

```txt
void setAccessOnDevice(int device, CUdeviceptr ptr, size_t size) {
    CUmemAccessDesc accessDesc = {};
    accessDesc.location.type = CU_MEM_LOCATION_TYPE_DEVICE;
    accessDesc.location.id = device;
    accessDesc.flags = CU_MEM_ACCESS_FLAGS_PROT_READWRITE;

    // Make the address accessible
    cuMemSetAccess(ptr, size, &accessDesc, 1);
}
```

The access control mechanism exposed with Virtual Memory Management allows users to be explicit about which allocations they want to share with other peer devices on the system. As specified earlier, cudaEnablePeerAccess forces all prior and future cudaMalloc’d allocations to be mapped to the target peer device. This can be convenient in many cases as user doesn’t have to worry about tracking the mapping state of every allocation to every device in the system. But for users concerned with performance of their applications this approach has performance implications. With access control at allocation granularity Virtual Memory Management exposes a mechanism to have peer mappings with minimal overhead.

The vectorAddMMAP sample can be used as an example for using the Virtual Memory Management APIs.

## 14.8. Fabric Memory

CUDA 12.4 introduced a new VMM allocation handle type CU\_MEM\_HANDLE\_TYPE\_FABRIC. On supported platforms and provided the NVIDIA IMEX daemon is running this allocation handle type enables sharing allocations not only intra node with any communication mechanism, e.g. MPI, but also inter node. This allows GPUs in a Multi Node NVLINK System to map the memory of all other GPUs part of the same NVLINK fabric even if they are in diferent nodes greatly increasing the scale of multi-GPU Programming with NVLINK.

## 14.8.1. Query for Support

Before attempting to use Fabric Memory, applications must ensure that the devices they want to use support Fabric Memory. The following code sample shows querying for Fabric Memory support:

```txt
int deviceSupportsFabricMem;
CUresult result = cuDeviceGetAttribute(&deviceSupportsFabricMem, CU_DEVICE_ATTRIBUTE_HANDLE_TYPE_FABRIC_SUPPORTED, device);
if (deviceSupportsFabricMem != 0) {
```

(continues on next page)

(continued from previous page)

```txt
// `device` supports Fabric Memory
}
```

Aside from using CU\_MEM\_HANDLE\_TYPE\_FABRIC as handle type and not requiring OS native mechanisms for inter process communication to exchange sharable handles there is no diference in using Fabric Memory compared to other allocation handle types.

## 14.9. Multicast Support

The Multicast Object Management APIs provide a way for the application to create Multicast Objects and in combination with the Virtual Memory Management APIs described above allow applications to leverage NVLINK SHARP on supported NVLINK connected GPUs if they are connected with NVSWITCH. NVLINK SHARP allows CUDA applications to leverage in fabric computing to accelerate operations like broadcast and reductions between GPUs connected with NVSWITCH. For this to work multiple NVLINK connected GPUs form a Multicast Team and each GPU from the team backs up a Multicast Object with physical memory. So a Multicast Team of N GPUs has N physical replicas, each local to one participating GPU, of a Multicast Object. The multimem PTX instructions using mappings of Multicast Objects work with all replicas of the Multicast Object.

To work with Multicast Objects an application needs to

▶ Query Multicast Support

Create a Multicast Handle with cuMulticastCreate.

Share the Multicast Handle with all processes that control a GPU which should participate in a Multicast Team. This works with cuMemExportToShareableHandle as described above.

▶ Add all GPUs that should participate in the Multicast Team with cuMulticastAddDevice.

For each participating GPU bind physical memory allocated with cuMemCreate as described above to the Multicast Handle. All devices need to be added to the Multicast Team before binding memory on any device.

▶ Reserve an address range, map the Multicast Handle and set Access Rights as described above for regular Unicast mappings. Unicast and Multicast mappings to the same physical memory are possible. See the Virtual Aliasing Support section above how to ensure consistency between multiple mappings to the same physical memory.

▶ Use the multimem PTX instructions with the multicast mappings.

The multi\_node\_p2p example in the Multi GPU Programming Models GitHub repository contains a complete example using Fabric Memory including Multicast Objects to leverage NVLINK SHARP. Please note that this example is for developers of libraries like NCCL or NVSHMEM. It shows how higher-level programming models like NVSHMEM work internally within a (multinode) NVLINK domain. Application developers generally should use the higher-level MPI, NCCL, or NVSHMEM interfaces instead of this API.

## 14.9.1. Query for Support

Before attempting to use Multicast Objects, applications must ensure that the devices they want to use support them. The following code sample shows querying for Fabric Memory support:

```javascript
int deviceSupportsMultiCast;
CUresult result = cuDeviceGetAttribute(&deviceSupportsMultiCast, CU_DEVICE_ATTRIBUTE_MULTICAST_SUPPORTED, device);
if (deviceSupportsMultiCast != 0) {
    // `device` supports Multicast Objects
}
```

## 14.9.2. Allocating Multicast Objects

Multicast Objects can be created with cuMulticastCreate:

```cpp
CUmemGenericAllocationHandle createMCHandle(int numDevices, size_t size) {
    CUmemAllocationProp mcProp = {};
    mcProp.numDevices = numDevices;
    mcProp.handleTypes = CU_MEM_HANDLE_TYPE_FABRIC; // or on single node CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR

    size_t granularity = 0;
    cuMulticastGetGranularity(&granularity, &mcProp, CU_MEM_ALLOC_GRANULARITY_MINIMUM);

    // Ensure size matches granularity requirements for the allocation
    size_t padded_size = ROUND_UP(size, granularity);

    mcProp.size = padded_size;

    // Create Multicast Object this has no devices and no physical memory associated yet
    CUmemGenericAllocationHandle mcHandle;
    cuMulticastCreate(&mcHandle, &mcProp);

    return mcHandle;
}
```

## 14.9.3. Add Devices to Multicast Objects

Devices can be added to a Multicast Team with cuMulticastAddDevice:

```javascript
cuMulticastAddDevice(&mcHandle, device);
```

This step needs to be completed on all processes controlling devices that should participate in a Multicast Team before memory on any device is bound to the Multicast Object.

## 14.9.4. Bind Memory to Multicast Objects

After a Multicast Object has been created and all participating devices have been added to the Multicast Object it needs to be backed with physical memory allocated with cuMemCreate for each device:

cuMulticastBindMem(mcHandle, mcOffset, memHandle, memOffset, size, 0 ∕\*flags\*∕);

## 14.9.5. Use Multicast Mappings

To use Multicast Mappings in CUDA C++ it is required to use the multimem PTX instructions with Inline PTX Assembly:

```txt
__global__ void all_reduce_norm_barrier_kernel(float* l2_norm,
                                float* partial_l2_norm_mc,
                                unsigned int* arrival_counter_uc,
    unsigned int* arrival_counter_mc,
                                const unsigned int expected_count) {
        assert( 1 == blockDim.x * blockDim.y * blockDim.z * gridDim.x * gridDim.y *
        gridDim.z );
        float l2_norm_sum = 0.0;
#if __CUDA_ARCH__ >= 900

        // atomic reduction to all replicas
        // this can be conceptually thought of as __threadfence_system(); atomicAdd_
        system(arrival_counter_mc, 1);
        asm volatile ("multimem.red.release.sys.global.add.u32 [%0], %1;" :: "l"(arrival_
        counter_mc), "n"(1) : "memory");

        // Need a fence between Multicast (mc) and Unicast (uc) access to the same memory
        `arrival_counter_uc` and `arrival_counter_mc`:
        // - fence.proxy instructions establish an ordering between memory accesses that
        may happen through different proxies
        // - Value .alias of the .proxykind qualifier refers to memory accesses performed
        using virtually aliased addresses to the same memory location.
        // from https://docs.nvidia.com/cuda/parallel-thread-execution/#parallel-
        synchronization-and-communication-instructions-membar
        asm volatile ("fence.proxy.alias;" ::: "memory");

        // spin wait with acquire ordering on UC mapping till all peers have arrived in
        this iteration
        // Note: all ranks need to reach another barrier after this kernel, such that it is
        not possible for the barrier to be unblocked by an
        // arrival of a rank for the next iteration if some other rank is slow.
        cuda::atomic_ref<unsigned int,cuda::thread_scope_system> ac(arrival_counter_uc);
        while (expected_count > ac.load(cuda::memory_order_acquire));

        // Atomic load reduction from all replicas. It does not provide ordering so it can
        be relaxed.
        asm volatile ("multimem.ld_reduce.relaxed.sys.global.add.f32 %0, [%1];" : "=f"(l2_
        norm_sum) : "l"(partial_l2_norm_mc) : "memory");

#else
    #error "ERROR: multimem instructions require compute capability 9.0 or larger."
#endif
```

(continues on next page)

(continued from previous page)

$$
* 1 2 \_ n o r m = s t d:: s q r t (1 2 \_ n o r m \_ s u m);
$$

# Chapter 15. Stream Ordered Memory Allocator
