# CUDA Dynamic Parallelism (CDP1) cudaGetParameterBuffer

The `cudaGetParameterBuffer` function is part of the CUDA Dynamic Parallelism 1 (CDP1) API. It is used to obtain a buffer for kernel parameters. This function must be declared at the PTX level before it is used.

## PTX-Level Declaration

The PTX-level declaration of `cudaGetParameterBuffer` must follow one of two forms, depending on the address size (`.address_size`) of the target architecture [CUDA_C_Programming_Guide:L14746-L14780].

### 64-bit Address Size

When `.address_size` is 64, the declaration is [CUDA_C_Programming_Guide:L14746-L14780]:

```txt
// PTX-level Declaration of cudaGetParameterBuffer() when .address_size is 64
// When .address_size is 64
.extern .func(.param .b64 func_retval0) cudaGetParameterBuffer
(
    .param .b64 alignment,
    .param .b64 size
)
;
```

### 32-bit Address Size

When `.address_size` is 32, the declaration is [CUDA_C_Programming_Guide:L14746-L14780]:

```txt
// PTX-level Declaration of cudaGetParameterBuffer() when .address_size is 32
.extern .func(.param .b32 func_retval0) cudaGetParameterBuffer
(
    .param .b32 alignment,
    .param .b32 size
)
;
```

## CUDA-Level Declaration

The following CUDA-level declaration maps to the PTX-level declarations above [CUDA_C_Programming_Guide:L14746-L14780]:

```c
// CUDA-level Declaration of cudaGetParameterBuffer()
extern "C" __device__
void *cudaGetParameterBuffer(size_t alignment, size_t size);
```

## Parameters

The function takes two parameters [CUDA_C_Programming_Guide:L14746-L14780]:

1.  **alignment**: Specifies the alignment requirement of the parameter buffer.
2.  **size**: Specifies the size requirement in bytes.

## Alignment and Portability

In the current implementation, the parameter buffer returned by `cudaGetParameterBuffer` is always guaranteed to be 64-byte aligned, and the `alignment` parameter is ignored [CUDA_C_Programming_Guide:L14746-L14780].

However, it is recommended to pass the correct alignment requirement value—which is the largest alignment of any parameter to be placed in the parameter buffer—to `cudaGetParameterBuffer` to ensure portability in the future [CUDA_C_Programming_Guide:L14746-L14780].

## See Also

For the CDP2 version of this document, see `cudaGetParameterBuffer` (CDP2) [CUDA_C_Programming_Guide:L14746-L14747].
