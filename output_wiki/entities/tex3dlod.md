# tex3DLod

The `tex3DLod` function fetches data from a three-dimensional texture object at a specified level-of-detail.

## Signature

```cpp
template<class T>
T tex3DLod(cudaTextureObject_t texObj, float x, float y, float z, float level);
```

## Description

This function retrieves values from the CUDA array or the region of linear memory specified by the three-dimensional texture object `texObj`. It uses the texture coordinates `(x, y, z)` and samples the data at the specific `level` of detail [CUDA_C_Programming_Guide:L7201-L7209].

## Parameters

- **texObj**: The three-dimensional texture object from which to fetch data.
- **x**: The x-component of the texture coordinate.
- **y**: The y-component of the texture coordinate.
- **z**: The z-component of the texture coordinate.
- **level**: The level-of-detail index to sample from.

## Return Value

The function returns a value of type `T`, representing the fetched texel data [CUDA_C_Programming_Guide:L7201-L7209].
