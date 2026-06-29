# tex2DGrad

The `tex2DGrad` function fetches data from a two-dimensional texture object specified by `texObj` using texture coordinates `(x, y)`. The level-of-detail (LOD) for the texture fetch is derived from the provided `dx` and `dy` gradients.

## Syntax

```cpp
template<class T>
T tex2DGrad(cudaTextureObject_t texObj, float x, float y,
                   float2 dx, float2 dy);
```

## Parameters

- **texObj**: The two-dimensional texture object from which to fetch data.
- **x**: The x-component of the texture coordinate.
- **y**: The y-component of the texture coordinate.
- **dx**: The gradient of the texture coordinate with respect to the x-axis (typically computed as `dx/dx_screen`).
- **dy**: The gradient of the texture coordinate with respect to the y-axis (typically computed as `dy/dy_screen`).

## Description

This function is used in CUDA programming to perform texture fetches where the level-of-detail is explicitly controlled by the caller-provided gradients rather than being automatically calculated by the hardware based on screen-space derivatives. This allows for more precise control over texture filtering and mipmapping behavior in specific rendering scenarios.

## References

- [CUDA_C_Programming_Guide:L7145-L7154]
