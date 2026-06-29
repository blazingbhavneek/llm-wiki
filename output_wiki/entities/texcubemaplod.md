# texCubemapLod

The `texCubemapLod` function fetches data from a CUDA array specified by a cubemap texture object. It retrieves the value using 3D texture coordinates `(x, y, z)` and a specific level-of-detail.

## Syntax

```cpp
template<class T>
T texCubemapLod(cudaTextureObject_t texObj, float x, float y, float z, float level);
```

## Parameters

- **texObj**: The cubemap texture object specifying the CUDA array to fetch from.
- **x, y, z**: The texture coordinates used for the fetch, as described in the context of Cubemap Textures.
- **level**: The specific level-of-detail (LOD) to use for the fetch operation.

## Description

This function is part of the CUDA Texture Object API (Section 10.8.1.30). It allows for explicit control over the level-of-detail when sampling from a cubemap texture, which is useful for applications requiring specific LOD levels rather than hardware-generated mipmaps.

## References

- [CUDA_C_Programming_Guide:L7347-L7356]
