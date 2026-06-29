# Cubemap Textures

A cubemap texture is a specialized type of two-dimensional layered texture consisting of six layers, each representing one face of a cube [CUDA_C_Programming_Guide:L3832-L3835].

## Structure and Addressing

Each layer within a cubemap texture must have a width equal to its height [CUDA_C_Programming_Guide:L3835-L3836].

Cubemaps are addressed using three texture coordinates ($x$, $y$, and $z$) that are interpreted as a direction vector emanating from the center of the cube [CUDA_C_Programming_Guide:L3836-L3838]. This vector points to a specific face of the cube and a texel within that face's layer [CUDA_C_Programming_Guide:L3838].

### Face Selection Logic

The specific face is selected based on the texture coordinate with the largest magnitude, denoted as $m$ [CUDA_C_Programming_Guide:L3838-L3840]. The corresponding layer is then addressed using normalized coordinates derived from $s$ and $t$, calculated as $(s/m+1)/2$ and $(t/m+1)/2$ [CUDA_C_Programming_Guide:L3840].

The values for $m$, $s$, and $t$ depend on which coordinate has the largest absolute magnitude and its sign, as defined in the following table:

| Condition | Sign | Face Index | $m$ | $s$ | $t$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $|x| > |y|$ and $|x| > |z|$ | $x \ge 0$ | 0 | $x$ | $-z$ | $-y$ |
| $|x| > |y|$ and $|x| > |z|$ | $x < 0$ | 1 | $-x$ | $z$ | $-y$ |
| $|y| > |x|$ and $|y| > |z|$ | $y \ge 0$ | 2 | $y$ | $x$ | $z$ |
| $|y| > |x|$ and $|y| > |z|$ | $y < 0$ | 3 | $-y$ | $x$ | $-z$ |
| $|z| > |x|$ and $|z| > |y|$ | $z \ge 0$ | 4 | $z$ | $x$ | $-y$ |
| $|z| > |x|$ and $|z| > |y|$ | $z < 0$ | 5 | $-z$ | $-x$ | $-y$ |

*Note: The original source uses a placeholder character for the greater-than-or-equal-to symbol in the table headers; the logic above reflects the standard interpretation of these conditions.* [CUDA_C_Programming_Guide:L3841-L3849]

## Implementation Details

### Creation

A cubemap texture must be created as a CUDA array by calling `cudaMalloc3DArray()` with the `cudaArrayCubemap` flag [CUDA_C_Programming_Guide:L3849-L3850].

### Fetching

Cubemap textures are accessed using the device function `texCubemap()` [CUDA_C_Programming_Guide:L3850-L3851].

### Hardware Support

Cubemap textures are supported only on devices with compute capability 2.0 and higher [CUDA_C_Programming_Guide:L3851-L3852].
