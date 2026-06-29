# tex3DGrad

`tex3DGrad` is a CUDA texture fetch function that retrieves data from a three-dimensional texture object. It allows for explicit control over the level-of-detail (LOD) calculation by accepting gradient information.

## Function Signature

```cpp
template<class T>
T tex3DGrad(cudaTextureObject_t texObj, float x, float y, float z,
                   float4 dx, float4 dy);
```

## Parameters

- **texObj**: The three-dimensional texture object specifying the CUDA array to fetch from.
- **x, y, z**: The texture coordinates used for the fetch.
- **dx**: The X gradient, provided as a `float4`.
- **dy**: The Y gradient, provided as a `float4`.

## Description

The function fetches from the CUDA array specified by `texObj` using the texture coordinate `(x, y, z)`. The level-of-detail is derived from the provided X and Y gradients (`dx` and `dy`) rather than being computed automatically from the coordinates [CUDA_C_Programming_Guide:L7220-L7229].

## Related Functions

- `tex3D`: Standard 3D texture fetch with automatic LOD computation.
- `tex3DGrad`: 3D texture fetch with explicit gradient-based LOD.
- `tex3DGrad`: 3D texture fetch with explicit gradient-based LOD.

## See Also

- CUDA C++ Programming Guide, Section 10.8.1.17
