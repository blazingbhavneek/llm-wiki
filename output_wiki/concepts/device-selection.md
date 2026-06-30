# Device Selection

Host threads can set the active device using cudaSetDevice(). All memory allocations and kernel launches occur on the currently set device. If unset, device 0 is used by default.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3471-L3494

Citation: [CUDA_C_Programming_Guide:L3471-L3494]

````text
## 6.2.9.2 Device Selection

A host thread can set the device it operates on at any time by calling cudaSetDevice(). Device memory allocations and kernel launches are made on the currently set device; streams and events are created in association with the currently set device. If no call to cudaSetDevice() is made, the current device is device 0.

The following code sample illustrates how setting the current device afects memory allocation and kernel execution.

```cpp
size_t size = 1024 * sizeof(float);
cudaSetDevice(0);          // Set device 0 as current
float* p0;
cudaMalloc(&p0, size);      // Allocate memory on device 0
MyKernel<<<1000, 128>>>(p0); // Launch kernel on device 0
cudaSetDevice(1);            // Set device 1 as current
float* p1;
```

(continues on next page)

```cpp
cudaMalloc(&p1, size);      // Allocate memory on device 1
MyKernel<<<1000, 128>>>(p1); // Launch kernel on device 1
```

(continued from previous page)
````
