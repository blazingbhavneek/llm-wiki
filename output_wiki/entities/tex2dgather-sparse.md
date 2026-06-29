# tex2Dgather (Sparse CUDA Arrays)

The `tex2Dgather` function provides gather semantics for 2D texture objects bound to sparse CUDA arrays, allowing applications to query the residency status of texels during fetch operations.

## Function Signature

```cpp
template<class T>
tex2Dgather(cudaTextureObject_t texObj,
    float x, float y, bool* isResident, int comp = 0);
```

## Parameters

- **texObj**: The 2D texture object specifying the CUDA array to fetch from.
- **x**: The texture coordinate in the x direction.
- **y**: The texture coordinate in the y direction.
- **isResident**: A pointer to a boolean value that indicates whether the texel is resident in memory.
- **comp**: The component parameter, described in the context of Texture Gather operations.

## Behavior

The function fetches data from the CUDA array specified by `texObj` using the provided texture coordinates `x` and `y`, along with the `comp` parameter, following the standard Texture Gather semantics [CUDA_C_Programming_Guide:L7135-L7144].

Additionally, it returns the residency status of the texel via the `isResident` pointer [CUDA_C_Programming_Guide:L7135-L7144]. If the texel is not resident in memory, the values fetched will be zeros [CUDA_C_Programming_Guide:L7135-L7144].

## See Also

- Texture Gather
- Sparse CUDA Arrays
