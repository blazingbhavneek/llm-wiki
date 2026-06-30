# CUDA C++ Language Restrictions and Features

This section details the support and restrictions for various C++ language features within CUDA, including class members, templates, const-qualified variables, attributes (deprecated, noreturn, likely/unlikely, const/pure), and specific C++11 and C++14 features such as lambda expressions, constexpr, inline namespaces, and variable templates. It also covers platform-specific constraints like those for the Microsoft and Intel host compilers.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17267-L17983

Citation: [CUDA_C_Programming_Guide:L17267-L17983]

````text
## 18.5.10.8 Operator Function

An operator function cannot be a \_\_global\_\_ function.

## 18.5.10.9 Allocation and Deallocation Functions

A user-defined operator new, operator new[], operator delete, or operator delete[] cannot be used to replace the corresponding \_\_host\_\_ or \_\_device\_\_ builtins provided by the compiler.

## 18.5.11. Classes

## 18.5.11.1 Data Members

Static data members are not supported except for those that are also const-qualified (see Constqualified variables).

## 18.5.11.2 Function Members

Static member functions cannot be \_\_global\_\_ functions.

## 18.5.11.3 Virtual Functions

When a function in a derived class overrides a virtual function in a base class, the execution space specifiers (i.e., \_\_host\_\_, \_\_device\_\_) on the overridden and overriding functions must match.

It is not allowed to pass as an argument to a \_\_global\_\_ function an object of a class with virtual functions.

If an object is created in host code, invoking a virtual function for that object in device code has undefined behavior.

If an object is created in device code, invoking a virtual function for that object in host code has undefined behavior.

See Windows-Specific for additional constraints when using the Microsoft host compiler.

Example:

```txt
struct S1 { virtual __host__ __device__ void foo() { } };

__managed__ S1 *ptr1, *ptr2;

__managed__ __align__(16) char buf1[128];
__global__ void kern() {
    ptr1->foo();      // error: virtual function call on a object
                        //          created in host code.
    ptr2 = new(buf1) S1();
}

int main(void) {
    void *buf;
    cudaMallocManaged(&buf, sizeof(S1), cudaMemAttachGlobal);
    ptr1 = new (buf) S1();
    kern<<<1,1>>>();
    cudaDeviceSynchronize();
    ptr2->foo();  // error: virtual function call on an object
                        //          created in device code.
}
```

## 18.5.11.4 Virtual Base Classes

It is not allowed to pass as an argument to a \_\_global\_\_ function an object of a class derived from virtual base classes.

See Windows-Specific for additional constraints when using the Microsoft host compiler.

## 18.5.11.5 Anonymous Unions

Member variables of a namespace scope anonymous union cannot be referenced in a \_\_global\_\_ or \_\_device\_\_ function.

## 18.5.11.6 Windows-Specific

The CUDA compiler follows the IA64 ABI for class layout, while the Microsoft host compiler does not. Let T denote a pointer to member type, or a class type that satisfies any of the following conditions:

▶ T has virtual functions.

▶ T has a virtual base class.

▶ T has multiple inheritance with more than one direct or indirect empty base class.

All direct and indirect base classes B of T are empty and the type of the first field F of T uses B in its definition, such that B is laid out at ofset 0 in the definition of F.

Let C denote T or a class type that has T as a field type or as a base class type. The CUDA compiler may compute the class layout and size diferently than the Microsoft host compiler for the type C.

As long as the type C is used exclusively in host or device code, the program should work correctly.

Passing an object of type C between host and device code has undefined behavior, for example, as an argument to a \_\_global\_\_ function or through cudaMemcpy\*() calls.

Accessing an object of type C or any subobject in device code, or invoking a member function in device code, has undefined behavior if the object is created in host code.

Accessing an object of type C or any subobject in host code, or invoking a member function in host code, has undefined behavior if the object is created in device code<sup>12</sup>.

## 18.5.12. Templates

A type or template cannot be used in the type, non-type or template template argument of a \_\_global\_\_ function template instantiation or a \_\_device\_\_∕\_\_constant\_\_ variable instantiation if either:

▶ The type or template is defined within a \_\_host\_\_ or \_\_host\_\_ \_\_device\_\_.

▶ The type or template is a class member with private or protected access and its parent class is not defined within a \_\_device\_\_ or \_\_global\_\_ function.

▶ The type is unnamed.

▶ The type is compounded from any of the types above.

<sup>12</sup> One way to debug suspected layout mismatch of a type C is to use printf to output the values of sizeof(C) and offsetof(C, field) in host and device code.

Example:

