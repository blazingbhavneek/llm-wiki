# tex2DLayered (Sparse CUDA Arrays)

The `tex2DLayered` function is a specialized texture fetch operation designed for sparse CUDA arrays. It retrieves data from a two-dimensional layered texture object and provides information regarding the memory residency of the requested texel.

## Function Signature

```cpp
template<class T>
T tex2DLayered(cudaTextureObject_t texObj,
        float x, float y, int layer, bool* isResident);
```

## Parameters

- **texObj**: The two-dimensional texture object specifying the CUDA array to fetch from.
- **x**: The x-coordinate of the texture fetch.
- **y**: The y-coordinate of the texture fetch.
- **layer**: The index of the layer within the layered texture.
- **isResident**: A pointer to a boolean value. Upon return, this indicates whether the fetched texel is resident in memory.

## Behavior

The function fetches the texel value at coordinates `(x, y)` and the specified `layer` index from the texture object `texObj`, adhering to the rules defined for layered textures [CUDA_C_Programming_Guide:L7278-L7287].

### Residency Handling

A key feature of this function in the context of sparse arrays is the `isResident` output parameter. It returns `true` if the texel is resident in memory, and `false` otherwise [CUDA_C_Programming_Guide:L7278-L7287].

If the texel is not resident (i.e., `isResident` is set to `false`), the function returns zero values for the fetched data [CUDA_C_Programming_Guide:L7278-L7287]. This allows applications to handle non-resident pages gracefully without triggering hardware page faults during the texture fetch operation itself.

## See Also

- Layered Textures
- Sparse CUDA Arrays
