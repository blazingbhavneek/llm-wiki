# Link Compatibility across Toolkit Revisions

## Overview
Link compatibility rules ensure that device objects compiled with different toolkit versions can be linked together without errors. Specific constraints apply when kernel parameters exceed certain size thresholds.

## Large Kernel Parameter Constraint
When linking device objects, if at least one device object contains a kernel with a parameter larger than 4KB, strict versioning requirements apply [CUDA_C_Programming_Guide:L17152-L17155].

### Requirement
All device objects involved in the link must be recompiled from their respective device sources using the **CUDA Toolkit 12.1 or higher** [CUDA_C_Programming_Guide:L17152-L17155].

### Consequence of Non-Compliance
Failure to recompile all objects with the required toolkit version before linking will result in a linker error [CUDA_C_Programming_Guide:L17152-L17155].

## Best Practices
- **Uniform Toolkit Version**: To avoid compatibility issues, especially when dealing with large kernel parameters, it is recommended to use the same toolkit version for compiling all device sources within a project.
- **Upgrade Early**: If any component of the project uses kernels with parameters > 4KB, ensure the entire build environment is upgraded to CUDA 12.1+ before linking.

## References
- CUDA C++ Programming Guide, Section 18.5.10.3.3 [CUDA_C_Programming_Guide:L17152-L17155]
