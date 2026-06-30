# CUDA Dynamic Parallelism Performance

Performance overheads associated with dynamic parallelism-enabled kernels and system software.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14208-L14219

Citation: [CUDA_C_Programming_Guide:L14208-L14219]

````text

This program may be built in a single step from the command line as follows:

```shell
$ nvcc -arch=sm_75 -rdc=true hello_world.cu -o hello -lcudadevrt
```

## 13.4.2. Performance

## 13.4.2.1 Dynamic-parallelism-enabled Kernel Overhead

System software which is active when controlling dynamic launches may impose an overhead on any kernel which is running at the time, whether or not it invokes kernel launches of its own. This overhead arises from the device runtime’s execution tracking and management software and may result in decreased performance. This overhead is, in general, incurred for applications that link against the device runtime library.
````
