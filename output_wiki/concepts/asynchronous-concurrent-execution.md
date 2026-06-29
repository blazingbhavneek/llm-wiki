# Asynchronous Concurrent Execution

CUDA exposes the following operations as independent tasks that can operate concurrently with one another [CUDA_C_Programming_Guide:L2117-L2133]:

* Computation on the host
* Computation on the device
* Memory transfers from the host to the device
* Memory transfers from the device to the host
* Memory transfers within the memory of a given device
* Memory transfers among devices

The level of concurrency achieved between these operations depends on the feature set and compute capability of the device [CUDA_C_Programming_Guide:L2117-L2133].

## Concurrent Execution between Host and Device

Concurrent host execution is facilitated through asynchronous library functions that return control to the host thread before the device completes the requested task [CUDA_C_Programming_Guide:L2134-L2151]. Using asynchronous calls, many device operations can be queued up together to be executed by the CUDA driver when appropriate device resources are available [CUDA_C_Programming_Guide:L2134-L2151]. This relieves the host thread of much of the responsibility to manage the device, leaving it free for other tasks [CUDA_C_Programming_Guide:L2134-L2151].

The following device operations are asynchronous with respect to the host [CUDA_C_Programming_Guide:L2134-L2151]:

* Kernel launches
* Memory copies within a single device’s memory
* Memory copies from host to device of a memory block of 64 KB or less
* Memory copies performed by functions that are suffixed with `Async`
* Memory set function calls

Programmers can globally disable asynchronicity of kernel launches for all CUDA applications running on a system by setting the `CUDA_LAUNCH_BLOCKING` environment variable to 1 [CUDA_C_Programming_Guide:L2134-L2151]. This feature is provided for debugging purposes only and should not be used as a way to make production software run reliably [CUDA_C_Programming_Guide:L2134-L2151].

Kernel launches are synchronous if hardware counters are collected via a profiler (Nsight Compute) unless concurrent kernel profiling is enabled [CUDA_C_Programming_Guide:L2134-L2151]. Asynchronous memory copies might also be synchronous if they involve host memory that is not page-locked [CUDA_C_Programming_Guide:L2134-L2151].

## Concurrent Kernel Execution

Some devices of compute capability 2.x and higher can execute multiple kernels concurrently [CUDA_C_Programming_Guide:L2152-L2162]. Applications may query this capability by checking the `concurrentKernels` device property (see Device Enumeration), which is equal to 1 for devices that support it [CUDA_C_Programming_Guide:L2152-L2162].

The maximum number of kernel launches that a device can execute concurrently depends on its compute capability and is listed in Table 27 of the CUDA C Programming Guide [CUDA_C_Programming_Guide:L2152-L2162].

A kernel from one CUDA context cannot execute concurrently with a kernel from another CUDA context [CUDA_C_Programming_Guide:L2152-L2162]. The GPU may time slice to provide forward progress to each context [CUDA_C_Programming_Guide:L2152-L2162]. If a user wants to run kernels from multiple process simultaneously on the SM, one must enable MPS [CUDA_C_Programming_Guide:L2152-L2162].

Kernels that use many textures or a large amount of local memory are less likely to execute concurrently with other kernels [CUDA_C_Programming_Guide:L2152-L2162].

## Overlap of Data Transfer and Kernel Execution

Some devices can perform an asynchronous memory copy to or from the GPU concurrently with kernel execution [CUDA_C_Programming_Guide:L2163-L2168]. Applications may query this capability by checking the `asyncEngineCount` device property (see Device Enumeration), which is greater than zero for devices that support it [CUDA_C_Programming_Guide:L2163-L2168]. If host memory is involved in the copy, it must be page-locked [CUDA_C_Programming_Guide:L2163-L2168].

It is also possible to perform an intra-device copy simultaneously with kernel execution (on devices that support the `concurrentKernels` device property) and/or with copies to or from the device (for devices that support the `asyncEngineCount` property) [CUDA_C_Programming_Guide:L2163-L2168]. Intra-device copies are initiated using the standard memory copy functions with destination and source addresses residing on the same device [CUDA_C_Programming_Guide:L2163-L2168].

## Concurrent Data Transfers

Some devices of compute capability 2.x and higher can overlap copies to and from the device [CUDA_C_Programming_Guide:L2169-L2171]. Applications may query this capability by checking the `asyncEngineCount` device property (see Device Enumeration), which is equal to 2 for devices that support it [CUDA_C_Programming_Guide:L2169-L2171]. In order to be overlapped, any host memory involved in the transfers must be page-locked [CUDA_C_Programming_Guide:L2169-L2171].
