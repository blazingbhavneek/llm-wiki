# Asynchronous Concurrent Execution

CUDA capability to execute host/device computations, memory transfers, and kernel launches concurrently. Covers host-device concurrency, concurrent kernel execution limits, and overlapping data transfers with kernel execution.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2117-L2172

Citation: [CUDA_C_Programming_Guide:L2117-L2172]

````text
## 6.2.8. Asynchronous Concurrent Execution

CUDA exposes the following operations as independent tasks that can operate concurrently with one another:

▶ Computation on the host;

▶ Computation on the device;

▶ Memory transfers from the host to the device;

▶ Memory transfers from the device to the host;

▶ Memory transfers within the memory of a given device;

▶ Memory transfers among devices.

The level of concurrency achieved between these operations will depend on the feature set and compute capability of the device as described below.

## 6.2.8.1 Concurrent Execution between Host and Device

Concurrent host execution is facilitated through asynchronous library functions that return control to the host thread before the device completes the requested task. Using asynchronous calls, many device operations can be queued up together to be executed by the CUDA driver when appropriate device resources are available. This relieves the host thread of much of the responsibility to manage the device, leaving it free for other tasks. The following device operations are asynchronous with respect to the host:

▶ Kernel launches;

▶ Memory copies within a single device’s memory;

Memory copies from host to device of a memory block of 64 KB or less;

Memory copies performed by functions that are sufixed with Async;

▶ Memory set function calls.

Programmers can globally disable asynchronicity of kernel launches for all CUDA applications running on a system by setting the CUDA\_LAUNCH\_BLOCKING environment variable to 1. This feature is provided for debugging purposes only and should not be used as a way to make production software run reliably.

Kernel launches are synchronous if hardware counters are collected via a profiler (Nsight Compute) unless concurrent kernel profiling is enabled. Async memory copies might also be synchronous if they involve host memory that is not page-locked

## 6.2.8.2 Concurrent Kernel Execution

Some devices of compute capability 2.x and higher can execute multiple kernels concurrently. Applications may query this capability by checking the concurrentKernels device property (see Device Enumeration), which is equal to 1 for devices that support it.

The maximum number of kernel launches that a device can execute concurrently depends on its compute capability and is listed in Table 27.

A kernel from one CUDA context cannot execute concurrently with a kernel from another CUDA context. The GPU may time slice to provide forward progress to each context. If a user wants to run kernels from multiple process simultaneously on the SM, one must enable MPS.

Kernels that use many textures or a large amount of local memory are less likely to execute concurrently with other kernels.

## 6.2.8.3 Overlap of Data Transfer and Kernel Execution

Some devices can perform an asynchronous memory copy to or from the GPU concurrently with kernel execution. Applications may query this capability by checking the asyncEngineCount device property (see Device Enumeration), which is greater than zero for devices that support it. If host memory is involved in the copy, it must be page-locked.

It is also possible to perform an intra-device copy simultaneously with kernel execution (on devices that support the concurrentKernels device property) and/or with copies to or from the device (for devices that support the asyncEngineCount property). Intra-device copies are initiated using the standard memory copy functions with destination and source addresses residing on the same device.

## 6.2.8.4 Concurrent Data Transfers

Some devices of compute capability 2.x and higher can overlap copies to and from the device. Applications may query this capability by checking the asyncEngineCount device property (see Device Enumeration), which is equal to 2 for devices that support it. In order to be overlapped, any host memory involved in the transfers must be page-locked.
````
