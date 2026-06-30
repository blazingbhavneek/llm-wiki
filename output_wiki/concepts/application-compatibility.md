# Application Compatibility

Describes how applications load compatible binary or PTX code, compiler options (-arch, -code, -gencode), runtime code selection, and macros for differentiating code paths.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L1167-L1203

Citation: [CUDA_C_Programming_Guide:L1167-L1203]

````text
## 6.1.4. Application Compatibility

To execute code on devices of specific compute capability, an application must load binary or PTX code that is compatible with this compute capability as described in Binary Compatibility and PTX Compatibility. In particular, to be able to execute code on future architectures with higher compute capability (for which no binary code can be generated yet), an application must load PTX code that will be just-in-time compiled for these devices (see Just-in-Time Compilation).

Which PTX and binary code gets embedded in a CUDA C++ application is controlled by the -arch and -code compiler options or the -gencode compiler option as detailed in the nvcc user manual. For example,

```txt
nvcc x.cu
    -gencode arch=compute_50,code=sm_50
    -gencode arch=compute_60,code=sm_60
    -gencode arch=compute_70,code=\"compute_70,sm_70\"
```

embeds binary code compatible with compute capability 5.0 and 6.0 (first and second -gencode options) and PTX and binary code compatible with compute capability 7.0 (third -gencode option).

Host code is generated to automatically select at runtime the most appropriate code to load and execute, which, in the above example, will be:

▶ 5.0 binary code for devices with compute capability 5.0 and 5.2,

▶ 6.0 binary code for devices with compute capability 6.0 and 6.1,

▶ 7.0 binary code for devices with compute capability 7.0 and 7.5,

PTX code which is compiled to binary code at runtime for devices with compute capability later than 7.5

x.cu can have an optimized code path that uses warp reduction operations, for example, which are only supported in devices of compute capability 8.0 and higher. The \_\_CUDA\_ARCH\_\_ macro can be used to diferentiate various code paths based on compute capability. It is only defined for device code. When compiling with -arch=compute\_80 for example, \_\_CUDA\_ARCH\_\_ is equal to 800.

If x.cu is compiled for Family-Specific Features with sm\_100f or compute\_100f, the code can only run on devices in that specific family, which are devices with compute capability 10.0 and 10.3. For family-specific code targets an additional macro \_\_CUDA\_ARCH\_FAMILY\_SPECIFIC\_\_ is defined. In this example, \_\_CUDA\_ARCH\_FAMILY\_SPECIFIC\_\_ is equal to 1000.

If x.cu is compiled for Architecture-Specific Features with sm\_100a or compute\_100a, the code can only run on devices with compute capability 10.0. For architecture-specific code targets an additional macro \_\_CUDA\_ARCH\_SPECIFIC\_\_ is defined. In this example, \_\_CUDA\_ARCH\_SPECIFIC\_\_ is equal to 1000. Because architecture-specific features are a superset of family-specific features, the familyspecific macro \_\_CUDA\_ARCH\_FAMILY\_SPECIFIC\_\_ is also defined and is equal to 1000.

Applications using the driver API must compile code to separate files and explicitly load and execute the most appropriate file at runtime.

The Volta architecture introduces Independent Thread Scheduling which changes the way threads are scheduled on the GPU. For code relying on specific behavior of SIMT scheduling in previous architectures, Independent Thread Scheduling may alter the set of participating threads, leading to incorrect results. To aid migration while implementing the corrective actions detailed in Independent Thread Scheduling, Volta developers can opt-in to Pascal’s thread scheduling with the compiler option combination -arch=compute\_60 -code=sm\_70.

The nvcc user manual lists various shorthands for the -arch, -code, and -gencode compiler options. For example, -arch=sm\_70 is a shorthand for -arch=compute\_70 -code=compute\_70, sm\_70 (which is the same as -gencode arch=compute\_70,code=\"compute\_70,sm\_70\").
````
