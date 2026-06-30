# Unified Memory Programming

Introduces CUDA Unified Memory, its system requirements, programming model, allocation APIs (cudaMallocManaged, __managed__), and examples demonstrating memory allocation and usage across host and device.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20754-L21100

Citation: [CUDA_C_Programming_Guide:L20754-L21100]

````text

# Chapter 24. Unified Memory Programming

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

Note: This chapter applies to devices with compute capability 5.0 or higher unless stated otherwise. For devices with compute capability lower than 5.0, refer to the CUDA toolkit documentation for CUDA 11.8.

This documentation on Unified Memory is divided into 3 parts:

▶ General description of unified memory

▶ Unified Memory on devices with full CUDA Unified Memory support

▶ Unified Memory on devices without full CUDA Unified Memory support

## 24.1. Unified Memory Introduction

CUDA Unified Memory provides all processors with:

▶ A single unified memory pool, that is, a single pointer value enables all processors in the system (all CPUs, all GPUs, etc.) to access this memory with all of their native memory operations (pointer dereferences, atomics, etc.).

▶ Concurrent access to the unified memory pool from all processors in the system.

Unified Memory improves GPU programming in several ways:

Productivity: GPU programs may access Unified Memory from GPU and CPU threads concurrently without needing to create separate allocations (cudaMalloc()) and copy memory manually back and forth (cudaMemcpy\*()).

▶ Performance:

▶ Data access speed may be maximized by migrating data towards processors that access it most frequently. Applications can trigger manual migration of data and may use hints to control migration heuristics.

▶ Total system memory usage may be reduced by avoiding duplicating memory on both CPUs and GPUs.

▶ Functionality: It enables GPU programs to work on data that exceeds the GPU memory’s capacity.

With CUDA Unified Memory, data movement still takes place, and hints may improve performance. These hints are not required for correctness or functionality, that is, programmers may focus on parallelizing their applications across GPUs and CPUs first, and worry about data-movement later in the development cycle as a performance optimization. Note that the physical location of data is invisible to a program and may be changed at any time, but accesses to the data’s virtual address will remain valid and coherent from any processor regardless of locality.

There are two main ways to obtain CUDA Unified Memory:

1 System-Allocated Memory: memory allocated on the host with system APIs: stack variables, global-/file-scope variables, malloc() / mmap() (see System-Allocated Memory: in-depth examples for in-depth examples), thread locals, etc.

▶ CUDA APIs that explicitly allocate Unified Memory: memory allocated with, for example, cudaMallocManaged(), are available on more systems and may perform better than System-Allocated Memory.

## 24.1.1. System Requirements for Unified Memory

The following table shows the diferent levels of support for CUDA Unified Memory, the device properties required to detect these levels of support and links to the documentation specific to each level of support:

Table 31: Overview of levels of unified memory support

<table><tr><td>Unified Memory Support Level</td><td>System device properties</td><td>Further documentation</td></tr><tr><td>Full CUDA Unified Memory: all memory has full support. This includes System-Allocated and CUDA Managed Memory.</td><td>Set to 1:pageableMemoryAccessSystems with hardware acceleration also have the following properties set to 1:hostNativeAtomicSupported, pageableMemoryAccessUse-sHostPageTables, directManagedMemAccess-FromHost</td><td>Unified Memory on devices with full CUDA Unified Memory support</td></tr><tr><td>Only CUDA Managed Memory has full support.</td><td>Set to 1: concurrentManagedAccessSet to 0:pageableMemoryAccess</td><td>Unified Memory on devices with only CUDA Managed Memory support</td></tr><tr><td>CUDA Managed Memory without full support: unified addressing but no concurrent access.</td><td>Set to 1: managedMemorySet to 0: concurrentManagedAccess</td><td>Unified Memory on Windows or devices with compute capability 5.xCUDA for Tegra Memory ManagementUnified Memory on Tegra</td></tr><tr><td>No Unified Memory support.</td><td>Set to 0: managedMemory</td><td>CUDA for Tegra Memory Management</td></tr></table>

The behavior of an application that attempts to use Unified Memory on a system that does not support it is undefined. The following properties enable CUDA applications to check the level of system support for Unified Memory, and to be portable between systems with diferent levels of support:

pageableMemoryAccess: This property is set to 1 on systems with CUDA Unified Memory support where all threads may access System-Allocated Memory and CUDA Managed Memory. These systems include NVIDIA Grace Hopper, IBM Power9 + Volta, and modern Linux systems with HMM enabled (see next bullet), among others.

▶ Linux HMM requires Linux kernel version 6.1.24+, 6.2.11+ or 6.3+, devices with compute capability 7.5 or higher and a CUDA driver version 535+ installed with Open Kernel Modules.

concurrentManagedAccess: This property is set to 1 on systems with full CUDA Managed Memory support. When this property is set to 0, there is only partial support for Unified Memory in CUDA Managed Memory. For Tegra support of Unified Memory, see CUDA for Tegra Memory Management.

A program may query the level of GPU support for CUDA Unified Memory, by querying the attributes

