# CUDA Dynamic Parallelism Legacy (CDP1)

Legacy CUDA Dynamic Parallelism (CDP1) execution environment, memory model, synchronization, and programming interface.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14284-L14531

Citation: [CUDA_C_Programming_Guide:L14284-L14531]

````text

Functions using CDP1 and CDP2 may be loaded and run simultaneously in the same context. The CDP1 functions are able to use CDP1-specific features (e.g. cudaDeviceSynchronize) and CDP2 functions are able to use CDP2-specific features (e.g. tail launch and fire-and-forget launch).

A function using CDP1 cannot launch a function using CDP2, and vice versa. If a function that would use CDP1 contains in its call graph a function that would use CDP2, or vice versa, cudaErrorCdpVersionMismatch would result during function load.

## 13.6. Legacy CUDA Dynamic Parallelism (CDP1)

See CUDA Dynamic Parallelism, above, for CDP2 version of document.

## 13.6.1. Execution Environment and Memory Model (CDP1)

See Execution Environment and Memory Model, above, for CDP2 version of document.

## 13.6.1.1 Execution Environment (CDP1)

See Execution Environment, above, for CDP2 version of document.

The CUDA execution model is based on primitives of threads, thread blocks, and grids, with kernel functions defining the program executed by individual threads within a thread block and grid. When a kernel function is invoked the grid’s properties are described by an execution configuration, which has a special syntax in CUDA. Support for dynamic parallelism in CUDA extends the ability to configure, launch, and synchronize upon new grids to threads that are running on the device.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) block is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

## 13.6.1.1.1 Parent and Child Grids (CDP1)

See Parent and Child Grids, above, for CDP2 version of document.

A device thread that configures and launches a new grid belongs to the parent grid, and the grid created by the invocation is a child grid.

The invocation and completion of child grids is properly nested, meaning that the parent grid is not considered complete until all child grids created by its threads have completed. Even if the invoking threads do not explicitly synchronize on the child grids launched, the runtime guarantees an implicit synchronization between the parent and child.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

## 13.6.1.1.2 Scope of CUDA Primitives (CDP1)

See Scope of CUDA Primitives, above, for CDP2 version of document.

On both host and device, the CUDA runtime ofers an API for launching kernels, for waiting for launched work to complete, and for tracking dependencies between launches via streams and events. On the host system, the state of launches and the CUDA primitives referencing streams and events are shared by all threads within a process; however processes execute independently and may not share CUDA objects.

A similar hierarchy exists on the device: launched kernels and CUDA objects are visible to all threads in a thread block, but are independent between thread blocks. This means for example that a stream may be created by one thread and used by any other thread in the same thread block, but may not be shared with threads in any other thread block.

![](images/3fa47f76eed8fe946625ca98225dc8e58a66ad3027fff8b9f51b60abf169ff37.jpg)  
Figure 31: Parent-Child Launch Nesting

## 13.6.1.1.3 Synchronization (CDP1)

See Synchronization, above, for CDP2 version of document.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

CUDA runtime operations from any thread, including kernel launches, are visible across a thread block. This means that an invoking thread in the parent grid may perform synchronization on the grids launched by that thread, by other threads in the thread block, or on streams created within the same thread block. Execution of a thread block is not considered complete until all launches by all threads in the block have completed. If all threads in a block exit before all child launches have completed, a synchronization operation will automatically be triggered.

## 13.6.1.1.4 Streams and Events (CDP1)

See Streams and Events, above, for CDP2 version of document.

CUDA Streams and Events allow control over dependencies between grid launches: grids launched into the same stream execute in-order, and events may be used to create dependencies between streams. Streams and events created on the device serve this exact same purpose.

Streams and events created within a grid exist within thread block scope but have undefined behavior when used outside of the thread block where they were created. As described above, all work launched by a thread block is implicitly synchronized when the block exits; work launched into streams is included in this, with all dependencies resolved appropriately. The behavior of operations on a stream that has been modified outside of thread block scope is undefined.

Streams and events created on the host have undefined behavior when used within any kernel, just as streams and events created by a parent grid have undefined behavior if used within a child grid.

## 13.6.1.1.5 Ordering and Concurrency (CDP1)

See Ordering and Concurrency, above, for CDP2 version of document.

The ordering of kernel launches from the device runtime follows CUDA Stream ordering semantics. Within a thread block, all kernel launches into the same stream are executed in-order. With multiple threads in the same thread block launching into the same stream, the ordering within the stream is dependent on the thread scheduling within the block, which may be controlled with synchronization primitives such as \_\_syncthreads().

Note that because streams are shared by all threads within a thread block, the implicit NULL stream is also shared. If multiple threads in a thread block launch into the implicit stream, then these launches will be executed in-order. If concurrency is desired, explicit named streams should be used.

Dynamic Parallelism enables concurrency to be expressed more easily within a program; however, the device runtime introduces no new concurrency guarantees within the CUDA execution model. There is no guarantee of concurrent execution between any number of diferent thread blocks on a device.

The lack of concurrency guarantee extends to parent thread blocks and their child grids. When a parent thread block launches a child grid, the child is not guaranteed to begin execution until the parent thread block reaches an explicit synchronization point (such as cudaDeviceSynchronize()).

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

While concurrency will often easily be achieved, it may vary as a function of deviceconfiguration, application workload, and runtime scheduling. It is therefore unsafe to depend upon any concurrency between diferent thread blocks.

