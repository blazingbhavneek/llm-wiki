# CUDA Heterogeneous Programming

The CUDA programming model is based on a heterogeneous architecture where the CUDA threads execute on a physically separate device that operates as a coprocessor to the host running the C++ program [CUDA_C_Programming_Guide:L1047-L1053]. A common example of this configuration is when computational kernels execute on a GPU while the remainder of the C++ program executes on a CPU [CUDA_C_Programming_Guide:L1047-L1053].

## Host-Device Memory Model

The CUDA programming model assumes that both the host and the device maintain their own separate memory spaces in DRAM, referred to as host memory and device memory, respectively [CUDA_C_Programming_Guide:L1047-L1053]. Consequently, programs must manage the global, constant, and texture memory spaces visible to kernels through calls to the CUDA runtime [CUDA_C_Programming_Guide:L1047-L1053]. This management includes device memory allocation and deallocation as well as explicit data transfer between host and device memory [CUDA_C_Programming_Guide:L1047-L1053].

## Unified Memory

Unified Memory provides managed memory to bridge the host and device memory spaces [CUDA_C_Programming_Guide:L1047-L1053]. Managed memory is accessible from all CPUs and GPUs in the system as a single, coherent memory image with a common address space [CUDA_C_Programming_Guide:L1047-L1053]. This capability enables oversubscription of device memory and can greatly simplify the task of porting applications by eliminating the need to explicitly mirror data on host and device [CUDA_C_Programming_Guide:L1047-L1053].
