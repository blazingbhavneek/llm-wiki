# texCubemapGrad

`texCubemapGrad` is a CUDA texture fetch function that retrieves data from a cubemap texture object using explicit partial derivatives to determine the level of detail (LOD).

## Syntax

```cpp
template<class T>
T texCubemapGrad(cudaTextureObject_t texObj, float x, float y, float z,
                 float4 dx, float4 dy);
```

## Description

The function fetches from the CUDA array specified by the cubemap texture object `texObj` using the texture coordinate `(x, y, z)` as described in Cubemap Textures. The level-of-detail used is derived from the `dx` and `dy` gradients [CUDA_C_Programming_Guide:L7337-L7346].

## Parameters

- **texObj**: The cubemap texture object from which to fetch.
- **x, y, z**: The texture coordinates for the fetch.
- **dx**: The partial derivatives with respect to the screen-space x-coordinate.
- **dy**: The partial derivatives with respect to the screen-space y-coordinate.
