# 10.36. Dynamic Global Memory Allocation and Operations

Dynamic global memory allocation and operations are only supported by devices of compute capability 2.x and higher.

```c
__host__ __device__ void* malloc(size_t size);
__device__ void *__nv_aligned_device_malloc(size_t size, size_t align);
__host__ __device__ void free(void* ptr);
```

allocate and free memory dynamically from a fixed-size heap in global memory.

\_\_host\_\_ \_\_device\_\_ void\* memcpy(void\* dest, const void\* src, size\_t size);

copy size bytes from the memory location pointed by src to the memory location pointed by dest.

\_\_host\_\_ \_\_device\_\_ void\* memset(void\* ptr, int value, size\_t size);

set size bytes of memory block pointed by ptr to value (interpreted as an unsigned char).

The CUDA in-kernel malloc()function allocates at least size bytes from the device heap and returns a pointer to the allocated memory or NULL if insuficient memory exists to fulfill the request. The returned pointer is guaranteed to be aligned to a 16-byte boundary.

The CUDA in-kernel \_\_nv\_aligned\_device\_malloc() function allocates at least size bytes from the device heap and returns a pointer to the allocated memory or NULL if insuficient memory exists to fulfill the requested size or alignment. The address of the allocated memory will be a multiple of align. align must be a non-zero power of 2.

The CUDA in-kernel free() function deallocates the memory pointed to by ptr, which must have been returned by a previous call to malloc() or \_\_nv\_aligned\_device\_malloc(). If ptr is NULL, the call to free() is ignored. Repeated calls to free() with the same ptr has undefined behavior.

The memory allocated by a given CUDA thread via malloc() or \_\_nv\_aligned\_device\_malloc() remains allocated for the lifetime of the CUDA context, or until it is explicitly released by a call to free(). It can be used by any other CUDA threads even from subsequent kernel launches. Any CUDA thread may free memory allocated by another thread, but care should be taken to ensure that the same pointer is not freed more than once.

## 10.36.1. Heap Memory Allocation

The device memory heap has a fixed size that must be specified before any program using malloc(), \_\_nv\_aligned\_device\_malloc() or free() is loaded into the context. A default heap of eight megabytes is allocated if any program uses malloc() or \_\_nv\_aligned\_device\_malloc() without explicitly specifying the heap size.

The following API functions get and set the heap size:

cudaDeviceGetLimit(size\_t\* size, cudaLimitMallocHeapSize)

cudaDeviceSetLimit(cudaLimitMallocHeapSize, size\_t size)

The heap size granted will be at least size bytes. cuCtxGetLimit()and cudaDeviceGetLimit() return the currently requested heap size.

The actual memory allocation for the heap occurs when a module is loaded into the context, either explicitly via the CUDA driver API (see Module), or implicitly via the CUDA runtime API (see CUDA Runtime). If the memory allocation fails, the module load will generate a CUDA\_ERROR\_SHARED\_OBJECT\_INIT\_FAILED error.

Heap size cannot be changed once a module load has occurred and it does not resize dynamically according to need.

Memory reserved for the device heap is in addition to memory allocated through host-side CUDA API calls such as cudaMalloc().

## 10.36.2. Interoperability with Host Memory API

Memory allocated via device malloc() or \_\_nv\_aligned\_device\_malloc() cannot be freed using the runtime (i.e., by calling any of the free memory functions from Device Memory).

Similarly, memory allocated via the runtime (i.e., by calling any of the memory allocation functions from Device Memory) cannot be freed via free().

In addition, memory allocated by a call to malloc() or \_\_nv\_aligned\_device\_malloc() in device code cannot be used in any runtime or driver API calls (i.e. cudaMemcpy, cudaMemset, etc).

## 10.36.3. Examples

## 10.36.3.1 Per Thread Allocation

The following code sample:

```c
#include <stdlib.h>
#include <stdio.h>

__global__ void mallocTest()
{
    size_t size = 123;
    char* ptr = (char*)malloc(size);
    memset(ptr, 0, size);
    printf("Thread %d got pointer: %p\n", threadIdx.x, ptr);
```

(continues on next page)

```cpp
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

(continued from previous page)

will output:

```txt
Thread 0 got pointer: 00057020
Thread 1 got pointer: 0005708c
Thread 2 got pointer: 000570f8
Thread 3 got pointer: 00057164
Thread 4 got pointer: 000571d0
```

Notice how each thread encounters the malloc() and memset() commands and so receives and initializes its own allocation. (Exact pointer values will vary: these are illustrative.)

## 10.36.3.2 Per Thread Block Allocation

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
```

(continues on next page)

```txt
if (threadIdx.x == 0)
        free(data);
}

int main()
{
    cudaDeviceSetLimit(cudaLimitMallocHeapSize, 128*1024*1024);
    mallocTest<<<10, 128>>>();
    cudaDeviceSynchronize();
    return 0;
}
```

(continued from previous page)
