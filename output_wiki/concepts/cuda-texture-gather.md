# Texture Gather

Details the tex2Dgather() function for 2D textures, which returns four 32-bit values for a specific component from the four texels used in bilinear filtering. Covers 8-bit fractional precision limitations, cudaArrayTextureGather flag requirements, size limits, and compute capability 2.0+ requirement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3863-L3872

Citation: [CUDA_C_Programming_Guide:L3863-L3872]

````text
## 6.2.14.1.6 Texture Gather

Texture gather is a special texture fetch that is available for two-dimensional textures only. It is performed by the tex2Dgather() function, which has the same parameters as tex2D(), plus an additional comp parameter equal to 0, 1, 2, or 3 (see tex2Dgather()). It returns four 32-bit numbers that correspond to the value of the component comp of each of the four texels that would have been used for bilinear filtering during a regular texture fetch. For example, if these texels are of values (253, 20, 31, 255), (250, 25, 29, 254), (249, 16, 37, 253), (251, 22, 30, 250), and comp is 2, tex2Dgather() returns (31, 29, 37, 30).

Note that texture coordinates are computed with only 8 bits of fractional precision. tex2Dgather() may therefore return unexpected results for cases where tex2D() would use 1.0 for one of its weights (fi or fi, see Linear Filtering). For example, with an x texture coordinate of 2.49805: xB=x-0.5=1.99805, however the fractional part of xB is stored in an 8-bit fixed-point format. Since 0.99805 is closer to 256.f/256.f than it is to 255.f/256.f, xB has the value 2. A tex2Dgather() in this case would therefore return indices 2 and 3 in x, instead of indices 1 and 2.

Texture gather is only supported for CUDA arrays created with the cudaArrayTextureGather flag and of width and height less than the maximum specified in Table 27 for texture gather, which is smaller than for regular texture fetch.

Texture gather is only supported on devices of compute capability 2.0 and higher.
````
