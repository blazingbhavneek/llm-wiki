# texCubemap

The `texCubemap` function is used to fetch data from a cubemap texture object. It retrieves values from the CUDA array specified by the texture object using 3D texture coordinates.

## Syntax

```cpp
template<class T>
T texCubemap(cudaTextureObject_t texObj, float x, float y, float z);
```

## Parameters

- **texObj**: The cubemap texture object from which to fetch the data.
- **x**: The x-component of the texture coordinate.
- **y**: The y-component of the texture coordinate.
- **z**: The z-component of the texture coordinate.

## Description

This function fetches the CUDA array specified by the cubemap texture object `texObj` using the texture coordinate `(x, y, z)`. The behavior and interpretation of these coordinates are defined according to the specifications for Cubemap Textures [CUDA_C_Programming_Guide:L7328-L7336].

## See Also

- Cubemap Textures