```cpp
template <typename T>
__global__ void myKernel(void) { }

class myClass {
private:
    struct inner_t { };
public:
    static void launch(void)
    {
        // error: inner_t is used in template argument
        // but it is private
        myKernel<inner_t><<<1,1>>>(();
    }
};

// C++14 only
template <typename T> __device__ T d1;

template <typename T1, typename T2> __device__ T1 d2;

void fn() {
    struct S1_t { };
    // error (C++14 only): S1_t is local to the function fn
    d1<S1_t> = {}

    auto lam1 = [] { };
    // error (C++14 only): a closure type cannot be used for
    // instantiating a variable template
    d2<int, decltype(lam1)> = 10;
}
```

## 18.5.13. Trigraphs and Digraphs

Trigraphs are not supported on any platform. Digraphs are not supported on Windows.

## 18.5.14. Const-qualified variables

Let ‘V’ denote a namespace scope variable or a class static member variable that has const qualified type and does not have execution space annotations (for example, \_\_device\_\_, \_\_constant\_\_, \_\_shared\_\_). V is considered to be a host code variable.

The value of V may be directly used in device code, if

V has been initialized with a constant expression before the point of use,

the type of V is not volatile-qualified, and

it has one of the following types:

▶ built-in floating point type except when the Microsoft compiler is used as the host compiler,

▶ built-in integral type.

Device source code cannot contain a reference to V or take the address of V.

Example:

```lisp
const int xxx = 10;
struct S1_t { static const int yyy = 20; };

extern const int zzz;
const float www = 5.0;
__device__ void foo(void) {
    int local1[xxx];          // OK
    int local2[S1_t::yyy];   // OK

    int val1 = xxx;                // OK

    int val2 = S1_t::yyy;   // OK

    int val3 = zzz;                 // error: zzz not initialized with constant
                                        // expression at the point of use.

    const int &val3 = xxx;     // error: reference to host variable
    const int *val4 = &xxx;   // error: address of host variable
    const float val5 = www;   // OK except when the Microsoft compiler is used as
                                        // the host compiler.
}
const int zzz = 20;
```

## 18.5.15. Long Double

The use of long double type is not supported in device code.

## 18.5.16. Deprecation Annotation

nvcc supports the use of deprecated attribute when using gcc, clang, xlC, icc or pgcc host compilers, and the use of deprecated declspec when using the cl.exe host compiler. It also supports the [[deprecated]] standard attribute when the C++14 dialect has been enabled. The CUDA frontend compiler will generate a deprecation diagnostic for a reference to a deprecated entity from within the body of a \_\_device\_\_, \_\_global\_\_ or \_\_host\_\_ \_\_device\_\_ function when \_\_CUDA\_ARCH\_\_ is defined (i.e., during device compilation phase). Other references to deprecated entities will be handled by the host compiler, e.g., a reference from within a \_\_host\_\_ function.

The CUDA frontend compiler does not support the #pragma gcc diagnostic or #pragma warning mechanisms supported by various host compilers. Therefore, deprecation diagnostics generated by the CUDA frontend compiler are not afected by these pragmas, but diagnostics generated by the host compiler will be afected. To suppress the warning for device-code, user can use NVIDIA specific pragma #pragma nv\_diag\_suppress. The nvcc flag -Wno-deprecated-declarations can be used to suppress all deprecation warnings, and the flag -Werror=deprecated-declarations can be used to turn deprecation warnings into errors.

## 18.5.17. Noreturn Annotation

nvcc supports the use of noreturn attribute when using gcc, clang, xlC, icc or pgcc host compilers, and the use of noreturn declspec when using the cl.exe host compiler. It also supports the [[noreturn]] standard attribute when the C++11 dialect has been enabled.

The attribute/declspec can be used in both host and device code.

## 18.5.18. [[likely]] / [[unlikely]] Standard Attributes

These attributes are accepted in all configurations that support the C++ standard attribute syntax. The attributes can be used to hint to the device compiler optimizer whether a statement is more or less likely to be executed compared to any alternative path that does not include the statement.

Example:

```txt
__device__ int foo(int x) {

  if (i < 10) [[likely]] { // the 'if' block will likely be entered
    return 4;
  }
  if (i < 20) [[unlikely]] { // the 'if' block will not likely be entered
    return 1;
  }
  return 0;
}
```

If these attributes are used in host code when \_\_CUDA\_ARCH\_\_ is undefined, then they will be present in the code parsed by the host compiler, which may generate a warning if the attributes are not supported. For example, clang11 host compiler will generate an ‘unknown attribute’ warning.

## 18.5.19. const and pure GNU Attributes

