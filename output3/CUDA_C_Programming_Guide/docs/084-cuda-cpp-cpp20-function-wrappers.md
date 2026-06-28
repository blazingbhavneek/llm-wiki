
C++20 features enabled by default by the host compiler are also supported by nvcc. Passing nvcc -std=c++20 flag turns on all C++20 features and also invokes the host preprocessor, compiler and linker with the corresponding C++20 dialect option<sup>22</sup>. This section describes the restrictions on the supported C++20 features.

## 18.5.25.1 Module support

Modules are not supported in CUDA C++, in either host or device code. Uses of the module, export and import keywords are diagnosed as errors.

## 18.5.25.2 Coroutine support

Coroutines are not supported in device code. Uses of the co\_await, co\_yield and co\_return keywords in the scope of a device function are diagnosed as error during device compilation.

## 18.5.25.3 Three-way comparison operator

The three-way comparison operator is supported in both host and device code, but some uses implicitly rely on functionality from the Standard Template Library provided by the host implementation. Uses of those operators may require specifying the flag --expt-relaxed-constexpr to silence warnings and the functionality requires that the host implementation satisfies the requirements of device code.

Example:

```cpp
#include<compare>
struct S {
    int x, y, z;
    auto operator<=>(const S& rhs) const = default;
    __host__ __device__ bool operator<=>(int rhs) const { return false; }
};
__host__ __device__ bool f(S a, S b) {
    if (a <=> 1) // ok, calls a user-defined host-device overload
        return true;
    return a < b; // call to an implicitly-declared function and requires
        // a device-compatible std::strong_ordering implementation
}
```

## 18.5.25.4 Consteval functions

Ordinarily, cross execution space calls are not allowed, and cause a compiler diagnostic (warning or error). This restriction does not apply when the called function is declared with the consteval specifier. Thus, a \_\_device\_\_ or \_\_global\_\_ function can call a \_\_host\_\_consteval function, and a \_\_host\_\_ function can call a \_\_device\_\_ consteval function.

Example:

```cpp
namespace N1 {
//consteval host function
consteval int hcallee() { return 10; }

__device__ int dfunc() { return hcallee(); /* OK */ }
__global__ void gfunc() { (void)hcallee(); /* OK */ }
__host__ __device__ int hdfunc() { return hcallee(); /* OK */ }
int hfunc() { return hcallee(); /* OK */ }
} // namespace N1

namespace N2 {
//consteval device function
consteval __device__ int dcallee() { return 10; }

__device__ int dfunc() { return dcallee(); /* OK */ }
__global__ void gfunc() { (void)dcallee(); /* OK */ }
__host__ __device__ int hdfunc() { return dcallee(); /* OK */ }
int hfunc() { return dcallee(); /* OK */ }
}
```

## 18.6. Polymorphic Function Wrappers

A polymorphic function wrapper class template nvstd::function is provided in the nvfunctional header. Instances of this class template can be used to store, copy and invoke any callable target, e.g., lambda expressions. nvstd::function can be used in both host and device code.

Example:

```cpp
#include <nvfunctional>

__device__ int foo_d() { return 1; }
__host__ __device__ int foo_hd () { return 2; }
__host__ int foo_h() { return 3; }

__global__ void kernel(int *result) {
    nvstd::function<int()> fn1 = foo_d;
    nvstd::function<int()> fn2 = foo_hd;
    nvstd::function<int()> fn3 = []() { return 10; };

    *result = fn1() + fn2() + fn3();
}

__host__ __device__ void hostdevice_func(int *result) {
    nvstd::function<int()> fn1 = foo_hd;
    nvstd::function<int()> fn2 = []() { return 10; };

    *result = fn1() + fn2();
}

__host__ void host_func(int *result) {
    nvstd::function<int()> fn1 = foo_h;
    nvstd::function<int()> fn2 = foo_hd;
    nvstd::function<int()> fn3 = []() { return 10; };

    *result = fn1() + fn2() + fn3();
}
```

Instances of nvstd::function in host code cannot be initialized with the address of a \_\_device\_\_ function or with a functor whose operator() is a \_\_device\_\_ function. Instances of nvstd::function in device code cannot be initialized with the address of a \_\_host\_\_ function or with a functor whose operator() is a \_\_host\_\_ function.

nvstd::function instances cannot be passed from host code to device code (and vice versa) at run time. nvstd::function cannot be used in the parameter type of a \_\_global\_\_ function, if the \_\_global\_\_ function is launched from host code.

Example:

```cpp
#include <nvfunctional>

__device__ int foo_d() { return 1; }
__host__ int foo_h() { return 3; }
auto lam_h = [] { return 0; };

__global__ void k(void) {
    // error: initialized with address of __host__ function
    nvstd::function<int()> fn1 = foo_h;

    // error: initialized with address of functor with
    // __host__ operator() function
    nvstd::function<int()> fn2 = lam_h;
}

__global__ void kern(nvstd::function<int()> f1) { }

void foo(void) {
```

```cpp
// error: initialized with address of __device__ function
nvstd::function<int()> fn1 = foo_d;

auto lam_d = [=] __device__ { return 1; };

// error: initialized with address of functor with
// __device__ operator() function
nvstd::function<int()> fn2 = lam_d;

// error: passing nvstd::function from host to device
kern<<<1,1>>>(fn2);
}
```

(continued from previous page)

nvstd::function is defined in the nvfunctional header as follows:

```txt
namespace nvstd {
  template <class _RetType, class ..._ArgTypes>
  class function<_RetType(_ArgTypes...)>
  {
    public:
      // constructors
      __device__ __host__ function() noexcept;
      __device__ __host__ function(nullptr_t) noexcept;
      __device__ __host__ function(const function &);
      __device__ __host__ function(function &&);

      template<class _F>
      __device__ __host__ function(_F);

      // destructor
      __device__ __host__ ~function();

      // assignment operators
      __device__ __host__ function& operator=(const function&);
      __device__ __host__ function& operator=(function&&);
      __device__ __host__ function& operator=(nullptr_t);
      __device__ __host__ function& operator=(_F&&);

      // swap
      __device__ __host__ void swap(function&) noexcept;

      // function capacity
      __device__ __host__ explicit operator bool() const noexcept;

      // function invocation
      __device__ _RetType operator()(_ArgTypes...) const;
  };

  // null pointer comparisons
  template <class _R, class... _ArgTypes>
  __device__ __host__
  bool operator==(const function<_R(_ArgTypes...)>&, nullptr_t) noexcept;

  template <class _R, class... _ArgTypes>
  __device__ __host__
  bool operator==(nullptr_t, const function<_R(_ArgTypes...)>&) noexcept;
```

(continues on next page)

```cpp
template <class _R, class... _ArgTypes>
__device__ __host__
bool operator!=(const function<_R(_ArgTypes...)>&, nullptr_t) noexcept;

template <class _R, class... _ArgTypes>
__device__ __host__
bool operator!=(nullptr_t, const function<_R(_ArgTypes...)>&) noexcept;

// specialized algorithms
template <class _R, class... _ArgTypes>
__device__ __host__
void swap(function<_R(_ArgTypes...)>&, function<_R(_ArgTypes...)>&);
}
```
