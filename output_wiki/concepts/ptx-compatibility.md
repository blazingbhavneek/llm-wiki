# PTX Compatibility

PTX (Parallel Thread Execution) compatibility is governed by the compute capabilities of the target hardware and the specific compiler flags used during compilation. The `-arch` compiler option specifies the compute capability assumed when compiling C++ code to PTX, ensuring that instructions used in the source code are supported by the target device.

## Instruction Support and Compute Capability

Not all PTX instructions are supported on all devices. Support is tied to specific compute capabilities. For instance, Warp Shuffle Functions are only supported on devices with compute capability 5.0 and above. Consequently, code utilizing these features must be compiled with a corresponding `-arch` flag, such as `-arch=compute_50` or higher, to ensure the generated PTX includes only supported instructions.

## Compilation and Binary Generation

PTX code generated for a specific compute capability can always be compiled into binary code for devices with a greater or equal compute capability. However, this process has limitations regarding hardware feature utilization. A binary compiled from an older PTX version may not leverage newer hardware features available on the target device. For example, a binary targeting compute capability 7.0 (Volta) compiled from PTX generated for compute capability 6.0 (Pascal) will not use Tensor Core instructions, as these were unavailable on Pascal hardware. This can result in suboptimal performance compared to binaries generated from the latest PTX version.

## Architecture-Specific and Family-Specific PTX

NVIDIA introduced specific PTX targets to manage compatibility more granularly:

### Architecture-Specific PTX

PTX code compiled to target Architecture-Specific Features (e.g., `sm_90a` or `compute_90a`) is strictly bound to the exact physical architecture. It is neither forward nor backward compatible. Code compiled with `sm_90a` will only run on devices with compute capability 9.0 and cannot run on other architectures.

### Family-Specific PTX

PTX code compiled to target Family-Specific Features (e.g., `sm_100f` or `compute_100f`) is compatible with the exact physical architecture and other architectures within the same family. This type of PTX is forward compatible with other devices in the same family but is not backward compatible. For example, code compiled with `sm_100f` runs on devices with compute capability 10.0 and 10.3.

## References

- CUDA C++ Programming Guide, Section 6.1.3: PTX Compatibility [CUDA_C_Programming_Guide:L1157-L1166]
