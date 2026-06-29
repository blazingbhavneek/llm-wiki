# tex1DLod

The `tex1DLod` function fetches data from a one-dimensional texture object at a specified level-of-detail.

## Syntax

```cpp
template<class T>
T tex1DLod(cudaTextureObject_t texObj, float x, float level);
```

## Parameters

- **texObj**: The one-dimensional texture object from which to fetch data.
- **x**: The texture coordinate used for the fetch.
- **level**: The level-of-detail index.

## Description

This function retrieves a value from the CUDA array specified by the texture object `texObj` using the texture coordinate `x` at the specified level-of-detail `level` [CUDA_C_Programming_Guide:L7089-L7097].

## See Also

- `tex1D`
- `tex1Dfetch`
- `tex2D`
- `tex3D`
