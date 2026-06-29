# Cubemap Layered Surfaces

Cubemap layered surfaces are accessed using `surfCubemapLayeredread()` and `surfCubemapLayeredwrite()` as a two-dimensional layered surface [CUDA_C_Programming_Guide:L3979-L3982]. This access method involves using an integer index denoting a face of one of the cubemaps and two floating-point texture coordinates addressing a texel within the layer corresponding to this face [CUDA_C_Programming_Guide:L3979-L3982].

Faces are ordered as indicated in Table 6, so index `((2 * 6) + 3)`, for example, accesses the fourth face of the third cubemap [CUDA_C_Programming_Guide:L3979-L3982].
