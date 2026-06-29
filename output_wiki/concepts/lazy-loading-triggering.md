# Triggering Lazy Loading

Loading kernels and variables happens automatically, without any need for explicit loading. Simply launching a kernel or referencing a variable or a kernel will automatically load relevant modules and kernels [CUDA_C_Programming_Guide:L22118-L22123].

However, if for any reason you wish to load a kernel without executing it or modifying it in any way, specific APIs can be used to trigger the loading process explicitly [CUDA_C_Programming_Guide:L22124-L22125].

## CUDA Driver API

In the CUDA Driver API, loading of kernels happens during the `cuModuleGetFunction()` call [CUDA_C_Programming_Guide:L22127-L22128]. This call is necessary even without Lazy Loading, as it is the only way to obtain a kernel handle [CUDA_C_Programming_Guide:L22129-L22130]. However, you can also use this API to control with finer granularity when kernels are loaded [CUDA_C_Programming_Guide:L22131-L22132].

## CUDA Runtime API

The CUDA Runtime API manages module management automatically, so explicit module loading functions are not typically required [CUDA_C_Programming_Guide:L22134-L22135]. Instead, it is recommended to simply use `cudaFuncGetAttributes()` to reference the kernel [CUDA_C_Programming_Guide:L22134-L22135]. This will ensure that the kernel is loaded without changing the state [CUDA_C_Programming_Guide:L22134-L22135].
