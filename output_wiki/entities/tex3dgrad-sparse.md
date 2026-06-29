# tex3DGrad (Sparse CUDA Arrays)

The `tex3DGrad` function is a specialized texture fetch operation designed for sparse CUDA arrays. It retrieves data from a three-dimensional texture object using texture coordinates while accounting for spatial gradients to determine the level-of-detail (LOD).

## Function Signature

```cpp
template<class T>
T tex3DGrad(cudaTextureObject_t texObj, float x, float y, float z,
    float4 dx, float4 dy, bool* isResident);
```

## Parameters

- **texObj**: The three-dimensional texture object specifying the CUDA array to fetch from.
- **x, y, z**: The texture coordinates for the fetch operation.
- **dx**: A `float4` structure containing the X gradient information. This is used to derive the level-of-detail.
- **dy**: A `float4` structure containing the Y gradient information. This is also used to derive the level-of-detail.
- **isResident**: A pointer to a boolean value. Upon return, this indicates whether the fetched texel is resident in memory.

## Behavior

The function fetches the value from the CUDA array at the specified `(x, y, z)` coordinates. The level-of-detail (LOD) for the fetch is derived from the provided X and Y gradients (`dx` and `dy`).

Because this operation targets sparse CUDA arrays, residency is not guaranteed. The function returns the resident status via the `isResident` pointer. If the texel is not resident in memory, the function returns zeros for the fetched value [CUDA_C_Programming_Guide:L7230-L7239].
