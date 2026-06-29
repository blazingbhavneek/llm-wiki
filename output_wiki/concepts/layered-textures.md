# Layered Textures

A one-dimensional or two-dimensional layered texture (also known as texture array in Direct3D and array texture in OpenGL) is a texture made up of a sequence of layers, all of which are regular textures of same dimensionality, size, and data type [CUDA_C_Programming_Guide:L3821-L3823].

## Addressing

A one-dimensional layered texture is addressed using an integer index and a floating-point texture coordinate; the index denotes a layer within the sequence and the coordinate addresses a texel within that layer [CUDA_C_Programming_Guide:L3823-L3825]. A two-dimensional layered texture is addressed using an integer index and two floatingpoint texture coordinates; the index denotes a layer within the sequence and the coordinates address a texel within that layer [CUDA_C_Programming_Guide:L3825-L3827].

## Creation

A layered texture can only be a CUDA array by calling cudaMalloc3DArray() with the cudaArrayLayered flag (and a height of zero for one-dimensional layered texture) [CUDA_C_Programming_Guide:L3827-L3828].

## Fetching

Layered textures are fetched using the device functions described in tex1DLayered() and tex2DLayered() [CUDA_C_Programming_Guide:L3828-L3829]. Texture filtering is done only within a layer, not across layers [CUDA_C_Programming_Guide:L3829].

## Support

Layered textures are only supported on devices of compute capability 2.0 and higher [CUDA_C_Programming_Guide:L3829-L3831].
