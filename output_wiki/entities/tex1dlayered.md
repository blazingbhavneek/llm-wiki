# tex1DLayered

`tex1DLayered` is a CUDA texture fetch function used to retrieve data from a one-dimensional layered texture object.

## Syntax

```cpp
template<class T>
tex1DLayered(cudaTextureObject_t texObj, float x, int layer);
```

## Description

The function fetches from the CUDA array specified by the one-dimensional texture object `texObj` using the texture coordinate `x` and the layer index `layer` [CUDA_C_Programming_Guide:L7240-L7248]. This operation is described in the context of Layered Textures [CUDA_C_Programming_Guide:L7240-L7248].

## Parameters

- **texObj**: The one-dimensional texture object from which to fetch data.
- **x**: The texture coordinate used for the fetch.
- **layer**: The index of the layer within the layered texture object.
