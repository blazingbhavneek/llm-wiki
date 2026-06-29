# CUDA Toolkit Compilation and Linking

When compiling and linking CUDA programs that utilize dynamic parallelism using the NVIDIA CUDA Compiler (`nvcc`), the build process automatically handles linking against the static device runtime library, `libcudadevrt` [CUDA_C_Programming_Guide:L14126-L14146].

## Device Runtime Library

The device runtime is provided as a static library. The file extension depends on the host operating system:

*   **Windows**: `cudadevrt.lib`
*   **Linux**: `libcudadevrt.a`

Any GPU application that uses the device runtime must be linked against this library [CUDA_C_Programming_Guide:L14126-L14146]. Linking of device libraries can be accomplished through `nvcc` or `nvlink` [CUDA_C_Programming_Guide:L14126-L14146].

## Compilation Examples

### Single-Step Compilation and Linking

A device runtime program may be compiled and linked in a single step if all required source files can be specified from the command line. The following example compiles `hello_world.cu` for the `sm_75` architecture and links it against `libcudadevrt`:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

### Two-Stage Compilation and Linking

It is also possible to perform compilation and linking in two stages. First, compile the CUDA `.cu` source files into object files using the `-dc` (device compilation) flag. Then, link these object files together [CUDA_C_Programming_Guide:L14126-L14146]:

```shell
$ nvcc -arch=sm_75 -dc hello_world.cu -o hello_world.o
$ nvcc -arch=sm_75 -rdc=true hello_world.o -o hello -lcudadevrt
```

For more details on separate compilation, refer to the "Using Separate Compilation" section of *The CUDA Driver Compiler NVCC* guide [CUDA_C_Programming_Guide:L14126-L14146].
