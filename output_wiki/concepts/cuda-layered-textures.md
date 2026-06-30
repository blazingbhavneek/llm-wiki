# Layered Textures

Explains one-dimensional and two-dimensional layered textures (texture arrays), addressing using integer layer indices and floating-point coordinates, CUDA array creation with cudaArray-Layered, fetch functions, and compute capability 2.0+ requirement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3821-L3832

Citation: [CUDA_C_Programming_Guide:L3821-L3832]

````text
## 6.2.14.1.3 Layered Textures

A one-dimensional or two-dimensional layered texture (also known as texture array in Direct3D and array texture in OpenGL) is a texture made up of a sequence of layers, all of which are regular textures of same dimensionality, size, and data type.

A one-dimensional layered texture is addressed using an integer index and a floating-point texture coordinate; the index denotes a layer within the sequence and the coordinate addresses a texel within that layer. A two-dimensional layered texture is addressed using an integer index and two floatingpoint texture coordinates; the index denotes a layer within the sequence and the coordinates address a texel within that layer.

A layered texture can only be a CUDA array by calling cudaMalloc3DArray() with the cudaArray-Layered flag (and a height of zero for one-dimensional layered texture).

Layered textures are fetched using the device functions described in tex1DLayered() and tex2DLayered(). Texture filtering (see Texture Fetching) is done only within a layer, not across layers.

Layered textures are only supported on devices of compute capability 2.0 and higher.
````
