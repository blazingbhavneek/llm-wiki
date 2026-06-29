# tex2DLayeredLod

## Overview

`tex2DLayeredLod` is a CUDA texture fetch function designed for two-dimensional layered textures. It retrieves data from a specific layer within a CUDA array texture object at a given texture coordinate and level of detail.

## Function Signature

```cpp
template<class T>
T tex2DLayeredLod(cudaTextureObject_t texObj, float x, float y, int layer,
                   float level);
```

## Parameters

- **texObj**: The texture object specifying the CUDA array.
- **x**: The x-component of the texture coordinate.
- **y**: The y-component of the texture coordinate.
- **layer**: The index of the layer within the layered texture to fetch from.
- **level**: The level-of-detail (LOD) index to use for the fetch.

## Description

This function fetches from the CUDA array specified by the two-dimensional layered texture at `layer` using texture coordinate `(x,y)` and the specified level of detail `level` [CUDA_C_Programming_Guide:L7288-L7297].

## See Also

- `tex2DLayered`
- `tex2D`
- `tex2DLod`
