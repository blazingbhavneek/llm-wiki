# tex1D

The `tex1D` function is used to fetch data from a one-dimensional CUDA array texture object.

## Signature

```cpp
template<class T>
tex1D(cudaTextureObject_t texObj, float x);
```

## Description

This function fetches from the CUDA array specified by the one-dimensional texture object `texObj` using the texture coordinate `x` [CUDA_C_Programming_Guide:L7080-L7088]. The template parameter `T` specifies the type of the value to be returned.

## Parameters

- **texObj**: A texture object of type `cudaTextureObject_t` that defines the one-dimensional texture resource.
- **x**: The texture coordinate used to fetch the data. This is a floating-point value.

## See Also

- `tex1Dfetch`
- `tex1D` (legacy API)
- CUDA Texture Objects
