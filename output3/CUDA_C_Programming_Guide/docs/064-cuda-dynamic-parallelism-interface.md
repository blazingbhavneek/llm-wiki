
## 13.3.1. CUDA C++ Reference

This section describes changes and additions to the CUDA C++ language extensions for supporting Dynamic Parallelism.

The language interface and API available to CUDA kernels using CUDA C++ for Dynamic Parallelism, referred to as the Device Runtime, is substantially like that of the CUDA Runtime API available on the host. Where possible the syntax and semantics of the CUDA Runtime API have been retained in order to facilitate ease of code reuse for routines that may run in either the host or device environments.

As with all code in CUDA C++, the APIs and code outlined here is per-thread code. This enables each thread to make unique, dynamic decisions regarding what kernel or operation to execute next. There are no synchronization requirements between threads within a block to execute any of the provided device runtime APIs, which enables the device runtime API functions to be called in arbitrarily divergent kernel code without deadlock.

## 13.3.1.1 Device-Side Kernel Launch

Kernels may be launched from the device using the standard CUDA <<< >>> syntax:

```erlang
kernel_name<<< Dg, Db, Ns, S >>>([kernel arguments]);
```

▶ Dg is of type dim3 and specifies the dimensions and size of the grid

▶ Db is of type dim3 and specifies the dimensions and size of each thread block

▶ Ns is of type size\_t and specifies the number of bytes of shared memory that is dynamically allocated per thread block for this call in addition to statically allocated memory. Ns is an optional argument that defaults to 0.

▶ S is of type cudaStream\_t and specifies the stream associated with this call. The stream must have been allocated in the same grid where the call is being made. S is an optional argument that defaults to the NULL stream.

## 13.3.1.1.1 Launches are Asynchronous

Identical to host-side launches, all device-side kernel launches are asynchronous with respect to the launching thread. That is to say, the <<<>>> launch command will return immediately and the launching thread will continue to execute until it hits an implicit launch-synchronization point (such as at a kernel launched into the cudaStreamTailLaunch stream).

The child grid launch is posted to the device and will execute independently of the parent thread. The child grid may begin execution at any time after launch, but is not guaranteed to begin execution until the launching thread reaches an implicit launch-synchronization point.

## 13.3.1.1.2 Launch Environment Configuration

All global device configuration settings (for example, shared memory and L1 cache size as returned from cudaDeviceGetCacheConfig(), and device limits returned from cudaDeviceGetLimit()) will be inherited from the parent. Likewise, device limits such as stack size will remain as-configured.

For host-launched kernels, per-kernel configurations set from the host will take precedence over the global setting. These configurations will be used when the kernel is launched from the device as well. It is not possible to reconfigure a kernel’s environment from the device.

## 13.3.1.2 Streams

Both named and unnamed (NULL) streams are available from the device runtime. Named streams may be used by any thread within a grid, but stream handles may not be passed to other child/parent kernels. In other words, a stream should be treated as private to the grid in which it is created.

Similar to host-side launch, work launched into separate streams may run concurrently, but actual concurrency is not guaranteed. Programs that depend upon concurrency between child kernels are not supported by the CUDA programming model and will have undefined behavior.

The host-side NULL stream’s cross-stream barrier semantic is not supported on the device (see below for details). In order to retain semantic compatibility with the host runtime, all device streams must be created using the cudaStreamCreateWithFlags() API, passing the cudaStreamNonBlocking flag. The cudaStreamCreate() call is a host-runtime- only API and will fail to compile for the device.

As cudaStreamSynchronize() and cudaStreamQuery() are unsupported by the device runtime, a kernel launched into the cudaStreamTailLaunch stream should be used instead when the application needs to know that stream-launched child kernels have completed.

## 13.3.1.2.1 The Implicit (NULL) Stream

Within a host program, the unnamed (NULL) stream has additional barrier synchronization semantics with other streams (see Default Stream for details). The device runtime ofers a single implicit, unnamed stream shared between all threads in a thread block, but as all named streams must be created with the cudaStreamNonBlocking flag, work launched into the NULL stream will not insert an implicit dependency on pending work in any other streams (including NULL streams of other thread blocks).

## 13.3.1.2.2 The Fire-and-Forget Stream

The fire-and-forget named stream (cudaStreamFireAndForget) allows the user to launch fire-andforget work with less boilerplate and without stream tracking overhead. It is functionally identical to, but faster than, creating a new stream per launch, and launching into that stream.

Fire-and-forget launches are immediately scheduled for launch without any dependency on the completion of previously launched grids. No other grid launches can depend on the completion of a fireand-forget launch, except through the implicit synchronization at the end of the parent grid. So a tail launch or the next grid in parent grid’s stream won’t launch before a parent grid’s fire-and-forget work has completed.

```dart
// In this example, C2's launch will not wait for C1's completion
__global__ void P( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}
```

The fire-and-forget stream cannot be used to record or wait on events. Attempting to do so results in cudaErrorInvalidValue. The fire-and-forget stream is not supported when compiled with CUDA\_FORCE\_CDP1\_IF\_SUPPORTED defined. Fire-and-forget stream usage requires compilation to be in 64-bit mode.