## 13.6.1.1.6 Device Management (CDP1)

See Device Management, above, for CDP2 version of document.

There is no multi-GPU support from the device runtime; the device runtime is only capable of operating on the device upon which it is currently executing. It is permitted, however, to query properties for any CUDA capable device in the system.

```lisp
__global__ void child_launch(int *data) {
    data[threadIdx.x] = data[threadIdx.x]+1;
}

__global__ void parent_launch(int *data) {
    data[threadIdx.x] = threadIdx.x;

    __syncthreads();

    if (threadIdx.x == 0) {
        child_launch<<< 1, 256 >>>(data);
        cudaDeviceSynchronize();
    }

    __syncthreads();
```

## 13.6.1.2 Memory Model (CDP1)

See Memory Model, above, for CDP2 version of document.

Parent and child grids share the same global and constant memory storage, but have distinct local and shared memory.

## 13.6.1.2.1 Coherence and Consistency (CDP1)

See Coherence and Consistency, above, for CDP2 version of document.

## 13.6.1.2.1.1 Global Memory (CDP1)

See Global Memory, above, for CDP2 version of document.

Parent and child grids have coherent access to global memory, with weak consistency guarantees between child and parent. There are two points in the execution of a child grid when its view of memory is fully consistent with the parent thread: when the child grid is invoked by the parent, and when the child grid completes as signaled by a synchronization API invocation in the parent thread.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ com pilation, and is slated for full removal in a future CUDA release.

All global memory operations in the parent thread prior to the child grid’s invocation are visible to the child grid. All memory operations of the child grid are visible to the parent after the parent has synchronized on the child grid’s completion.

In the following example, the child grid executing child\_launch is only guaranteed to see the modifications to data made before the child grid was launched. Since thread 0 of the parent is performing the launch, the child will be consistent with the memory seen by thread 0 of the parent. Due to the first \_\_syncthreads() call, the child will see data[0]=0, data[1]=1, …, data[255]=255 (without the \_\_syncthreads() call, only data[0] would be guaranteed to be seen by the child). When the child grid returns, thread 0 is guaranteed to see modifications made by the threads in its child grid. Those modifications become available to the other threads of the parent grid only after the second \_\_syncthreads() call:

(continues on next page)

```txt
}

void host_launch(int *data) {
    parent_launch<<< 1, 256 >>>(data);
}
```

(continued from previous page)

## 13.6.1.2.1.2 Zero Copy Memory (CDP1)

See Zero Copy Memory, above, for CDP2 version of document.

Zero-copy system memory has identical coherence and consistency guarantees to global memory, and follows the semantics detailed above. A kernel may not allocate or free zero-copy memory, but may use pointers to zero-copy passed in from the host program.

## 13.6.1.2.1.3 Constant Memory (CDP1)

See Constant Memory, above, for CDP2 version of document.

Constants are immutable and may not be modified from the device, even between parent and child launches. That is to say, the value of all \_\_constant\_\_ variables must be set from the host prior to launch. Constant memory is inherited automatically by all child kernels from their respective parents.

Taking the address of a constant memory object from within a kernel thread has the same semantics as for all CUDA programs, and passing that pointer from parent to child or from a child to parent is naturally supported.

## 13.6.1.2.1.4 Shared and Local Memory (CDP1)

See Shared and Local Memory, above, for CDP2 version of document.

Shared and Local memory is private to a thread block or thread, respectively, and is not visible or coherent between parent and child. Behavior is undefined when an object in one of these locations is referenced outside of the scope within which it belongs, and may cause an error.

The NVIDIA compiler will attempt to warn if it can detect that a pointer to local or shared memory is being passed as an argument to a kernel launch. At runtime, the programmer may use the \_\_is-Global() intrinsic to determine whether a pointer references global memory and so may safely be passed to a child launch.

Note that calls to cudaMemcpy\*Async() or cudaMemset\*Async() may invoke new child kernels on the device in order to preserve stream semantics. As such, passing shared or local memory pointers to these APIs is illegal and will return an error.

## 13.6.1.2.1.5 Local Memory (CDP1)

See Local Memory, above, for CDP2 version of document.

Local memory is private storage for an executing thread, and is not visible outside of that thread. It is illegal to pass a pointer to local memory as a launch argument when launching a child kernel. The result of dereferencing such a local memory pointer from a child will be undefined.

For example the following is illegal, with undefined behavior if x\_array is accessed by child\_launch:

```cpp
int x_array[10];      // Creates x_array in parent's local memory
child_launch<<< 1, 1 >>>(x_array);
```

It is sometimes dificult for a programmer to be aware of when a variable is placed into local memory by the compiler. As a general rule, all storage passed to a child kernel should be allocated explicitly from the global-memory heap, either with cudaMalloc(), new() or by declaring \_\_device\_\_ storage at global scope. For example:

```dart
// Correct - "value" is global storage
__device__ int value;
__device__ void x() {
    value = 5;
    child<<< 1, 1 >>>(&value);
}
```

```dart
// Invalid - "value" is local storage
__device__ void y() {
    int value = 5;
    child<<< 1, 1 >>>(&value);
}
```

## 13.6.1.2.1.6 Texture Memory (CDP1)

See Texture Memory, above, for CDP2 version of document.

