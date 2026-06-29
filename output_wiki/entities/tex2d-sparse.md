# tex2D (Sparse CUDA Arrays)

The `tex2D` function provides a specialized interface for fetching data from sparse CUDA arrays using a two-dimensional texture object. This variant allows the caller to determine whether the requested texel is currently resident in memory.

## Function Signature

```cpp
template<class T>
T tex2D(cudaTextureObject_t texObj, float x, float y, bool* isResident);
```

## Parameters

- **texObj**: The two-dimensional texture object specifying the CUDA array to fetch from.
- **x**: The x-coordinate of the texture fetch.
- **y**: The y-coordinate of the texture fetch.
- **isResident**: A pointer to a boolean value that indicates whether the texel at the specified coordinates is resident in memory.

## Behavior

The function fetches the value from the CUDA array specified by `texObj` using the texture coordinates `(x, y)`. 

- If the texel is resident in memory, the function returns the actual texel value.
- If the texel is **not** resident in memory, the function returns `0` (zeros). In this case, the `isResident` pointer is set to `false`.

This behavior allows applications to handle sparse data structures where not all texels are loaded into memory simultaneously, enabling efficient processing of large datasets that exceed available GPU memory.

## References

- [CUDA_C_Programming_Guide:L7116-L7124]
