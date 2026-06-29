# Cubemap Surfaces

Cubemap surfaces are accessed using the `surfCubemapread()` and `surfCubemapwrite()` functions as a two-dimensional layered surface. This access method involves using an integer index to denote a specific face, and two floating-point texture coordinates to address a texel within the layer corresponding to that face [CUDA_C_Programming_Guide:L3975-L3978]. The ordering of the faces is indicated in Table 6 of the CUDA C Programming Guide [CUDA_C_Programming_Guide:L3975-L3978].
