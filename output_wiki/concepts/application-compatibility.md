# Application Compatibility

Application compatibility in CUDA ensures that code can execute on devices of specific compute capabilities. To achieve this, an application must load binary or PTX code that is compatible with the target device's compute capability [CUDA_C_Programming_Guide:L1167-L1203].

## Embedding Code

The PTX and binary code embedded in a CUDA C++ application are controlled by the `-arch` and `-code` compiler options, or the `-gencode` compiler option [CUDA_C_Programming_Guide:L1167-L1203].

For example, the following command embeds:
*   Binary code compatible with compute capability 5.0 and 6.0.
*   PTX and binary code compatible with compute capability 7.0.

```txt
nvcc x.cu \
    -gencode arch=compute_50,code=sm_50 \
    -gencode arch=compute_60,code=sm_60 \
    -gencode arch=compute_70,code="compute_70,sm_70"
```

### Shorthands

The `nvcc` user manual lists various shorthands for these options. For instance, `-arch=sm_70` is a shorthand for `-arch=compute_70 -code=compute_70,sm_70` [CUDA_C_Programming_Guide:L1167-L1203].

## Runtime Selection and JIT Compilation

Host code is generated to automatically select the most appropriate code to load and execute at runtime [CUDA_C_Programming_Guide:L1167-L1203]. Using the example above:

*   Devices with compute capability 5.0 and 5.2 load the 5.0 binary code.
*   Devices with compute capability 6.0 and 6.1 load the 6.0 binary code.
*   Devices with compute capability 7.0 and 7.5 load the 7.0 binary code.
*   Devices with compute capability later than 7.5 load the PTX code, which is compiled to binary code at runtime (Just-in-Time Compilation) [CUDA_C_Programming_Guide:L1167-L1203].

This mechanism allows applications to execute on future architectures with higher compute capabilities for which no binary code can be generated at compile time, provided PTX code is embedded [CUDA_C_Programming_Guide:L1167-L1203].

## Device Code Differentiation

Device code can differentiate execution paths based on compute capability using the `__CUDA_ARCH__` macro [CUDA_C_Programming_Guide:L1167-L1203].

*   The macro is only defined for device code.
*   Its value corresponds to the compute capability. For example, when compiling with `-arch=compute_80`, `__CUDA_ARCH__` is equal to 800 [CUDA_C_Programming_Guide:L1167-L1203].

### Family and Architecture Specific Features

Specific macros are defined for code compiled for family-specific or architecture-specific features:

*   **Family-Specific Features**: If compiled with `sm_100f` or `compute_100f`, the code runs only on devices in that specific family (e.g., compute capability 10.0 and 10.3). The macro `__CUDA_ARCH_FAMILY_SPECIFIC__` is defined (e.g., equal to 1000) [CUDA_C_Programming_Guide:L1167-L1203].
*   **Architecture-Specific Features**: If compiled with `sm_100a` or `compute_100a`, the code runs only on devices with compute capability 10.0. The macro `__CUDA_ARCH_SPECIFIC__` is defined (e.g., equal to 1000). Since architecture-specific features are a superset of family-specific features, `__CUDA_ARCH_FAMILY_SPECIFIC__` is also defined and equal to 1000 in this case [CUDA_C_Programming_Guide:L1167-L1203].

## Volta and Independent Thread Scheduling

The Volta architecture introduced Independent Thread Scheduling, which changes how threads are scheduled on the GPU [CUDA_C_Programming_Guide:L1167-L1203].

*   Code relying on specific SIMT scheduling behavior from previous architectures may produce incorrect results due to changes in the set of participating threads [CUDA_C_Programming_Guide:L1167-L1203].
*   To aid migration, Volta developers can opt-in to Pascal’s thread scheduling using the compiler option combination `-arch=compute_60 -code=sm_70` [CUDA_C_Programming_Guide:L1167-L1203].

## Driver API

Applications using the driver API must compile code to separate files and explicitly load and execute the most appropriate file at runtime [CUDA_C_Programming_Guide:L1167-L1203].
