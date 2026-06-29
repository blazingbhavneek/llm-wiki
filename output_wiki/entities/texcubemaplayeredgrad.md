# texCubemapLayeredGrad

The `texCubemapLayeredGrad` function fetches data from a cubemap layered texture object, using texture coordinates and layer index, with the level-of-detail (LOD) derived from provided spatial gradients.

## Function Signature

```cpp
template<class T>
T texCubemapLayeredGrad(cudaTextureObject_t texObj, float x, float y, float z,
                   int layer, float4 dx, float4 dy);
```

## Parameters

- **texObj**: The cubemap layered texture object specifying the CUDA array to fetch from.
- **x, y, z**: The texture coordinates used for the fetch operation.
- **layer**: The index of the layer within the cubemap layered texture.
- **dx**: A `float4` structure containing the partial derivatives with respect to x.
- **dy**: A `float4` structure containing the partial derivatives with respect to y.

## Description

This function retrieves a value of type `T` from the specified `texObj` at the given texture coordinates `(x, y, z)` and `layer`. The level-of-detail (LOD) for the texture fetch is automatically derived from the gradient information provided in `dx` and `dy` [CUDA_C_Programming_Guide:L7367-L7376]. This allows for efficient mipmap selection based on the rate of change of the texture coordinates across the screen or compute grid.

## See Also

- Cubemap Layered Textures
- `texCubemapLayered`
