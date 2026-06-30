# This Capture By Value

C++17 `*this` capture mode for lambdas in CUDA, solving host memory access runtime errors by copying the object instead of capturing the pointer. Covers supported contexts and dialect requirements.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L18902-L19041

Citation: [CUDA_C_Programming_Guide:L18902-L19041]

````text
## 18.7.4. \*this Capture By Value

When a lambda is defined within a non-static class member function, and the body of the lambda refers to a class member variable, C++11/C++14 rules require that the this pointer of the class is captured by value, instead of the referenced member variable. If the lambda is an extended \_\_device\_\_ or \_\_host\_\_\_\_device\_\_ lambda defined in a host function, and the lambda is executed on the GPU, accessing the referenced member variable on the GPU will cause a run time error if the this pointer points to host memory.

Example:

```c
#include <cstdio>

template <typename T>
__global__ void foo(T in) { printf("\n value = %d", in()); }

struct S1_t {
  int xxx;
  __host__ __device__ S1_t(void) : xxx(10) { };

  void doit(void) {
```

(continues on next page)

```txt
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

int main(void) {
    S1_t s1;
    s1.doit();
}
```

(continued from previous page)

C++17 solves this problem by adding a new “\*this” capture mode. In this mode, the compiler makes a copy of the object denoted by “\*this” instead of capturing the pointer this by value. The “\*this” capture mode is described in more detail here: http:∕∕www.open-std.org∕jtc1∕sc22∕wg21∕docs∕ papers∕2016∕p0018r3.html .

The CUDA compiler supports the “\*this” capture mode for lambdas defined within \_\_device\_\_ and \_\_global\_\_ functions and for extended \_\_device\_\_ lambdas defined in host code, when the --extended-lambda nvcc flag is used.

Here’s the above example modified to use “\*this” capture mode:

```cpp
#include <cstdio>

template <typename T>
__global__ void foo(T in) { printf("\n value = %d", in()); }

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

(continues on next page)

```dart
int main(void) {
    S1_t s1;
    s1.doit();
}
```

(continued from previous page)

“\*this” capture mode is not allowed for unannotated lambdas defined in host code, or for extended \_\_host\_\_\_\_device\_\_ lambdas, unless “\*this” capture is enabled by the selected language dialect. Examples of supported and unsupported usage:

```txt
struct S1_t {
    int xxx;
    __host__ __device__ S1_t(void) : xxx(10) { };

    void host_func(void) {

        // OK: use in an extended __device__ lambda
        auto lam1 = [=, *this] __device__ { return xxx; };

        // Use in an extended __host__ __device__ lambda
        // Error if *this capture not enabled by language dialect
        auto lam2 = [=, *this] __host__ __device__ { return xxx; };

        // Use in an unannotated lambda in host function
        // Error if *this capture not enabled by language dialect
        auto lam3 = [=, *this] { return xxx; };
    }

    __device__ void device_func(void) {

        // OK: use in a lambda defined in a __device__ function
        auto lam1 = [=, *this] __device__ { return xxx; };

        // OK: use in a lambda defined in a __device__ function
        auto lam2 = [=, *this] __host__ __device__ { return xxx; };

        // OK: use in a lambda defined in a __device__ function
        auto lam3 = [=, *this] { return xxx; };
    }

    __host__ __device__ void host_device_func(void) {

        // OK: use in an extended __device__ lambda
        auto lam1 = [=, *this] __device__ { return xxx; };

        // Use in an extended __host__ __device__ lambda
        // Error if *this capture not enabled by language dialect
        auto lam2 = [=, *this] __host__ __device__ { return xxx; };

        // Use in an unannotated lambda in a __host__ __device__ function
        // Error if *this capture not enabled by language dialect
        auto lam3 = [=, *this] { return xxx; };
    }
};
```

## 18.7.5. Additional Notes
````
