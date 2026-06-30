# CUDA Dynamic Parallelism Limitations

Implementation restrictions including memory footprint, pending launch limits, configuration options, and SM/Warp ID volatility.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14220-L14253

Citation: [CUDA_C_Programming_Guide:L14220-L14253]

````text

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
````