## 13.3.1.2.3 The Tail Launch Stream

The tail launch named stream (cudaStreamTailLaunch) allows a grid to schedule a new grid for launch after its completion. It should be possible to to use a tail launch to achieve the same functionality as a cudaDeviceSynchronize() in most cases.

Each grid has its own tail launch stream. All non-tail launch work launched by a grid is implicitly synchronized before the tail stream is kicked of. I.e. A parent grid’s tail launch does not launch until the parent grid and all work launched by the parent grid to ordinary streams or per-thread or fire-andforget streams have completed. If two grids are launched to the same grid’s tail launch stream, the later grid does not launch until the earlier grid and all its descendent work has completed.

```txt
// In this example, C2 will only launch after C1 completes.
__global__ void P( ... ) {
    C1<<< ... , cudaStreamTailLaunch >>>( ... );
    C2<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

Grids launched into the tail launch stream will not launch until the completion of all work by the parent grid, including all other grids (and their descendants) launched by the parent in all non-tail launched streams, including work executed or launched after the tail launch.

```txt
// In this example, C will only launch after all X, F and P complete.
__global__ void P( ... ) {
    C<<< ... , cudaStreamTailLaunch >>>( ... );
    X<<< ... , cudaStreamPerThread >>>( ... );
    F<<< ... , cudaStreamFireAndForget >>>( ... )
}
```

The next grid in the parent grid’s stream will not be launched before a parent grid’s tail launch work has completed. In other words, the tail launch stream behaves as if it were inserted between its parent grid and the next grid in its parent grid’s stream.

```txt
// In this example, P2 will only launch after C completes.
__global__ void P1( ... ) {
    C<<< ... , cudaStreamTailLaunch >>>( ... );
}

__global__ void P2( ... ) {
}

int main ( ... ) {
    ...
    P1<<< ... >>>( ... );
    P2<<< ... >>>( ... );
    ...
}
```

Each grid only gets one tail launch stream. To tail launch concurrent grids, it can be done like the example below.

```txt
// In this example, C1 and C2 will launch concurrently after P's completion
__global__ void T( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}

