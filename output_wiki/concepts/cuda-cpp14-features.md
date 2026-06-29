# C++14 Features in CUDA

CUDA's `nvcc` compiler supports C++14 features that are enabled by default by the host compiler [CUDA_C_Programming_Guide:L17901-L17904]. To enable these features, users must pass the `-std=c++14` flag to `nvcc` [CUDA_C_Programming_Guide:L17901-L17904].

When this flag is used, `nvcc` not only enables C++14 features for device code but also invokes the host preprocessor, compiler, and linker with the corresponding C++14 dialect option [CUDA_C_Programming_Guide:L17901-L17904]. This ensures consistency between the host and device compilation environments regarding C++14 support [CUDA_C_Programming_Guide:L17901-L17904].

The CUDA C++ Programming Guide notes that there are specific restrictions on the supported C++14 features, which are detailed in the relevant section of the documentation [CUDA_C_Programming_Guide:L17901-L17904].