in Table 31 using cudaGetDeviceProperties().

## 24.1.2. Programming Model

With CUDA Unified Memory, separate allocations between host and device, and explicit memory transfers between them, are no longer required. Programs may allocate Unified Memory in the following ways:

▶ System-Allocation APIs: on systems with full CUDA Unified Memory support via any system allocation of the host process (C’s malloc(), C++’s new operator, POSIX’s mmap and so on).

▶ CUDA Managed Memory Allocation APIs: via the cudaMallocManaged() API which is syntactically similar to cudaMalloc().

CUDA Managed Variables: variables declared with \_\_managed\_\_, which are semantically similar to a \_\_device\_\_ variable.

Most examples in this chapter provide at least two versions, one using CUDA Managed Memory and one using System-Allocated Memory. Tabs allow you to choose between them. The following samples illustrate how Unified Memory simplifies CUDA programs:

System (malloc())

```cpp
__global__ void write_value(int* ptr,
    int v) {
        *ptr = v;
    }
int main() {
    int* d_ptr = nullptr;
    // Does not require any unified memory
    support
    cudaMalloc(&d_ptr, sizeof(int));
    write_value<<<1, 1>>>(d_ptr, 1);
    int h_value;
    // Copy memory back to the host and
    synchronize
    cudaMemcpy(&h_value, d_ptr,
    sizeof(int),
            cudaMemcpyDefault);
    printf("value = %d\n", h_value);
    cudaFree(d_ptr);
    return 0;
}
```

System (Stack)

```cpp
__global__ void write_value(int* ptr,
    int v) {
        *ptr = v;
    }
int main() {
    int* d_ptr = nullptr;
    // Does not require any unified memory
    support
    cudaMalloc(&d_ptr, sizeof(int));
    write_value<<<1, 1>>>(d_ptr, 1);
    int h_value;
    // Copy memory back to the host and
    synchronize
    cudaMemcpy(&h_value, d_ptr,
    sizeof(int),
            cudaMemcpyDefault);
    printf("value = %d\n", h_value);
    cudaFree(d_ptr);
    return 0;
}
```

Managed (cudaMallocManaged())

```cpp
__global__ void write_value(int* ptr,
    int v) {
        *ptr = v;
}

int main() {
    int* d_ptr = nullptr;
    // Does not require any unified memory
    support
    cudaMalloc(&d_ptr, sizeof(int));
    write_value<<<1, 1>>>(d_ptr, 1);
    int h_value;
    // Copy memory back to the host and
    synchronize
    cudaMemcpy(&h_value, d_ptr,
    sizeof(int),
            cudaMemcpyDefault);
    printf("value = %d\n", h_value);
    cudaFree(d_ptr);
    return 0;
}
```

```cpp
__global__ void write_value(int* ptr,
    int v) {
        *ptr = v;
}

int main() {
    int* ptr = nullptr;
    // Requires CUDA Managed Memory support
    cudaMallocManaged(&ptr, sizeof(int));
    write_value<<<1, 1>>>(ptr, 1);
    // Synchronize required
    // (before, cudaMemcpy was
    synchronizing)
    cudaDeviceSynchronize();
    printf("value = %d\n", *ptr);
    cudaFree(ptr);
    return 0;
}
```

Managed (\_\_managed\_\_)

```cpp
__global__ void write_value(int* ptr,
    int v) {
        *ptr = v;
    }

int main() {
    int* d_ptr = nullptr;
    // Does not require any unified memory
    support
    cudaMalloc(&d_ptr, sizeof(int));
    write_value<<<1, 1>>>(d_ptr, 1);
    int h_value;
    // Copy memory back to the host and
    synchronize
    cudaMemcpy(&h_value, d_ptr,
    sizeof(int),
            cudaMemcpyDefault);
    printf("value = %d\n", h_value);
    cudaFree(d_ptr);
    return 0;
}
```

In the example above, the device writes a value which is then read by the host:

▶ Without Unified Memory: both host- and device-side storage for the written value is required (h\_value and d\_ptr in the example), as is an explicit copy between the two using cudaMemcpy().

With Unified Memory: device accesses data directly from the host. ptr / value may be used without a separate h\_value / d\_ptr allocation and no copy routine is required, greatly simplifying and reducing the size of the program. With:

▶ System Allocated: no other changes required.

Managed Memory: data allocation changed to use cudaMallocManaged(), which returns a pointer valid from both host and device code.

## 24.1.2.1 Allocation APIs for System-Allocated Memory

On systems with full CUDA Unified Memory support, all memory is unified memory. This includes memory allocated with system allocation APIs, such as malloc(), mmap(), C++ new() operator, and also automatic variables on CPU thread stacks, thread locals, global variables, and so on.

System-Allocated Memory may be populated on first touch, depending on the API and system settings used. First touch means that:

▶ The allocation APIs allocate virtual memory and return immediately, and

▶ physical memory is populated when a thread accesses the memory for the first time.

Usually, the physical memory will be chosen “close” to the processor that thread is running on. For example,

▶ GPU thread accesses it first: physical GPU memory of GPU that thread runs on is chosen.

