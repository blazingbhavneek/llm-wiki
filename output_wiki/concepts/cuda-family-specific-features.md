# CUDA Family-Specific Features

Beginning with devices of Compute Capability 10.0, NVIDIA introduced the concept of "family-specific features" to group architecture-specific capabilities that are common to devices across more than one compute capability [CUDA_C_Programming_Guide:L19457-L19460].

## Definition and Scope

Devices that share these common architecture-specific features are considered part of the same family [CUDA_C_Programming_Guide:L19457-L19460]. A key characteristic of family-specific features is that they are guaranteed to be available on all devices within the same family [CUDA_C_Programming_Guide:L19457-L19460].

## Compiler Targets and Execution

To utilize family-specific features, a family-specific compiler target is required [CUDA_C_Programming_Guide:L19457-L19460]. Code compiled for a family-specific target is restricted in its execution scope; it can only be run on GPUs that are members of that specific family [CUDA_C_Programming_Guide:L19457-L19460].

## References

- [CUDA_C_Programming_Guide:L19457-L19460]
