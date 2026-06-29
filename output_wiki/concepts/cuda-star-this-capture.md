# CUDA *this Capture Mode

CUDA *this capture mode is a feature introduced in C++17 that allows lambdas defined within non-static class member functions to capture the object instance (`*this`) by value, rather than capturing the `this` pointer by value. This mechanism prevents runtime errors that occur when a lambda executed on the GPU attempts to access member variables via a `this` pointer that points to host memory.

## Problem Context

In C++11 and C++14, when a lambda is defined within a non-static class member function and refers to a class member variable, the compiler implicitly captures the `this` pointer by value [CUDA_C_Programming_Guide:L18902-L18930]. If this lambda is an extended `__device__` or `__host__ __device__` lambda defined in host code and is subsequently executed on the GPU, accessing the referenced member variable causes a runtime error because the captured `this` pointer points to host memory, which is not accessible from the device [CUDA_C_Programming_Guide:L18902-L18930].

For example, in the following code, the lambda `lam1` captures the `this` pointer. When `foo` is launched as a kernel, it fails at runtime because `this->xxx` is not accessible from the GPU [CUDA_C_Programming_Guide:L18932-L18955]:

```cpp
struct S1_t {
  int xxx;
  __host__ __device__ S1_t(void) : xxx(10) { };

  void doit(void) {
    auto lam1 = [=] __device__ {
        // reference to "xxx" causes
        // the 'this' pointer (S1_t*) to be captured by value
        return xxx + 1;
    };
    // Kernel launch fails at run time because 'this->xxx'
    // is not accessible from the GPU
    foo<<<1,1>>>(lam1);
    cudaDeviceSynchronize();
  }
};
```

## Solution: *this Capture

C++17 resolves this issue by introducing the `*this` capture mode. In this mode, the compiler creates a copy of the object denoted by `*this` instead of capturing the pointer [CUDA_C_Programming_Guide:L18957-L18965]. When the lambda accesses a member variable, it accesses the corresponding member of the copied object on the device [CUDA_C_Programming_Guide:L18995-L18999].

### Usage

The CUDA compiler supports the `*this` capture mode for:
1. Lambdas defined within `__device__` and `__global__` functions.
2. Extended `__device__` lambdas defined in host code, provided the `--extended-lambda` nvcc flag is used [CUDA_C_Programming_Guide:L18967-L18970].

Using the `*this` capture specification allows the kernel launch to succeed, as the member variable `xxx` is copied to the device along with the lambda [CUDA_C_Programming_Guide:L18972-L18999]:

```cpp
struct S1_t {
  int xxx;
  __host__ __device__ S1_t(void) : xxx(10) { };

  void doit(void) {
    // note the "*this" capture specification
    auto lam1 = [=, *this] __device__ {
      // reference to "xxx" causes
      // the object denoted by '*this' to be captured by
      // value, and the GPU code will access copy_of_star_this->xxx
      return xxx + 1;
    };

    // Kernel launch succeeds
    foo<<<1,1>>>(lam1);
    cudaDeviceSynchronize();
  }
};
```

### Restrictions and Dialect Requirements

The `*this` capture mode is subject to specific restrictions based on the lambda's annotation and the function context:

*   **Unannotated Lambdas in Host Code**: `*this` capture is not allowed for unannotated lambdas defined in host code unless enabled by the selected language dialect [CUDA_C_Programming_Guide:L18972-L18975].
*   **Extended `__host__ __device__` Lambdas**: Using `*this` capture in an extended `__host__ __device__` lambda results in an error if `*this` capture is not enabled by the language dialect [CUDA_C_Programming_Guide:L18977-L18980].

#### Supported Scenarios

*   **Inside `__device__` Functions**: `*this` capture is allowed in lambdas defined within `__device__` functions, regardless of whether the lambda is annotated as `__device__`, `__host__ __device__`, or unannotated [CUDA_C_Programming_Guide:L18982-L18990].
*   **Inside `__host__ __device__` Functions**: `*this` capture is allowed in extended `__device__` lambdas. However, it is an error for unannotated lambdas or extended `__host__ __device__` lambdas unless the language dialect enables it [CUDA_C_Programming_Guide:L18992-L19000].

#### Unsupported Scenarios (Without Dialect Enablement)

*   **Inside `__host__` Functions**: `*this` capture is an error for unannotated lambdas and extended `__host__ __device__` lambdas unless the language dialect enables it [CUDA_C_Programming_Guide:L18977-L18980, CUDA_C_Programming_Guide:L18982-L18985].

## References

*   [CUDA_C_Programming_Guide:L18902-L19039]
*   [http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0018r3.html](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0018r3.html) [CUDA_C_Programming_Guide:L18963-L18965]