These attributes are supported for both host and device functions, when using a language dialect and host compiler that also supports these attributes e.g. with g++ host compiler.

For a device function annotated with the pure attribute, the device code optimizer assumes that the function does not change any mutable state visible to caller functions (e.g. memory).

For a device function annotated with the const attribute, the device code optimizer assumes that the function does not access or change any mutable state visible to caller functions (e.g. memory).

Example:

```lisp
__attribute__((const)) __device__ int get(int in);

__device__ int doit(int in) {
int sum = 0;

//because 'get' is marked with 'const' attribute
//device code optimizer can recognize that the
//second call to get() can be commoned out.
sum = get(in);
```

(continues on next page)

```txt
sum += get(in);

return sum;
}
```

(continued from previous page)

## 18.5.20. \_\_nv\_pure\_\_ Attribute

The \_\_nv\_pure\_\_ attributed is supported for both host and device functions. For host functions, when using a language dialect that supports the pure GNU attribute, the \_\_nv\_pure\_\_ attribute is translated to the pure GNU attribute. Similarly when using MSVC as the host compiler, the attribute is translated to the MSVC noalias attribute.

When a device function is annotated with the \_\_nv\_pure\_\_ attribute, the device code optimizer assumes that the function does not change any mutable state visible to caller functions (e.g. memory).

## 18.5.21. Intel Host Compiler Specific

The CUDA frontend compiler parser does not recognize some of the intrinsic functions supported by the Intel compiler (e.g. icc). When using the Intel compiler as a host compiler, nvcc will therefore enable the macro \_\_INTEL\_COMPILER\_USE\_INTRINSIC\_PROTOTYPES during preprocessing. This macro enables explicit declarations of the Intel compiler intrinsic functions in the associated header files, allowing nvcc to support use of such functions in host code<sup>13</sup>.

## 18.5.22. C++11 Features

C++11 features that are enabled by default by the host compiler are also supported by nvcc, subject to the restrictions described in this document. In addition, invoking nvcc with -std=c++11 flag turns on all C++11 features and also invokes the host preprocessor, compiler and linker with the corresponding C++11 dialect option<sup>14</sup>.

## 18.5.22.1 Lambda Expressions

The execution space specifiers for all member functions<sup>15</sup> of the closure class associated with a lambda expression are derived by the compiler as follows. As described in the C++11 standard, the compiler creates a closure type in the smallest block scope, class scope or namespace scope that contains the lambda expression. The innermost function scope enclosing the closure type is computed, and the corresponding function’s execution space specifiers are assigned to the closure class member functions. If there is no enclosing function scope, the execution space specifier is \_\_host\_\_.

Examples of lambda expressions and computed execution space specifiers are shown below (in comments).

```javascript
auto globalVar = [] { return 0; }; // __host--

void f1(void) {
    auto l1 = [] { return 1; };      // __host__
}

__device__ void f2(void) {
    auto l2 = [] { return 2; };      // __device__
}

__host__ __device__ void f3(void) {
    auto l3 = [] { return 3; };      // __host__ __device__
}

__device__ void f4(int (*fp)() = [] { return 4; } /* __host__ */) {
}

__global__ void f5(void) {
    auto l5 = [] { return 5; };      // __device__
}

__device__ void f6(void) {
    struct S1_t {
        static void helper(int (*fp)() = [] {return 6; } /* __device__ */) {
            }
        };
}
```

The closure type of a lambda expression cannot be used in the type or non-type argument of a \_\_global\_\_ function template instantiation, unless the lambda is defined within a \_\_device\_\_ or \_\_global\_\_ function.

Example:

```cpp
template <typename T>
__global__ void foo(T in) { };

template <typename T>
struct S1_t { };

void bar(void) {
  auto temp1 = [] { };

  foo<<<1,1>>>(temp1);                      // error: lambda closure type used in
                                // template type argument
  foo<<<1,1>>>( S1_t<decltype(temp1)>()); // error: lambda closure type used in
                                // template type argument
}
```

## 18.5.22.2 std::initializer\_list

By default, the CUDA compiler will implicitly consider the member functions of std::initializer\_list to have \_\_host\_\_ \_\_device\_\_ execution space specifiers, and therefore they can be invoked directly from device code. The nvcc flag --no-host-device-initializer-list will disable this behavior; member functions of std::initializer\_list will then be considered as \_\_host\_\_ functions and will not be directly invokable from device code.

Example:

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

## 18.5.22.3 Rvalue references

