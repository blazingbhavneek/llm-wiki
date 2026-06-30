# CUDA Dynamic Parallelism Launch Setup APIs

Low-level kernel launch APIs (`cudaGetParameterBuffer`, `cudaLaunchDevice`) exposed by the device runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14028-L14041

Citation: [CUDA_C_Programming_Guide:L14028-L14041]

````text
Table 13: New Device-only Launch Implementation Functions

<table><tr><td>Runtime API Launch Functions</td><td>Description of Difference From Host Runtime Behaviour (behavior is identical if no description)</td></tr><tr><td>cudaGetParameter-Buffer</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr><tr><td>cudaLaunchDevice</td><td>Generated automatically from &lt;&lt;&gt;&gt;&gt;. Note different API to host equivalent.</td></tr></table>

The APIs for these launch functions are diferent to those of the CUDA Runtime API, and are defined as follows:

```c
extern    device  cudaError_t cudaGetParameterBuffer(void **params);
extern __device__  cudaError_t cudaLaunchDevice(void *kernel,
                               void *params, dim3 gridDim,
                               dim3 blockDim,
                               unsigned int sharedMemSize = 0,
                               cudaStream_t stream = 0);
```
````
