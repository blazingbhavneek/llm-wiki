
```txt
__constant__ int x2b;                     // error
        __shared__ int x3b;                       // error

        texture<int> q2;                            // error
        surface<int> s2;                            // error
    }
};
```

## 18.5.22.7 thread\_local

The thread\_local storage specifier is not allowed in device code.

## 18.5.22.8 \_\_global\_\_ functions and function templates

If the closure type associated with a lambda expression is used in a template argument of a \_\_global\_\_ function template instantiation, the lambda expression must either be defined in the immediate or nested block scope of a \_\_device\_\_ or \_\_global\_\_ function, or must be an extended lambda.

Example:

```cpp
template <typename T>
__global__ void kernel(T in) { }

__device__ void foo_device(void)
{
    // All kernel instantiations in this function
    // are valid, since the lambdas are defined inside
    // a __device__ function.

    kernel<<<1,1>>>( [] __device__ { } );
    kernel<<<1,1>>>( [] __host__ __device__ { } );
    kernel<<<1,1>>>( [] { } );
}

auto lam1 = [] { };

auto lam2 = [] __host__ __device__ { };

void foo_host(void)
{
    // OK: instantiated with closure type of an extended __device__ lambda
    kernel<<<1,1>>>( [] __device__ { } );

    // OK: instantiated with closure type of an extended __host__ __device__
    // lambda
    kernel<<<1,1>>>( [] __host__ __device__ { } );

    // error: unsupported: instantiated with closure type of a lambda
    // that is not an extended lambda
    kernel<<<1,1>>>( [] { } );

    // error: unsupported: instantiated with closure type of a lambda
```

(continued from previous page)

```txt
// that is not an extended lambda
kernel<<<1,1>>>( lam1);

// error: unsupported: instantiated with closure type of a lambda
// that is not an extended lambda
kernel<<<1,1>>>( lam2);
```

A \_\_global\_\_ function or function template cannot be declared as constexpr.

A \_\_global\_\_ function or function template cannot have a parameter of type std::initializer\_list or va\_list.

A \_\_global\_\_ function cannot have a parameter of rvalue reference type.

A variadic \_\_global\_\_ function template has the following restrictions:

▶ Only a single pack parameter is allowed.

The pack parameter must be listed last in the template parameter list.

## Example:

```lisp
// ok
template <template <typename...> class Wrapper, typename... Pack>
__global__ void foo1(Wrapper<Pack...>);

// error: pack parameter is not last in parameter list
template <typename... Pack, template <typename...> class Wrapper>
__global__ void foo2(Wrapper<Pack...>);

// error: multiple parameter packs
template <typename... Pack1, int...Pack2, template<typename...> class Wrapper1,
    template<int...> class Wrapper2>
__global__ void foo3(Wrapper1<Pack1...>, Wrapper2<Pack2...>);
```

## 18.5.22.9 \_\_managed\_\_ and \_\_shared\_\_ variables

\`\_\_managed\_\_ and \_\_shared\_\_ variables cannot be marked with the keyword constexpr.

## 18.5.22.10 Defaulted functions

Execution space specifiers on a non-virtual function that is explicitly-defaulted on its first declaration are ignored by the CUDA compiler. Instead, the CUDA compiler will infer the execution space specifiers as described in Implicitly-declared and non-virtual explicitly-defaulted functions.

Execution space specifiers are not ignored if the function is either:

▶ Explicitly-defaulted but not on its first declaration.

▶ Explicitly-defaulted and virtual.

## Example:

```solidity
struct S1 {
  // warning: __host__ annotation is ignored on a non-virtual function that
  //          is explicitly-defaulted on its first declaration
```

(continues on next page)

(continued from previous page)

```cpp
__host__ S1() = default;
};

__device__ void foo1() {
    //note: __device__ execution space is derived for S1::S1
    //      based on implicit call from within __device__ function
    //      foo1
    S1 s1;
}

struct S2 {
    __host__ S2();
};

//note: S2::S2 is not defaulted on its first declaration, and
//      its execution space is fixed to __host__  based on its
//      first declaration.
S2::S2() = default;

