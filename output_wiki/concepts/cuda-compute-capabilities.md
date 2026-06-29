# CUDA Compute Capabilities

CUDA Compute Capability is a versioning scheme used to identify the features supported by NVIDIA GPU hardware. Represented as a version number with a major revision (X) and a minor revision (Y), denoted as X.Y, it is also sometimes referred to as the "SM version" [CUDA_C_Programming_Guide:L1079-L1081].

Applications use the compute capability at runtime to determine which hardware features and instructions are available on the present GPU [CUDA_C_Programming_Guide:L1079-L1081]. The major revision number typically corresponds to a specific NVIDIA GPU architecture, while the minor revision number corresponds to incremental improvements to the core architecture, which may include new features [CUDA_C_Programming_Guide:L1089-L1091].

## Architecture Mapping

The following table maps major revision numbers to their corresponding NVIDIA GPU architectures [CUDA_C_Programming_Guide:L1085-L1087]:

| Major Revision Number | NVIDIA GPU Architecture |
| :--- | :--- |
| 9 | NVIDIA Hopper GPU Architecture |
| 8 | NVIDIA Ampere GPU Architecture |
| 7 | NVIDIA Volta GPU Architecture |
| 6 | NVIDIA Pascal GPU Architecture |
| 5 | NVIDIA Maxwell GPU Architecture |
| 3 | NVIDIA Kepler GPU Architecture |

Some architectures share features across different compute capability versions. For example, the NVIDIA Turing GPU Architecture (Compute Capability 7.5) is based on the NVIDIA Volta GPU Architecture [CUDA_C_Programming_Guide:L1095-L1095].

## Compute Capability Versions

The CUDA programming guide documents specific compute capability versions and their associated features, including architecture details, global memory, shared memory, and specialized computation features. The supported versions include [CUDA_C_Programming_Guide:L626-L666]:

*   **Compute Capability 5.x**: Based on the Maxwell architecture. Includes specific global memory and shared memory configurations [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 6.x**: Based on the Pascal architecture. Includes specific global memory and shared memory configurations [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 7.x**: Based on the Volta architecture. Includes specific global memory and shared memory configurations, as well as Independent Thread Scheduling [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 8.x**: Based on the Ampere architecture. Includes specific global memory and shared memory configurations [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 9.0**: Based on the Hopper architecture. Includes specific global memory, shared memory, and features accelerating specialized computations [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 10.0**: Includes specific global memory, shared memory, and features accelerating specialized computations [CUDA_C_Programming_Guide:L626-L666].
*   **Compute Capability 12.0**: Includes specific global memory, shared memory, and features accelerating specialized computations [CUDA_C_Programming_Guide:L626-L666].

## Feature Availability

Features are categorized based on their availability across different hardware generations [CUDA_C_Programming_Guide:L626-L666]:

*   **Architecture-Specific Features**: Features unique to a specific GPU architecture [CUDA_C_Programming_Guide:L626-L666].
*   **Family-Specific Features**: Features shared across a family of architectures [CUDA_C_Programming_Guide:L626-L666].
*   **Feature Set Compiler Targets**: Specific compiler targets defined for feature sets [CUDA_C_Programming_Guide:L626-L666].

## Floating-Point Standard

Compute capabilities also define the floating-point standards supported by the hardware [CUDA_C_Programming_Guide:L626-L666].

## Technical Specifications

Detailed technical specifications for features and capabilities are provided for each compute capability version [CUDA_C_Programming_Guide:L626-L666].