Writes to the global memory region over which a texture is mapped are incoherent with respect to texture accesses. Coherence for texture memory is enforced at the invocation of a child grid and when a child grid completes. This means that writes to memory prior to a child kernel launch are reflected in texture memory accesses of the child. Similarly, writes to memory by a child will be reflected in the texture memory accesses by a parent, but only after the parent synchronizes on the child’s completion. Concurrent accesses by parent and child may result in inconsistent data.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

## 13.6.2. Programming Interface (CDP1)

See Programming Interface, above, for CDP2 version of document.

## 13.6.2.1 CUDA C++ Reference (CDP1)

See CUDA C++ Reference, above, for CDP2 version of document.

This section describes changes and additions to the CUDA C++ language extensions for supporting Dynamic Parallelism.

The language interface and API available to CUDA kernels using CUDA C++ for Dynamic Parallelism, referred to as the Device Runtime, is substantially like that of the CUDA Runtime API available on the host. Where possible the syntax and semantics of the CUDA Runtime API have been retained in order to facilitate ease of code reuse for routines that may run in either the host or device environments.

As with all code in CUDA C++, the APIs and code outlined here is per-thread code. This enables each thread to make unique, dynamic decisions regarding what kernel or operation to execute next. There are no synchronization requirements between threads within a block to execute any of the provided device runtime APIs, which enables the device runtime API functions to be called in arbitrarily divergent kernel code without deadlock.

## 13.6.2.1.1 Device-Side Kernel Launch (CDP1)

See Kernel Launch APIs, above, for CDP2 version of document.

Kernels may be launched from the device using the standard CUDA <<< >>> syntax:

```erlang
kernel_name<<< Dg, Db, Ns, S >>>([kernel arguments]);
```

▶ Dg is of type dim3 and specifies the dimensions and size of the grid

▶ Db is of type dim3 and specifies the dimensions and size of each thread block

Ns is of type size\_t and specifies the number of bytes of shared memory that is dynamically allocated per thread block for this call and addition to statically allocated memory. Ns is an optional argument that defaults to 0.

S is of type cudaStream\_t and specifies the stream associated with this call. The stream must have been allocated in the same thread block where the call is being made. S is an optional argument that defaults to 0.

## 13.6.2.1.1.1 Launches are Asynchronous (CDP1)

See Launches are Asynchronous, above, for CDP2 version of document.

Identical to host-side launches, all device-side kernel launches are asynchronous with respect to the launching thread. That is to say, the <<<>>> launch command will return immediately and the launching thread will continue to execute until it hits an explicit launch-synchronization point such as cudaDeviceSynchronize().

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

The grid launch is posted to the device and will execute independently of the parent thread. The child grid may begin execution at any time after launch, but is not guaranteed to begin execution until the launching thread reaches an explicit launch-synchronization point.

## 13.6.2.1.1.2 Launch Environment Configuration (CDP1)

See Launch Environment Configuration, above, for CDP2 version of document.

All global device configuration settings (for example, shared memory and L1 cache size as returned from cudaDeviceGetCacheConfig(), and device limits returned from cudaDeviceGetLimit()) will be inherited from the parent. Likewise, device limits such as stack size will remain as-configured.

For host-launched kernels, per-kernel configurations set from the host will take precedence over the global setting. These configurations will be used when the kernel is launched from the device as well. It is not possible to reconfigure a kernel’s environment from the device.
````

## Source CUDA_C_Programming_Guide:L14532-L14984

Citation: [CUDA_C_Programming_Guide:L14532-L14984]

````text
## 13.6.2.1.2 Streams (CDP1)

See Streams, above, for CDP2 version of document.

Both named and unnamed (NULL) streams are available from the device runtime. Named streams may be used by any thread within a thread-block, but stream handles may not be passed to other blocks or child/parent kernels. In other words, a stream should be treated as private to the block in which it is created. Stream handles are not guaranteed to be unique between blocks, so using a stream handle within a block that did not allocate it will result in undefined behavior.

Similar to host-side launch, work launched into separate streams may run concurrently, but actual concurrency is not guaranteed. Programs that depend upon concurrency between child kernels are not supported by the CUDA programming model and will have undefined behavior.

The host-side NULL stream’s cross-stream barrier semantic is not supported on the device (see below for details). In order to retain semantic compatibility with the host runtime, all device streams must be created using the cudaStreamCreateWithFlags() API, passing the cudaStreamNonBlocking flag. The cudaStreamCreate() call is a host-runtime- only API and will fail to compile for the device.

As cudaStreamSynchronize() and cudaStreamQuery() are unsupported by the device runtime, cudaDeviceSynchronize() should be used instead when the application needs to know that stream-launched child kernels have completed.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ com pilation, and is slated for full removal in a future CUDA release.

## 13.6.2.1.2.1 The Implicit (NULL) Stream (CDP1)

See The Implicit (NULL) Stream, above, for CDP2 version of document.

Within a host program, the unnamed (NULL) stream has additional barrier synchronization semantics with other streams (see Default Stream for details). The device runtime ofers a single implicit, unnamed stream shared between all threads in a block, but as all named streams must be created with the cudaStreamNonBlocking flag, work launched into the NULL stream will not insert an implicit dependency on pending work in any other streams (including NULL streams of other thread blocks).

## 13.6.2.1.3 Events (CDP1)

See Events, above, for CDP2 version of document.

