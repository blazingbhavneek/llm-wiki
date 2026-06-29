# texCubemapLayeredLod

The `texCubemapLayeredLod` function fetches data from a cubemap layered texture object using specific texture coordinates, a layer index, and a level-of-detail value.

## Function Signature

```cpp
template<class T>
T texCubemapLayeredLod(cudaTextureObject_t texObj, float x, float y, float z,
                   int layer, float level);
```

## Parameters

- `texObj`: The cubemap layered texture object specifying the CUDA array to fetch from.
- `x`, `y`, `z`: The texture coordinates used for the fetch operation.
- `layer`: The index of the layer within the cubemap layered texture.
- `level`: The level-of-detail (LOD) at which to perform the fetch.

## Description

This function retrieves a value of type `T` from the CUDA array specified by `texObj`. It uses the provided texture coordinates `(x, y, z)` and the `layer` index to identify the specific location within the cubemap layered texture, as described in the documentation for Cubemap Layered Textures. The fetch is performed at the specified `level` of detail.

## References

- [CUDA_C_Programming_Guide:L7377-L7386]
