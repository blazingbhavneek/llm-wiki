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

# Chapter 14. Virtual Memory Management
