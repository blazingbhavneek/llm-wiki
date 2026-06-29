# cuda::pipeline Interface Requirements

The `cuda::pipeline` interface is part of the CUDA C++ library (libcudacxx) and provides asynchronous memory copy capabilities, such as `cuda::memcpy_async`. To use this C++ interface, the following requirements must be met:

*   **CUDA Version**: At least CUDA 11.0 is required [CUDA_C_Programming_Guide:L10136-L10147].
*   **C++ Standard**: The code must be compiled with at least ISO C++ 2011 compatibility (e.g., using the `-std=c++11` compiler flag) [CUDA_C_Programming_Guide:L10136-L10147].
*   **Header Inclusion**: The `<cuda/pipeline>` header must be included in the source file [CUDA_C_Programming_Guide:L10136-L10147].

For environments that do not support ISO C++ 2011, a C-like interface is available via the Pipeline Primitives Interface [CUDA_C_Programming_Guide:L10136-L10147].
