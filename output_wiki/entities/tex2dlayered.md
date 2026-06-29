# tex2DLayered

The `tex2DLayered` function fetches data from a CUDA array specified by a two-dimensional texture object. It utilizes texture coordinates (x, y) and a specific layer index to retrieve the value.

## Signature

```cpp
template<class T>
T tex2DLayered(cudaTextureObject_t texObj,
               float x, float y, int layer);
```

## Parameters

- **texObj**: The two-dimensional texture object specifying the CUDA array.
- **x**: The x-component of the texture coordinate.
- **y**: The y-component of the texture coordinate.
- **layer**: The index of the layer within the layered texture.

## Description

This function is used to access data from layered textures, as described in the Layered Textures section of the CUDA documentation. It allows for sampling from a specific slice (layer) of a 2D texture array at the given coordinates.

## References

- [CUDA_C_Programming_Guide:L7268-L7277]
