# CUDA Dynamic Parallelism

CUDA Dynamic Parallelism (CDP) is an extension to the CUDA programming model that enables a CUDA kernel to create and synchronize with new work directly on the GPU [CUDA_C_Programming_Guide:L13635-L13641]. This capability allows for the dynamic creation of parallelism at any point in a program where it is needed, offering significant flexibility in how workloads are structured and executed [CUDA_C_Programming_Guide:L13635-L13641].

## Overview

The primary benefit of Dynamic Parallelism is the reduction in the need to transfer execution control and data between the host (CPU) and the device (GPU) [CUDA_C_Programming_Guide:L13635-L13641]. By allowing launch configuration decisions to be made at runtime by threads executing on the device, CDP facilitates more efficient handling of data-dependent parallel work [CUDA_C_Programming_Guide:L13635-L13641].

Key capabilities include:
*   **Inline Generation:** Data-dependent parallel work can be generated inline within a kernel at runtime [CUDA_C_Programming_Guide:L13635-L13641].
*   **Hardware Utilization:** This approach takes advantage of the GPU’s hardware schedulers and load balancers dynamically, adapting in response to data-driven decisions or workloads [CUDA_C_Programming_Guide:L13635-L13641].
*   **Algorithmic Transparency:** Algorithms and programming patterns that previously required modifications to eliminate recursion, irregular loop structures, or other constructs incompatible with flat, single-level parallelism can now be expressed more transparently [CUDA_C_Programming_Guide:L13635-L13641].

## Hardware Requirements

Dynamic Parallelism is only supported by devices with a compute capability of 3.5 and higher [CUDA_C_Programming_Guide:L13642-L13642].

## Programming Model

The CUDA programming model has been extended to support Dynamic Parallelism, including modifications and additions necessary to exploit this capacity [CUDA_C_Programming_Guide:L13635-L13641]. Developers are expected to follow specific guidelines and best practices to effectively utilize these extended capabilities [CUDA_C_Programming_Guide:L13635-L13641].
