# Compute Capabilities

Details compute capability versions, architecture-specific and family-specific features, compiler targets, and technical specifications (grids, blocks, warps, memory limits) per capability.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19438-L19523

Citation: [CUDA_C_Programming_Guide:L19438-L19523]

````text
# Chapter 20. Compute Capabilities

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

The general specifications and features of a compute device depend on its compute capability (see Compute Capability).

Table 26 and Table 27 show the features and technical specifications associated with each compute capability that is currently supported.

Section Floating-Point Standard reviews compliance with the IEEE floating-point standard.

Sections Compute Capability 5.x, Compute Capability 6.x, Compute Capability 7.x, Compute Capability 8.x, Compute Capability 9.0, Compute Capability 10.0, and Compute Capability 12.0 give more details on the architecture of devices with these respective compute capabilities.

## 20.1. Feature Availability

Most compute features introduced with a compute architecture are intended to be available on all subsequent architectures. This is shown in Table 26 by the “yes” for availability of a feature on compute capabilities subsequent to its introduction.

## 20.1.1. Architecture-Specific Features

Beginning with devices of Compute Capability 9.0, specialized compute features that are introduced with an architecture may not be guaranteed to be available on all subsequent compute capabilities. These features are called architecture-specific features and target acceleration of specialized operations, such as Tensor Core operations, which are not intended for all classes of compute capabilities or may significantly change on future generations. Code must be compiled with an architecture-specific compiler target (see Feature Set Compiler Targets) to enable architecture-specific features. Code compiled with an architecture-specific compiler target can only be run on the exact compute capability it was compiled for.

## 20.1.2. Family-Specific Features

Beginning with devices of Compute Capability 10.0, some architecture-specific features are common to devices of more than one compute capability. The devices that contain these features are part of the same family and these features can also be called family-specific features. Family-specific features are guaranteed to be available on all devices in the same family. A family-specific compiler target is required to enable family-specific features. See Section 20.1.3. Code compiled for a family-specific target can only be run on GPUs which are members of that family.

## 20.1.3. Feature Set Compiler Targets

There are three sets of compute features which the compiler can target:

Baseline Feature Set: The predominant set of compute features that are introduced with the intent to be available for subsequent compute architectures. These features and their availability are summarized in Table 26.

Architecture-Specific Feature Set: A small and highly specialized set of features called architecturespecific, that are introduced to accelerate specialized operations, which are not guaranteed to be available or might change significantly on subsequent compute architectures. These features are summarized in the respective “Compute Capability #.#” subsections. The architecture-specific feature set is a superset of the family-specific feature set. Architecture-specific compiler targets were introduced with Compute Capability 9.0 devices and are selected by using an a sufix in the compilation target, for example by specifying compute\_100a or compute\_120a as the compute target.

Family-Specific Feature Set: Some architecture-specific features are common to GPUs of more than one compute capability. These features are summarized in the respective “Compute Capability #.#” subsections. With a few exceptions, later generation devices with the same major compute capability are in the same family. Table 25 indicates the compatibility of family-specific targets with device compute capability, including exceptions. The family-specific feature set is a superset of the baseline feature set. Family-specific compiler targets were introduced with Compute Capability 10.0 devices and are selected by using a f sufix in the compilation target, for example by specifying compute\_100f or compute\_120f as the compute target.

All devices starting from compute capability 9.0 have a set of features that are architecture-specific. To utilize the complete set of these features on a specific GPU, the architecture-specific compiler target with the sufix a must be used. Additionally, starting from compute capability 10.0, there are sets of features that appear in multiple devices with diferent minor compute capability. These sets of instructions are called family-specific features, and the devices which share these features are said to be part of the same family. The family-specific features are a subset of the architecture-specific features that are shared by all members of that GPU family. The family-specific compiler target with the sufix f allows the compiler to generate code which uses this common subset of architecturespecific features.

For example:

The compute\_100 compilation target does not allow use of architecture-specific features. This target will be compatible with all devices of compute capability 10.0 and later.

The compute\_100f family-specific compilation target allows the use of the subset of architecture-specific features that are common across the GPU family. This target will only be compatible with devices that are part of the GPU family. In this example it is compatible with devices of Compute Capability 10.0 and Compute Capability 10.3. The features available in the family-specific compute\_100f target is a superset of the features available in the baseline compute\_100 target.

