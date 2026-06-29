# std::initializer_list in CUDA

By default, the CUDA compiler implicitly treats the member functions of `std::initializer_list` as having `__host__ __device__` execution space specifiers. This allows these member functions to be invoked directly from device code [CUDA_C_Programming_Guide:L17592-L17614].

## Configuration

The behavior of `std::initializer_list` in device code can be modified using the `nvcc` compiler flag `--no-host-device-initializer-list`. When this flag is enabled:

*   Member functions of `std::initializer_list` are considered `__host__` only.
*   They are no longer directly invokable from device code [CUDA_C_Programming_Guide:L17592-L17614].

## Example Usage

The following example demonstrates the use of `std::initializer_list` within a `__device__` function:

```cpp
#include <initializer_list>

__device__ int foo(std::initializer_list<int> in);

__device__ void bar(void)
{
    foo({4,5,6});    // (a) initializer list containing only
        // constant expressions.

    int i = 4;
    foo({i,5,6});    // (b) initializer list with at least one
        // non-constant element.
        // This form may have better performance than (a).
}
```

In this context, both constant and non-constant initializer lists can be passed to device functions, provided the default `__host__ __device__` behavior is active [CUDA_C_Programming_Guide:L17592-L17614].
