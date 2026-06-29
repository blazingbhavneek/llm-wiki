# Unified Memory Programming

Unified Memory Programming is a CUDA feature that provides a single, system-wide address space for both CPU and GPU memory. This model simplifies programming by allowing applications to access memory from both the host and device without explicit data movement or separate memory allocations. The implementation and capabilities of Unified Memory vary depending on the hardware support level of the GPU.

## System Requirements

Unified Memory support requires specific hardware and software configurations. The system must have a GPU with compute capability 3.0 or higher, although full Unified Memory features are available on devices with compute capability 3.5 or higher. Devices with compute capability 5.x or running on Windows may have limited support, often referred to as "CUDA Managed Memory" support, which lacks some features like hardware coherency [CUDA_C_Programming_Guide:L693-L723].

## Programming Model

The Unified Memory programming model allows developers to allocate memory that is accessible by both the CPU and GPU. This is achieved through specific allocation APIs and managed variables.

### Allocation APIs

*   **cudaMallocManaged()**: This is the primary API for allocating CUDA managed memory. It allocates memory that is accessible from both the host and device. The memory is initially allocated on the host, and the CUDA runtime automatically migrates pages to the device as needed when accessed by the GPU [CUDA_C_Programming_Guide:L693-L723].
*   **System-Allocated Memory**: Unified Memory can also be used with system-allocated memory, where the memory is managed by the operating system but accessed by the GPU. This includes file-backed Unified Memory and Inter-Process Communication (IPC) with Unified Memory [CUDA_C_Programming_Guide:L693-L723].

### Managed Variables

Global-scope managed variables can be declared using the `__managed__` keyword. These variables are automatically allocated in the unified memory space and are accessible from both host and device code without explicit pointer passing [CUDA_C_Programming_Guide:L693-L723].

### Unified Memory vs. Mapped Memory

It is important to distinguish between Unified Memory and Mapped Memory. Mapped memory typically refers to memory that is explicitly mapped into the GPU's address space using `cudaHostAlloc` and `cudaHostGetDevicePointer`, requiring explicit data movement. Unified Memory, in contrast, provides a single address space with automatic migration and coherency (on supported hardware) [CUDA_C_Programming_Guide:L693-L723].

### Pointer Attributes

Pointer attributes can be used to query and manage the properties of Unified Memory pointers, such as the device where the memory is currently resident [CUDA_C_Programming_Guide:L693-L723].

## Runtime Detection of Support Level

Applications can detect the level of Unified Memory support at runtime. This is crucial for handling differences between devices with full Unified Memory support (hardware coherency) and those with only Managed Memory support (software-managed coherency) [CUDA_C_Programming_Guide:L693-L723].

## Unified Memory on Devices with Full Support

On devices with full CUDA Unified Memory support (typically compute capability 3.5+), the following features are available:

*   **System-Allocated Memory**: In-depth examples include file-backed Unified Memory and IPC with Unified Memory [CUDA_C_Programming_Guide:L693-L723].
*   **Performance Tuning**: Developers can tune performance by understanding memory paging, page sizes, and direct Unified Memory access from the host [CUDA_C_Programming_Guide:L693-L723].
*   **Host Native Atomics**: Native atomic operations are supported on the host for Unified Memory [CUDA_C_Programming_Guide:L693-L723].
*   **Atomic Accesses & Synchronization**: Proper handling of atomic accesses and synchronization primitives is required for concurrent access [CUDA_C_Programming_Guide:L693-L723].
*   **Memcpy()/Memset() Behavior**: The behavior of `memcpy` and `memset` operations with Unified Memory is defined, ensuring correct data movement and initialization [CUDA_C_Programming_Guide:L693-L723].
*   **GPU Memory Oversubscription**: Support for GPU memory oversubscription allows the GPU to access more memory than physically available on the device, paging to host memory as needed [CUDA_C_Programming_Guide:L693-L723].

## Unified Memory on Devices Without Full Support

On devices with only CUDA Managed Memory support (e.g., compute capability 5.x or Windows), the following limitations and behaviors apply:

*   **Data Migration and Coherency**: Data migration is handled by the CUDA runtime, but hardware coherency is not guaranteed. Developers may need to use explicit synchronization or memory fences [CUDA_C_Programming_Guide:L693-L723].
*   **GPU Memory Oversubscription**: Similar to full support, oversubscription is possible, but performance implications may differ [CUDA_C_Programming_Guide:L693-L723].
*   **Multi-GPU**: Multi-GPU support is available, but care must be taken with data placement and coherency across devices [CUDA_C_Programming_Guide:L693-L723].
*   **Coherency and Concurrency**: Software-managed coherency requires careful handling of concurrent access to avoid data races [CUDA_C_Programming_Guide:L693-L723].

## Performance Hints

Performance tuning is essential for optimal Unified Memory usage. Key considerations include:

*   **Memory Paging and Page Sizes**: Understanding how memory is paged and the impact of page sizes on performance [CUDA_C_Programming_Guide:L693-L723].
*   **Direct Unified Memory Access from Host**: Optimizing host access to Unified Memory to minimize overhead [CUDA_C_Programming_Guide:L693-L723].
*   **Host Native Atomics**: Leveraging native atomic operations on the host for better performance [CUDA_C_Programming_Guide:L693-L723].
*   **Atomic Accesses & Synchronization**: Using appropriate synchronization primitives to manage concurrent access [CUDA_C_Programming_Guide:L693-L723].
*   **Memcpy()/Memset() Behavior**: Understanding the behavior of memory copy and set operations to avoid unnecessary data movement [CUDA_C_Programming_Guide:L693-L723].

## Lazy Loading

Lazy loading is a feature that can be used with Unified Memory to defer memory allocation and migration until the memory is actually accessed, improving performance and reducing memory overhead [CUDA_C_Programming_Guide:L693-L723].
