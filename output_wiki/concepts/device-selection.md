# Device Selection

A host thread can set the device it operates on at any time by calling `cudaSetDevice()` [CUDA_C_Programming_Guide:L3470-L3473].

## Current Device Context

Once a device is set as current, all subsequent operations are associated with that specific device [CUDA_C_Programming_Guide:L3470-L3473]. This includes:

*   **Device memory allocations**: Calls to `cudaMalloc` allocate memory on the currently set device [CUDA_C_Programming_Guide:L3470-L3473].
*   **Kernel launches**: Kernels are executed on the currently set device [CUDA_C_Programming_Guide:L3470-L3473].
*   **Streams and events**: These are created in association with the currently set device [CUDA_C_Programming_Guide:L3470-L3473].

If no call to `cudaSetDevice()` is made, the current device defaults to device 0 [CUDA_C_Programming_Guide:L3470-L3473].

## Example Usage

The following code sample illustrates how setting the current device affects memory allocation and kernel execution [CUDA_C_Programming_Guide:L3474-L3493]:

```cpp
size_t size = 1024 * sizeof(float);
cudaSetDevice(0);          // Set device 0 as current
float* p0;
cudaMalloc(&p0, size);      // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0); // Launch kernel on device 0
cudaSetDevice(1);            // Set device 1 as current
float* p1;
cudaMalloc(&p1, size);      // Allocate memory on device 1
MyKernel<<<1000, 128>>>(p1); // Launch kernel on device 1
```

In this example, `p0` and the first kernel launch are associated with device 0, while `p1` and the second kernel launch are associated with device 1 [CUDA_C_Programming_Guide:L3474-L3493].
