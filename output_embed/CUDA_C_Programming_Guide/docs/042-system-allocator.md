## System Allocator

```txt
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}
void test_malloc() {
    int *ret = (int*)malloc(1000 * sizeof(int));
    // for shared page table systems, the following hint is not necessary
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directManagedMemAccessFromHost=1:
CPU accesses GPU memory directly without migrations
                                // directManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    free(ret);
}
```

## Managed

```cpp
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}

void test_managed() {
    int *ret;
    cudaMallocManaged(&ret, 1000 * sizeof(int));
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);  // set direct access hint

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directedManagedMemAccessFromHost=1:
CPU accesses GPU memory directly without migrations
                                // directedManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directedManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directedManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    cudaFree(ret);
}
```

After write kernel is completed, ret will be created and initialized in GPU memory. Next, the CPU will access ret followed by append kernel using the same ret memory again. This code will show diferent behavior depending on the system architecture and support of hardware coherency:

▶ On systems with directManagedMemAccessFromHost=1: CPU accesses to the managed bufer will not trigger any migrations; the data will remain resident in GPU memory and any subsequent GPU kernels can continue to access it directly without inflicting faults or migrations.

▶ On systems with directManagedMemAccessFromHost=0: CPU accesses to the managed bufer will page fault and initiate data migration; any GPU kernel trying to access the same data first time will page fault and migrate pages back to GPU memory.

## 24.2.2.3 Host Native Atomics

Some devices, including NVLink-connected devices in hardware coherent systems, support hardwareaccelerated atomic accesses to CPU-resident memory. This implies that atomic accesses to host memory do not have to be emulated with a page fault. For these devices, the attribute cudaDevAttrHostNativeAtomicSupported is set to 1.

## 24.2.2.4 Atomic accesses & synchronization primitives

CUDA Unified Memory supports all atomic operations available to host and device threads, enabling all threads to cooperate by concurrently accessing the same shared memory location. The CUDA C++ standard library provides many heterogeneous synchronization primitives tuned for concurrent use between host and device threads, including cuda::atomic, cuda::atomic\_ref, cuda::barrier, cuda::semaphore, among many others.

On systems without CPU and GPU page tables: hardware coherency vs. software coherency, atomic accesses from the device to file-backed host memory are not supported. The following example code is valid on systems with CPU and GPU page tables: hardware coherency vs. software coherency but exhibits undefined behavior on other systems:

```cpp
#include <cuda/atomic>

#include <cstdio>
#include <fcntl.h>
#include <sys/mman.h>

#define ERR(msg, ...) { fprintf(stderr, msg, ##__VA_ARGS_); return EXIT_FAILURE; }

__global__ void kernel(int* ptr) {
    cuda::atomic_ref{*ptr}.store(2);
}

int main() {
    // this will be closed/deleted by default on exit
    FILE* tmp_file = tmpfile64();
    // need to allocate space in the file, we do this with posix_fallocate here
    int status = posix_fallocate(fileno(tmp_file), 0, 4096);
    if (status != 0) ERR("Failed to allocate space in temp file\n");
    int* ptr = (int*)mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE, fileno(tmp_file), 0);
    if (ptr == MAP_FAILED) ERR("Failed to map temp file\n");

    // initialize the value in our file-backed memory
    *ptr = 1;
    printf("Atom value: %d\n", *ptr);

    // device and host thread access ptr concurrently, using cuda::atomic_ref
    kernel<<<1, 1>>>(ptr);
    while (cuda::atomic_ref{*ptr}.load() != 2);
    // this will always be 2
    printf("Atom value: %d\n", *ptr);

    return EXIT_SUCCESS;
}
```

On systems without CPU and GPU page tables: hardware coherency vs. software coherency, atomic accesses to unified memory may incur page faults which can lead to significant latencies. Note that this is not the case for all GPU atomics to CPU memory on these systems: operations listed by nvidia-smi -q | grep "Atomic Caps Outbound" may avoid page faults.

On systems with CPU and GPU page tables: hardware coherency vs. software coherency, atomics between host and device do not require page faults, but may still fault for other reasons that any memory access can fault for.

## 24.2.2.5 Memcpy()/Memset() Behavior With Unified Memory

cudaMemcpy\*() and cudaMemset\*() accept any unified memory pointer as arguments.

