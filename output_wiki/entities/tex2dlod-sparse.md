# tex2DLod (Sparse CUDA Arrays)

The `tex2DLod` function is used to fetch data from a CUDA array specified by a two-dimensional texture object, specifically within the context of sparse CUDA arrays.

## Function Signature

```cpp
template<class T>
tex2DLod(cudaTextureObject_t texObj, float x, float y, float level, bool* isResident);
```

## Parameters

- **texObj**: The two-dimensional texture object specifying the CUDA array.
- **x**: The x-coordinate of the texture coordinate.
- **y**: The y-coordinate of the texture coordinate.
- **level**: The level-of-detail (LOD) at which to fetch the texel.
- **isResident**: A pointer to a boolean value that indicates whether the fetched texel is resident in memory.

## Behavior

The function fetches the texel value from the CUDA array at the specified texture coordinates `(x, y)` and level-of-detail `level` [CUDA_C_Programming_Guide:L7174-L7182].

For sparse CUDA arrays, the function also returns the residency status of the texel via the `isResident` pointer [CUDA_C_Programming_Guide:L7174-L7182]. If the texel is not resident in memory, the function returns zeros for the fetched values [CUDA_C_Programming_Guide:L7174-L7182].

## See Also

- `tex2D` for standard 2D texture fetches.
- Sparse CUDA Arrays documentation for details on memory residency and paging.
