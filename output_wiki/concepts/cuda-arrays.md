# CUDA Arrays

CUDA arrays are opaque memory layouts optimized for texture fetching [CUDA_C_Programming_Guide:L3983-L3986]. They support one-dimensional, two-dimensional, and three-dimensional configurations [CUDA_C_Programming_Guide:L3983-L3986].

Each element within a CUDA array consists of 1, 2, or 4 components [CUDA_C_Programming_Guide:L3983-L3986]. These components may be signed or unsigned 8-bit, 16-bit, or 32-bit integers, as well as 16-bit or 32-bit floating-point values [CUDA_C_Programming_Guide:L3983-L3986].

Access to CUDA arrays by kernels is restricted to texture fetching and surface reading/writing operations [CUDA_C_Programming_Guide:L3983-L3986]. Direct memory access is not supported; instead, kernels must utilize texture references or surface references to interact with the data [CUDA_C_Programming_Guide:L3983-L3986].
