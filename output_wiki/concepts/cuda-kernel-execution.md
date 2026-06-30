# CUDA Kernel Execution

Details the cuLaunchKernel API, parameter passing mechanisms (array of pointers vs extra options buffer), and strict alignment requirements for device code types, structures, and CUdeviceptr.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20257-L20324

Citation: [CUDA_C_Programming_Guide:L20257-L20324]

````text
## 21.3. Kernel Execution

cuLaunchKernel() launches a kernel with a given execution configuration.

Parameters are passed either as an array of pointers (next to last parameter of cuLaunchKernel()) where the nth pointer corresponds to the nth parameter and points to a region of memory from which the parameter is copied, or as one of the extra options (last parameter of cuLaunchKernel()).

When parameters are passed as an extra option (the CU\_LAUNCH\_PARAM\_BUFFER\_POINTER option), they are passed as a pointer to a single bufer where parameters are assumed to be properly ofset with respect to each other by matching the alignment requirement for each parameter type in device code.

Alignment requirements in device code for the built-in vector types are listed in Table 7. For all other basic types, the alignment requirement in device code matches the alignment requirement in host code and can therefore be obtained using \_\_alignof(). The only exception is when the host compiler aligns double and long long (and long on a 64-bit system) on a one-word boundary instead of a two-word boundary (for example, using gcc’s compilation flag -mno-align-double) since in device code these types are always aligned on a two-word boundary.

CUdeviceptr is an integer, but represents a pointer, so its alignment requirement is \_\_alignof(void\*).

The following code sample uses a macro (ALIGN\_UP()) to adjust the ofset of each parameter to meet its alignment requirement and another macro (ADD\_TO\_PARAM\_BUFFER()) to add each parameter to the parameter bufer passed to the CU\_LAUNCH\_PARAM\_BUFFER\_POINTER option.

```c
#define ALIGN_UP(offset, alignment) \
    (offset) = ((offset) + (alignment) - 1) & ~((alignment) - 1)

char paramBuffer[1024];
size_t paramBufferSize = 0;

#define ADD_TO_PARAM_BUFFER(value, alignment) \
    do {
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

The alignment requirement of a structure is equal to the maximum of the alignment requirements of its fields. The alignment requirement of a structure that contains built-in vector types, CUdeviceptr, or non-aligned double and long long, might therefore difer between device code and host code. Such a structure might also be padded diferently. The following structure, for example, is not padded at all in host code, but it is padded in device code with 12 bytes after field f since the alignment requirement for field f4 is 16.

```txt
typedef struct {
    float  f;
    float4 f4;
```

(continues on next page)

} myStruct;

(continued from previous page)

## 21.4. Interoperability between Runtime and Driver APIs
````
