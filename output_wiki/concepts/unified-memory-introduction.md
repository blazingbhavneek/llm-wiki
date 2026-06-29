# Unified Memory Introduction

Unified Memory is a programming model that simplifies memory management by providing a single, unified memory space accessible by both the host (CPU) and device (GPU) [CUDA_C_Programming_Guide:L20755-L20767]. This model allows developers to allocate memory that can be accessed concurrently by both processors, facilitating easier data sharing and reducing the complexity of explicit memory transfers [CUDA_C_Programming_Guide:L20755-L20767].

## Prerequisites and Compatibility

The Unified Memory programming model is available on devices with compute capability 5.0 or higher [CUDA_C_Programming_Guide:L20755-L20767]. For devices with compute capability lower than 5.0, specific support and documentation are provided in the CUDA toolkit documentation for CUDA 11.8 [CUDA_C_Programming_Guide:L20755-L20767].

## Documentation Structure

The comprehensive documentation for Unified Memory is divided into three main parts:

1. General description of unified memory [CUDA_C_Programming_Guide:L20755-L20767].
2. Unified Memory on devices with full CUDA Unified Memory support [CUDA_C_Programming_Guide:L20755-L20767].
3. Unified Memory on devices without full CUDA Unified Memory support [CUDA_C_Programming_Guide:L20755-L20767].

## Legacy Notice

Please note that this specific documentation chapter (Chapter 24) is considered legacy as of CUDA 13.0, having been replaced by the new CUDA Programming Guide [CUDA_C_Programming_Guide:L20755-L20767]. Users are advised to refer to the current CUDA Programming Guide for up-to-date information [CUDA_C_Programming_Guide:L20755-L20767].
