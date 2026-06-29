# Lazy Loading Version Support

Lazy Loading is a feature of the CUDA Runtime and CUDA Driver. Utilizing this feature may require upgrades to both the runtime and driver components [CUDA_C_Programming_Guide:L22092-L22094].

## Driver Requirements

Lazy Loading requires the R515+ user-mode library. While it supports Forward Compatibility, allowing it to run on top of older kernel mode drivers, the feature is unavailable without the R515+ user-mode library, regardless of the toolkit version [CUDA_C_Programming_Guide:L22096-L22101].

## Toolkit Requirements

Lazy Loading was introduced in CUDA 11.7 and received significant upgrades in CUDA 11.8 [CUDA_C_Programming_Guide:L22103-L22104].

To realize the benefits of Lazy Loading when using the CUDA Runtime, an application must utilize CUDA 11.7+ Runtime [CUDA_C_Programming_Guide:L22106-L22107]. Since the CUDA Runtime is typically linked statically into programs and libraries, this necessitates recompiling the program with the CUDA 11.7+ toolkit and using CUDA 11.7+ libraries [CUDA_C_Programming_Guide:L22109-L22111]. If the driver version supports Lazy Loading but the application uses an older runtime, the benefits will not be observed [CUDA_C_Programming_Guide:L22112-L22113].

If only a subset of an application's libraries are built with CUDA 11.7+, Lazy Loading benefits will only apply to those specific libraries. Other libraries will continue to load resources eagerly [CUDA_C_Programming_Guide:L22115-L22117].

## Compiler Support

Lazy Loading does not require any specific compiler support [CUDA_C_Programming_Guide:L22119-L22120]. SASS and PTX code compiled with pre-11.7 compilers can be loaded with Lazy Loading enabled and will receive the full benefits of the feature [CUDA_C_Programming_Guide:L22120-L22122]. However, the requirement for CUDA 11.7+ CUDA Runtime still applies [CUDA_C_Programming_Guide:L22123-L22124].
