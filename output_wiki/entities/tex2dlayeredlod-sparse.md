# tex2DLayeredLod (Sparse CUDA Arrays)

The `tex2DLayeredLod` function is designed for use with sparse CUDA arrays, allowing access to two-dimensional layered textures at a specific level of detail (LOD). It provides a mechanism to determine whether the requested texel data is currently resident in device memory.

## Function Signature

```cpp
template<class T>
tex2DLayeredLod(cudaTextureObject_t texObj, float x, float y, int layer,
    float level, bool* isResident);
```

## Parameters

- **texObj**: The CUDA texture object specifying the two-dimensional layered texture.
- **x**: The x-coordinate of the texture coordinate.
- **y**: The y-coordinate of the texture coordinate.
- **layer**: The specific layer within the layered texture to fetch from.
- **level**: The level of detail (LOD) to use for the fetch.
- **isResident**: A pointer to a boolean value that is set to indicate whether the fetched texel is resident in memory.

## Behavior

The function fetches data from the specified CUDA array at the given texture coordinates `(x, y)`, layer, and LOD. 

- **Residency Check**: The function populates the `isResident` pointer with a boolean value indicating if the texel is resident in memory.
- **Non-Resident Data**: If the texel is not resident in memory, the function returns zeros for the fetched values.

## References

- [CUDA_C_Programming_Guide:L7298-L7307] CUDA C Programming Guide, Section 10.8.1.25: tex2DLayeredLod() for sparse CUDA arrays.
