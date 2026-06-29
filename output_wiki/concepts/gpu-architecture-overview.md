# GPU Architecture Overview

The NVIDIA GPU architecture is built around a scalable array of multithreaded Streaming Multiprocessors (SMs) [CUDA_C_Programming_Guide:L6123-L6134]. This architecture is designed to execute hundreds of threads concurrently, leveraging both instruction-level and thread-level parallelism [CUDA_C_Programming_Guide:L6123-L6134].

## Streaming Multiprocessors (SMs)

The core execution unit of the GPU is the Streaming Multiprocessor (SM). When a CUDA program on the host CPU invokes a kernel grid, the blocks of the grid are enumerated and distributed to multiprocessors that have available execution capacity [CUDA_C_Programming_Guide:L6123-L6134].

*   **Concurrency**: Threads of a single thread block execute concurrently on one multiprocessor, and multiple thread blocks can execute concurrently on the same multiprocessor [CUDA_C_Programming_Guide:L6123-L6134].
*   **Dynamic Scheduling**: As thread blocks terminate, new blocks are automatically launched on the vacated multiprocessors [CUDA_C_Programming_Guide:L6123-L6134].

## SIMT Execution Model

To manage the large number of concurrent threads, the SM employs a unique architecture called SIMT (Single-Instruction, Multiple-Thread) [CUDA_C_Programming_Guide:L6123-L6134]. In this model:

*   Instructions are issued in order [CUDA_C_Programming_Guide:L6123-L6134].
*   Unlike CPU cores, there is no branch prediction or speculative execution [CUDA_C_Programming_Guide:L6123-L6134].

## Hardware Multithreading

The GPU architecture utilizes extensive thread-level parallelism through simultaneous hardware multithreading [CUDA_C_Programming_Guide:L6123-L6134]. Instructions are pipelined, which leverages instruction-level parallelism within a single thread as well as the broader thread-level parallelism provided by the SIMT model [CUDA_C_Programming_Guide:L6123-L6134].

## Data Representation

The NVIDIA GPU architecture uses a little-endian representation for data [CUDA_C_Programming_Guide:L6123-L6134].

## Architecture Versions

Specific architectural features of the streaming multiprocessor are common to all devices, but specific details vary by compute capability. Compute Capability 5.x, 6.x, and 7.x provide the specifics for devices of those respective generations [CUDA_C_Programming_Guide:L6123-L6134].

## Note on Documentation

The source document for this overview (Chapter 7. Hardware Implementation) is considered legacy and was replaced by the new CUDA Programming Guide as of CUDA 13.0 [CUDA_C_Programming_Guide:L6123-L6134]. Users should refer to the current CUDA Programming Guide for up-to-date information [CUDA_C_Programming_Guide:L6123-L6134].
