# Multicast Support

Details NVLINK SHARP support via Multicast Objects, cuMulticastCreate, cuMulticastAddDevice, and multimem PTX instructions for broadcast/reductions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15256-L15391

Citation: [CUDA_C_Programming_Guide:L15256-L15391]

````text
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

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.
````