For cudaMemcpy\*(), the direction specified as cudaMemcpyKind is a performance hint, which can have a higher performance impact if any of the arguments is a unified memory pointer.

Thus, it is recommended to follow the following performance advice:

▶ When the physical location of unified memory is known, use an accurate cudaMemcpyKind hint.

Prefer cudaMemcpyDefault over an inaccurate cudaMemcpyKind hint.

Always use populated (initialized) bufers: avoid using these APIs to initialize memory.

▶ Avoid using cudaMemcpy\*() if both pointers point to System-Allocated Memory: launch a kernel or use a CPU memory copy algorithm such as std::memcpy instead.

## 24.3. Unified memory on devices without full CUDA Unified Memory support

## 24.3.1. Unified memory on devices with only CUDA Managed Memory support

For devices with compute capability 6.x or higher but without pageable memory access, CUDA Managed Memory is fully supported and coherent. The programming model and performance tuning of unified memory is largely similar to the model as described in Unified memory on devices with full CUDA Unified Memory support, with the notable exception that system allocators cannot be used to allocate memory. Thus, the following list of sub-sections do not apply:

▶ System-Allocated Memory: in-depth examples

▶ Hardware/Software Coherency

## 24.3.2. Unified memory on Windows or devices with compute capability 5.x

Devices with compute capability lower than 6.0 or Windows platforms support CUDA Managed Memory v1.0 with limited support for data migration and coherency as well as memory oversubscription. The following sub-sections describe in more detail how to use and optimize Managed Memory on these platforms.

## 24.3.2.1 Data Migration and Coherency

GPU architectures of compute capability lower than 6.0 do not support fine-grained movement of the managed data to GPU on-demand. Whenever a GPU kernel is launched all managed memory generally has to be transferred to GPU memory to avoid faulting on memory access. With compute capability 6.x a new GPU page faulting mechanism is introduced that provides more seamless Unified Memory functionality. Combined with the system-wide virtual address space, page faulting provides several benefits. First, page faulting means that the CUDA system software doesn’t need to synchronize all managed memory allocations to the GPU before each kernel launch. If a kernel running on the GPU accesses a page that is not resident in its memory, it faults, allowing the page to be automatically migrated to the GPU memory on-demand. Alternatively, the page may be mapped into the GPU address space for access over the PCIe or NVLink interconnects (mapping on access can sometimes be faster than migration). Note that Unified Memory is system-wide: GPUs (and CPUs) can fault on and migrate memory pages either from CPU memory or from the memory of other GPUs in the system.

## 24.3.2.2 GPU Memory Oversubscription

Devices of compute capability lower than 6.0 cannot allocate more managed memory than the physical size of GPU memory.

## 24.3.2.3 Multi-GPU

On systems with devices of compute capabilities lower than 6.0 managed allocations are automatically visible to all GPUs in a system via the peer-to-peer capabilities of the GPUs. Managed memory allocations behave similar to unmanaged memory allocated using cudaMalloc(): the current active device is the home for the physical allocation but other GPUs in the system will access the memory at reduced bandwidth over the PCIe bus.

On Linux the managed memory is allocated in GPU memory as long as all GPUs that are actively being used by a program have the peer-to-peer support. If at any time the application starts using a GPU that doesn’t have peer-to-peer support with any of the other GPUs that have managed allocations on them, then the driver will migrate all managed allocations to system memory. In this case, all GPUs experience PCIe bandwidth restrictions.

On Windows, if peer mappings are not available (for example, between GPUs of diferent architectures), then the system will automatically fall back to using zero-copy memory, regardless of whether both GPUs are actually used by a program. If only one GPU is actually going to be used, it is necessary to set the CUDA\_VISIBLE\_DEVICES environment variable before launching the program. This constrains which GPUs are visible and allows managed memory to be allocated in GPU memory.

Alternatively, on Windows users can also set CUDA\_MANAGED\_FORCE\_DEVICE\_ALLOC to a non-zero value to force the driver to always use device memory for physical storage. When this environment variable is set to a non-zero value, all devices used in that process that support managed memory have to be peer-to-peer compatible with each other. The error ::cudaErrorInvalidDevice will be returned if a device that supports managed memory is used and it is not peer-to-peer compatible with any of the other managed memory supporting devices that were previously used in that process, even if ::cudaDeviceReset has been called on those devices. These environment variables are described in CUDA Environment Variables. Note that starting from CUDA 8.0 CUDA\_MANAGED\_FORCE\_DEVICE\_ALLOC has no efect on Linux operating systems.

