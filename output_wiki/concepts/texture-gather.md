# Texture Gather

Texture gather is a special texture fetch operation available only for two-dimensional textures. It is performed using the `tex2Dgather()` function, which allows a kernel to retrieve the values of four specific components from the four texels that would normally be used for bilinear filtering in a standard texture fetch.

## Functionality

The `tex2Dgather()` function accepts the same parameters as `tex2D()`, plus an additional `comp` parameter that specifies which component (0, 1, 2, or 3) to gather from each texel. The function returns four 32-bit numbers, each corresponding to the value of the specified component from one of the four surrounding texels.

For example, if the four texels involved in the filter have values `(253, 20, 31, 255)`, `(250, 25, 29, 254)`, `(249, 16, 37, 253)`, and `(251, 22, 30, 250)`, and the `comp` parameter is set to 2, `tex2Dgather()` returns the vector `(31, 29, 37, 30)` [CUDA_C_Programming_Guide:L3862-L3871].

## Precision Limitations

Texture coordinates for texture gather are computed with only 8 bits of fractional precision. This limited precision can lead to unexpected results compared to standard `tex2D()` operations, particularly in cases where `tex2D()` would assign a weight of 1.0 to a texel (i.e., when the fractional part of the coordinate is exactly 0 or 1) [CUDA_C_Programming_Guide:L3862-L3871].

For instance, consider an x texture coordinate of 2.49805:
1. The base index calculation involves `xB = x - 0.5`, resulting in 1.99805.
2. The fractional part of `xB` is stored in an 8-bit fixed-point format.
3. Since 0.99805 is closer to `256.f/256.f` (which equals 1.0) than to `255.f/256.f`, the value rounds up, causing `xB` to effectively become 2.
4. Consequently, `tex2Dgather()` would return indices 2 and 3 in the x-dimension, whereas `tex2D()` might have used indices 1 and 2 depending on the exact filtering logic [CUDA_C_Programming_Guide:L3862-L3871].

## Requirements and Support

Texture gather is subject to specific hardware and memory configuration requirements:

*   **Compute Capability**: It is only supported on devices with compute capability 2.0 and higher [CUDA_C_Programming_Guide:L3862-L3871].
*   **Memory Flags**: CUDA arrays used for texture gather must be created with the `cudaArrayTextureGather` flag [CUDA_C_Programming_Guide:L3862-L3871].
*   **Dimensions**: The width and height of the texture array must be less than the maximum specified for texture gather, which is smaller than the maximum allowed for regular texture fetches [CUDA_C_Programming_Guide:L3862-L3871].

## See Also

*   `tex2D()`
*   `cudaArrayTextureGather`
*   Linear Filtering
