# CUDA Linear Filtering

Linear filtering is a texture sampling mode in CUDA that is exclusively available for floating-point textures. In this mode, the value returned by a texture fetch is an interpolated result derived from the neighboring texels surrounding the sampled coordinate.

## Mathematical Formulation

The interpolation formulas for 1D, 2D, and 3D textures are defined as follows:

### One-Dimensional Texture
For a one-dimensional texture, the interpolated value is:
$$ tex(x) = (1 - \alpha) T[i] + \alpha T[i + 1] $$

### Two-Dimensional Texture
For a two-dimensional texture, the value is computed using bilinear interpolation:
$$ tex(x, y) = (1 - \alpha)(1 - \beta) T[i, j] + \alpha(1 - \beta) T[i + 1, j] + (1 - \alpha)\beta T[i, j + 1] + \alpha\beta T[i + 1, j + 1] $$

### Three-Dimensional Texture
For a three-dimensional texture, trilinear interpolation is applied:
$$
\begin{aligned}
tex(x, y, z) = & (1 - \alpha)(1 - \beta)(1 - \gamma) T[i, j, k] + \alpha(1 - \beta)(1 - \gamma) T[i + 1, j, k] + \\
& (1 - \alpha)\beta(1 - \gamma) T[i, j + 1, k] + \alpha\beta(1 - \gamma) T[i + 1, j + 1, k] + \\
& (1 - \alpha)(1 - \beta)\gamma T[i, j, k + 1] + \alpha(1 - \beta)\gamma T[i + 1, j, k + 1] + \\
& (1 - \alpha)\beta\gamma T[i, j + 1, k + 1] + \alpha\beta\gamma T[i + 1, j + 1, k + 1]
\end{aligned}
$$

## Coordinate and Weight Definitions

The indices $i, j, k$ and the fractional weights $\alpha, \beta, \gamma$ are derived from the texture coordinates $x, y, z$ and the texture dimensions (or bounds) as follows:

- $i = floor(x_B)$, $\alpha = frac(x_B)$, where $x_B = x - 0.5$
- $j = floor(y_B)$, $\beta = frac(y_B)$, where $y_B = y - 0.5$
- $k = floor(z_B)$, $\gamma = frac(z_B)$, where $z_B = z - 0.5$

### Fixed-Point Representation
The weights $\alpha, \beta,$ and $\gamma$ are stored in a 9-bit fixed-point format with 8 bits of fractional value. This format ensures that the value 1.0 is exactly represented.

## Visualization

Linear filtering of a one-dimensional texture with $N=4$ is illustrated in Figure 37 of the CUDA C Programming Guide, showing how the interpolated value is calculated between adjacent texels.

## References

- CUDA C Programming Guide: Section 19.2. Linear Filtering [CUDA_C_Programming_Guide:L19398-L19428]