## 24.3.2.4 Coherency and Concurrency

Simultaneous access to managed memory on devices of compute capability lower than 6.0 is not possible, because coherence could not be guaranteed if the CPU accessed a Unified Memory allocation while a GPU kernel was active.

## 24.3.2.4.1 GPU Exclusive Access To Managed Memory

To ensure coherency on pre-6.x GPU architectures, the Unified Memory programming model puts constraints on data accesses while both the CPU and GPU are executing concurrently. In efect, the GPU has exclusive access to all managed data while any kernel operation is executing, regardless of whether the specific kernel is actively using the data. When managed data is used with cudaMemcpy\*() or cudaMemset\*(), the system may choose to access the source or destination from the host or the device, which will put constraints on concurrent CPU access to that data while the cudaMemcpy\*() or cudaMemset\*() is executing. See Memcpy()/Memset() Behavior With Unified Memory for further details.

It is not permitted for the CPU to access any managed allocations or variables while the GPU is active for devices with concurrentManagedAccess property set to 0. On these systems concurrent CPU/GPU accesses, even to diferent managed memory allocations, will cause a segmentation fault because the page is considered inaccessible to the CPU.

```txt
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    kernel<<< 1, 1 >>>();
    y = 20;          // Error on GPUs not supporting concurrent access

    cudaDeviceSynchronize();
    return  0;
}
```

In example above, the GPU program kernel is still active when the CPU touches y. (Note how it occurs before cudaDeviceSynchronize().) The code runs successfully on devices of compute capability 6.x due to the GPU page faulting capability which lifts all restrictions on simultaneous access. However, such memory access is invalid on pre-6.x architectures even though the CPU is accessing diferent data than the GPU. The program must explicitly synchronize with the GPU before accessing y:

```txt
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    kernel<<< 1, 1 >>>();
```

(continues on next page)

(continued from previous page)

```txt
cudaDeviceSynchronize();
y = 20;          // Success on GPUs not supporting concurrent access
return  0;
}
```

As this example shows, on systems with pre-6.x GPU architectures, a CPU thread may not access any managed data in between performing a kernel launch and a subsequent synchronization call, regardless of whether the GPU kernel actually touches that same data (or any managed data at all). The mere potential for concurrent CPU and GPU access is suficient for a process-level exception to be raised.

Note that if memory is dynamically allocated with cudaMallocManaged() or cuMemAllocManaged() while the GPU is active, the behavior of the memory is unspecified until additional work is launched or the GPU is synchronized. Attempting to access the memory on the CPU during this time may or may not cause a segmentation fault. This does not apply to memory allocated using the flag cudaMemAttachHost or CU\_MEM\_ATTACH\_HOST.

## 24.3.2.4.2 Explicit Synchronization and Logical GPU Activity

Note that explicit synchronization is required even if kernel runs quickly and finishes before the CPU touches y in the above example. Unified Memory uses logical activity to determine whether the GPU is idle. This aligns with the CUDA programming model, which specifies that a kernel can run at any time following a launch and is not guaranteed to have finished until the host issues a synchronization call.

Any function call that logically guarantees the GPU completes its work is valid. This includes cudaDeviceSynchronize(); cudaStreamSynchronize() and cudaStreamQuery() (provided it returns cudaSuccess and not cudaErrorNotReady) where the specified stream is the only stream still executing on the GPU; cudaEventSynchronize() and cudaEventQuery() in cases where the specified event is not followed by any device work; as well as uses of cudaMemcpy() and cudaMemset() that are documented as being fully synchronous with respect to the host.

Dependencies created between streams will be followed to infer completion of other streams by synchronizing on a stream or event. Dependencies can be created via cudaStreamWaitEvent() or implicitly when using the default (NULL) stream.

It is legal for the CPU to access managed data from within a stream callback, provided no other stream that could potentially be accessing managed data is active on the GPU. In addition, a callback that is not followed by any device work can be used for synchronization: for example, by signaling a condition variable from inside the callback; otherwise, CPU access is valid only for the duration of the callback(s).

There are several important points of note:

▶ It is always permitted for the CPU to access non-managed zero-copy data while the GPU is active.

