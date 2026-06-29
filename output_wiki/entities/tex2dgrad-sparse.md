# tex2DGrad (Sparse CUDA Arrays)

The `tex2DGrad` function is designed for fetching data from sparse CUDA arrays via a two-dimensional texture object. It allows for explicit control over the level-of-detail (LOD) calculation using gradient information.

## Function Signature

```cpp
template<class T>
tex2DGrad(cudaTextureObject_t texObj, float x, float y,
    float2 dx, float2 dy, bool* isResident);
```

## Parameters

- **texObj**: The two-dimensional texture object specifying the CUDA array to fetch from.
- **x, y**: The texture coordinates used for the fetch operation.
- **dx, dy**: Gradient vectors (`float2`) used to derive the level-of-detail for texture filtering.
- **isResident**: A pointer to a boolean value that indicates whether the fetched texel is resident in memory.

## Behavior

The function fetches the texel value at the specified texture coordinates `(x, y)` from the CUDA array associated with `texObj`. The level-of-detail for the texture lookup is derived from the provided gradient vectors `dx` and `dy`.

Because the underlying array is sparse, the function also reports the residency status of the requested texel via the `isResident` output parameter:

- If the texel is resident in memory, `*isResident` is set to `true`.
- If the texel is not resident, `*isResident` is set to `false`, and the function returns zero values for the fetched data [CUDA_C_Programming_Guide:L7155-L7164].

## Usage Context

This function is part of the CUDA C Programming Guide's section on texture object functions for sparse arrays (Section 10.8.1.10). It is particularly useful when working with sparse textures where memory residency is not guaranteed, allowing applications to handle missing data explicitly rather than relying on default padding or error states. The explicit gradient parameters allow for more precise control over mipmapping and filtering behavior compared to functions that compute gradients internally.
