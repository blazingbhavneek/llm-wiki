# Function Recursion

__global__ functions do not support recursion.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17235-L17236

Citation: [CUDA_C_Programming_Guide:L17235-L17236]

````text

The address of a \_\_global\_\_ function taken in host code cannot be used in device code (e.g. to launch the kernel). Similarly, the address of a \_\_global\_\_ function taken in device code cannot be used in host code.
````
