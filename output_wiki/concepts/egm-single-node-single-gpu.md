# EGM: Single-Node, Single-GPU

## Overview

In a single-node, single-GPU configuration, the Extended Global Memory (EGM) framework allows the use of existing CUDA host allocators and system-allocated memory to benefit from high-bandwidth CPU-to-CPU (C2C) communication [CUDA_C_Programming_Guide:L22252-L22252].

## Memory Access Model

From the user's perspective, accessing memory in this configuration is identical to standard host allocation behavior. Local access to these memory regions functions exactly as it does for traditional host allocations [CUDA_C_Programming_Guide:L22252-L22252]. This design ensures compatibility with existing CUDA programming models while enabling the performance benefits of high-bandwidth interconnects within the node [CUDA_C_Programming_Guide:L22250-L22250].