By default, the CUDA compiler will implicitly consider std::move and std::forward function templates to have \_\_host\_\_ \_\_device\_\_ execution space specifiers, and therefore they can be invoked directly from device code. The nvcc flag --no-host-device-move-forward will disable this behavior; std::move and std::forward will then be considered as \_\_host\_\_ functions and will not be directly invokable from device code.

## 18.5.22.4 Constexpr functions and function templates

By default, a constexpr function cannot be called from a function with incompatible execution space<sup>16</sup>. The experimental nvcc flag --expt-relaxed-constexpr removes this restriction<sup>17</sup>. When this flag is specified, host code can invoke a \_\_device\_\_ constexpr function and device code can invoke a \_\_host\_\_ constexpr function. nvcc will define the macro \_\_CUDACC\_RELAXED\_CONSTEXPR\_\_ when --expt-relaxed-constexpr has been specified. Note that a function template instantiation may not be a constexpr function even if the corresponding template is marked with the keyword constexpr (C++11 Standard Section [dcl.constexpr.p6]).

## 18.5.22.5 Constexpr variables

Let ‘V’ denote a namespace scope variable or a class static member variable that has been marked constexpr and that does not have execution space annotations (e.g., \_\_device\_\_, \_\_constant\_\_, \_\_shared\_\_). V is considered to be a host code variable.

If V is of scalar type<sup>18</sup> other than long double and the type is not volatile-qualified, the value of V can be directly used in device code. In addition, if V is of a non-scalar type then scalar elements of V can be used inside a constexpr \_\_device\_\_ or \_\_host\_\_ \_\_device\_\_ function, if the call to the function is a constant expression<sup>19</sup>. Device source code cannot contain a reference to V or take the address of V.

## Example:

```txt
constexpr int xxx = 10;
constexpr int yyy = xxx + 4;
struct S1_t { static constexpr int qqq = 100; };

constexpr int host_arr[] = { 1, 2, 3};
constexpr __device__ int get(int idx) { return host_arr[idx]; }

__device__ int foo(int idx) {
    int v1 = xxx + yyy + S1_t::qqq; // OK
    const int &v2 = xxx; // error: reference to host constexpr
// variable
    const int *v3 = &xxx; // error: address of host constexpr
// variable
    const int &v4 = S1_t::qqq; // error: reference to host constexpr
// variable
    const int *v5 = &S1_t::qqq; // error: address of host constexpr
// variable

    v1 += get(2); // OK: 'get(2)' is a constant
// expression.
    v1 += get(idx); // error: 'get(idx)' is not a constant
// expression
    v1 += host_arr[2]; // error: 'host_arr' does not have
// scalar type.
    return v1;
}
```

## 18.5.22.6 Inline namespaces

For an input CUDA translation unit, the CUDA compiler may invoke the host compiler for compiling the host code within the translation unit. In the code passed to the host compiler, the CUDA compiler will inject additional compiler generated code, if the input CUDA translation unit contained a definition of any of the following entities:

▶ \_\_global\_\_ function or function template instantiation

```python
__device__, __constant__
```

▶ variables with surface or texture type

```txt
$^{18}$ C++ Standard Section [basic.types]
$^{19}$ C++ Standard Section [expr.const]
```

The compiler generated code contains a reference to the defined entity. If the entity is defined within an inline namespace and another entity of the same name and type signature is defined in an enclosing namespace, this reference may be considered ambiguous by the host compiler and host compilation will fail.

This limitation can be avoided by using unique names for such entities defined within an inline namespace.

## Example:

```txt
__device__ int Gvar;
inline namespace N1 {
  __device__ int Gvar;
}

// <-- CUDA compiler inserts a reference to "Gvar" at this point in the
// translation unit. This reference will be considered ambiguous by the
// host compiler and compilation will fail.
```

Example:

```cpp
inline namespace N1 {
    namespace N2 {
        __device__ int Gvar;
    }
}

namespace N2 {
    __device__ int Gvar;
}

// <-- CUDA compiler inserts reference to "::N2::Gvar" at this point in
// the translation unit. This reference will be considered ambiguous by
// the host compiler and compilation will fail.
```

## 18.5.22.6.1 Inline unnamed namespaces

The following entities cannot be declared in namespace scope within an inline unnamed namespace:

```txt
__managed__, __device__, __shared__ and __constant__ variables
```

\_\_global\_\_ function and function templates

▶ variables with surface or texture type

## Example:

```cpp
inline namespace {
  namespace N2 {
    template <typename T>
      __global__ void foo(void);          // error

      __global__ void bar(void) { }         // error

      template <>
      __global__ void foo<int>(void) { }     // error

      __device__ int x1b;                    // error
```

(continues on next page)

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
````