Only the inter-stream synchronization capabilities of CUDA events are supported. This means that cudaStreamWaitEvent() is supported, but cudaEventSynchronize(), cudaEventElapsedTime(), and cudaEventQuery() are not. As cudaEventElapsedTime() is not supported, cudaEvents must be created via cudaEventCreateWithFlags(), passing the cudaEventDisableTiming flag.

As for all device runtime objects, event objects may be shared between all threads within the threadblock which created them but are local to that block and may not be passed to other kernels, or between blocks within the same kernel. Event handles are not guaranteed to be unique between blocks, so using an event handle within a block that did not create it will result in undefined behavior.

## 13.6.2.1.4 Synchronization (CDP1)

See Synchronization, above, for CDP2 version of document.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ com pilation, and is slated for full removal in a future CUDA release.

The cudaDeviceSynchronize() function will synchronize on all work launched by any thread in the thread-block up to the point where cudaDeviceSynchronize() was called. Note that cudaDeviceSynchronize() may be called from within divergent code (see Block Wide Synchronization (CDP1)).

It is up to the program to perform suficient additional inter-thread synchronization, for example via a call to \_\_syncthreads(), if the calling thread is intended to synchronize with child grids invoked from other threads.

## 13.6.2.1.4.1 Block Wide Synchronization (CDP1)

See CUDA Dynamic Parallelism, above, for CDP2 version of document.

The cudaDeviceSynchronize() function does not imply intra-block synchronization. In particular, without explicit synchronization via a \_\_syncthreads() directive the calling thread can make no assumptions about what work has been launched by any thread other than itself. For example if multiple threads within a block are each launching work and synchronization is desired for all this work at once (perhaps because of event-based dependencies), it is up to the program to guarantee that this work is submitted by all threads before calling cudaDeviceSynchronize().

Because the implementation is permitted to synchronize on launches from any thread in the block, it is quite possible that simultaneous calls to cudaDeviceSynchronize() by multiple threads will drain all work in the first call and then have no efect for the later calls.

## 13.6.2.1.5 Device Management (CDP1)

See Device Management, above, for CDP2 version of document.

Only the device on which a kernel is running will be controllable from that kernel. This means that device APIs such as cudaSetDevice() are not supported by the device runtime. The active device as seen from the GPU (returned from cudaGetDevice()) will have the same device number as seen from the host system. The cudaDeviceGetAttribute() call may request information about another device as this API allows specification of a device ID as a parameter of the call. Note that the catch-all cudaGetDeviceProperties() API is not ofered by the device runtime - properties must be queried individually.

## 13.6.2.1.6 Memory Declarations (CDP1)

See Memory Declarations, above, for CDP2 version of document.

## 13.6.2.1.6.1 Device and Constant Memory (CDP1)

See Device and Constant Memory, above, for CDP2 version of document.

Memory declared at file scope with \_\_device\_\_ or \_\_constant\_\_ memory space specifiers behaves identically when using the device runtime. All kernels may read or write device variables, whether the kernel was initially launched by the host or device runtime. Equivalently, all kernels will have the same view of \_\_constant\_\_s as declared at the module scope.

## 13.6.2.1.6.2 Textures and Surfaces (CDP1)

See Textures and Surfaces, above, for CDP2 version of document.

CUDA supports dynamically created texture and surface objects<sup>Page</sup> <sup>327,</sup> <sup>7</sup>, where a texture object may be created on the host, passed to a kernel, used by that kernel, and then destroyed from the host. The device runtime does not allow creation or destruction of texture or surface objects from within device code, but texture and surface objects created from the host may be used and passed around freely on the device. Regardless of where they are created, dynamically created texture objects are always valid and may be passed to child kernels from a parent.

Note: The device runtime does not support legacy module-scope (i.e., Fermi-style) textures and surfaces within a kernel launched from the device. Module-scope (legacy) textures may be created from the host and used in device code as for any kernel, but may only be used by a top-level kernel (i.e., the one which is launched from the host).

## 13.6.2.1.6.3 Shared Memory Variable Declarations (CDP1)

See Shared Memory Variable Declarations, above, for CDP2 version of document.

In CUDA C++ shared memory can be declared either as a statically sized file-scope or function-scoped variable, or as an extern variable with the size determined at runtime by the kernel’s caller via a launch configuration argument. Both types of declarations are valid under the device runtime.

```txt
__global__ void permute(int n, int *data) {
    extern __shared__ int smem[];
    if (n <= 1)
        return;

    smem[threadIdx.x] = data[threadIdx.x];
    __syncthreads();

    permute_data(smem, n);
    __syncthreads();

    // Write back to GMEM since we can't pass SMEM to children.
    data[threadIdx.x] = smem[threadIdx.x];
    __syncthreads();

    if (threadIdx.x == 0) {
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data);
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data+n/2);
    }
}

void host_launch(int *data) {
    permute<<< 1, 256, 256*sizeof(int) >>>(256, data);
}
```

## 13.6.2.1.6.4 Symbol Addresses (CDP1)

See Symbol Addresses, above, for CDP2 version of document.

Device-side symbols (i.e., those marked \_\_device\_\_) may be referenced from within a kernel simply via the & operator, as all global-scope device variables are in the kernel’s visible address space. This also applies to \_\_constant\_\_ symbols, although in this case the pointer will reference read-only data.

Given that device-side symbols can be referenced directly, those CUDA runtime APIs which reference symbols (for example, cudaMemcpyToSymbol() or cudaGetSymbolAddress()) are redundant and hence not supported by the device runtime. Note this implies that constant data cannot be altered from within a running kernel, even ahead of a child kernel launch, as references to \_\_constant\_\_ space are read-only.