The compute\_100a architecture-specific compilation target allows use of the complete set of architecture-specific features in Compute Capability 10.0 devices. This target will only be compatible with devices of Compute Capability 10.0 and no others. The features available in the compute\_100a target form a superset of the features available in the compute\_100f target.

Table 25: Family-Specific Compatibility

<table><tr><td>Compilation Target</td><td colspan="2">Compatible with Compute Capability</td></tr><tr><td>compute_100f</td><td>10.0</td><td>10.3</td></tr><tr><td>compute_103f</td><td colspan="2"> $10.3^{26}$ </td></tr><tr><td>compute_110f</td><td colspan="2"> $11.0^{26}$ </td></tr><tr><td>compute_120f</td><td>12.0</td><td>12.1</td></tr><tr><td>compute_121f</td><td colspan="2"> $12.1^{26}$ </td></tr></table>

## 20.2. Features and Technical Specifications

Table 26: Feature Support per Compute Capability

<table><tr><td>Feature Support</td><td colspan="6">Compute Capability</td></tr><tr><td>(Unlisted features are supported for all compute capabilities)</td><td>7.x</td><td>8.x</td><td>9.0</td><td>10.0</td><td>11.0</td><td>12.0</td></tr><tr><td>Atomic functions operating on 128-bit integer values in global memory (Atomic Functions)</td><td colspan="2">No</td><td colspan="4">Yes</td></tr></table>

continues on next page

Table 26 – continued from previous page

<table><tr><td>Feature Support</td><td colspan="2">Compute Capability</td></tr><tr><td>Atomic functions operating on 128-bit integer values in shared memory (Atomic Functions)</td><td>No</td><td>Yes</td></tr><tr><td>Atomic addition operating on float2 and float4 floating point vectors in global memory (atomicAdd())</td><td>No</td><td>Yes</td></tr><tr><td>Bfloat16-precision floating-point operations: addition, subtraction, multiplication, comparison, warp shuffle functions, conversion</td><td>No</td><td>Yes</td></tr><tr><td>Hardware-accelerated memcpy_async (Asyn-chronous Data Copies using cuda::pipeline)</td><td>No</td><td>Yes</td></tr></table>

continues on next page

Table 26 – continued from previous page

<table><tr><td>Feature Support</td><td colspan="3">Compute Capability</td></tr><tr><td>Hardware-accelerated Split Arrive/Wait Barrier (Asyn-chronous Barrier)</td><td>No</td><td colspan="2">Yes</td></tr><tr><td>L2 Cache Residency Manage-ment (Device Memory L2 Access Manage-ment)</td><td>No</td><td colspan="2">Yes</td></tr><tr><td>DPX Instructions for Ac-celerated Dynamic Program-ming</td><td colspan="2">No</td><td>Yes</td></tr><tr><td>Distributed Shared Memory</td><td colspan="2">No</td><td>Yes</td></tr><tr><td>Thread Block Clus-ter</td><td colspan="2">No</td><td>Yes</td></tr><tr><td>Tensor Memory Accelerator (TMA) unit</td><td colspan="2">No</td><td>Yes</td></tr></table>

Note that the KB and K units used in the following table correspond to 1024 bytes (i.e., a KiB) and 1024 respectively.

Table 27: Technical Specifications per Compute Capability

<table><tr><td></td><td colspan="9">Compute Capability</td></tr><tr><td>Technical Specifications</td><td>7.5</td><td>8.0</td><td>8.6</td><td>8.7</td><td>8.9</td><td>9.0</td><td>10.0</td><td>11.0</td><td>12.0</td></tr></table>

continues on next page

Table 27 – continued from previous page