The GPU is considered active when it is running any kernel, even if that kernel does not make use of managed data. If a kernel might use data, then access is forbidden, unless device property concurrentManagedAccess is 1.

There are no constraints on concurrent inter-GPU access of managed memory, other than those that apply to multi-GPU access of non-managed memory.

▶ There are no constraints on concurrent GPU kernels accessing managed data.

Note how the last point allows for races between GPU kernels, as is currently the case for non-managed GPU memory. As mentioned previously, managed memory functions identically to non-managed memory from the perspective of the GPU. The following code example illustrates these points:

```cpp
int main() {
    cudaStream_t stream1, stream2;
    cudaStreamCreate(&stream1);
    cudaStreamCreate(&stream2);
    int *non_managed, *managed, *also_managed;
    cudaMallocHost(&non_managed, 4);      // Non-managed, CPU-accessible memory
    cudaMallocManaged(&managed, 4);
    cudaMallocManaged(&also_managed, 4);
    // Point 1: CPU can access non-managed data.
    kernel<<< 1, 1, 0, stream1 >>>(managed);
    *non_managed = 1;
    // Point 2: CPU cannot access any managed data while GPU is busy,
    //          unless concurrentManagedAccess = 1
    // Note we have not yet synchronized, so "kernel" is still active.
    *also_managed = 2;          // Will issue segmentation fault
    // Point 3: Concurrent GPU kernels can access the same data.
    kernel<<< 1, 1, 0, stream2 >>>(managed);
    // Point 4: Multi-GPU concurrent access is also permitted.
    cudaSetDevice(1);
    kernel<<< 1, 1 >>>(managed);
    return   0;
}
```

## 24.3.2.4.3 Managing Data Visibility and Concurrent CPU + GPU Access with Streams

Until now it was assumed that for SM architectures before 6.x: 1) any active kernel may use any managed memory, and 2) it was invalid to use managed memory from the CPU while a kernel is active. Here we present a system for finer-grained control of managed memory designed to work on all devices supporting managed memory, including older architectures with concurrentManagedAccess equal to 0.

The CUDA programming model provides streams as a mechanism for programs to indicate dependence and independence among kernel launches. Kernels launched into the same stream are guaranteed to execute consecutively, while kernels launched into diferent streams are permitted to execute concurrently. Streams describe independence between work items and hence allow potentially greater eficiency through concurrency.

Unified Memory builds upon the stream-independence model by allowing a CUDA program to explicitly associate managed allocations with a CUDA stream. In this way, the programmer indicates the use of data by kernels based on whether they are launched into a specified stream or not. This enables opportunities for concurrency based on program-specific data access patterns. The function to control this behavior is:

```txt
cudaError_t cudaStreamAttachMemAsync(cudaStream_t stream,
                                      void *ptr,
                                      size_t length=0,
                                      unsigned int flags=0);
```

The cudaStreamAttachMemAsync() function associates length bytes of memory starting from ptr with the specified stream. (Currently, length must always be 0 to indicate that the entire region should be attached.) Because of this association, the Unified Memory system allows CPU access to this memory region so long as all operations in stream have completed, regardless of whether other streams are active. In efect, this constrains exclusive ownership of the managed memory region by an active GPU to per-stream activity instead of whole-GPU activity.

Most importantly, if an allocation is not associated with a specific stream, it is visible to all running kernels regardless of their stream. This is the default visibility for a cudaMallocManaged() allocation or a \_\_managed\_\_ variable; hence, the simple-case rule that the CPU may not touch the data while any kernel is running.

By associating an allocation with a specific stream, the program makes a guarantee that only kernels launched into that stream will touch that data. No error checking is performed by the Unified Memory system: it is the programmer’s responsibility to ensure that guarantee is honored.

In addition to allowing greater concurrency, the use of cudaStreamAttachMemAsync() can (and typically does) enable data transfer optimizations within the Unified Memory system that may afect latencies and other overhead.

## 24.3.2.4.4 Stream Association Examples

