# Cubemap Layered Textures

Defines cubemap layered textures as layered textures where layers are cubemaps. Covers addressing with integer cubemap indices and three texture coordinates, CUDA array creation with cudaArrayLayered and cudaArrayCubemap flags, texCubemapLayered() fetch function, filtering scope, and compute capability 2.0+ requirement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3851-L3862

Citation: [CUDA_C_Programming_Guide:L3851-L3862]

````text
## 6.2.14.1.5 Cubemap Layered Textures

A cubemap layered texture is a layered texture whose layers are cubemaps of same dimension.

A cubemap layered texture is addressed using an integer index and three floating-point texture coordinates; the index denotes a cubemap within the sequence and the coordinates address a texel within that cubemap.

A cubemap layered texture can only be a CUDA array by calling cudaMalloc3DArray() with the cudaArrayLayered and cudaArrayCubemap flags.

Cubemap layered textures are fetched using the device function described in texCubemapLayered(). Texture filtering (see Texture Fetching) is done only within a layer, not across layers.

Cubemap layered textures are only supported on devices of compute capability 2.0 and higher.
````