▶ CPU thread accesses it first: physical CPU memory in the memory NUMA node of the CPU core that thread runs on is chosen.

CUDA Unified Memory Hint and Prefetch APIs, cudaMemAdvise and cudaMemPreftchAsync, may be used on System-Allocated Memory. These APIs are covered below in the Data Usage Hints section.

```txt
__global__ void printme(char *str) {
    printf(str);
}

int main() {
    // Allocate 100 bytes of memory, accessible to both Host and Device code
    char *s = (char*)malloc(100);
    // Physical allocation placed in CPU memory because host accesses "s" first
    strncpy(s, "Hello Unified Memory\n", 99);
    // Here we pass "s" to a kernel without explicitly copying
    printme<<< 1, 1 >>>(s);
    cudaDeviceSynchronize();
    // Free as for normal CUDA allocations
    cudaFree(s);
    return  0;
}
```

## 24.1.2.2 Allocation API for CUDA Managed Memory: cudaMallocManaged()

On systems with CUDA Managed Memory support, unified memory may be allocated using:

```c
__host__ cudaError_t cudaMallocManaged(void **devPtr, size_t size);
```

This API is syntactically identical to cudaMalloc(): it allocates size bytes of managed memory and sets devPtr to refer to the allocation. CUDA Managed Memory is also deallocated with cudaFree().

On systems with full CUDA Managed Memory support, managed memory allocations may be accessed concurrently by all CPUs and GPUs in the system. Replacing host calls to cudaMalloc() with cudaMallocManaged() does not impact program semantics on these systems; device code is not able to call cudaMallocManaged().

The following example shows the use of cudaMallocManaged():

```cpp
__global__ void printme(char *str) {
    printf(str);
}

int main() {
    // Allocate 100 bytes of memory, accessible to both Host and Device code
    char *s;
    cudaMallocManaged(&s, 100);
    // Note direct Host-code use of "s"
    strncpy(s, "Hello Unified Memory\n", 99);
    // Here we pass "s" to a kernel without explicitly copying
    printme<<< 1, 1 >>>(s);
    cudaDeviceSynchronize();
    // Free as for normal CUDA allocations
    cudaFree(s);
    return 0;
}
```

Note: For systems that support CUDA Managed Memory allocations, but do not provide full support, see Coherency and Concurrency. Implementation details (may change any time):

▶ Devices of compute capability 5.x allocate CUDA Managed Memory on the GPU.

▶ Devices of compute capability 6.x and greater populate the memory on first touch, just like System-Allocated Memory APIs.

## 24.1.2.3 Global-Scope Managed Variables Using \_\_managed\_\_

CUDA \_\_managed\_\_ variables behave as if they were allocated via cudaMallocManaged() (see Allocation API for CUDA Managed Memory: cudaMallocManaged()). They simplify programs with global variables, making it particularly easy to exchange data between host and device without manual allocations or copying.

On systems with full CUDA Unified Memory support, file-scope or global-scope variables cannot be directly accessed by device code. But a pointer to these variables may be passed to the kernel as an argument, see System-Allocated Memory: in-depth examples for examples.

## System Allocator

```cpp
__global__ void write_value(int* ptr, int v) {
    *ptr = v;
}

int main() {
    // Requires System-Allocated Memory support
    int value;
    write_value<<<1, 1>>>(&value, 1);
    // Synchronize required
    // (before, cudaMemcpy was synchronizing)
    cudaDeviceSynchronize();
    printf("value = %d\n", value);
    return 0;
}
```

## Managed

```cpp
__global__ void write_value(int* ptr, int v) {
    *ptr = v;
}

// Requires CUDA Managed Memory support
__managed__ int value;

int main() {
    write_value<<<1, 1>>>(&value, 1);
    // Synchronize required
    // (before, cudaMemcpy was synchronizing)
    cudaDeviceSynchronize();
    printf("value = %d\n", value);
```

(continues on next page)

```scss
return 0;
}
```

(continued from previous page)

Note the absence of explicit cudaMemcpy() commands and the fact that the written value value is visible on both CPU and GPU.

CUDA \_\_managed\_\_ variable implies \_\_device\_\_ and is equivalent to \_\_managed\_\_ \_\_device\_\_, which is also allowed. Variables marked \_\_constant\_\_ may not be marked as \_\_managed\_\_.

A valid CUDA context is necessary for the correct operation of \_\_managed\_\_ variables. Accessing \_\_managed\_\_ variables can trigger CUDA context creation if a context for the current device hasn’t already been created. In the example above, accessing value before the kernel launch triggers context creation on the default device. In the absence of that access, the kernel launch would have triggered context creation.

C++ objects declared as \_\_managed\_\_ are subject to certain specific constraints, particularly where static initializers are concerned. Please refer to C++ Language Support for a list of these constraints.

Note: For devices with CUDA Managed Memory without full support, visibility of \_\_managed\_\_ variables for asynchronous operations executing in CUDA streams is discussed in the section on Managing Data Visibility and Concurrent CPU + GPU Access with Streams.
````
