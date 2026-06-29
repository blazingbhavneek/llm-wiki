# C++11 Features in CUDA

The NVIDIA CUDA compiler (`nvcc`) supports C++11 features that are enabled by default by the host compiler, subject to specific restrictions [CUDA_C_Programming_Guide:L17531-L17534]. 

To enable all C++11 features, users can invoke `nvcc` with the `-std=c++11` flag. This flag not only enables the features within the CUDA code but also invokes the host preprocessor, compiler, and linker with the corresponding C++11 dialect option [CUDA_C_Programming_Guide:L17531-L17534].

## Key Points

- **Default Support**: C++11 features enabled by the host compiler are supported by `nvcc` by default, subject to restrictions.
- **Explicit Enablement**: The `-std=c++11` flag turns on all C++11 features.
- **Host Toolchain Integration**: Using `-std=c++11` ensures the host toolchain (preprocessor, compiler, linker) uses the C++11 dialect.

## References

- [CUDA_C_Programming_Guide:L17531-L17534] CUDA C++ Programming Guide, Section 18.5.22. C++11 Features.
