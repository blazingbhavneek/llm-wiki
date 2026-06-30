# Cubemap Surfaces

Describes cubemap surface access using surfCubemapread() and surfCubemapwrite() as a two-dimensional layered surface, referencing face ordering from Table 6.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3976-L3979

Citation: [CUDA_C_Programming_Guide:L3976-L3979]

````text
## 6.2.14.2.2 Cubemap Surfaces

Cubemap surfaces are accessed usingsurfCubemapread() and surfCubemapwrite() (surfCubemapread() and surfCubemapwrite()) as a two-dimensional layered surface, i.e., using an integer index denoting a face and two floating-point texture coordinates addressing a texel within the layer corresponding to this face. Faces are ordered as indicated in Table 6.
````
