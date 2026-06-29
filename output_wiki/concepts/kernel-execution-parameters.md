# Kernel Execution Parameters and Alignment

## Overview
The `cuLaunchKernel` function launches a kernel with a specified execution configuration. Kernel parameters (arguments) are passed to the kernel using one of two methods: an array of pointers or a parameter buffer [CUDA_C_Programming_Guide:L20257-L20323].

## Parameter Passing Methods

### Array of Pointers
Parameters can be passed as an array of pointers, which is the next-to-last parameter of `cuLaunchKernel`. In this method, the nth pointer in the array corresponds to the nth parameter of the kernel and points to a region of memory from which the parameter value is copied [CUDA_C_Programming_Guide:L20257-L20323].

### Parameter Buffer
Alternatively, parameters can be passed as an extra option using the `CU_LAUNCH_PARAM_BUFFER_POINTER` flag, which is the last parameter of `cuLaunchKernel`. This approach involves passing a pointer to a single buffer where parameters are stored sequentially [CUDA_C_Programming_Guide:L20257-L20323].

When using a parameter buffer, parameters must be properly offset with respect to each other, matching the alignment requirements for each parameter type as defined in device code [CUDA_C_Programming_Guide:L20257-L20323].

## Alignment Requirements

Proper alignment is critical when using the parameter buffer approach. Alignment requirements in device code for built-in vector types are defined separately (see Table 7 in the CUDA C Programming Guide). For all other basic types, the alignment requirement in device code typically matches that in host code and can be obtained using the `__alignof()` macro [CUDA_C_Programming_Guide:L20257-L20323].

### Exceptions and Specific Types

*   **Double and Long Long:** The only exception to the general rule is when the host compiler aligns `double` and `long long` (and `long` on a 64-bit system) on a one-word boundary instead of a two-word boundary (e.g., using GCC's `-mno-align-double` flag). In device code, these types are always aligned on a two-word boundary [CUDA_C_Programming_Guide:L20257-L20323].
*   **CUdeviceptr:** Although `CUdeviceptr` is an integer type, it represents a pointer. Therefore, its alignment requirement is `__alignof(void*)` [CUDA_C_Programming_Guide:L20257-L20323].

### Structure Alignment
The alignment requirement of a structure is equal to the maximum of the alignment requirements of its fields. Consequently, structures containing built-in vector types, `CUdeviceptr`, or non-aligned `double` and `long long` may have different alignment requirements and padding between host code and device code [CUDA_C_Programming_Guide:L20257-L20323].

For example, a structure containing a `float` followed by a `float4` is not padded in host code but is padded in device code with 12 bytes after the `float` field to satisfy the 16-byte alignment requirement of `float4` [CUDA_C_Programming_Guide:L20257-L20323].

```c
typedef struct {
    float  f;
    float4 f4;
} myStruct;
```

## Implementation Example

The following code demonstrates how to manage offsets and alignment when constructing a parameter buffer. It uses an `ALIGN_UP` macro to adjust the offset to meet alignment requirements and an `ADD_TO_PARAM_BUFFER` macro to copy values into the buffer [CUDA_C_Programming_Guide:L20257-L20323].

```c
#define ALIGN_UP(offset, alignment) \
    (offset) = ((offset) + (alignment) - 1) & ~((alignment) - 1)

char paramBuffer[1024];
size_t paramBufferSize = 0;

#define ADD_TO_PARAM_BUFFER(value, alignment) \
    do { \
        paramBufferSize = ALIGN_UP(paramBufferSize, alignment); \
        memcpy(paramBuffer + paramBufferSize, \
            &(value), sizeof(value)); \
        paramBufferSize += sizeof(value); \
    } while (0)

int i;
ADD_TO_PARAM_BUFFER(i, __alignof(i));
float4 f4;
ADD_TO_PARAM_BUFFER(f4, 16); // float4's alignment is 16
char c;
ADD_TO_PARAM_BUFFER(c, __alignof(c));
float f;
ADD_TO_PARAM_BUFFER(f, __alignof(f));
CUdeviceptr devPtr;
ADD_TO_PARAM_BUFFER(devPtr, __alignof(devPtr));
float2 f2;
ADD_TO_PARAM_BUFFER(f2, 8); // float2's alignment is 8

void* extra[] = {
    CU_LAUNCH_PARAM_BUFFER_POINTER, paramBuffer,
    CU_LAUNCH_PARAM_BUFFER_SIZE,      &paramBufferSize,
    CU_LAUNCH_PARAM_END
};
cuLaunchKernel(cuFunction,
                    blockWidth, blockHeight, blockDepth,
                    gridWidth, gridHeight, gridDepth,
                    0, 0, 0, extra);
```

## References
- CUDA C Programming Guide, Section 21.3. Kernel Execution [CUDA_C_Programming_Guide:L20257-L20323]
