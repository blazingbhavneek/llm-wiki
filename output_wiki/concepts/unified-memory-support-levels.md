# Unified Memory Support Levels

CUDA Unified Memory provides all processors in a system (CPUs, GPUs, etc.) with a single unified memory pool accessible via a single pointer value, enabling concurrent access and native memory operations like pointer dereferences and atomics [CUDA_C_Programming_Guide:L20768-L20803]. The level of support varies by hardware and software environment, defined by specific device properties.

## Levels of Support

There are four distinct levels of Unified Memory support, determined by the values of specific device properties [CUDA_C_Programming_Guide:L20768-L20803]:

### 1. Full CUDA Unified Memory
In this mode, all memory (both System-Allocated and CUDA Managed Memory) has full support, including concurrent access and hardware acceleration features [CUDA_C_Programming_Guide:L20768-L20803].

**Detection Properties:**
*   `pageableMemoryAccess`: 1
*   `hostNativeAtomicSupported`: 1 (for systems with hardware acceleration)
*   `pageableMemoryAccessUseHostPageTables`: 1 (for systems with hardware acceleration)
*   `directManagedMemAccessFromHost`: 1 (for systems with hardware acceleration)

### 2. Only CUDA Managed Memory Support
In this mode, only CUDA Managed Memory allocations have full support. System-Allocated Memory does not have the same level of support [CUDA_C_Programming_Guide:L20768-L20803].

**Detection Properties:**
*   `concurrentManagedAccess`: 1
*   `pageableMemoryAccess`: 0

### 3. CUDA Managed Memory Without Full Support
This level provides unified addressing but does not support concurrent access between processors [CUDA_C_Programming_Guide:L20768-L20803]. This level is typically found on Windows systems, devices with compute capability 5.x, or Tegra devices [CUDA_C_Programming_Guide:L20768-L20803].

**Detection Properties:**
*   `managedMemory`: 1
*   `concurrentManagedAccess`: 0

**Implementation Details:**
*   Devices with compute capability 5.x allocate CUDA Managed Memory directly on the GPU [CUDA_C_Programming_Guide:L21032-L21037].
*   Devices with compute capability 6.x and greater populate the memory on first touch, similar to System-Allocated Memory APIs [CUDA_C_Programming_Guide:L21032-L21037].

### 4. No Unified Memory Support
The device does not support Unified Memory [CUDA_C_Programming_Guide:L20768-L20803].

**Detection Properties:**
*   `managedMemory`: 0

## Memory Allocation Methods

CUDA Unified Memory can be obtained through two primary methods [CUDA_C_Programming_Guide:L20768-L20803]:

1.  **System-Allocated Memory:** Memory allocated on the host using system APIs, such as stack variables, global/file-scope variables, `malloc()`, `mmap()`, and thread locals. This method is available on systems with full Unified Memory support [CUDA_C_Programming_Guide:L20768-L20803].
2.  **CUDA Managed Memory:** Memory explicitly allocated using CUDA APIs like `cudaMallocManaged()`. This method is available on more systems and may offer better performance than System-Allocated Memory [CUDA_C_Programming_Guide:L20768-L20803].

## Key Characteristics

*   **Concurrent Access:** Unified Memory allows GPU and CPU threads to access memory concurrently without manual copying between separate allocations [CUDA_C_Programming_Guide:L20768-L20803].
*   **Data Migration:** Data movement occurs automatically or via hints to migrate data towards the processor accessing it most frequently, maximizing data access speed [CUDA_C_Programming_Guide:L20768-L20803].
*   **Memory Efficiency:** It reduces total system memory usage by avoiding duplication of memory on both CPUs and GPUs [CUDA_C_Programming_Guide:L20768-L20803].
*   **Virtual Addressing:** The physical location of data is invisible to the program and may change at any time, but accesses to the virtual address remain valid and coherent from any processor [CUDA_C_Programming_Guide:L20768-L20803].
*   **Hints:** Applications can use hints to control migration heuristics, but these are not required for correctness or functionality [CUDA_C_Programming_Guide:L20768-L20803].

## References

*   [CUDA_C_Programming_Guide:L20768-L20803]
*   [CUDA_C_Programming_Guide:L21032-L21037]
