# cudaGetDriverEntryPointByVersion

The CUDA runtime API `cudaGetDriverEntryPointByVersion` is designed to allow users to request a specific CUDA driver version. Unless specified otherwise, this function follows similar guidelines to the driver entry point `cuGetProcAddress` [CUDA_C_Programming_Guide:L20564-L20566].

## Guidelines for Runtime API Usage

As part of the guidelines for runtime API usage, `cudaGetDriverEntryPointByVersion` is treated analogously to `cuGetProcAddress` due to its capability to target specific driver versions [CUDA_C_Programming_Guide:L20564-L20566].

## See Also

- [cuGetProcAddress](concept/cuGetProcAddress)
