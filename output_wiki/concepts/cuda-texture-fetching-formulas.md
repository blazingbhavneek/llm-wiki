# CUDA Texture Fetching Coordinate Formulas

This section describes the formulas used to compute the value returned by CUDA texture functions, based on the attributes of the texture object [CUDA_C_Programming_Guide:L19366-L19378].

## Texture Representation

The texture bound to the texture object is represented as an array $T$ with dimensions depending on the texture type [CUDA_C_Programming_Guide:L19366-L19378]:

*   **One-dimensional texture**: $N$ texels
*   **Two-dimensional texture**: $N \times M$ texels
*   **Three-dimensional texture**: $N \times M \times L$ texels

## Coordinate Systems

Texture fetching uses coordinates to access texels from the array $T$ [CUDA_C_Programming_Guide:L19366-L19378]. There are two primary coordinate representations [CUDA_C_Programming_Guide:L19366-L19378]:

1.  **Non-normalized coordinates**: Direct integer or floating-point coordinates $x, y, z$.
2.  **Normalized coordinates**: Coordinates scaled by the texture dimensions, expressed as $x/N, y/M, z/L$ [CUDA_C_Programming_Guide:L19366-L19378].

## Addressing and Range

*   The formulas assume coordinates are within the valid range [CUDA_C_Programming_Guide:L19366-L19378].
*   Out-of-range coordinates are remapped to the valid range based on the addressing mode, as detailed in the Texture Memory documentation [CUDA_C_Programming_Guide:L19366-L19378].

## References

*   [CUDA_C_Programming_Guide:L19366-L19378] CUDA C Programming Guide, Section on Texture Fetching Formulas.
