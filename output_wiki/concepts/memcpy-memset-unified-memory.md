# Memcpy/Memset Behavior with Unified Memory

The `cudaMemcpy*()` and `cudaMemset*()` functions accept any unified memory pointer as arguments. When working with unified memory, the direction specified via the `cudaMemcpyKind` parameter in `cudaMemcpy*()` serves as a performance hint. This hint can have a significant performance impact if any of the arguments is a unified memory pointer [CUDA_C_Programming_Guide:L21799-L21815].

## Performance Advice

To optimize performance when using these APIs with unified memory, follow these recommendations [CUDA_C_Programming_Guide:L21799-L21815]:

*   **Accurate Hints**: When the physical location of the unified memory is known, use an accurate `cudaMemcpyKind` hint.
*   **Default Preference**: Prefer `cudaMemcpyDefault` over an inaccurate `cudaMemcpyKind` hint.
*   **Avoid Initialization**: Always use populated (initialized) buffers; avoid using these APIs to initialize memory.
*   **System-Allocated Memory**: Avoid using `cudaMemcpy*()` if both pointers point to System-Allocated Memory. Instead, launch a kernel or use a CPU memory copy algorithm such as `std::memcpy`.
