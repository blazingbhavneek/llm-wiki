# tex3D (Sparse CUDA Arrays)

The `tex3D` function provides an interface for fetching data from a three-dimensional sparse CUDA array via a texture object. This variant of the texture fetch function is specifically designed to handle the residency status of texels within sparse arrays.

## Function Signature

```cpp
template<class T>
T tex3D(cudaTextureObject_t texObj, float x, float y, float z, bool* isResident);
```

## Parameters

*   **texObj**: The three-dimensional texture object specifying the CUDA array to fetch from.
*   **x, y, z**: The texture coordinates used to locate the texel within the array.
*   **isResident**: A pointer to a boolean value. Upon return, this indicates whether the texel at the specified coordinates is resident in memory.

## Behavior

The function fetches the value from the CUDA array specified by `texObj` using the provided texture coordinates `(x, y, z)`.

Crucially, for sparse CUDA arrays, the function also returns the residency status of the texel via the `isResident` pointer. If the texel is not resident in memory, the value fetched will be zeros [CUDA_C_Programming_Guide:L7192-L7200].

## Section Reference

This function is documented in Section 10.8.1.14 "tex3D() for sparse CUDA arrays" of the CUDA C Programming Guide [CUDA_C_Programming_Guide:L7192-L7200].
