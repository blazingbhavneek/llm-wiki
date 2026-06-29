# tex2D

The `tex2D` function is used to fetch data from a two-dimensional texture object. It operates on either a CUDA array or a region of linear memory specified by the texture object.

## Syntax

```cpp
template<class T>
T tex2D(cudaTextureObject_t texObj, float x, float y);
```

## Parameters

- **texObj**: The two-dimensional texture object from which to fetch data.
- **x**: The x-coordinate of the texture coordinate.
- **y**: The y-coordinate of the texture coordinate.

## Description

The function fetches a value of type `T` from the texture object `texObj` using the provided texture coordinates `(x, y)`. The texture object defines the underlying storage, which can be either a CUDA array or linear memory. The coordinates are interpreted according to the texture object's configuration, including address modes and filtering modes.

## References

- [CUDA_C_Programming_Guide:L7107-L7115]
