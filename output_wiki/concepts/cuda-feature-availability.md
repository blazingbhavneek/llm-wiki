# CUDA Feature Availability and Architecture-Specific Features

## General Feature Availability

Most compute features introduced with a specific compute architecture are intended to be available on all subsequent architectures. This backward compatibility is typically indicated in feature availability tables by a "yes" for availability on compute capabilities subsequent to the feature's introduction [CUDA_C_Programming_Guide:L19449-L19456].

## Architecture-Specific Features

Beginning with devices of Compute Capability 9.0, the general rule of backward compatibility has an exception for specialized compute features. These are known as **architecture-specific features** [CUDA_C_Programming_Guide:L19449-L19456].

### Definition and Purpose

Architecture-specific features are specialized compute features introduced with an architecture that may not be guaranteed to be available on all subsequent compute capabilities [CUDA_C_Programming_Guide:L19449-L19456]. These features target the acceleration of specialized operations, such as Tensor Core operations, which are either:

*   Not intended for all classes of compute capabilities.
*   Likely to change significantly on future generations [CUDA_C_Programming_Guide:L19449-L19456].

### Compilation and Execution Constraints

To use architecture-specific features, developers must adhere to specific compilation and execution rules:

1.  **Compiler Target**: Code must be compiled with an architecture-specific compiler target to enable these features (see Feature Set Compiler Targets) [CUDA_C_Programming_Guide:L19449-L19456].
2.  **Execution Restriction**: Code compiled with an architecture-specific compiler target can only be run on the exact compute capability it was compiled for [CUDA_C_Programming_Guide:L19449-L19456].

## References

*   CUDA C++ Programming Guide, Section 20.1: Feature Availability [CUDA_C_Programming_Guide:L19449-L19456]