## 13.6.2.1.7 API Errors and Launch Failures (CDP1)

See API Errors and Launch Failures, above, for CDP2 version of document.

As usual for the CUDA runtime, any function may return an error code. The last error code returned is recorded and may be retrieved via the cudaGetLastError() call. Errors are recorded per-thread, so that each thread can identify the most recent error that it has generated. The error code is of type cudaError\_t.

Similar to a host-side launch, device-side launches may fail for many reasons (invalid arguments, and so on). The user must call cudaGetLastError() to determine if a launch generated an error, however lack of an error after launch does not imply the child kernel completed successfully.

For device-side exceptions, for example, access to an invalid address, an error in a child grid will be returned to the host instead of being returned by the parent’s call to cudaDeviceSynchronize().

## 13.6.2.1.7.1 Launch Setup APIs (CDP1)

See Launch Setup APIs, above, for CDP2 version of document.

Kernel launch is a system-level mechanism exposed through the device runtime library, and as such is available directly from PTX via the underlying cudaGetParameterBuffer() and cudaLaunchDevice() APIs. It is permitted for a CUDA application to call these APIs itself, with the same requirements as for PTX. In both cases, the user is then responsible for correctly populating all necessary data structures in the correct format according to specification. Backwards compatibility is guaranteed in these data structures.

As with host-side launch, the device-side operator <<<>>> maps to underlying kernel launch APIs. This is so that users targeting PTX will be able to enact a launch, and so that the compiler front-end can translate <<<>>> into these calls.

Table 15: New Device-only Launch Implementation Functions

<table><tr><td>Runtime API Launch Functions</td><td>Description of Difference From Host Runtime Behaviour (behavior is identical if no description)</td></tr><tr><td>cudaGetParameter-Buffer</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr><tr><td>cudaLaunchDevice</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr></table>

The APIs for these launch functions are diferent to those of the CUDA Runtime API, and are defined as follows:

```txt
extern    device    cudaError_t cudaGetParameterBuffer(void **params);
extern __device__  cudaError_t cudaLaunchDevice(void *kernel,
                               void *params, dim3 gridDim,
                               dim3 blockDim,
                               unsigned int sharedMemSize = 0,
                               cudaStream_t stream = 0);
```

## 13.6.2.1.8 API Reference (CDP1)

See API Reference, above, for CDP2 version of document.

The portions of the CUDA Runtime API supported in the device runtime are detailed here. Host and device runtime APIs have identical syntax; semantics are the same except where indicated. The table below provides an overview of the API relative to the version available from the host.

Table 16: Supported API Functions

<table><tr><td>Runtime API Functions</td><td>Details</td></tr><tr><td>cudaDeviceSynchronize</td><td>Synchronizes on work launched from thread&#x27;s own block only.Warning: Note that calling this API from device code is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release.</td></tr><tr><td>cudaDeviceGetCacheConfig</td><td></td></tr><tr><td>cudaDeviceGetLimit</td><td></td></tr><tr><td>cudaGetLastError</td><td>Last error is per-thread state, not per-block state</td></tr><tr><td>cudaPeekAtLastError</td><td></td></tr><tr><td>cudaGetErrorString</td><td></td></tr><tr><td>cudaGetDeviceCount</td><td></td></tr><tr><td>cudaDeviceGetAttribute</td><td>Will return attributes for any device</td></tr><tr><td>cudaGetDevice</td><td>Always returns current device ID as would be seen from host</td></tr><tr><td>cudaStreamCreateWithFlags</td><td>Must pass cudaStreamNonBlocking flag</td></tr><tr><td>cudaStreamDestroy</td><td></td></tr><tr><td>cudaStreamWaitEvent</td><td></td></tr><tr><td>cudaEventCreateWithFlags</td><td>Must pass cudaEventDisableTiming flag</td></tr><tr><td>cudaEventRecord</td><td></td></tr><tr><td>cudaEventDestroy</td><td></td></tr><tr><td>cudaFuncGetAttributes</td><td></td></tr><tr><td>cudaMemcpyAsync</td><td rowspan="4">Notes about all memcpy/memset functions:► Only async memcpy/set functions are supported► Only device-to-device memcpy is permitted► May not pass in local or shared memory pointers</td></tr><tr><td>cudaMemcpy2DAsync</td></tr><tr><td>cudaMemcpy3DAsync</td></tr><tr><td>cudaMemsetAsync</td></tr><tr><td>cudaMemset2DAsync</td><td></td></tr><tr><td>cudaMemset3DAsync</td><td></td></tr><tr><td>cudaRuntimeGetVersion</td><td></td></tr><tr><td>cudaMalloc</td><td rowspan="2">May not call cudaFree on the device on a pointer created on the host, and vice-versa</td></tr><tr><td>cudaFree</td></tr><tr><td>cudaOccupancyMaxActiveBlocksPerMulti-processor</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize-VariableSMem</td><td></td></tr></table>

13.6. Legacy CUDA Dynamic Parallelism (CDP1)

## 13.6.2.2 Device-side Launch from PTX (CDP1)

See Device-side Launch from PTX, above, for CDP2 version of document.

This section is for the programming language and compiler implementers who target Parallel Thread Execution (PTX) and plan to support Dynamic Parallelism in their language. It provides the low-level details related to supporting kernel launches at the PTX level.

