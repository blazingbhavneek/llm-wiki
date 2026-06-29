# Dynamic Global Memory Allocation

Dynamic global memory allocation enables CUDA kernels to allocate and deallocate memory from a fixed-size heap located in global memory [CUDA_C_Programming_Guide:L11304-L11331]. This feature is supported on devices with compute capability 2.x and higher [CUDA_C_Programming_Guide:L11304-L11331].

## Overview

The CUDA runtime provides several functions for in-kernel memory management:

*   `malloc(size_t size)`: Allocates at least `size` bytes from the device heap. Returns a pointer aligned to a 16-byte boundary, or `NULL` if insufficient memory exists [CUDA_C_Programming_Guide:L11304-L11331].
*   `__nv_aligned_device_malloc(size_t size, size_t align)`: Allocates at least `size` bytes with a specific alignment. The address is a multiple of `align`, which must be a non-zero power of 2. Returns `NULL` if the request cannot be fulfilled [CUDA_C_Programming_Guide:L11304-L11331].
*   `free(void* ptr)`: Deallocates memory previously allocated by `malloc` or `__nv_aligned_device_malloc`. If `ptr` is `NULL`, the call is ignored. Repeated calls with the same pointer result in undefined behavior [CUDA_C_Programming_Guide:L11304-L11331].
*   `memcpy(void* dest, const void* src, size_t size)`: Copies `size` bytes from `src` to `dest` [CUDA_C_Programming_Guide:L11304-L11331].
*   `memset(void* ptr, int value, size_t size)`: Sets `size` bytes of memory pointed to by `ptr` to `value` [CUDA_C_Programming_Guide:L11304-L11331].

Memory allocated by a CUDA thread persists for the lifetime of the CUDA context or until explicitly released via `free()` [CUDA_C_Programming_Guide:L11304-L11331]. Allocated memory can be accessed by any other CUDA threads, including those in subsequent kernel launches [CUDA_C_Programming_Guide:L11304-L11331]. Any thread may free memory allocated by another thread, but care must be taken to ensure the same pointer is not freed more than once [CUDA_C_Programming_Guide:L11304-L11331].

## Heap Configuration

The device memory heap has a fixed size that must be specified before any program using `malloc()`, `__nv_aligned_device_malloc()`, or `free()` is loaded into the context [CUDA_C_Programming_Guide:L11332-L11348].

*   **Default Size**: If no explicit size is specified, a default heap of 8 megabytes is allocated [CUDA_C_Programming_Guide:L11332-L11348].
*   **API Functions**: The heap size can be queried and set using:
    *   `cudaDeviceGetLimit(size_t* size, cudaLimitMallocHeapSize)`
    *   `cudaDeviceSetLimit(cudaLimitMallocHeapSize, size_t size)` [CUDA_C_Programming_Guide:L11332-L11348]
*   **Constraints**: The heap size cannot be changed once a module has been loaded into the context [CUDA_C_Programming_Guide:L11332-L11348]. It does not resize dynamically based on need [CUDA_C_Programming_Guide:L11332-L11348].
*   **Separation**: Memory reserved for the device heap is separate from memory allocated via host-side APIs like `cudaMalloc()` [CUDA_C_Programming_Guide:L11332-L11348].

## Interoperability

Memory allocated via device-side functions (`malloc`, `__nv_aligned_device_malloc`) is distinct from memory allocated via the CUDA runtime API (`cudaMalloc`, etc.) [CUDA_C_Programming_Guide:L11349-L11357].

*   Device-allocated memory cannot be freed using runtime free functions [CUDA_C_Programming_Guide:L11349-L11357].
*   Runtime-allocated memory cannot be freed using the device `free()` function [CUDA_C_Programming_Guide:L11349-L11357].
*   Memory allocated by `malloc()` or `__nv_aligned_device_malloc()` in device code cannot be used in runtime or driver API calls such as `cudaMemcpy` or `cudaMemset` [CUDA_C_Programming_Guide:L11349-L11357].