__device__ void foo2() {
    // error: call from __device__ function 'foo2' to
    //      __host__ function 'S2::S2'
    S2 s2;
}

struct S3 {
    //note: S3::~S3 has __host__ execution space
    virtual __host__ ~S3() = default;
};

__device__ void foo3() {
    S3 qqq;
}  /*(implicit destructor call for 'qqq'):
        error: call from a __device__ fuction 'foo3' to a
        __host__ function 'S3::~S3' */
```

## 18.5.23. C++14 Features

C++14 features enabled by default by the host compiler are also supported by nvcc. Passing nvcc -std=c++14 flag turns on all C++14 features and also invokes the host preprocessor, compiler and linker with the corresponding C++14 dialect option<sup>20</sup>. This section describes the restrictions on the supported C++14 features.

## 18.5.23.1 Functions with deduced return type

A \_\_global\_\_ function cannot have a deduced return type.

If a \_\_device\_\_ function has deduced return type, the CUDA frontend compiler will change the function declaration to have a void return type, before invoking the host compiler. This may cause issues for introspecting the deduced return type of the \_\_device\_\_ function in host code. Thus, the CUDA compiler will issue compile-time errors for referencing such deduced return type outside device function bodies, except if the reference is absent when \_\_CUDA\_ARCH\_\_ is undefined.

Examples:

```c
__device__ auto fn1(int x) {
    return x;
}

__device__ decltype(auto) fn2(int x) {
    return x;
}

__device__ void device_fn1() {
    // OK
    int (*p1)(int) = fn1;
}

// error: referenced outside device function bodies
decltype(fn1(10)) g1;

void host_fn1() {
    // error: referenced outside device function bodies
    int (*p1)(int) = fn1;

    struct S_local_t {
        // error: referenced outside device function bodies
        decltype(fn2(10)) m1;

        S_local_t() : m1(10) { }
    };
}

// error: referenced outside device function bodies
template <typename T = decltype(fn2)>
void host_fn2() { }

template<typename T> struct S1_t { };

// error: referenced outside device function bodies
struct S1_derived_t : S1_t<decltype(fn1)> { };
```

## 18.5.23.2 Variable templates

A \_\_device\_\_∕\_\_constant\_\_ variable template cannot have a const qualified type when using the Microsoft host compiler.

Examples:

```c
// error: a __device__ variable template cannot
// have a const qualified type on Windows
template <typename T>
__device__ const T d1(2);

int *const x = nullptr;
// error: a __device__ variable template cannot
// have a const qualified type on Windows
template <typename T>
__device__ T *const d2(x);

// OK
template <typename T>
__device__ const T *d3;

__device__ void fn() {
    int t1 = d1<int>;

    int *const t2 = d2<int>;

    const int *t3 = d3<int>;
}
```

## 18.5.24. C++17 Features

C++17 features enabled by default by the host compiler are also supported by nvcc. Passing nvcc -std=c++17 flag turns on all C++17 features and also invokes the host preprocessor, compiler and linker with the corresponding C++17 dialect option<sup>21</sup>. This section describes the restrictions on the supported C++17 features.

## 18.5.24.1 Inline Variable

▶ A namespace scope inline variable declared with \_\_device\_\_ or \_\_constant\_\_ or \_\_managed\_\_ memory space specifier must have internal linkage, if the code is compiled with nvcc in whole program compilation mode.

Examples:

```txt
inline __device__ int xxx; //error when compiled with nvcc in
//whole program compilation mode.
//ok when compiled with nvcc in
//separate compilation mode.

inline __shared__ int yyyy0; // ok.
```

(continues on next page)

(continued from previous page)

```txt
static inline __device__ int yyy; // ok: internal linkage
namespace {
inline __device__ int zzz; // ok: internal linkage
}
```

▶ When using g++ host compiler, an inline variable declared with \_\_managed\_\_ memory space specifier may not be visible to the debugger.

## 18.5.24.2 Structured Binding

A structured binding cannot be declared with a variable memory space specifier.

Example:

```c
struct S { int x; int y; };
__device__ auto [a1, b1] = S{4,5}; // error
```

## 18.5.25. C++20 Features