<table><tr><td></td><td colspan="7">Compute Capability</td></tr><tr><td>Maximum number of resident grids per device (Concurrent Kernel Execution)</td><td colspan="7">128</td></tr><tr><td>Maximum dimensionality of grid of thread blocks</td><td colspan="7">3</td></tr><tr><td>Maximum x -dimension of a grid of thread blocks</td><td colspan="7"> $2^{31}-1$ </td></tr><tr><td>Maximum y- or z-dimension of a grid of thread blocks</td><td colspan="7">65535</td></tr><tr><td>Maximum dimensionality of thread block</td><td colspan="7">3</td></tr><tr><td>Maximum x- or y-dimensionality of a block</td><td colspan="7">1024</td></tr><tr><td>Maximum z-dimension of a block</td><td colspan="7">64</td></tr><tr><td>Maximum number of threads per block</td><td colspan="7">1024</td></tr><tr><td>Warp size</td><td colspan="7">32</td></tr><tr><td>Maximum number of resident blocks per SM</td><td>16</td><td>32</td><td>16</td><td>24</td><td>32</td><td colspan="2">24</td></tr><tr><td>Maximum number of resident warps per SM</td><td>32</td><td>64</td><td colspan="2">48</td><td>64</td><td colspan="2">48</td></tr><tr><td>Maximum number of resident threads per SM</td><td>1024</td><td>2048</td><td colspan="2">1536</td><td>2048</td><td colspan="2">1536</td></tr><tr><td>Number of 32-bit registers per SM</td><td colspan="7">64 K</td></tr><tr><td>Maximum number of 32-bit registers per thread block</td><td colspan="7">64 K</td></tr><tr><td>Maximum number of 32-bit registers per thread</td><td colspan="7">255</td></tr><tr><td>Maximum amount of shared memory per SM</td><td>64 KB</td><td>164 KB</td><td>100 KB</td><td>164 KB</td><td>100 KB</td><td>228 KB</td><td>100 KB</td></tr><tr><td>Maximum amount of shared memory per thread  $block^{27}$ </td><td>64 KB</td><td>163 KB</td><td>99 KB</td><td>163 KB</td><td>99 KB</td><td>227 KB</td><td>99 KB</td></tr><tr><td>Number of shared memory banks</td><td colspan="7">32</td></tr><tr><td>Maximum amount of local memory per thread</td><td colspan="7">512 KB</td></tr><tr><td>Constant memory size</td><td colspan="7">64 KB</td></tr><tr><td>Cache working set per SM for constant memory</td><td colspan="7">8 KB</td></tr><tr><td>Cache working set per SM for texture memory</td><td>32 or 64 KB</td><td>28 KB ~ 192 KB</td><td>28 KB ~ 128 KB</td><td>28 KB ~ 192 KB</td><td>28 KB ~ 128 KB</td><td>28 KB ~ 256 KB</td><td>28 KB ~ 128 KB</td></tr></table>

continues on next page

Table 27 – continued from previous page

<table><tr><td></td><td>Compute Capability</td></tr><tr><td>Maximum width for a 1D texture object using a CUDA array</td><td>131072</td></tr><tr><td>Maximum width for a 1D texture object using linear memory</td><td> $2^{28}$ </td></tr><tr><td>Maximum width and number of layers for a 1D layered texture object</td><td>32768 x 2048</td></tr><tr><td>Maximum width and height for a 2D texture object using a CUDA array</td><td>131072 x 65536</td></tr><tr><td>Maximum width and height for a 2D texture object using linear memory</td><td>131072 x 65000</td></tr><tr><td>Maximum width and height for a 2D texture object using a CUDA array supporting texture gather</td><td>32768 x 32768</td></tr><tr><td>Maximum width, height, and number of layers for a 2D layered texture object</td><td>32768 x 32768 x 2048</td></tr><tr><td>Maximum width, height, and depth for a 3D texture object using to a CUDA array</td><td>16384 x 16384 x 16384</td></tr><tr><td>Maximum width (and height) for a cubemap texture object</td><td>32768</td></tr><tr><td>Maximum width (and height) and number of layers for a cubemap layered texture object</td><td>32768 x 2046</td></tr><tr><td>Maximum number of textures that can be bound to a kernel</td><td>256</td></tr><tr><td>Maximum width for a 1D surface object using a CUDA array</td><td>32768</td></tr><tr><td>Maximum width and number of layers for a 1D layered surface object</td><td>32768 x 2048</td></tr><tr><td>Maximum width and height for a 2D surface object using a CUDA array</td><td>131072 x 65536</td></tr><tr><td>Maximum width, height, and number of layers for a 2D layered surface object</td><td>32768 x 32768 x 1048</td></tr><tr><td>Maximum width, height, and depth for a 3D surface object using a CUDA array</td><td>16384 x 16384 x 16384</td></tr><tr><td>Maximum width (and height) for a cubemap surface object using a CUDA array</td><td>32768</td></tr><tr><td>Maximum width (and height) and number of layers for a cubemap layered surface object</td><td>32768 x 2046</td></tr><tr><td>Maximum number of surfaces that can use a kernel</td><td>32</td></tr></table>

<sup>27</sup> above 48 KB requires dynamic shared memory
````