__global__ void P( ... ) {
    ...
    T<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

The tail launch stream cannot be used to record or wait on events. Attempting to do so results in cudaErrorInvalidValue. The tail launch stream is not supported when compiled with CUDA\_FORCE\_CDP1\_IF\_SUPPORTED defined. Tail launch stream usage requires compilation to be in 64-bit mode.

## 13.3.1.3 Events

Only the inter-stream synchronization capabilities of CUDA events are supported. This means that cudaStreamWaitEvent() is supported, but cudaEventSynchronize(), cudaEventElapsedTime(), and cudaEventQuery() are not. As cudaEventElapsedTime() is not supported, cudaEvents must be created via cudaEventCreateWithFlags(), passing the cudaEventDisableTiming flag.

As with named streams, event objects may be shared between all threads within the grid which created them but are local to that grid and may not be passed to other kernels. Event handles are not guaranteed to be unique between grids, so using an event handle within a grid that did not create it will result in undefined behavior.

## 13.3.1.4 Synchronization

It is up to the program to perform suficient inter-thread synchronization, for example via a CUDA Event, if the calling thread is intended to synchronize with child grids invoked from other threads.

As it is not possible to explicitly synchronize child work from a parent thread, there is no way to guarantee that changes occurring in child grids are visible to threads within the parent grid.

## 13.3.1.5 Device Management

Only the device on which a kernel is running will be controllable from that kernel. This means that device APIs such as cudaSetDevice() are not supported by the device runtime. The active device as seen from the GPU (returned from cudaGetDevice()) will have the same device number as seen from the host system. The cudaDeviceGetAttribute() call may request information about another device as this API allows specification of a device ID as a parameter of the call. Note that the catch-all cudaGetDeviceProperties() API is not ofered by the device runtime - properties must be queried individually.

## 13.3.1.6 Memory Declarations

## 13.3.1.6.1 Device and Constant Memory

Memory declared at file scope with \_\_device\_\_ or \_\_constant\_\_ memory space specifiers behaves identically when using the device runtime. All kernels may read or write device variables, whether the kernel was initially launched by the host or device runtime. Equivalently, all kernels will have the same view of \_\_constant\_\_s as declared at the module scope.

## 13.3.1.6.2 Textures and Surfaces

CUDA supports dynamically created texture and surface objects<sup>7</sup>, where a texture object may be created on the host, passed to a kernel, used by that kernel, and then destroyed from the host. The device runtime does not allow creation or destruction of texture or surface objects from within device code, but texture and surface objects created from the host may be used and passed around freely on the device. Regardless of where they are created, dynamically created texture objects are always valid and may be passed to child kernels from a parent.

Note: The device runtime does not support legacy module-scope (i.e., Fermi-style) textures and surfaces within a kernel launched from the device. Module-scope (legacy) textures may be created from the host and used in device code as for any kernel, but may only be used by a top-level kernel (i.e., the one which is launched from the host).

## 13.3.1.6.3 Shared Memory Variable Declarations

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

## 13.3.1.6.4 Symbol Addresses

Device-side symbols (i.e., those marked \_\_device\_\_) may be referenced from within a kernel simply via the & operator, as all global-scope device variables are in the kernel’s visible address space. This also applies to \_\_constant\_\_ symbols, although in this case the pointer will reference read-only data.

Given that device-side symbols can be referenced directly, those CUDA runtime APIs which reference symbols (e.g., cudaMemcpyToSymbol() or cudaGetSymbolAddress()) are redundant and hence not supported by the device runtime. Note this implies that constant data cannot be altered from within a running kernel, even ahead of a child kernel launch, as references to \_\_constant\_\_ space are readonly.

## 13.3.1.7 API Errors and Launch Failures

As usual for the CUDA runtime, any function may return an error code. The last error code returned is recorded and may be retrieved via the cudaGetLastError() call. Errors are recorded per-thread, so that each thread can identify the most recent error that it has generated. The error code is of type cudaError\_t.

Similar to a host-side launch, device-side launches may fail for many reasons (invalid arguments, etc). The user must call cudaGetLastError() to determine if a launch generated an error, however lack of an error after launch does not imply the child kernel completed successfully.

For device-side exceptions, e.g., access to an invalid address, an error in a child grid will be returned to the host.

## 13.3.1.7.1 Launch Setup APIs

Kernel launch is a system-level mechanism exposed through the device runtime library, and as such is available directly from PTX via the underlying cudaGetParameterBuffer() and cudaLaunchDevice() APIs. It is permitted for a CUDA application to call these APIs itself, with the same requirements as for PTX. In both cases, the user is then responsible for correctly populating all necessary data structures in the correct format according to specification. Backwards compatibility is guaranteed in these data structures.

As with host-side launch, the device-side operator <<<>>> maps to underlying kernel launch APIs. This is so that users targeting PTX will be able to enact a launch, and so that the compiler front-end can translate <<<>>> into these calls.

Table 13: New Device-only Launch Implementation Functions

<table><tr><td>Runtime API Launch Functions</td><td>Description of Difference From Host Runtime Behaviour (behavior is identical if no description)</td></tr><tr><td>cudaGetParameter-Buffer</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr><tr><td>cudaLaunchDevice</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr></table>

The APIs for these launch functions are diferent to those of the CUDA Runtime API, and are defined as follows:

```c
extern    device  cudaError_t cudaGetParameterBuffer(void **params);
extern __device__  cudaError_t cudaLaunchDevice(void *kernel,
                               void *params, dim3 gridDim,
                               dim3 blockDim,
                               unsigned int sharedMemSize = 0,
                               cudaStream_t stream = 0);
```

## 13.3.1.8 API Reference

The portions of the CUDA Runtime API supported in the device runtime are detailed here. Host and device runtime APIs have identical syntax; semantics are the same except where indicated. The following table provides an overview of the API relative to the version available from the host.

Table 14: Supported API Functions

<table><tr><td>Runtime API Functions</td><td>Details</td></tr><tr><td>cudaDeviceGetCacheConfig</td><td></td></tr><tr><td>cudaDeviceGetLimit</td><td></td></tr><tr><td>cudaGetLastError</td><td>Last error is per-thread state, not per-block state</td></tr><tr><td>cudaPeekAtLastError</td><td></td></tr><tr><td>cudaGetErrorString</td><td></td></tr><tr><td>cudaGetDeviceCount</td><td></td></tr><tr><td>cudaDeviceGetAttribute</td><td>Will return attributes for any device</td></tr><tr><td>cudaGetDevice</td><td>Always returns current device ID as would be seen from host</td></tr><tr><td>cudaStreamCreateWithFlags</td><td>Must pass cudaStreamNonBlocking flag</td></tr><tr><td>cudaStreamDestroy</td><td></td></tr><tr><td>cudaStreamWaitEvent</td><td></td></tr><tr><td>cudaEventCreateWithFlags</td><td>Must pass cudaEventDisableTiming flag</td></tr><tr><td>cudaEventRecord</td><td></td></tr><tr><td>cudaEventDestroy</td><td></td></tr><tr><td>cudaFuncGetAttributes</td><td></td></tr><tr><td>cudaMemcpyAsync</td><td rowspan="4">Notes about all memcpy/memset functions:► Only async memcpy/set functions are supported► Only device-to-device memcpy is permitted► May not pass in local or shared memory pointers</td></tr><tr><td>cudaMemcpy2DAsync</td></tr><tr><td>cudaMemcpy3DAsync</td></tr><tr><td>cudaMemsetAsync</td></tr><tr><td>cudaMemset2DAsync</td><td></td></tr><tr><td>cudaMemset3DAsync</td><td></td></tr><tr><td>cudaRuntimeGetVersion</td><td></td></tr><tr><td>cudaMalloc</td><td rowspan="2">May not call cudaFree on the device on a pointer created on the host, and vice-versa</td></tr><tr><td>cudaFree</td></tr><tr><td>cudaOccupancyMaxActiveBlocksPerMulti-processor</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize</td><td></td></tr><tr><td>cudaOccupancyMaxPotentialBlockSize-VariableSMem</td><td></td></tr></table>