Associating data with a stream allows fine-grained control over CPU + GPU concurrency, but what data is visible to which streams must be kept in mind when using devices of compute capability lower than 6.0. Looking at the earlier synchronization example:

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    cudaStream_t stream1;
    cudaStreamCreate(&stream1);
    cudaStreamAttachMemAsync(stream1, &y, 0, cudaMemcpyAttachHost);
    cudaDeviceSynchronize();          // Wait for Host attachment to occur.
    kernel<<< 1, 1, 0, stream1 >>>(); // Note: Launches into stream1.
    y = 20;                               // Success - a kernel is running but "y"
                                // has been associated with no stream.
    return  0;
}
```

Here we explicitly associate y with host accessibility, thus enabling access at all times from the CPU. (As before, note the absence of cudaDeviceSynchronize() before the access.) Accesses to y by the GPU running kernel will now produce undefined results.

Note that associating a variable with a stream does not change the associating of any other variable. For example, associating x with stream1 does not ensure that only x is accessed by kernels launched in stream1, thus an error is caused by this code:

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    cudaStream_t stream1;
    cudaStreamCreate(&stream1);
    cudaStreamAttachMemAsync(stream1, &x); // Associate "x" with stream1.
    cudaDeviceSynchronize();          // Wait for "x" attachment to occur.
    kernel<<< 1, 1, 0, stream1 >>>();
    y = 20;                                // ERROR: "y" is still associated globally
                                        // with all streams by default
    return  0;
}
```

Note how the access to y will cause an error because, even though x has been associated with a stream, we have told the system nothing about who can see y. The system therefore conservatively assumes that kernel might access it and prevents the CPU from doing so.

## 24.3.2.4.5 Stream Attach With Multithreaded Host Programs

The primary use for cudaStreamAttachMemAsync() is to enable independent task parallelism using CPU threads. Typically in such a program, a CPU thread creates its own stream for all work that it generates because using CUDA’s NULL stream would cause dependencies between threads.

The default global visibility of managed data to any GPU stream can make it dificult to avoid interactions between CPU threads in a multi-threaded program. Function cudaStreamAttachMemAsync() is therefore used to associate a thread’s managed allocations with that thread’s own stream, and the association is typically not changed for the life of the thread.

Such a program would simply add a single call to cudaStreamAttachMemAsync() to use unified memory for its data accesses:

```aidl
// This function performs some task, in its own private stream.
void run_task(int *in, int *out, int length) {
    // Create a stream for us to use.
    cudaStream_t stream;
    cudaStreamCreate(&stream);
    // Allocate some managed data and associate with our stream.
    // Note the use of the host-attach flag to cudaMallocManaged();
    // we then associate the allocation with our stream so that
    // our GPU kernel launches can access it.
    int *data;
    cudaMallocManaged((void **)&data, length, cudaMemcpyAttachHost);
    cudaStreamAttachMemAsync(stream, data);
    cudaStreamSynchronize(stream);
    // Iterate on the data in some way, using both Host & Device.
    for(int i=0; i<N; i++) {
        transform<<< 100, 256, 0, stream >>>(in, data, length);
        cudaStreamSynchronize(stream);
        host_process(data, length);      // CPU uses managed data.
        convert<<< 100, 256, 0, stream >>>(out, data, length);
    }
    cudaStreamSynchronize(stream);
    cudaStreamDestroy(stream);
    cudaFree(data);
}
```

In this example, the allocation-stream association is established just once, and then data is used repeatedly by both the host and device. The result is much simpler code than occurs with explicitly copying data between host and device, although the result is the same.

## 24.3.2.4.6 Advanced Topic: Modular Programs and Data Access Constraints

In the previous example cudaMallocManaged() specifies the cudaMemAttachHost flag, which creates an allocation that is initially invisible to device-side execution. (The default allocation would be visible to all GPU kernels on all streams.) This ensures that there is no accidental interaction with another thread’s execution in the interval between the data allocation and when the data is acquired for a specific stream.

Without this flag, a new allocation would be considered in-use on the GPU if a kernel launched by another thread happens to be running. This might impact the thread’s ability to access the newly allocated data from the CPU (for example, within a base-class constructor) before it is able to explicitly attach it to a private stream. To enable safe independence between threads, therefore, allocations should be made specifying this flag.

Note: An alternative would be to place a process-wide barrier across all threads after the allocation has been attached to the stream. This would ensure that all threads complete their data/stream associations before any kernels are launched, avoiding the hazard. A second barrier would be needed before the stream is destroyed because stream destruction causes allocations to revert to their default visibility. The cudaMemAttachHost flag exists both to simplify this process, and because it is not always possible to insert global barriers where required.

## 24.3.2.4.7 Memcpy()/Memset() Behavior With Stream-associated Unified Memory

