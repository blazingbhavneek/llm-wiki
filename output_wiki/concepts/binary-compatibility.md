# Binary Compatibility

Details architecture-specific binary code generation, cubin objects, and compatibility guarantees across minor and major compute capability revisions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L1151-L1166

Citation: [CUDA_C_Programming_Guide:L1151-L1166]

````text
## 6.1.2. Binary Compatibility

Binary code is architecture-specific. A cubin object is generated using the compiler option -code that specifies the targeted architecture: For example, compiling with -code=sm\_80 produces binary code for devices of compute capability 8.0. Binary compatibility is guaranteed from one minor revision to the next one, but not from one minor revision to the previous one or across major revisions. In other words, a cubin object generated for compute capability X.y will only execute on devices of compute capability X.z where zfiy.

Note: Binary compatibility is supported only for the desktop. It is not supported for Tegra. Also, the binary compatibility between desktop and Tegra is not supported.

## 6.1.3. PTX Compatibility

Some PTX instructions are only supported on devices of higher compute capabilities. For example, Warp Shufle Functions are only supported on devices of compute capability 5.0 and above. The -arch compiler option specifies the compute capability that is assumed when compiling C++ to PTX code. So, code that contains warp shufle, for example, must be compiled with -arch=compute\_50 (or higher).

PTX code produced for some specific compute capability can always be compiled to binary code of greater or equal compute capability. Note that a binary compiled from an earlier PTX version may not make use of some hardware features. For example, a binary targeting devices of compute capability 7.0 (Volta) compiled from PTX generated for compute capability 6.0 (Pascal) will not make use of Tensor Core instructions, since these were not available on Pascal. As a result, the final binary may perform worse than would be possible if the binary were generated using the latest version of PTX.

PTX code compiled to target Architecture-Specific Features only runs on the exact same physical architecture and nowhere else. Architecture-specific PTX code is not forward and backward compatible. Example code compiled with sm\_90a or compute\_90a only runs on devices with compute capability 9.0 and is not backward or forward compatible.

PTX code compiled to target Family-Specific Features only runs on the exact same physical architecture and other architectures in the same family. Family-specific PTX code is forward compatible with other devices in the same family, and is not backward compatible. Example code compiled with sm\_100f or compute\_100f only runs on devices with compute capability 10.0 and 10.3. Table 25 shows the compatibility of family-specific targets with compute capability.
````
