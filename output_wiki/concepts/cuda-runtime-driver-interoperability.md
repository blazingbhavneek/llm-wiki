# CUDA Runtime and Driver API Interoperability

Explains how runtime and driver APIs can be mixed. Driver-created contexts are picked up by runtime calls, and vice versa. Memory allocated via one API can be cast and used by the other.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20325-L20352

Citation: [CUDA_C_Programming_Guide:L20325-L20352]

````text

An application can mix runtime API code with driver API code.

If a context is created and made current via the driver API, subsequent runtime calls will pick up this context instead of creating a new one.

If the runtime is initialized (implicitly as mentioned in CUDA Runtime), cuCtxGetCurrent() can be used to retrieve the context created during initialization. This context can be used by subsequent driver API calls.

The implicitly created context from the runtime is called the primary context (see Initialization). It can be managed from the driver API with the Primary Context Management functions.

Device memory can be allocated and freed using either API. CUdeviceptr can be cast to regular pointers and vice-versa:

```txt
CUdeviceptr devPtr;
float* d_data;

// Allocation using driver API
cuMemAlloc(&devPtr, size);
d_data = (float*)devPtr;

// Allocation using runtime API
cudaMalloc(&d_data, size);
devPtr = (CUdeviceptr)d_data;
```

In particular, this means that applications written using the driver API can invoke libraries written using the runtime API (such as cuFFT, cuBLAS, …).

All functions from the device and version management sections of the reference manual can be used interchangeably.
````
