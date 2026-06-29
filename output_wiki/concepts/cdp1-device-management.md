# CDP1 Device Management

## Overview

The Compute Device Programming (CDP) version 1 (CDP1) device runtime has specific limitations regarding device scope. Unlike later versions or host-side APIs, the CDP1 device runtime does not support multi-GPU operations.

## Scope and Limitations

### Single-Device Execution

The device runtime is restricted to operating only on the device upon which it is currently executing. There is no multi-GPU support from the device runtime itself [CUDA_C_Programming_Guide:L14360-L14382]. This means that kernels launched from within a device function cannot directly manage or execute on other GPUs in the system.

### Device Property Queries

While execution is confined to the current device, the runtime permits querying properties for any CUDA-capable device in the system [CUDA_C_Programming_Guide:L14360-L14382]. This allows device code to inspect system configuration without performing cross-device operations.

## Example Usage

The following example demonstrates a parent kernel launching a child kernel on the same device. The parent kernel initializes data, synchronizes threads, and then launches the child kernel from thread 0, followed by synchronization to ensure completion before proceeding [CUDA_C_Programming_Guide:L14360-L14382].

```lisp
__global__ void child_launch(int *data) {
    data[threadIdx.x] = data[threadIdx.x]+1;
}

__global__ void parent_launch(int *data) {
    data[threadIdx.x] = threadIdx.x;

    __syncthreads();

    if (threadIdx.x == 0) {
        child_launch<<< 1, 256 >>>(data);
        cudaDeviceSynchronize();
    }

    __syncthreads();
}
```

## Comparison with CDP2

For features including multi-GPU support, refer to the Device Management section for the CDP2 version of the documentation [CUDA_C_Programming_Guide:L14360-L14382].

## See Also

- [CUDA_C_Programming_Guide:L14360-L14382] Device Management (CDP1)
