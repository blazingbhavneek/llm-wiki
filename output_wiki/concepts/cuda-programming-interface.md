# CUDA Programming Interface & NVCC Compilation

Covers Chapter 6: Programming interface overview, C++ extensions, runtime library, and nvcc compilation workflow.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L1103-L1140

Citation: [CUDA_C_Programming_Guide:L1103-L1140]

````text
# Chapter 6. Programming Interface

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

CUDA C++ provides a simple path for users familiar with the C++ programming language to easily write programs for execution by the device.

It consists of a minimal set of extensions to the C++ language and a runtime library.

The core language extensions have been introduced in Programming Model. They allow programmers to define a kernel as a C++ function and use some new syntax to specify the grid and block dimension each time the function is called. A complete description of all extensions can be found in C++ Language Extensions. Any source file that contains some of these extensions must be compiled with nvcc as outlined in Compilation with NVCC.

The runtime is introduced in CUDA Runtime. It provides C and C++ functions that execute on the host to allocate and deallocate device memory, transfer data between host memory and device memory, manage systems with multiple devices, etc. A complete description of the runtime can be found in the CUDA reference manual.

The runtime is built on top of a lower-level C API, the CUDA driver API, which is also accessible by the application. The driver API provides an additional level of control by exposing lower-level concepts such as CUDA contexts - the analogue of host processes for the device - and CUDA modules - the analogue of dynamically loaded libraries for the device. Most applications do not use the driver API as they do not need this additional level of control and when using the runtime, context and module management are implicit, resulting in more concise code. As the runtime is interoperable with the driver API, most applications that need some driver API features can default to use the runtime API and only use the driver API where needed. The driver API is introduced in Driver API and fully described in the reference manual.

## 6.1. Compilation with NVCC

Kernels can be written using the CUDA instruction set architecture, called PTX, which is described in the PTX reference manual. It is however usually more efective to use a high-level programming language such as C++. In both cases, kernels must be compiled into binary code by nvcc to execute on the device.

nvcc is a compiler driver that simplifies the process of compiling C++ or PTX code: It provides simple and familiar command line options and executes them by invoking the collection of tools that implement the diferent compilation stages. This section gives an overview of nvcc workflow and command options. A complete description can be found in the nvcc user manual.

## 6.1.1. Compilation Workflow

## 6.1.1.1 Ofline Compilation

Source files compiled with nvcc can include a mix of host code (i.e., code that executes on the host) and device code (i.e., code that executes on the device). nvcc’s basic workflow consists in separating device code from host code and then:

▶ compiling the device code into an assembly form (PTX code) and/or binary form (cubin object),

▶ and modifying the host code by replacing the <<<...>>> syntax introduced in Kernels (and described in more details in Execution Configuration) by the necessary CUDA runtime function calls to load and launch each compiled kernel from the PTX code and/or cubin object.

The modified host code is output either as C++ code that is left to be compiled using another tool or as object code directly by letting nvcc invoke the host compiler during the last compilation stage.

Applications can then:

Either link to the compiled host code (this is the most common case),

▶ Or ignore the modified host code (if any) and use the CUDA driver API (see Driver API) to load and execute the PTX code or cubin object.
````
