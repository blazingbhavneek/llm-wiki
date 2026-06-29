# CUDA TMA PTX Wrappers (cp.async.bulk.tensor)

The `cuda::device::experimental::cp_async_bulk_tensor` family of functions provides C++ wrapper interfaces for the PTX `cp.async.bulk.tensor` instructions. These instructions initiate bulk tensor asynchronous copies between global memory and shared memory [CUDA_C_Programming_Guide:L10572-L10645].

The wrappers are categorized by dimensionality (1D through 5D) and direction of data transfer: global-to-shared and shared-to-global [CUDA_C_Programming_Guide:L10572-L10645].

## Global to Shared Memory Wrappers

The following functions initiate asynchronous copies from global memory (defined by a `CUtensorMap`) to shared memory. They require a destination pointer, a tensor map, coordinate arguments corresponding to the dimensionality, and a barrier object for synchronization [CUDA_C_Programming_Guide:L10572-L10645].

### 1D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_1d_global_to_shared(
    void *dest, const CUtensorMap *tensor_map, int c0,
    cuda::barrier<cuda::thread_scope_block> &bar
);
```

### 2D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_2d_global_to_shared(
    void *dest, const CUtensorMap *tensor_map, int c0, int c1,
    cuda::barrier<cuda::thread_scope_block> &bar
);
```

### 3D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_3d_global_to_shared(
    void *dest, const CUtensorMap *tensor_map, int c0, int c1, int c2,
    cuda::barrier<cuda::thread_scope_block> &bar
);
```

### 4D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_4d_global_to_shared(
    void *dest, const CUtensorMap *tensor_map, int c0, int c1, int c2, int c3,
    cuda::barrier<cuda::thread_scope_block> &bar
);
```

### 5D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_5d_global_to_shared(
    void *dest, const CUtensorMap *tensor_map, int c0, int c1, int c2, int c3, int c4,
    cuda::barrier<cuda::thread_scope_block> &bar
);
```

## Shared to Global Memory Wrappers

The following functions initiate asynchronous copies from shared memory to global memory (defined by a `CUtensorMap`). They require a tensor map, coordinate arguments, and a source pointer [CUDA_C_Programming_Guide:L10572-L10645].

### 1D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_1d_shared_to_global(
    const CUtensorMap *tensor_map, int c0, const void *src
);
```

### 2D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_2d_shared_to_global(
    const CUtensorMap *tensor_map, int c0, int c1, const void *src
);
```

### 3D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_3d_shared_to_global(
    const CUtensorMap *tensor_map, int c0, int c1, int c2, const void *src
);
```

### 4D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_4d_shared_to_global(
    const CUtensorMap *tensor_map, int c0, int c1, int c2, int c3, const void *src
);
```

### 5D
```cpp
inline __device__
void cuda::device::experimental::cp_async_bulk_tensor_5d_shared_to_global(
    const CUtensorMap *tensor_map, int c0, int c1, int c2, int c3, int c4, const void *src
);
```

## References
- [CUDA_C_Programming_Guide:L10572-L10645]
