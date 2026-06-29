# tex3DLod (Sparse CUDA Arrays)

The `tex3DLod` function is designed for use with sparse CUDA arrays, allowing texture fetches from three-dimensional texture objects while explicitly checking memory residency.

## Function Signature

```cpp
template<class T>
T tex3DLod(cudaTextureObject_t texObj, float x, float y, float z, float level, bool* isResident);
```

## Parameters

- **texObj**: The three-dimensional texture object specifying the CUDA array or region of linear memory.
- **x, y, z**: The texture coordinates for the fetch.
- **level**: The level-of-detail (LOD) at which to fetch the texel.
- **isResident**: A pointer to a boolean value that indicates whether the requested texel is resident in memory.

## Behavior

The function fetches the texel value from the specified texture object at the given coordinates `(x, y, z)` and LOD `level` [CUDA_C_Programming_Guide:L7210-L7219].

For sparse CUDA arrays, the function also returns the residency status of the texel via the `isResident` pointer [CUDA_C_Programming_Guide:L7210-L7219]. If the texel is not resident in memory, the function returns zero values for the fetched data [CUDA_C_Programming_Guide:L7210-L7219].

## Usage Context

This function is part of the CUDA C++ programming interface for texture operations, specifically handling the complexities of sparse memory where pages may not be resident on the device [CUDA_C_Programming_Guide:L7210-L7219]. It enables applications to handle non-resident texels gracefully by checking the `isResident` flag before relying on the fetched data.

## See Also

- `tex3D`: Standard 3D texture fetch.
- Sparse CUDA Arrays: Documentation on managing sparse memory residency.
