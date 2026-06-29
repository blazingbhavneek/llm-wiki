# tex2DLod

The `tex2DLod` function fetches data from a two-dimensional texture object at a specified level-of-detail.

## Syntax

```cpp
template<class T>
tex2DLod(cudaTextureObject_t texObj, float x, float y, float level);
```

## Description

This function retrieves values from the CUDA array or the region of linear memory specified by the two-dimensional texture object `texObj`. It uses the texture coordinates `(x, y)` and samples the data at the specific `level-of-detail` provided by the `level` parameter [CUDA_C_Programming_Guide:L7165-L7173].
