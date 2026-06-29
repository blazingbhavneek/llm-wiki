# Cubemap Layered Textures

A cubemap layered texture is a layered texture whose layers are cubemaps of the same dimension [CUDA_C_Programming_Guide:L3850-L3861].

## Addressing

A cubemap layered texture is addressed using an integer index and three floating-point texture coordinates [CUDA_C_Programming_Guide:L3850-L3861]. The integer index denotes a specific cubemap within the sequence, while the three floating-point coordinates address a texel within that selected cubemap [CUDA_C_Programming_Guide:L3850-L3861].

## Creation

Cubemap layered textures can only be created as CUDA arrays by calling `cudaMalloc3DArray()` with both the `cudaArrayLayered` and `cudaArrayCubemap` flags [CUDA_C_Programming_Guide:L3850-L3861].

## Fetching and Filtering

Cubemap layered textures are fetched using the device function `texCubemapLayered()` [CUDA_C_Programming_Guide:L3850-L3861]. Texture filtering is performed only within a single layer, not across layers [CUDA_C_Programming_Guide:L3850-L3861].

## Hardware Support

Cubemap layered textures are supported on devices with compute capability 2.0 and higher [CUDA_C_Programming_Guide:L3850-L3861].