See Memcpy()/Memset() Behavior With Unified Memory for a general overview of cudaMemcpy\* / cudaMemset\* behavior on devices with concurrentManagedAccess set. On devices where concurrentManagedAccess is not set, the following rules apply:

If cudaMemcpyHostTo\* is specified and the source data is unified memory, then it will be accessed from the host if it is coherently accessible from the host in the copy stream (1); otherwise it will be accessed from the device. Similar rules apply to the destination when cudaMemcpy\*ToHost is specified and the destination is unified memory.

If cudaMemcpyDeviceTo\* is specified and the source data is unified memory, then it will be accessed from the device. The source must be coherently accessible from the device in the copy stream (2); otherwise, an error is returned. Similar rules apply to the destination when cudaMemcpy\*ToDevice is specified and the destination is unified memory.

If cudaMemcpyDefault is specified, then unified memory will be accessed from the host either if it cannot be coherently accessed from the device in the copy stream (2) or if the preferred location for the data is cudaCpuDeviceId and it can be coherently accessed from the host in the copy stream (1); otherwise, it will be accessed from the device.

When using cudaMemset\*() with unified memory, the data must be coherently accessible from the device in the stream being used for the cudaMemset() operation (2); otherwise, an error is returned.

When data is accessed from the device either by cudaMemcpy\* or cudaMemset\*, the stream of operation is considered to be active on the GPU. During this time, any CPU access of data that is associated with that stream or data that has global visibility, will result in a segmentation fault if the GPU has a zero value for the device attribute concurrentManagedAccess. The program must synchronize appropriately to ensure the operation has completed before accessing any associated data from the CPU.

1. Coherently accessible from the host in a given stream means that the memory neither has global visibility nor is it associated with the given stream.

2. Coherently accessible from the device in a given stream means that the memory either has global visibility or is associated with the given stream.

# Chapter 25. Lazy Loading

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## 25.1. What is Lazy Loading?

Lazy Loading delays loading of CUDA modules and kernels from program initialization closer to kernels execution. If a program does not use every single kernel it has included, then some kernels will be loaded unneccessarily. This is very common, especially if you include any libraries. Most of the time, programs only use a small amount of kernels from libraries they include.

Thanks to Lazy Loading, programs are able to only load kernels they are actually going to use, saving time on initialization. This reduces memory overhead, both on GPU memory and host memory.

Lazy Loading is enabled by setting the CUDA\_MODULE\_LOADING environment variable to LAZY

Firstly, CUDA Runtime will no longer load all modules during program initialization, with the exception of modules containing managed variables. Each module will be loaded on first usage of a variable or a kernel from that module. This optimization is only relevant to CUDA Runtime users, CUDA Driver users who use cuModuleLoad are unafected. This optimization shipped in CUDA 11.8. The behavior for CUDA Driver users who use cuLibraryLoad to load module data into memory can be changed by setting the CUDA\_MODULE\_DATA\_LOADING environment variable.

Secondly, loading a module (cuModuleLoad\*() family of functions) will not be loading kernels immediately, instead it will delay loading of a kernel until cuModuleGetFunction() is called. There are certain exceptions here, some kernels have to be loaded during cuModuleLoad\*(), such as kernels of which pointers are stored in global variables. This optimization is relevant to both CUDA Runtime and CUDA Driver users. CUDA Runtime will only call cuModuleGetFunction() when a kernel is used/referenced for the first time. This optimization shipped in CUDA 11.7.

Both of these optimizations are designed to be invisible to the user, assuming CUDA Programming Model is followed.

## 25.2. Lazy Loading version support

Lazy Loading is a CUDA Runtime and CUDA Driver feature. Upgrades to both might be necessary to utilize the feature.

## 25.2.1. Driver

Lazy Loading requires R515+ user-mode library, but it supports Forward Compatibility, meaning it can run on top of older kernel mode drivers.

Without R515+ user-mode library, Lazy Loading is not available in any shape or form, even if toolkit version is 11.7+.

## 25.2.2. Toolkit

Lazy Loading was introduced in CUDA 11.7, and received a significant upgrade in CUDA 11.8.

If your application uses CUDA Runtime, then in order to see benefits from Lazy Loading your application must use 11.7+ CUDA Runtime.

As CUDA Runtime is usually linked statically into programs and libraries, this means that you have to recompile your program with CUDA 11.7+ toolkit and use CUDA 11.7+ libraries.

