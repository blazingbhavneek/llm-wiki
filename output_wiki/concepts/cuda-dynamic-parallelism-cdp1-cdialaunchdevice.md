# CUDA Dynamic Parallelism (CDP1) cudaLaunchDevice

The `cudaLaunchDevice` function is the API used for launching kernels from device code in CUDA Dynamic Parallelism version 1 (CDP1). It allows a kernel running on the GPU to launch other kernels.

## PTX-Level Declaration

At the PTX level, `cudaLaunchDevice()` must be declared before it is used. The declaration depends on the address size (32-bit or 64-bit) of the compilation target.

### 64-bit Address Space

When `.address_size` is 64, the PTX-level declaration is:

```txt
// PTX-level Declaration of cudaLaunchDevice() when .address_size is 64
 extern .func(.param .b32 func_retval0) cudaLaunchDevice
(
  .param .b64 func,
  .param .b64 parameterBuffer,
  .param .align 4 .b8 gridDimension[12],
  .param .align 4 .b8 blockDimension[12],
  .param .b32 sharedMemSize,
  .param .b64 stream
)
;
```

### 32-bit Address Space

When `.address_size` is 32, the PTX-level declaration is:

```txt
// PTX-level Declaration of cudaLaunchDevice() when .address_size is 32
.extern .func(.param .b32 func_retval0) cudaLaunchDevice
(
    .param .b32 func,
    .param .b32 parameterBuffer,
    .param .align 4 .b8 gridDimension[12],
    .param .align 4 .b8 blockDimension[12],
    .param .b32 sharedMemSize,
    .param .b32 stream
)
;
```

## CUDA-Level Declaration

The CUDA-level declaration is mapped to one of the aforementioned PTX-level declarations and is found in the system header file `cuda_device_runtime_api.h`:

```c
// CUDA-level declaration of cudaLaunchDevice()
extern "C" __device__
cudaError_t cudaLaunchDevice(void *func, void *parameterBuffer,
                       dim3 gridDimension, dim3 blockDimension,
                       unsigned int sharedMemSize,
                       cudaStream_t stream);
```

This function is defined in the `cudadevrt` system library, which must be linked with a program in order to use device-side kernel launch functionality.

## Parameters

- **func**: A pointer to the kernel to be launched.
- **parameterBuffer**: A pointer to the parameter buffer that holds the actual parameters to the launched kernel. The layout of the parameter buffer is explained in Parameter Buffer Layout (CDP1).
- **gridDimension**: Specifies the grid dimension of the launch configuration.
- **blockDimension**: Specifies the block dimension of the launch configuration.
- **sharedMemSize**: Specifies the amount of shared memory to be allocated per block for the launched kernel.
- **stream**: Specifies the stream associated with the launch.

For detailed descriptions of the launch configuration parameters (grid, block, shared memory, stream), refer to Execution Configuration.

## See Also

- For the CDP2 version of this document, see `cudaLaunchDevice`.
- Parameter Buffer Layout (CDP1)
- Execution Configuration
