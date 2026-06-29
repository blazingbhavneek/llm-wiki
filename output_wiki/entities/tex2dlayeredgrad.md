# tex2DLayeredGrad

`tex2DLayeredGrad` is a CUDA texture fetch function that retrieves data from a two-dimensional layered texture array. It allows the programmer to specify the level-of-detail (LOD) explicitly through gradient information rather than relying on automatic LOD calculation based on texture coordinates.

## Function Signature

```cpp
template<class T>
T tex2DLayeredGrad(cudaTextureObject_t texObj, float x, float y, int layer,
                   float2 dx, float2 dy);
```

## Parameters

*   **texObj**: The texture object specifying the CUDA array and texture parameters.
*   **x**: The x-component of the texture coordinate.
*   **y**: The y-component of the texture coordinate.
*   **layer**: The index of the layer within the layered texture to fetch from.
*   **dx**: A `float2` structure containing the partial derivatives of the texture coordinates with respect to the screen-space x-coordinate ($\frac{dx}{dx_{screen}}$). These are used to determine the LOD.
*   **dy**: A `float2` structure containing the partial derivatives of the texture coordinates with respect to the screen-space y-coordinate ($\frac{dy}{dy_{screen}}$). These are used to determine the LOD.

## Description

The function fetches the texel value from the specified `layer` of the texture array at the normalized texture coordinates `(x, y)`. Unlike `tex2DLayered`, which uses the texture coordinates to automatically compute the LOD, `tex2DLayeredGrad` uses the provided `dx` and `dy` gradients to calculate the LOD. This provides finer control over mipmap selection, which is particularly useful in custom shading algorithms or when performing operations where the standard derivative calculation is insufficient or incorrect.

The return type `T` is determined by the texture object's format and the template instantiation.

## References

*   CUDA C Programming Guide, Section 10.8.1.26 [CUDA_C_Programming_Guide:L7308-L7317]
