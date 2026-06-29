# CUDA Programming Interface

The CUDA Programming Interface provides a straightforward mechanism for developers familiar with the C++ programming language to write programs that execute on the GPU device. This interface is designed to minimize the learning curve by leveraging existing C++ knowledge.

The interface consists of two primary components:

1. **C++ Language Extensions**: A minimal set of extensions to the standard C++ language that allow for the definition of kernels and device-side functions.
2. **Runtime Library**: A library that manages the execution of these programs on the device, handling tasks such as memory management and kernel launch.

This combination allows users to easily transition from host-side C++ development to heterogeneous computing without requiring a complete paradigm shift in programming style [CUDA_C_Programming_Guide:L1107-L1109].

## See Also

* CUDA C++ Extensions
* CUDA Runtime
