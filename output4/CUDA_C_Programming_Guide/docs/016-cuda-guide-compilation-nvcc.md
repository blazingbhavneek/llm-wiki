Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

CUDA C++ provides a simple path for users familiar with the C++ programming language to easily write programs for execution by the device.

It consists of a minimal set of extensions to the C++ language and a runtime library.

The core language extensions have been introduced in Programming Model. They allow programmers to define a kernel as a C++ function and use some new syntax to specify the grid and block dimension each time the function is called. A complete description of all extensions can be found in C++ Language Extensions. Any source file that contains some of these extensions must be compiled with nvcc as outlined in Compilation with NVCC.

The runtime is introduced in CUDA Runtime. It provides C and C++ functions that execute on the host to allocate and deallocate device memory, transfer data between host memory and device memory, manage systems with multiple devices, etc. A complete description of the runtime can be found in the CUDA reference manual.

The runtime is built on top of a lower-level C API, the CUDA driver API, which is also accessible by the application. The driver API provides an additional level of control by exposing lower-level concepts such as CUDA contexts - the analogue of host processes for the device - and CUDA modules - the analogue of dynamically loaded libraries for the device. Most applications do not use the driver API as they do not need this additional level of control and when using the runtime, context and module management are implicit, resulting in more concise code. As the runtime is interoperable with the driver API, most applications that need some driver API features can default to use the runtime API and only use the driver API where needed. The driver API is introduced in Driver API and fully described in the reference manual.

## 6.1. Compilation with NVCC

Kernels can be written using the CUDA instruction set architecture, called PTX, which is described in the PTX reference manual. It is however usually more efective to use a high-level programming language such as C++. In both cases, kernels must be compiled into binary code by nvcc to execute on the device.

nvcc is a compiler driver that simplifies the process of compiling C++ or PTX code: It provides simple and familiar command line options and executes them by invoking the collection of tools that implement the diferent compilation stages. This section gives an overview of nvcc workflow and command options. A complete description can be found in the nvcc user manual.

## 6.1.1. Compilation Workflow

## 6.1.1.1 Ofline Compilation

Source files compiled with nvcc can include a mix of host code (i.e., code that executes on the host) and device code (i.e., code that executes on the device). nvcc’s basic workflow consists in separating device code from host code and then:

▶ compiling the device code into an assembly form (PTX code) and/or binary form (cubin object),

▶ and modifying the host code by replacing the <<<...>>> syntax introduced in Kernels (and described in more details in Execution Configuration) by the necessary CUDA runtime function calls to load and launch each compiled kernel from the PTX code and/or cubin object.

The modified host code is output either as C++ code that is left to be compiled using another tool or as object code directly by letting nvcc invoke the host compiler during the last compilation stage.

Applications can then:

Either link to the compiled host code (this is the most common case),

▶ Or ignore the modified host code (if any) and use the CUDA driver API (see Driver API) to load and execute the PTX code or cubin object.

## 6.1.1.2 Just-in-Time Compilation

Any PTX code loaded by an application at runtime is compiled further to binary code by the device driver. This is called just-in-time compilation. Just-in-time compilation increases application load time, but allows the application to benefit from any new compiler improvements coming with each new device driver. It is also the only way for applications to run on devices that did not exist at the time the application was compiled, as detailed in Application Compatibility.

When the device driver just-in-time compiles some PTX code for some application, it automatically caches a copy of the generated binary code in order to avoid repeating the compilation in subsequent invocations of the application. The cache - referred to as compute cache - is automatically invalidated when the device driver is upgraded, so that applications can benefit from the improvements in the new just-in-time compiler built into the device driver.

Environment variables are available to control just-in-time compilation as described in CUDA Environment Variables

As an alternative to using nvcc to compile CUDA C++ device code, NVRTC can be used to compile CUDA C++ device code to PTX at runtime. NVRTC is a runtime compilation library for CUDA C++; more information can be found in the NVRTC User guide.

## 6.1.2. Binary Compatibility

Binary code is architecture-specific. A cubin object is generated using the compiler option -code that specifies the targeted architecture: For example, compiling with -code=sm\_80 produces binary code for devices of compute capability 8.0. Binary compatibility is guaranteed from one minor revision to the next one, but not from one minor revision to the previous one or across major revisions. In other words, a cubin object generated for compute capability X.y will only execute on devices of compute capability X.z where zfiy.

Note: Binary compatibility is supported only for the desktop. It is not supported for Tegra. Also, the binary compatibility between desktop and Tegra is not supported.

## 6.1.3. PTX Compatibility

Some PTX instructions are only supported on devices of higher compute capabilities. For example, Warp Shufle Functions are only supported on devices of compute capability 5.0 and above. The -arch compiler option specifies the compute capability that is assumed when compiling C++ to PTX code. So, code that contains warp shufle, for example, must be compiled with -arch=compute\_50 (or higher).

PTX code produced for some specific compute capability can always be compiled to binary code of greater or equal compute capability. Note that a binary compiled from an earlier PTX version may not make use of some hardware features. For example, a binary targeting devices of compute capability 7.0 (Volta) compiled from PTX generated for compute capability 6.0 (Pascal) will not make use of Tensor Core instructions, since these were not available on Pascal. As a result, the final binary may perform worse than would be possible if the binary were generated using the latest version of PTX.

PTX code compiled to target Architecture-Specific Features only runs on the exact same physical architecture and nowhere else. Architecture-specific PTX code is not forward and backward compatible. Example code compiled with sm\_90a or compute\_90a only runs on devices with compute capability 9.0 and is not backward or forward compatible.

PTX code compiled to target Family-Specific Features only runs on the exact same physical architecture and other architectures in the same family. Family-specific PTX code is forward compatible with other devices in the same family, and is not backward compatible. Example code compiled with sm\_100f or compute\_100f only runs on devices with compute capability 10.0 and 10.3. Table 25 shows the compatibility of family-specific targets with compute capability.

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

## 6.1.5. C++ Compatibility

The front end of the compiler processes CUDA source files according to C++ syntax rules. Full C++ is supported for the host code. However, only a subset of C++ is fully supported for the device code as described in C++ Language Support.

## 6.1.6. 64-Bit Compatibility

The 64-bit version of nvcc compiles device code in 64-bit mode (i.e., pointers are 64-bit). Device code compiled in 64-bit mode is only supported with host code compiled in 64-bit mode.