Otherwise you will not see the benefits of Lazy Loading, even if your driver version supports it.

If only some of your libraries are 11.7+, you will only see benefits of Lazy Loading in those libraries. Other libraries will still load everything eagerly.

## 25.2.3. Compiler

Lazy Loading does not require any compiler support. Both SASS and PTX compiled with pre-11.7 compilers can be loaded with Lazy Loading enabled, and will see full benefits of the feature. However, 11.7+ CUDA Runtime is still required, as described above.

## 25.3. Triggering loading of kernels in lazy mode

Loading kernels and variables happens automatically, without any need for explicit loading. Simply launching a kernel or referencing a variable or a kernel will automatically load relevant modules and kernels.

However, if for any reason you wish to load a kernel without executing it or modifying it in any way, we recommend the following.

## 25.3.1. CUDA Driver API

Loading of kernels happens during cuModuleGetFunction() call. This call is necessary even without Lazy Loading, as it is the only way to obtain a kernel handle.

However, you can also use this API to control with finer granularity when kernels are loaded.

## 25.3.2. CUDA Runtime API

CUDA Runtime API manages module management automatically, so we recommend simply using cudaFuncGetAttributes() to reference the kernel.

This will ensure that the kernel is loaded without changing the state.

## 25.4. Querying whether Lazy Loading is Turned On

In order to check whether user enabled Lazy Loading, CUresult cuModuleGetLoadingMode ( CUmoduleLoadingMode\* mode ) can be used.

It’s important to note that CUDA must be initialized before running this function. Sample usage can be seen in the snippet below.

```cpp
#include "cuda.h"
#include "assert.h"
#include "iostream"

int main() {
    CUmoduleLoadingMode mode;

    assert(CUDA_SUCCESS == cuInit(0));
    assert(CUDA_SUCCESS == cuModuleGetLoadingMode(&mode));

    std::cout << "CUDA Module Loading Mode is " << ((mode == CU_MODULE_LAZY_LOADING) ? "lazy" : "eager") << std::endl;

    return 0;
}
```

# 25.5. Possible Issues when Adopting Lazy Loading

Lazy Loading is designed so that it should not require any modifications to applications to use it. That said, there are some caveats, especially when applications are not fully compliant with CUDA Programming Model.

## 25.5.1. Concurrent Execution

Loading kernels might require context synchronization. Some programs incorrectly treat the possibility of concurrent execution of kernels as a guarantee. In such cases, if program assumes that two kernels will be able to execute concurrently, and one of the kernels will not return without the other kernel executing, there is a possibility of a deadlock.

If kernel A will be spinning in an infinite loop until kernel B is executing. In such case launching kernel B will trigger lazy loading of kernel B. If this loading will require context synchronization, then we have a deadlock: kernel A is waiting for kernel B, but loading kernel B is stuck waiting for kernel A to finish to synchronize the context.

Such program is an anti-pattern, but if for any reason you want to keep it you can do the following:

▶ preload all kernels that you hope to execute concurrently prior to launching them

▶ run application with CUDA\_MODULE\_DATA\_LOADING=EAGER to force loading data eagerly without forcing each function to load eagerly

## 25.5.2. Allocators

Lazy Loading delays loading code from initialization phase of the program closer to execution phase. Loading code onto the GPU requires memory allocation.

If your application tries to allocate the entire VRAM on startup, for example, to use it for its own allocator, then it might turn out that there will be no more memory left to load the kernels. This is despite the fact that overall Lazy Loading frees up more memory for the user. CUDA will need to allocate some memory to load each kernel, which usually happens at first launch time of each kernel. If your application allocator greedily allocated everything, CUDA will fail to allocate memory.

Possible solutions:

▶ use cudaMallocAsync() instead of an allocator that allocates the entire VRAM on startup

▶ add some bufer to compensate for the delayed loading of kernels

▶ preload all kernels that will be used in the program before trying to initialize your allocator

## 25.5.3. Autotuning

Some applications launch several kernels implementing the same functionality to determine which one is the fastest. While it is overall advisable to run at least one warmup iteration, it becomes especially important with Lazy Loading. After all, including time taken to load the kernel will skew your results.

Possible solutions:

▶ do at least one warmup interaction prior to measurement

▶ preload the benchmarked kernel prior to launching it
