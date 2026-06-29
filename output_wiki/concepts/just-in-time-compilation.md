# Just-in-Time Compilation

Just-in-Time (JIT) compilation is the process by which the CUDA device driver compiles PTX code to binary code at runtime [CUDA_C_Programming_Guide:L1141-L1150]. This mechanism increases application load time but provides significant benefits, including the ability to leverage new compiler improvements introduced in subsequent device driver updates and the capability to run applications on devices that did not exist at the time the application was originally compiled [CUDA_C_Programming_Guide:L1141-L1150].

## Compute Cache

When the device driver performs JIT compilation for an application, it automatically caches the generated binary code to avoid repeating the compilation process in subsequent invocations of the application [CUDA_C_Programming_Guide:L1141-L1150]. This cache is referred to as the compute cache [CUDA_C_Programming_Guide:L1141-L1150]. The compute cache is automatically invalidated when the device driver is upgraded, ensuring that applications can benefit from the improvements in the new JIT compiler built into the updated driver [CUDA_C_Programming_Guide:L1141-L1150].

## Runtime Compilation with NVRTC

As an alternative to using `nvcc` to compile CUDA C++ device code, the NVIDIA Runtime Compilation (NVRTC) library can be used to compile CUDA C++ device code to PTX at runtime [CUDA_C_Programming_Guide:L1141-L1150]. NVRTC serves as a runtime compilation library for CUDA C++ [CUDA_C_Programming_Guide:L1141-L1150].

## Configuration

Environment variables are available to control JIT compilation behavior [CUDA_C_Programming_Guide:L1141-L1150].
