# Toolkit and Driver Compatibility

Requirements for 12.1 Toolkit/r530 driver+ for kernels with >4KB parameters, and link compatibility rules across toolkit revisions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17149-L17155

Citation: [CUDA_C_Programming_Guide:L17149-L17155]

````text
## 18.5.10.3.2 Toolkit and Driver Compatibility

Developers must use the 12.1 Toolkit and r530 driver or higher to compile, launch, and debug kernels that accept parameters larger than 4KB. If such kernels are launched on older drivers, CUDA will issue the error CUDA\_ERROR\_NOT\_SUPPORTED.

## 18.5.10.3.3 Link Compatibility across Toolkit Revisions

When linking device objects, if at least one device object contains a kernel with a parameter larger than 4KB, the developer must recompile all objects from their respective device sources with the 12.1 toolkit or higher before linking them together. Failure to do so will result in a linker error.
````
