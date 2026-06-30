# Cubemap Textures

Describes cubemap textures as a special two-dimensional layered texture with six faces. Details addressing via direction vectors, face selection logic, coordinate mapping (Table 6), CUDA array creation with cudaArray-Cubemap, texCubemap() fetch function, and compute capability 2.0+ requirement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3833-L3849

Citation: [CUDA_C_Programming_Guide:L3833-L3849]

````text
## 6.2.14.1.4 Cubemap Textures

A cubemap texture is a special type of two-dimensional layered texture that has six layers representing the faces of a cube:

▶ The width of a layer is equal to its height.

▶ The cubemap is addressed using three texture coordinates x, y, and z that are interpreted as a direction vector emanating from the center of the cube and pointing to one face of the cube and a texel within the layer corresponding to that face. More specifically, the face is selected by the coordinate with largest magnitude m and the corresponding layer is addressed using coordinates (s/m+1)/2 and (t/m+1)/2 where s and t are defined in Table 6.

Table 6: Cubemap Fetch

<table><tr><td colspan="2"></td><td>face</td><td>m</td><td>s</td><td>t</td></tr><tr><td rowspan="2"> $|x| > |y|$  and  $|x| > |z|$ </td><td>x □ 0</td><td>0</td><td>x</td><td>-z</td><td>-y</td></tr><tr><td>x &lt; 0</td><td>1</td><td>-x</td><td>z</td><td>-y</td></tr><tr><td rowspan="2"> $|y| > |x|$  and  $|y| > |z|$ </td><td>y □ 0</td><td>2</td><td>y</td><td>x</td><td>z</td></tr><tr><td>y &lt; 0</td><td>3</td><td>-y</td><td>x</td><td>-z</td></tr><tr><td rowspan="2"> $|z| > |x|$  and  $|z| > |y|$ </td><td>z □ 0</td><td>4</td><td>z</td><td>x</td><td>-y</td></tr><tr><td>z &lt; 0</td><td>5</td><td>-z</td><td>-x</td><td>-y</td></tr></table>

A cubemap texture can only be a CUDA array by calling cudaMalloc3DArray() with the cudaArray-Cubemap flag.

Cubemap textures are fetched using the device function described in texCubemap().

Cubemap textures are only supported on devices of compute capability 2.0 and higher.
````