## 13.6.2.2.1 Kernel Launch APIs (CDP1)

See Kernel Launch APIs, above, for CDP2 version of document.

Device-side kernel launches can be implemented using the following two APIs accessible from PTX: cudaLaunchDevice() and cudaGetParameterBuffer(). cudaLaunchDevice() launches the specified kernel with the parameter bufer that is obtained by calling cudaGetParameterBuffer() and filled with the parameters to the launched kernel. The parameter bufer can be NULL, i.e., no need to invoke cudaGetParameterBuffer(), if the launched kernel does not take any parameters.

## 13.6.2.2.1.1 cudaLaunchDevice (CDP1)

See cudaLaunchDevice, above, for CDP2 version of document.

At the PTX level, cudaLaunchDevice()needs to be declared in one of the two forms shown below before it is used.

```txt
// PTX-level Declaration of cudaLaunchDevice() when .address_size is 64
 extern .func(.param .b32 func_retval0) cudaLaunchDevice
(
  .param .b64 func,
  .param .b64 parameterBuffer,
  .param .align 4 .b8 gridDimension[12],
  .param .align 4 .b8 blockDimension[12],
  .param .b32 sharedMemSize,
  .param .b64 stream
)
;
```

```txt
// PTX-level Declaration of cudaLaunchDevice() when .address_size is 32
.extern .func(.param .b32 func_retval0) cudaLaunchDevice
(
    .param .b32 func,
    .param .b32 parameterBuffer,
    .param .align 4 .b8 gridDimension[12],
    .param .align 4 .b8 blockDimension[12],
    .param .b32 sharedMemSize,
    .param .b32 stream
)
;
```

The CUDA-level declaration below is mapped to one of the aforementioned PTX-level declarations and is found in the system header file cuda\_device\_runtime\_api.h. The function is defined in the cudadevrt system library, which must be linked with a program in order to use device-side kernel launch functionality.

```c
// CUDA-level declaration of cudaLaunchDevice()
extern "C" __device__
cudaError_t cudaLaunchDevice(void *func, void *parameterBuffer,
                       dim3 gridDimension, dim3 blockDimension,
                       unsigned int sharedMemSize,
                       cudaStream_t stream);
```

