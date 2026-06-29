# tex1DGrad

The `tex1DGrad` function is used to fetch data from a one-dimensional CUDA texture object. It retrieves the value at a specified texture coordinate while calculating the appropriate level-of-detail based on provided gradient information.

## Syntax

```cpp
template<class T>
tex1DGrad(cudaTextureObject_t texObj, float x, float dx, float dy);
```

## Parameters

- **texObj**: The one-dimensional texture object from which to fetch data.
- **x**: The texture coordinate used for the fetch.
- **dx**: The X-gradient used to derive the level-of-detail.
- **dy**: The Y-gradient used to derive the level-of-detail.

## Description

This function fetches from the CUDA array specified by the one-dimensional texture object `texObj` using the texture coordinate `x`. The level-of-detail for the texture lookup is derived from the X-gradient `dx` and the Y-gradient `dy` [CUDA_C_Programming_Guide:L7098-L7106].

## See Also

- `tex1D`
