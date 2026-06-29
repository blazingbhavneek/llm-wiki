# tex3D

The `tex3D` function is used to fetch data from a three-dimensional texture object in CUDA. It retrieves values from a CUDA array specified by the texture object using three-dimensional texture coordinates.

## Syntax

```cpp
template<class T>
T tex3D(cudaTextureObject_t texObj, float x, float y, float z);
```

## Parameters

- **texObj**: The three-dimensional texture object from which to fetch data.
- **x**: The x-coordinate of the texture fetch.
- **y**: The y-coordinate of the texture fetch.
- **z**: The z-coordinate of the texture fetch.

## Description

The function fetches from the CUDA array specified by the three-dimensional texture object `texObj` using texture coordinate `(x,y,z)` [CUDA_C_Programming_Guide:L7183-L7191].

## See Also

- `tex2D`
- `tex1D`
- `cudaTextureObject_t`
