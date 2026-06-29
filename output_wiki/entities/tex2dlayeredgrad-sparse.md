# tex2DLayeredGrad (Sparse CUDA Arrays)

The `tex2DLayeredGrad` function is designed for use with sparse CUDA arrays, allowing texture fetches from two-dimensional layered textures while providing information about memory residency.

## Function Signature

```cpp
template<class T>
tex2DLayeredGrad(cudaTextureObject_t texObj, float x, float y, int layer,
    float2 dx, float2 dy, bool* isResident);
```

## Description

This function fetches data from a CUDA array specified by a two-dimensional layered texture object [`CUDA_C_Programming_Guide:L7318-L7327`]. The operation is defined by the following parameters:

*   **texObj**: The texture object specifying the CUDA array.
*   **x, y**: The texture coordinates used for the fetch.
*   **layer**: The specific layer within the layered texture to access.
*   **dx, dy**: Gradient vectors used to derive the level-of-detail (LOD) for the texture fetch [`CUDA_C_Programming_Guide:L7318-L7327`].
*   **isResident**: A pointer to a boolean value that indicates whether the fetched texel is resident in memory [`CUDA_C_Programming_Guide:L7318-L7327`].

## Behavior

If the texel specified by the coordinates and layer is not resident in memory, the function returns zero values for the fetched data, and the `isResident` pointer is set to indicate non-residency [`CUDA_C_Programming_Guide:L7318-L7327`]. This behavior is critical for applications relying on sparse textures, as it allows the kernel to handle missing data gracefully without causing faults.

## See Also

*   Sparse CUDA Arrays
*   Texture Objects
*   `tex2DLayered`