## Usage Examples

### Per-Thread Allocation

Each thread can allocate its own memory. In the following example, each of the 5 threads allocates 123 bytes, initializes it, and then frees it [CUDA_C_Programming_Guide:L11358-L11405].

```c
#include <stdlib.h>
#include <stdio.h>

__global__ void mallocTest()
{
    size_t size = 123;
    char* ptr = (char*)malloc(size);
    memset(ptr, 0, size);
    printf("Thread %d got pointer: %p\n", threadIdx.x, ptr);
    free(ptr);
}

int main()
{
    // Set a heap size of 128 megabytes. Note that this must
    // be done before any kernel is launched.
    cudaDeviceSetLimit(cudaLimitMallocHeapSize, 128*1024*1024);
    mallocTest<<<1, 5>>>();
    cudaDeviceSynchronize();
    return 0;
}
```

### Per-Thread Block Allocation

To allow all threads in a block to share allocated memory, one thread (e.g., `threadIdx.x == 0`) performs the allocation and stores the pointer in shared memory [CUDA_C_Programming_Guide:L11406-L11457].

```c
#include <stdlib.h>

__global__ void mallocTest()
{
    __shared__ int* data;

    // The first thread in the block does the allocation and then
    // shares the pointer with all other threads through shared memory,
    // so that access can easily be coalesced.
    // 64 bytes per thread are allocated.
    if (threadIdx.x == 0) {
        size_t size = blockDim.x * 64;
        data = (int*)malloc(size);
    }
    __syncthreads();

    // Check for failure
    if (data == NULL)
        return;

    // Threads index into the memory, ensuring coalescence
    int* ptr = data;
    for (int i = 0; i < 64; ++i)
        ptr[i * blockDim.x + threadIdx.x] = threadIdx.x;

    // Ensure all threads complete before freeing
    __syncthreads();

    // Only one thread may free the memory!
    if (threadIdx.x == 0)
        free(data);
}
```

### Allocation Persisting Between Kernel Launches

Memory allocated in one kernel launch can be accessed by subsequent kernel launches if the pointer is stored in device global memory [CUDA_C_Programming_Guide:L11458-L11532].

```c
#include <stdlib.h>
#include <stdio.h>

#define NUM_BLOCKS 20

__device__ int* dataptr[NUM_BLOCKS]; // Per-block pointer

__global__ void allocmem()
{
    // Only the first thread in the block does the allocation
    // since we want only one allocation per block.
    if (threadIdx.x == 0)
        dataptr[blockIdx.x] = (int*)malloc(blockDim.x * 4);
    __syncthreads();

    // Check for failure
    if (dataptr[blockIdx.x] == NULL)
        return;

    // Zero the data with all threads in parallel
    dataptr[blockIdx.x][threadIdx.x] = 0;
}

// Simple example: store thread ID into each element
__global__ void usemem()
{
    int* ptr = dataptr[blockIdx.x];
    if (ptr != NULL)
        ptr[threadIdx.x] += threadIdx.x;
}

// Print the content of the buffer before freeing it
__global__ void freemem()
{
    int* ptr = dataptr[blockIdx.x];
    if (ptr != NULL)
        printf("Block %d, Thread %d: final value = %d\n",
            blockIdx.x, threadIdx.x, ptr[threadIdx.x]);

    // Only free from one thread!
    if (threadIdx.x == 0)
        free(ptr);
}

int main()
{
    cudaDeviceSetLimit(cudaLimitMallocHeapSize, 128*1024*1024);

    // Allocate memory
    allocmem<<< NUM_BLOCKS, 10 >>>();

    // Use memory
    usemem<<< NUM_BLOCKS, 10 >>>();
    usemem<<< NUM_BLOCKS, 10 >>>();
    usemem<<< NUM_BLOCKS, 10 >>>();

    // Free memory
    freemem<<< NUM_BLOCKS, 10 >>>();

    cudaDeviceSynchronize();

    return 0;
}
```
