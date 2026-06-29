# CUDA NVCC Compiler

nvcc is the compiler driver for CUDA, designed to simplify the process of compiling code for execution on NVIDIA devices. It supports high-level programming languages such as C++ as well as the CUDA instruction set architecture known as PTX [CUDA_C_Programming_Guide:L1119-L1121].

## Overview

While kernels can be written directly in PTX, it is generally more effective to use a high-level language like C++ [CUDA_C_Programming_Guide:L1119-L1121]. Regardless of the source language, all kernels must be compiled into binary code by nvcc before they can execute on the device [CUDA_C_Programming_Guide:L1119-L1121].

nvcc acts as a compiler driver that provides simple and familiar command-line options. It executes these options by invoking a collection of tools that implement the different compilation stages [CUDA_C_Programming_Guide:L1119-L1121].

## Workflow

Source files compiled with nvcc can contain a mix of host code (code that executes on the host) and device code (code that executes on the device) [CUDA_C_Programming_Guide:L1127-L1133]. The basic workflow of nvcc involves the following steps:

1. **Separation**: nvcc separates device code from host code [CUDA_C_Programming_Guide:L1127-L1133].
2. **Device Compilation**: The device code is compiled into an assembly form (PTX code) and/or a binary form (cubin object) [CUDA_C_Programming_Guide:L1127-L1133].
3. **Host Code Modification**: nvcc modifies the host code by replacing the `<<<...>>>` kernel launch syntax with the necessary CUDA runtime function calls. These calls are required to load and launch each compiled kernel from the PTX code and/or cubin object [CUDA_C_Programming_Guide:L1127-L1133].

The modified host code is output either as C++ code, which is then compiled using another tool, or as object code directly if nvcc invokes the host compiler during the final stage [CUDA_C_Programming_Guide:L1127-L1133].

## See Also

For a complete description of nvcc workflow and command options, refer to the nvcc user manual [CUDA_C_Programming_Guide:L1119-L1121].
