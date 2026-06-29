# Unified Memory Programming Model

Unified Memory is a programming model that simplifies CUDA applications by removing the requirement for separate memory allocations between the host and device, as well as explicit memory transfers between them [CUDA_C_Programming_Guide:L20930-L20933]. This model allows data to be accessed by both CPU and GPU threads seamlessly, with the system managing the migration of pages between host and device memory as needed.

## Allocation Methods

Programs may allocate Unified Memory using three primary methods [CUDA_C_Programming_Guide:L20935-L20943]:

1. **System-Allocation APIs**: On systems with full CUDA Unified Memory support, any standard system allocation from the host process can be used. This includes C's `malloc()`, C++'s `new` operator, and POSIX's `mmap` [CUDA_C_Programming_Guide:L20937-L20939].
2. **CUDA Managed Memory Allocation APIs**: The `cudaMallocManaged()` API can be used, which is syntactically similar to `cudaMalloc()` [CUDA_C_Programming_Guide:L20941-L20942].
3. **CUDA Managed Variables**: Variables declared with the `__managed__` qualifier, which are semantically similar to `__device__` variables [CUDA_C_Programming_Guide:L20943-L20944].

## System Support and Portability

The behavior of an application that attempts to use Unified Memory on a system that does not support it is undefined [CUDA_C_Programming_Guide:L20804-L20805]. To ensure portability across systems with different levels of support, applications can query specific device properties using `cudaGetDeviceProperties()` [CUDA_C_Programming_Guide:L20805-L20807, L20823-L20824].

### Key Properties

*   **pageableMemoryAccess**: This property is set to 1 on systems with CUDA Unified Memory support where all threads may access System-Allocated Memory and CUDA Managed Memory [CUDA_C_Programming_Guide:L20807-L20810]. Examples of such systems include NVIDIA Grace Hopper, IBM Power9 + Volta, and modern Linux systems with Heterogeneous Memory Management (HMM) enabled [CUDA_C_Programming_Guide:L20810-L20812].
    *   Linux HMM support requires Linux kernel version 6.1.24+, 6.2.11+, or 6.3+, devices with compute capability 7.5 or higher, and a CUDA driver version 535+ installed with Open Kernel Modules [CUDA_C_Programming_Guide:L20814-L20816].

*   **concurrentManagedAccess**: This property is set to 1 on systems with full CUDA Managed Memory support [CUDA_C_Programming_Guide:L20818-L20820]. When this property is 0, there is only partial support for Unified Memory in CUDA Managed Memory [CUDA_C_Programming_Guide:L20820-L20821]. For Tegra support of Unified Memory, refer to CUDA for Tegra Memory Management [CUDA_C_Programming_Guide:L20821-L20822].

## Implementation Notes

Most examples in the CUDA documentation provide at least two versions of code: one using CUDA Managed Memory and one using System-Allocated Memory, allowing developers to choose between them [CUDA_C_Programming_Guide:L20946-L20948]. Tabs in the documentation samples facilitate switching between these implementation styles [CUDA_C_Programming_Guide:L20948-L20949].

## References

- [CUDA_C_Programming_Guide:L20804-L20827] CUDA C Programming Guide: Unified Memory Support and Properties
- [CUDA_C_Programming_Guide:L20930-L20949] CUDA C Programming Guide: Programming Model and Allocation Methods
