# Runtime and Driver API Interoperability

An application can mix runtime API code with driver API code to leverage the strengths of both interfaces. This interoperability allows for flexible integration, such as enabling applications written using the driver API to invoke libraries written using the runtime API (such as cuFFT, cuBLAS, etc.) [CUDA_C_Programming_Guide:L20324-L20352].

## Context Management

The CUDA runtime and driver APIs share context state, allowing them to operate on the same execution context.

### Driver API to Runtime

If a context is created and made current via the driver API, subsequent runtime calls will pick up this context instead of creating a new one [CUDA_C_Programming_Guide:L20324-L20352]. This allows driver-based applications to seamlessly use runtime API functions for device operations.

### Runtime API to Driver

When the runtime is initialized (implicitly, as mentioned in CUDA Runtime), a context is created during this process. This context can be retrieved using `cuCtxGetCurrent()` and used by subsequent driver API calls [CUDA_C_Programming_Guide:L20324-L20352].

### Primary Context

The implicitly created context from the runtime is called the **primary context** [CUDA_C_Programming_Guide:L20324-L20352]. It can be managed from the driver API using the Primary Context Management functions [CUDA_C_Programming_Guide:L20324-L20352].

## Device Memory Interoperability

Device memory can be allocated and freed using either API. The memory pointers are compatible between the two interfaces through casting between `CUdeviceptr` and regular host pointers [CUDA_C_Programming_Guide:L20324-L20352].

### Casting Pointers

`CUdeviceptr` can be cast to regular pointers and vice-versa [CUDA_C_Programming_Guide:L20324-L20352].

```c
CUdeviceptr devPtr;
float* d_data;

// Allocation using driver API
cuMemAlloc(&devPtr, size);
d_data = (float*)devPtr;

// Allocation using runtime API
cudaMalloc(&d_data, size);
devPtr = (CUdeviceptr)d_data;
```

## General Function Compatibility

All functions from the device and version management sections of the reference manual can be used interchangeably between the runtime and driver APIs [CUDA_C_Programming_Guide:L20324-L20352].
