# texCubemapLayered

The `texCubemapLayered` function fetches data from a CUDA array specified by a cubemap layered texture object. It retrieves values using 3D texture coordinates and a specific layer index.

## Signature

```cpp
template<class T>
T texCubemapLayered(cudaTextureObject_t texObj,
                   float x, float y, float z, int layer);
```

## Parameters

- **texObj**: The cubemap layered texture object specifying the CUDA array to fetch from.
- **x, y, z**: The texture coordinates used for the fetch operation.
- **layer**: The index of the layer within the cubemap layered texture.

## Description

This function operates on cubemap layered textures, allowing access to specific layers within a layered texture array. The coordinates (x, y, z) are used to sample the texture, and the `layer` parameter selects the specific face or layer within the cubemap structure. For detailed behavior regarding coordinate handling and layer indexing, refer to the documentation on Cubemap Layered Textures [CUDA_C_Programming_Guide:L7357-L7366].

## See Also

- Cubemap Layered Textures
