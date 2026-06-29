# tex1DLayeredGrad

## Overview

`tex1DLayeredGrad` is a CUDA texture fetch function that retrieves data from a one-dimensional layered texture. It allows for explicit control over the level-of-detail (LOD) by accepting gradient parameters.

## Function Signature

```cpp
template<class T>
T tex1DLayeredGrad(cudaTextureObject_t texObj, float x, int layer,
                   float dx, float dy);
```

## Parameters

- **texObj**: The texture object specifying the CUDA array.
- **x**: The texture coordinate for the fetch.
- **layer**: The specific layer within the layered texture to access.
- **dx**: The gradient in the x direction, used to derive the level-of-detail.
- **dy**: The gradient in the y direction, used to derive the level-of-detail.

## Description

This function fetches from the CUDA array specified by the one-dimensional layered texture at the specified `layer` using the texture coordinate `x`. The level-of-detail is derived from the provided `dx` and `dy` gradients [CUDA_C_Programming_Guide:L7258-L7267].

## Related

- `tex1DLayered`: Standard layered texture fetch without explicit LOD control.
- `tex1DGrad`: 1D texture fetch with explicit LOD control but without layering.
