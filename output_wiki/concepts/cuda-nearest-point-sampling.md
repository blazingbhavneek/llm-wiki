# CUDA Nearest-Point Sampling

Nearest-point sampling is a filtering mode used in CUDA texture fetches where the returned value is determined by the integer part of the texture coordinates. This mode effectively maps continuous texture coordinates to the nearest discrete texel based on the floor function.

## Mathematical Definition

In this filtering mode, the value returned by the texture fetch is defined as follows [CUDA_C_Programming_Guide:L19379-L19397]:

- For a one-dimensional texture: `tex(x) = T[i]`
- For a two-dimensional texture: `tex(x,y) = T[i,j]`
- For a three-dimensional texture: `tex(x,y,z) = T[i,j,k]`

Where the indices are calculated using the floor of the coordinates [CUDA_C_Programming_Guide:L19379-L19397]:

- `i = floor(x)`
- `j = floor(y)`
- `k = floor(z)`

## Integer Texture Remapping

For integer textures, the value returned by the texture fetch can be optionally remapped to the range `[0.0, 1.0]` [CUDA_C_Programming_Guide:L19379-L19397].

## Visual Representation

The behavior of nearest-point sampling is illustrated for a one-dimensional texture with `N=4` in Figure 36 of the CUDA C Programming Guide [CUDA_C_Programming_Guide:L19379-L19397].

![Nearest-Point Sampling Filtering Mode](images/ad3287b3c5908ab2171c292f030ef07b01561b84fe6190e0b4bcf05ca38fff94.jpg)

*Figure 36: Nearest-Point Sampling Filtering Mode* [CUDA_C_Programming_Guide:L19379-L19397]
