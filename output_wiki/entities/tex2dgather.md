# tex2Dgather

## Overview

`tex2Dgather` is a CUDA texture function that fetches multiple values from a 2D texture object using gather semantics. It operates on a CUDA array specified by a 2D texture object.

## Syntax

```cpp
template<class T>
T tex2Dgather(cudaTextureObject_t texObj,
               float x, float y, int comp = 0);
```

## Parameters

- **texObj**: The 2D texture object from which to fetch data.
- **x**: The texture coordinate in the x direction.
- **y**: The texture coordinate in the y direction.
- **comp**: The component parameter, as described in the Texture Gather documentation. Defaults to 0.

## Description

The function fetches data from the CUDA array specified by `texObj` using the provided texture coordinates `x` and `y`, along with the `comp` parameter. The specific behavior regarding the gather operation is detailed in the Texture Gather section of the CUDA C Programming Guide.

## References

- [CUDA_C_Programming_Guide:L7125-L7134]
