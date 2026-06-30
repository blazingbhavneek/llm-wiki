# Texture Fetching

Explains texture coordinate systems, nearest-point sampling, linear filtering formulas for 1D/2D/3D textures, and table lookup implementations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19363-L19437

Citation: [CUDA_C_Programming_Guide:L19363-L19437]

````text
## Chapter 19. Texture Fetching

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

This section gives the formula used to compute the value returned by the texture functions of Texture Functions depending on the various attributes of the texture object (see Texture and Surface Memory).

The texture bound to the texture object is represented as an array T of

▶ N texels for a one-dimensional texture,

N x M texels for a two-dimensional texture,

▶ N x M x L texels for a three-dimensional texture.

It is fetched using non-normalized texture coordinates x, y, and z, or the normalized texture coordinates x/N, y/M, and z/L as described in Texture Memory. In this section, the coordinates are assumed to be in the valid range. Texture Memory explained how out-of-range coordinates are remapped to the valid range based on the addressing mode.

## 19.1. Nearest-Point Sampling

In this filtering mode, the value returned by the texture fetch is

▶ tex(x)=T[i] for a one-dimensional texture,

▶ tex(x,y)=T[i,j] for a two-dimensional texture,

▶ tex(x,y,z)=T[i,j,k] for a three-dimensional texture,

where i=floor(x), j=floor(y), and k=floor(z).

Figure 36 illustrates nearest-point sampling for a one-dimensional texture with N=4.

For integer textures, the value returned by the texture fetch can be optionally remapped to [0.0, 1.0] (see Texture Memory).

![](images/ad3287b3c5908ab2171c292f030ef07b01561b84fe6190e0b4bcf05ca38fff94.jpg)  
Figure 36: Nearest-Point Sampling Filtering Mode

## 19.2. Linear Filtering

In this filtering mode, which is only available for floating-point textures, the value returned by the texture fetch is

▶ $t e x ( x ) = ( 1 - \alpha ) T [ i ] + \alpha T [ i + 1 ]$ for a one-dimensional texture,

▶ $t e x ( x ) = ( 1 - \alpha ) T [ i ] + \alpha T [ i + 1 ]$ for a one-dimensional texture,

▶ $\begin{array} { r } { \varepsilon x ( x , y ) = ( 1 - \alpha ) ( 1 - \beta ) T [ i , j ] + \alpha ( 1 - \beta ) T [ i + 1 , j ] + ( 1 - \alpha ) \beta T [ i , j + 1 ] + \alpha \beta T [ i + 1 , j + 1 ] } \end{array}$ for a two-dimensional texture,

▶ tex(x, y, z) =

$$
\begin{array}{l} (1 - \alpha) (1 - \beta) (1 - \gamma) T [ i, j, k ] + \alpha (1 - \beta) (1 - \gamma) T [ i + 1, j, k ] + \\ (1 - \alpha) \beta (1 - \gamma) T [ i, j + 1, k ] + \alpha \beta (1 - \gamma) T [ i + 1, j + 1, k ] + \\ (1 - \alpha) (1 - \beta) \gamma T [ i, j, k + 1 ] + \alpha (1 - \beta) \gamma T [ i + 1, j, k + 1 ] + \\ (1 - \alpha) \beta \gamma T [ i, j + 1, k + 1 ] + \alpha \beta \gamma T [ i + 1, j + 1, k + 1 ] \end{array}
$$

for a three-dimensional texture,

where:

$$
\begin{array}{l} \blacktriangleright i = f l o o r (x B) *, \alpha = f r a c (x B) *, * x B = x - 0. 5, \\ \blacktriangleright j = f l o o r (y B) *, \beta = f r a c (y B) *, * y B = y - 0. 5, \\ \blacktriangleright k = f l o o r (z B) *, \gamma = f r a c (z B) *, * z B = z - 0. 5, \end{array}
$$

$\alpha , \beta ,$ and γ are stored in 9-bit fixed point format with 8 bits of fractional value (so 1.0 is exactly represented).

Figure 37 illustrates linear filtering of a one-dimensional texture with $N { = } 4 .$

![](images/1e8abd5f7d3dd35ce4932a9ca9bfe7b911ae56cd533b031aa567099c245b397f.jpg)  
Figure 37: Linear Filtering Mode

## 19.3. Table Lookup

A table lookup TL(x) where x spans the interval [0,R] can be implemented as $T L ( x ) { = } t e x ( ( N - l ) / R ) x { + } 0 . 5 )$ in order to ensure that $T L ( O ) = T [ O ]$ and $T L ( R ) { = } T [ N { - } l ]$

Figure 38 illustrates the use of texture filtering to implement a table lookup with R=4 or R=1 from a one-dimensional texture with N=4.

![](images/89e823f2e9056596055c9a6244f7035950127ee991ea576680a185263ab93230.jpg)  
Figure 38: One-Dimensional Table Lookup Using Linear Filtering
````
