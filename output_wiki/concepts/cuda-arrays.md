# CUDA Arrays

Defines CUDA arrays as opaque, optimized memory layouts for texture fetching (1D, 2D, 3D) with various component types. Notes they are only accessible via texture fetching or surface read/write operations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3984-L3987

Citation: [CUDA_C_Programming_Guide:L3984-L3987]

````text
## 6.2.14.3 CUDA Arrays

CUDA arrays are opaque memory layouts optimized for texture fetching. They are one dimensional, two dimensional, or three-dimensional and composed of elements, each of which has 1, 2 or 4 components that may be signed or unsigned 8-, 16-, or 32-bit integers, 16-bit floats, or 32-bit floats. CUDA arrays are only accessible by kernels through texture fetching as described in Texture Memory or surface reading and writing as described in Surface Memory.
````
