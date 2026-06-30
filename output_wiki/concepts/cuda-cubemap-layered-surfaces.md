# Cubemap Layered Surfaces

Describes cubemap layered surface access using surfCubemapLayeredread() and surfCubemapLayeredwrite() as a two-dimensional layered surface, explaining index calculation for faces across multiple cubemaps.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3980-L3983

Citation: [CUDA_C_Programming_Guide:L3980-L3983]

````text
## 6.2.14.2.3 Cubemap Layered Surfaces

Cubemap layered surfaces are accessed using surfCubemapLayeredread() and surfCubemapLayeredwrite() (surfCubemapLayeredread() and surfCubemapLayeredwrite()) as a two-dimensional layered surface, i.e., using an integer index denoting a face of one of the cubemaps and two floating-point texture coordinates addressing a texel within the layer corresponding to this face. Faces are ordered as indicated in Table 6, so index ((2 \* 6) + 3), for example, accesses the fourth face of the third cubemap.
````
