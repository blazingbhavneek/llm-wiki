
(continues on next page)

(continued from previous page)

```cpp
if (cudaSuccess != cudaGetLastError()) {
    return;
}

// launch tail into cudaStreamTailLaunch stream
// implicitly synchronizes: waits for child to complete
tailKernel<<<1,1,0,cudaStreamTailLaunch>>>();

}

int main(int argc, char *argv[])
{
    // launch parent
    parentKernel<<<1,1>>>();
    if (cudaSuccess != cudaGetLastError()) {
        return 1;
    }

    // wait for parent to complete
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

## 13.4.2. Performance

## 13.4.2.1 Dynamic-parallelism-enabled Kernel Overhead

System software which is active when controlling dynamic launches may impose an overhead on any kernel which is running at the time, whether or not it invokes kernel launches of its own. This overhead arises from the device runtime’s execution tracking and management software and may result in decreased performance. This overhead is, in general, incurred for applications that link against the device runtime library.

## 13.4.3. Implementation Restrictions and Limitations

Dynamic Parallelism guarantees all semantics described in this document, however, certain hardware and software resources are implementation-dependent and limit the scale, performance and other properties of a program which uses the device runtime.

## 13.4.3.1 Runtime

## 13.4.3.1.1 Memory Footprint

The device runtime system software reserves memory for various management purposes, in particular a reservation for tracking pending grid launches. Configuration controls are available to reduce the size of this reservation in exchange for certain launch limitations. See Configuration Options, below, for details.

## 13.4.3.1.2 Pending Kernel Launches

When a kernel is launched, all associated configuration and parameter data is tracked until the kernel completes. This data is stored within a system-managed launch pool.

The size of the fixed-size launch pool is configurable by calling cudaDeviceSetLimit() from the host and specifying cudaLimitDevRuntimePendingLaunchCount.

## 13.4.3.1.3 Configuration Options

Resource allocation for the device runtime system software is controlled via the cudaDevice-SetLimit() API from the host program. Limits must be set before any kernel is launched, and may not be changed while the GPU is actively running programs.

The following named limits may be set:

<table><tr><td>Limit</td><td>Behavior</td></tr><tr><td>cudaLimitDevRuntimePendingLaunchCount</td><td>Controls the amount of memory set aside for buffering kernel launches and events which have not yet begun to execute, due either to unresolved dependencies or lack of execution resources. When the buffer is full, an attempt to allocate a launch slot during a device side kernel launch will fail and return cudaError-LaunchOutOfBoundsException, while an attempt to allocate an event slot will fail and return cudaMemoryAllocation. The default number of launch slots is 2048. Applications may increase the number of launch and/or event slots by setting cudaLimitDevRuntimePendingLaunchCount. The number of event slots allocated is twice the value of that limit.</td></tr><tr><td>cudaLimitStackSize</td><td>Controls the stack size in bytes of each GPU thread. The CUDA driver automatically increases the per-thread stack size for each kernel launch as needed. This size isn&#x27;t reset back to the original value after each launch. To set the per-thread stack size to a different value, cudaDeviceSetLimit() can be called to set this limit. The stack will be immediately resized, and if necessary, the device will block until all preceding requested tasks are complete. cudaDeviceGetLimit() can be called to get the current per-thread stack size.</td></tr></table>

## 13.4.3.1.4 Memory Allocation and Lifetime

cudaMalloc() and cudaFree() have distinct semantics between the host and device environments. When invoked from the host, cudaMalloc() allocates a new region from unused device memory. When invoked from the device runtime these functions map to device-side malloc() and free(). This implies that within the device environment the total allocatable memory is limited to the device malloc() heap size, which may be smaller than the available unused device memory. Also, it is an error to invoke cudaFree() from the host program on a pointer which was allocated by cudaMalloc() on the device or vice-versa.

<table><tr><td></td><td>cudaMalloc() on Host</td><td>cudaMalloc() on Device</td></tr><tr><td>cudaFree() on Host</td><td>Supported</td><td>Not Supported</td></tr><tr><td>cudaFree() on Device</td><td>Not Supported</td><td>Supported</td></tr><tr><td>Allocation limit</td><td>Free device memory</td><td>cudaLimitMallocHeapSize</td></tr></table>

## 13.4.3.1.5 SM Id and Warp Id

Note that in PTX %smid and %warpid are defined as volatile values. The device runtime may reschedule thread blocks onto diferent SMs in order to more eficiently manage resources. As such, it is unsafe to rely upon %smid or %warpid remaining unchanged across the lifetime of a thread or thread block.

## 13.4.3.1.6 ECC Errors

No notification of ECC errors is available to code within a CUDA kernel. ECC errors are reported at the host side once the entire launch tree has completed. Any ECC errors which arise during execution of a nested program will either generate an exception or continue execution (depending upon error and configuration).

## 13.5. CDP2 vs CDP1

This section summarises the diferences between, and the compatibility and interoperability of, the new (CDP2) and legacy (CDP1) CUDA Dynamic Parallelism interfaces. It also shows how to opt-out of the CDP2 interface on devices of compute capability less than 9.0.

## 13.5.1. Diferences Between CDP1 and CDP2

Explicit device-side synchronization is no longer possible with CDP2 or on devices of compute capability 9.0 or higher. Implicit synchronization (such as tail launches) must be used instead.

Attempting to query or set cudaLimitDevRuntimeSyncDepth (or CU\_LIMIT\_DEV\_RUNTIME\_SYNC\_DEPTH) with CDP2 or on devices of compute capability 9.0 or higher results in cudaErrorUnsupportedLimit.

CDP2 no longer has a virtualized pool for pending launches that don’t fit in the fixed-sized pool. cudaLimitDevRuntimePendingLaunchCount must be set to be large enough to avoid running out of launch slots.

For CDP2, there is a limit to the total number of events existing at once (note that events are destroyed only after a launch completes), equal to twice the pending launch count. cudaLimitDevRuntimePendingLaunchCount must be set to be large enough to avoid running out of event slots.

Streams are tracked per grid with CDP2 or on devices of compute capability 9.0 or higher, not per thread block. This allows work to be launched into a stream created by another thread block. Attempting to do so with the CDP1 results in cudaErrorInvalidValue.

CDP2 introduces the tail launch (cudaStreamTailLaunch) and fire-and-forget (cudaStreamFireAndForget) named streams.

CDP2 is supported only under 64-bit compilation mode.

## 13.5.2. Compatibility and Interoperability

CDP2 is the default. Functions can be compiled with -DCUDA\_FORCE\_CDP1\_IF\_SUPPORTED to opt-out of using CDP2 on devices of compute capability less than 9.0.

<table><tr><td></td><td>Function compiler with CUDA 12.0 and newer (default)</td><td>Function compiled with pre-CUDA 12.0 or with CUDA 12.0 and newer with -DCUDA_FORCE_CDP1_IF_SUPPORTED specified</td></tr><tr><td>Compilation</td><td>Compile error if device code references cudaDeviceSynchronize.</td><td>Compile error if code references cudaStream-TailLaunch or cudaStreamFireAndForget. Compile error if device code references cudaDeviceSynchronize and code is compiled for sm_90 or newer.</td></tr><tr><td>Compute capability &lt; 9.0</td><td>New interface is used.</td><td>Legacy interface is used.</td></tr><tr><td>Compute capability 9.0 and higher</td><td>New interface is used.</td><td>New interface is used. If function references cudaDeviceSynchronize in device code, function load returns cudaErrorSymbolNotFound (this could happen if the code is compiled for devices of compute capability less than 9.0, but run on devices of compute capability 9.0 or higher using JIT).</td></tr></table>

Functions using CDP1 and CDP2 may be loaded and run simultaneously in the same context. The CDP1 functions are able to use CDP1-specific features (e.g. cudaDeviceSynchronize) and CDP2 functions are able to use CDP2-specific features (e.g. tail launch and fire-and-forget launch).

A function using CDP1 cannot launch a function using CDP2, and vice versa. If a function that would use CDP1 contains in its call graph a function that would use CDP2, or vice versa, cudaErrorCdpVersionMismatch would result during function load.

## 13.6. Legacy CUDA Dynamic Parallelism (CDP1)
