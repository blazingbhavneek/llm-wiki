# EGM Allocators

## Overview

Extended GPU Memory (EGM) allows the GPU to access system memory with performance characteristics that can exceed local access in multi-socket configurations. This is achieved by guaranteeing that traffic is routed over NVLinks rather than the PCIe interconnect.

## Supported Allocators

Currently, the following CUDA memory allocation APIs are supported for EGM, provided they are configured with appropriate location types and NUMA identifiers:

*   `cuMemCreate`
*   `cudaMemPoolCreate`

## Performance Characteristics

Mapping system memory as EGM does not incur performance penalties. In fact, accessing system memory on a remote socket via EGM is faster than traditional methods. This performance benefit is due to the guaranteed routing of EGM traffic over NVLinks, which provides higher bandwidth and lower latency compared to PCIe-based access between sockets.

## References

- [CUDA_C_Programming_Guide:L22230-L22230]
- [CUDA_C_Programming_Guide:L22232-L22232]
