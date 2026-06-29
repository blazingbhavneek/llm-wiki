# tex1DLayeredLod

`tex1DLayeredLod` is a CUDA texture fetch function designed for one-dimensional layered textures. It retrieves data from a specified layer and level-of-detail within a CUDA array texture object.

## Function Signature

```cpp
template<class T>
T tex1DLayeredLod(cudaTextureObject_t texObj, float x, int layer, float level);
```

## Parameters

- **texObj**: The texture object specifying the CUDA array.
- **x**: The texture coordinate used for the fetch.
- **layer**: The specific layer index within the layered texture to access.
- **level**: The level-of-detail (LOD) index to use for the fetch.

## Description

The function fetches data from the one-dimensional layered texture specified by `texObj`. It uses the texture coordinate `x`, accesses the layer specified by `layer`, and samples at the level-of-detail specified by `level` [CUDA_C_Programming_Guide:L7249-L7257].

## Related Functions

- `tex1DLayered`: Fetches from a 1D layered texture using the default level-of-detail.
- `tex1DLayeredLod`: Allows explicit specification of the level-of-detail.

## See Also

- CUDA Texture Objects
- One-Dimensional Layered Textures
