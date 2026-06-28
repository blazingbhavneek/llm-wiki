Example

```txt
template <typename T>
__global__ void kernel(T in) { in(); }

__host__ __device__ void foo(void) {
    // Error: the number and relative declaration
    // order of extended lambdas depends on
    // __CUDA_ARCH__
#if defined(__CUDA_ARCH__)
    auto lam1 = [] __device__ { return 0; };
    auto lam1b = [] __host__ __device__ { return 10; };
#endif
    auto lam2 = [] __device__ { return 4; };
    kernel<<<1,1>>>(lam2);
}
```

14. As described above, the CUDA compiler replaces a \_\_device\_\_ extended lambda defined in a host function with a placeholder type defined in namespace scope. Unless the trait \_\_nv\_is\_extended\_device\_lambda\_with\_preserved\_return\_type() returns true for the closure type of the extended lambda, the placeholder type does not define a operator() function equivalent to the original lambda declaration. An attempt to determine the return type or parameter types of the operator() function of such a lambda may therefore work incorrectly in host code, as the code processed by the host compiler will be semantically diferent than the input code processed by the CUDA compiler. However, it is OK to introspect the return type or parameter types of the operator() function within device code. Note that this restriction does not apply to \_\_host\_\_ \_\_device\_\_ extended lambdas, or to \_\_device\_\_ extended lambdas for which the trait \_\_nv\_is\_extended\_device\_lambda\_with\_preserved\_return\_type() returns true.

Example

```cpp
#include <type_traits>
const char& getRef(const char* p) { return *p; }

void foo(void) {
    auto lam1 = [] __device__ { return "10"; };

    // Error: attempt to extract the return type
```

(continues on next page)

(continued from previous page)

```cpp
// of a __device__ lambda in host code
std::result_of<decltype(lam1)()>::type xx1 = "abc";

auto lam2 = [] __host__ __device__ { return "10"; };

// OK : lam2 represents a __host__ __device__ extended lambda
std::result_of<decltype(lam2)()>::type xx2 = "abc";

auto lam3 = [] __device__ () -> const char * { return "10"; };

// OK : lam3 represents a __device__ extended lambda with preserved return type
std::result_of<decltype(lam3)()>::type xx2 = "abc";
static_assert( std::is_same_v< std::result_of<decltype(lam3)()>::type, const char *>

auto lam4 = [] __device__ (char x) -> decltype(getRef(&x)) { return 0; };
// lam4's return type is not preserved because it references the operator()'s
// parameter types in the trailing return type.
static_assert( ! __nv_is_extended_device_lambda_with_preserved_return_type(decltype(lam4)), "" );
}
```

15. For an extended device lambda: - Introspecting the parameter type of operator() is only supported in device code. - Introspecting the return type of operator() is supported only in device code, unless the trait function \_\_nv\_is\_extended\_device\_lambda\_with\_preserved\_return\_type() returns true.

16. If the functor object represented by an extended lambda is passed from host to device code (e.g., as the argument of a \_\_global\_\_ function), then any expression in the body of the lambda expression that captures variables must be remain unchanged irrespective of whether the \_\_CUDA\_ARCH\_\_ macro is defined, and whether the macro has a particular value. This restriction arises because the lambda’s closure class layout depends on the order in which captured variables are encountered when the compiler processes the lambda expression; the program may execute incorrectly if the closure class layout difers in device and host compilation.

Example

```lisp
__device__ int result;

template <typename T>
__global__ void kernel(T in) { result = in(); }

void foo(void) {
    int x1 = 1;
    auto lam1 = [=] __host__ __device__ {
        // Error: "x1" is only captured when __CUDA_ARCH__ is defined.
#ifdef __CUDA_ARCH__
        return x1 + 1;
#else
        return 10;
#endif
    };
    kernel<<<1,1>>>(lam1);
}
```

17. As described previously, the CUDA compiler replaces an extended \_\_device\_\_ lambda expression with an instance of a placeholder type in the code sent to the host compiler. This placeholder type does not define a pointer-to-function conversion operator in host code, however the conversion operator is provided in device code. Note that this restriction does not apply to \_\_host\_\_ \_\_device\_\_ extended lambdas.

Example

```c
template <typename T>
__global__ void kern(T in) {
  int (*fp)(double) = in;

  // OK: conversion in device code is supported
  fp(0);
  auto lam1 = [](double) { return 1; };

  // OK: conversion in device code is supported
  fp = lam1;
  fp(0);
}

void foo(void) {
  auto lam_d = [] __device__ (double) { return 1; };
  auto lam_hd = [] __host__ __device__ (double) { return 1; };
  kern<<<1,1>>>(lam_d);
  kern<<<1,1>>>(lam_hd);

  // OK : conversion for __host__ __device__ lambda is supported
  // in host code
  int (*fp)(double) = lam_hd;

  // Error: conversion for __device__ lambda is not supported in
  // host code.
  int (*fp2)(double) = lam_d;
}
```

18. As described previously, the CUDA compiler replaces an extended \_\_device\_\_ or \_\_host\_\_ \_device\_\_ lambda expression with an instance of a placeholder type in the code sent to the host compiler. This placeholder type may define C++ special member functions (e.g. constructor, destructor). As a result, some standard C++ type traits may return diferent results for the closure type of the extended lambda, in the CUDA frontend compiler versus the host compiler. The following type traits are afected: std::is\_trivially\_copyable, std::is\_trivially\_constructible, std::is\_trivially\_copy\_constructible, std::is\_trivially\_move\_constructible, std::is\_trivially\_destructible.

Care must be taken that the results of these type traits are not used in \_\_global\_\_ function template instantiation or in \_\_device\_\_ ∕ \_\_constant\_\_ ∕ \_\_managed\_\_ variable template instantiation.

Example

```txt
template <bool b>
void __global__ foo() { printf("hi"); }

template <typename T>
void dolaunch() {

// ERROR: this kernel launch may fail, because CUDA frontend compiler
// and host compiler may disagree on the result of
```

(continues on next page)

(continued from previous page)

```cpp
// std::is_trivially_copyable() trait on the closure type of the
// extended lambda
foo<std::is_trivially_copyable<T>::value<<<1,1>>>();
cudaDeviceSynchronize();
}

int main() {
int x = 0;
auto lam1 = [=] __host__ __device__ () { return x; };
dolaunch<decltype(lam1)>();
}
```

The CUDA compiler will generate compiler diagnostics for a subset of cases described in 1-12; no diagnostic will be generated for cases 13-17, but the host compiler may fail to compile the generated code.

## 18.7.3. Notes on \_\_host\_\_ \_\_device\_\_ lambdas

Unlike \_\_device\_\_ lambdas, \_\_host\_\_ \_\_device\_\_ lambdas can be called from host code. As described earlier, the CUDA compiler replaces an extended lambda expression defined in host code with an instance of a named placeholder type. The placeholder type for an extended \_\_host \_device\_\_ lambda invokes the original lambda’s operator() with an indirect function call<sup>Page</sup> <sup>458,</sup> <sup>24</sup>.

The presence of the indirect function call may cause an extended \_\_host\_\_ \_\_device\_\_ lambda to be less optimized by the host compiler than lambdas that are implicitly or explicitly \_\_host\_\_ only. In the latter case, the host compiler can easily inline the body of the lambda into the calling context. But in case of an extended \_\_host\_\_ \_\_device\_\_ lambda, the host compiler encounters the indirect function call and may not be able to easily inline the original \_\_host\_\_ \_\_device\_\_ lambda body.

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
