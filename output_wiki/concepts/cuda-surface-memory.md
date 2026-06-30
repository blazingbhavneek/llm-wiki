# Surface Memory

Introduces surface memory for compute capability 2.0+ devices, allowing read/write access to CUDA arrays via surface objects. References Table 27 for maximum surface dimensions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3873-L3879

Citation: [CUDA_C_Programming_Guide:L3873-L3879]

````text
## 6.2.14.2 Surface Memory

For devices of compute capability 2.0 and higher, a CUDA array (described in Cubemap Surfaces), created with the cudaArraySurfaceLoadStore flag, can be read and written via a surface object using the functions described in Surface Functions.

Table 27 lists the maximum surface width, height, and depth depending on the compute capability of the device.

## 6.2.14.2.1 Surface Object API
````