The first parameter is a pointer to the kernel to be is launched, and the second parameter is the parameter bufer that holds the actual parameters to the launched kernel. The layout of the parameter bufer is explained in Parameter Bufer Layout (CDP1), below. Other parameters specify the launch configuration, i.e., as grid dimension, block dimension, shared memory size, and the stream associated with the launch (please refer to Execution Configuration for the detailed description of launch configuration.

## 13.6.2.2.1.2 cudaGetParameterBufer (CDP1)

See cudaGetParameterBufer, above, for CDP2 version of document.

cudaGetParameterBuffer() needs to be declared at the PTX level before it’s used. The PTX-level declaration must be in one of the two forms given below, depending on address size:

```txt
// PTX-level Declaration of cudaGetParameterBuffer() when .address_size is 64
// When .address_size is 64
.extern .func(.param .b64 func_retval0) cudaGetParameterBuffer
(
    .param .b64 alignment,
    .param .b64 size
)
;

// PTX-level Declaration of cudaGetParameterBuffer() when .address_size is 32
.extern .func(.param .b32 func_retval0) cudaGetParameterBuffer
(
    .param .b32 alignment,
    .param .b32 size
)
;
```

The following CUDA-level declaration of cudaGetParameterBuffer() is mapped to the aforementioned PTX-level declaration:

```c
// CUDA-level Declaration of cudaGetParameterBuffer()
extern "C" __device__
void *cudaGetParameterBuffer(size_t alignment, size_t size);
```

The first parameter specifies the alignment requirement of the parameter bufer and the second parameter the size requirement in bytes. In the current implementation, the parameter bufer returned by cudaGetParameterBuffer() is always guaranteed to be 64- byte aligned, and the alignment requirement parameter is ignored. However, it is recommended to pass the correct alignment requirement value - which is the largest alignment of any parameter to be placed in the parameter bufer - to cudaGetParameterBuffer() to ensure portability in the future

## 13.6.2.2.2 Parameter Bufer Layout (CDP1)

See Parameter Bufer Layout, above, for CDP2 version of document.

Parameter reordering in the parameter bufer is prohibited, and each individual parameter placed in the parameter bufer is required to be aligned. That is, each parameter must be placed at the n<sup>th</sup> byte in the parameter bufer, where n is the smallest multiple of the parameter size that is greater than the ofset of the last byte taken by the preceding parameter. The maximum size of the parameter bufer is 4KB.

For a more detailed description of PTX code generated by the CUDA compiler, please refer to the PTX-3.5 specification.

## 13.6.2.3 Toolkit Support for Dynamic Parallelism (CDP1)

See Toolkit Support for Dynamic Parallelism, above, for CDP2 version of document.

## 13.6.2.3.1 Including Device Runtime API in CUDA Code (CDP1)

See Including Device Runtime API in CUDA Code, above, for CDP2 version of document.

Similar to the host-side runtime API, prototypes for the CUDA device runtime API are included automatically during program compilation. There is no need to include cuda\_device\_runtime\_api.h explicitly.

## 13.6.2.3.2 Compiling and Linking (CDP1)

See Compiling and Linking, above, for CDP2 version of document.

When compiling and linking CUDA programs using dynamic parallelism with nvcc, the program will automatically link against the static device runtime library libcudadevrt.

The device runtime is ofered as a static library (cudadevrt.lib on Windows, libcudadevrt.a under Linux), against which a GPU application that uses the device runtime must be linked. Linking of device libraries can be accomplished through nvcc and/or nvlink. Two simple examples are shown below.

A device runtime program may be compiled and linked in a single step, if all required source files can be specified from the command line:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

It is also possible to compile CUDA .cu source files first to object files, and then link these together in a two-stage process:

```shell
$ nvcc -arch=sm_75 -dc hello_world.cu -o hello_world.o
$ nvcc -arch=sm_75 -rdc=true hello_world.o -o hello -lcudadevrt
```

Please see the Using Separate Compilation section of The CUDA Driver Compiler NVCC guide for more details.

## 13.6.3. Programming Guidelines (CDP1)

See Programming Guidelines, above, for CDP2 version of document.

## 13.6.3.1 Basics (CDP1)

See Basics, above, for CDP2 version of document.

The device runtime is a functional subset of the host runtime. API level device management, kernel launching, device memcpy, stream management, and event management are exposed from the device runtime.

Programming for the device runtime should be familiar to someone who already has experience with CUDA. Device runtime syntax and semantics are largely the same as that of the host API, with any exceptions detailed earlier in this document.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

The following example shows a simple Hello World program incorporating dynamic parallelism:

```cpp
#include <stdio.h>

__global__ void childKernel()
{
    printf("Hello ");
}

__global__ void parentKernel()
{
    // launch child
    childKernel<<<1,1>>>();
    if (cudaSuccess != cudaGetLastError()) {
        return;
    }

    // wait for child to complete
    if (cudaSuccess != cudaDeviceSynchronize()) {
        return;
    }

    printf("World!\n");
}

int main(int argc, char *argv[])
{
    // launch parent
    parentKernel<<<1,1>>>();
    if (cudaSuccess != cudaGetLastError()) {
        return 1;
    }

    // wait for parent to complete
```

(continues on next page)

```txt
if (cudaSuccess != cudaDeviceSynchronize()) {
    return 2;
}

return 0;
}
```

This program may be built in a single step from the command line as follows:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

## 13.6.3.2 Performance (CDP1)

See Performance, above, for CDP2 version of document.

## 13.6.3.2.1 Synchronization (CDP1)

See CUDA Dynamic Parallelism, above, for CDP2 version of document.

Warning: Explicit synchronization with child kernels from a parent block (such as using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

Synchronization by one thread may impact the performance of other threads in the same Thread Block, even when those other threads do not call cudaDeviceSynchronize() themselves. This impact will depend upon the underlying implementation. In general the implicit synchronization of child kernels done when a thread block ends is more eficient compared to calling cudaDeviceSynchronize() explicitly. It is therefore recommended to only call cudaDeviceSynchronize() if it is needed to synchronize with a child kernel before a thread block ends.

## 13.6.3.2.2 Dynamic-parallelism-enabled Kernel Overhead (CDP1)

## See Dynamic-parallelism-enabled Kernel Overhead, above, for CDP2 version of document.

System software which is active when controlling dynamic launches may impose an overhead on any kernel which is running at the time, whether or not it invokes kernel launches of its own. This overhead arises from the device runtime’s execution tracking and management software and may result in decreased performance for example, library calls when made from the device compared to from the host side. This overhead is, in general, incurred for applications that link against the device runtime library.

## 13.6.3.3 Implementation Restrictions and Limitations (CDP1)

See Implementation Restrictions and Limitations, above, for CDP2 version of document.

Dynamic Parallelism guarantees all semantics described in this document, however, certain hardware and software resources are implementation-dependent and limit the scale, performance and other properties of a program which uses the device runtime.

## 13.6.3.3.1 Runtime (CDP1)

See Runtime, above, for CDP2 version of document.

## 13.6.3.3.1.1 Memory Footprint (CDP1)

See Memory Footprint, above, for CDP2 version of document.

The device runtime system software reserves memory for various management purposes, in particular one reservation which is used for saving parent-grid state during synchronization, and a second reservation for tracking pending grid launches. Configuration controls are available to reduce the size of these reservations in exchange for certain launch limitations. See Configuration Options (CDP1), below, for details.

The majority of reserved memory is allocated as backing-store for parent kernel state, for use when synchronizing on a child launch. Conservatively, this memory must support storing of state for the maximum number of live threads possible on the device. This means that each parent generation at which cudaDeviceSynchronize() is callable may require up to 860MB of device memory, depending on the device configuration, which will be unavailable for program use even if it is not all consumed.

## 13.6.3.3.1.2 Nesting and Synchronization Depth (CDP1)

See CUDA Dynamic Parallelism, above, for CDP2 version of document.

Using the device runtime, one kernel may launch another kernel, and that kernel may launch another, and so on. Each subordinate launch is considered a new nesting level, and the total number of levels is the nesting depth of the program. The synchronization depth is defined as the deepest level at which the program will explicitly synchronize on a child launch. Typically this is one less than the nesting depth of the program, but if the program does not need to call cudaDeviceSynchronize() at all levels then the synchronization depth might be substantially diferent to the nesting depth.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ com pilation, and is slated for full removal in a future CUDA release.

The overall maximum nesting depth is limited to 24, but practically speaking the real limit will be the amount of memory required by the system for each new level (see Memory Footprint (CDP1) above). Any launch which would result in a kernel at a deeper level than the maximum will fail. Note that this may also apply to cudaMemcpyAsync(), which might itself generate a kernel launch. See Configuration Options (CDP1) for details.

By default, suficient storage is reserved for two levels of synchronization. This maximum synchronization depth (and hence reserved storage) may be controlled by calling cudaDeviceSetLimit()

and specifying cudaLimitDevRuntimeSyncDepth. The number of levels to be supported must be configured before the top-level kernel is launched from the host, in order to guarantee successful execution of a nested program. Calling cudaDeviceSynchronize() at a depth greater than the specified maximum synchronization depth will return an error.

An optimization is permitted where the system detects that it need not reserve space for the parent’s state in cases where the parent kernel never calls cudaDeviceSynchronize(). In this case, because explicit parent/child synchronization never occurs, the memory footprint required for a program will be much less than the conservative maximum. Such a program could specify a shallower maximum synchronization depth to avoid over-allocation of backing store.

## 13.6.3.3.1.3 Pending Kernel Launches (CDP1)

See Pending Kernel Launches, above, for CDP2 version of document.

When a kernel is launched, all associated configuration and parameter data is tracked until the kernel completes. This data is stored within a system-managed launch pool.

The launch pool is divided into a fixed-size pool and a virtualized pool with lower performance. The device runtime system software will try to track launch data in the fixed-size pool first. The virtualized pool will be used to track new launches when the fixed-size pool is full.

The size of the fixed-size launch pool is configurable by calling cudaDeviceSetLimit() from the host and specifying cudaLimitDevRuntimePendingLaunchCount.

## 13.6.3.3.1.4 Configuration Options (CDP1)

See Configuration Options, above, for CDP2 version of document.

Resource allocation for the device runtime system software is controlled via the cudaDevice-SetLimit() API from the host program. Limits must be set before any kernel is launched, and may not be changed while the GPU is actively running programs.

Warning: Explicit synchronization with child kernels from a parent block (i.e. using cudaDeviceSynchronize() in device code) is deprecated in CUDA 11.6, removed for compute\_90+ compilation, and is slated for full removal in a future CUDA release.

The following named limits may be set:

<table><tr><td>Limit</td><td>Behavior</td></tr><tr><td>cudaLimitDevRun-timeSyncDepth</td><td>Sets the maximum depth at which cudaDeviceSynchronize() may be called. Launches may be performed deeper than this, but explicit synchronization deeper than this limit will return the cudaErrorLaunchMaxDepthExceeded. The default maximum sync depth is 2.</td></tr><tr><td>cudaLimitDevRuntimePendingLaunchCount</td><td>Controls the amount of memory set aside for buffering kernel launches which have not yet begun to execute, due either to unresolved dependencies or lack of execution resources. When the buffer is full, the device runtime system software will attempt to track new pending launches in a lower performance virtualized buffer. If the virtualized buffer is also full, i.e. when all available heap space is consumed, launches will not occur, and the thread&#x27;s last error will be set to cudaErrorLaunchPendingCountExceeded. The default pending launch count is 2048 launches.</td></tr><tr><td>cudaLimitStackSize</td><td>Controls the stack size in bytes of each GPU thread. The CUDA driver automatically increases the per-thread stack size for each kernel launch as needed. This size isn&#x27;t reset back to the original value after each launch. To set the per-thread stack size to a different value, cudaDeviceSetLimit() can be called to set this limit. The stack will be immediately resized, and if necessary, the device will block until all preceding requested tasks are complete. cudaDeviceGetLimit() can be called to get the current per-thread stack size.</td></tr></table>

## 13.6.3.3.1.5 Memory Allocation and Lifetime (CDP1)

See Memory Allocation and Lifetime, above, for CDP2 version of document.

cudaMalloc() and cudaFree() have distinct semantics between the host and device environments. When invoked from the host, cudaMalloc() allocates a new region from unused device memory. When invoked from the device runtime these functions map to device-side malloc() and free(). This implies that within the device environment the total allocatable memory is limited to the device malloc() heap size, which may be smaller than the available unused device memory. Also, it is an error to invoke cudaFree() from the host program on a pointer which was allocated by cudaMalloc() on the device or vice-versa.

<table><tr><td></td><td>cudaMalloc() on Host</td><td>cudaMalloc() on Device</td></tr><tr><td>cudaFree() on Host</td><td>Supported</td><td>Not Supported</td></tr><tr><td>cudaFree() on Device</td><td>Not Supported</td><td>Supported</td></tr><tr><td>Allocation limit</td><td>Free device memory</td><td>cudaLimitMallocHeapSize</td></tr></table>

## 13.6.3.3.1.6 SM Id and Warp Id (CDP1)

See SM Id and Warp Id, above, for CDP2 version of document.

Note that in PTX %smid and %warpid are defined as volatile values. The device runtime may reschedule thread blocks onto diferent SMs in order to more eficiently manage resources. As such, it is unsafe to rely upon %smid or %warpid remaining unchanged across the lifetime of a thread or thread block.

## 13.6.3.3.1.7 ECC Errors (CDP1)

See ECC Errors, above, for CDP2 version of document.

No notification of ECC errors is available to code within a CUDA kernel. ECC errors are reported at the host side once the entire launch tree has completed. Any ECC errors which arise during execution of a nested program will either generate an exception or continue execution (depending upon error and configuration).
````
