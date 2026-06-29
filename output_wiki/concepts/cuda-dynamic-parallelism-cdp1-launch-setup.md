# CUDA Dynamic Parallelism (CDP1) Launch Setup APIs

Kernel launch is a system-level mechanism exposed through the device runtime library, and as such is available directly from PTX via the underlying `cudaGetParameterBuffer()` and `cudaLaunchDevice()` APIs [CUDA_C_Programming_Guide:L14653-L14675]. It is permitted for a CUDA application to call these APIs itself, with the same requirements as for PTX [CUDA_C_Programming_Guide:L14653-L14675]. In both cases, the user is then responsible for correctly populating all necessary data structures in the correct format according to specification [CUDA_C_Programming_Guide:L14653-L14675]. Backwards compatibility is guaranteed in these data structures [CUDA_C_Programming_Guide:L14653-L14675].

As with host-side launch, the device-side operator `<<<>>>` maps to underlying kernel launch APIs [CUDA_C_Programming_Guide:L14653-L14675]. This is so that users targeting PTX will be able to enact a launch, and so that the compiler front-end can translate `<<<>>>` into these calls [CUDA_C_Programming_Guide:L14653-L14675].

## API Definitions

The APIs for these launch functions are different to those of the CUDA Runtime API, and are defined as follows [CUDA_C_Programming_Guide:L14653-L14675]:

```cpp
extern __device__ cudaError_t cudaGetParameterBuffer(void **params);
extern __device__ cudaError_t cudaLaunchDevice(void *kernel,
                               void *params, dim3 gridDim,
                               dim3 blockDim,
                               unsigned int sharedMemSize = 0,
                               cudaStream_t stream = 0);
```

## Implementation Details

The following table summarizes the new device-only launch implementation functions [CUDA_C_Programming_Guide:L14653-L14675]:

| Runtime API Launch Functions | Description of Difference From Host Runtime Behaviour |
| :--- | :--- |
| `cudaGetParameterBuffer` | Generated automatically from `<<<>>>`. Note different API to host equivalent. |
| `cudaLaunchDevice` | Generated automatically from `<<<>>>`. Note different API to host equivalent. |

For the CDP2 version of these APIs, see Launch Setup APIs, above [CUDA_C_Programming_Guide:L14653-L14675].
