
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
