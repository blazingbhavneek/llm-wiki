# CUDA C++ Language Support

Support matrix and restrictions for C++11, C++14, C++17, and C++20 features in CUDA device code, including __CUDA_ARCH__ constraints.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16487-L16639

Citation: [CUDA_C_Programming_Guide:L16487-L16639]

````text

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

As described in Compilation with NVCC, CUDA source files compiled with nvcc can include a mix of host code and device code. The CUDA front-end compiler aims to emulate the host compiler behavior with respect to C++ input code. The input source code is processed according to the C++ ISO/IEC 14882:2003, C++ ISO/IEC 14882:2011, C++ ISO/IEC 14882:2014 or C++ ISO/IEC 14882:2017 specifications, and the CUDA front-end compiler aims to emulate any host compiler divergences from the ISO specification. In addition, the supported language is extended with CUDA-specific constructs described in this document<sup>?</sup>, and is subject to the restrictions described below.

C++11 Language Features, C++14 Language Features and C++17 Language Features provide support matrices for the C++11, C++14, C++17 and C++20 features, respectively. Restrictions lists the language restrictions. Polymorphic Function Wrappers and Extended Lambdas describe additional features. Code Samples gives code samples.

## 18.1. C++11 Language Features

The following table lists new language features that have been accepted into the C++11 standard. The “Proposal” column provides a link to the ISO C++ committee proposal that describes the feature, while the “Available in nvcc (device code)” column indicates the first version of nvcc that contains an implementation of this feature (if it has been implemented) for device code.

Table 23: C++11 Language Features

<table><tr><td>Language Feature</td><td>C++11 Proposal</td><td>Available in nvcc (device code)</td></tr><tr><td>Rvalue references</td><td>N2118</td><td>7.0</td></tr><tr><td>Rvalue references for *this</td><td>N2439</td><td>7.0</td></tr><tr><td>Initialization of class objects by rvalues</td><td>N1610</td><td>7.0</td></tr><tr><td>Non-static data member initializers</td><td>N2756</td><td>7.0</td></tr><tr><td>Variadic templates</td><td>N2242</td><td>7.0</td></tr></table>

continues on next page

Table 23 – continued from previous page

<table><tr><td>Language Feature</td><td>C++11 Proposal</td><td>Available in nvcc (device code)</td></tr><tr><td>Extending variadic template template parameters</td><td>N2555</td><td>7.0</td></tr><tr><td>Initializer lists</td><td>N2672</td><td>7.0</td></tr><tr><td>Static assertions</td><td>N1720</td><td>7.0</td></tr><tr><td>auto-typed variables</td><td>N1984</td><td>7.0</td></tr><tr><td>Multi-declarator auto</td><td>N1737</td><td>7.0</td></tr><tr><td>Removal of auto as a storage-class specifier</td><td>N2546</td><td>7.0</td></tr><tr><td>New function declarator syntax</td><td>N2541</td><td>7.0</td></tr><tr><td>Lambda expressions</td><td>N2927</td><td>7.0</td></tr><tr><td>Declared type of an expression</td><td>N2343</td><td>7.0</td></tr><tr><td>Incomplete return types</td><td>N3276</td><td>7.0</td></tr><tr><td>Right angle brackets</td><td>N1757</td><td>7.0</td></tr><tr><td>Default template arguments for function templates</td><td>DR226</td><td>7.0</td></tr><tr><td>Solving the SFINAE problem for expressions</td><td>DR339</td><td>7.0</td></tr><tr><td>Alias templates</td><td>N2258</td><td>7.0</td></tr><tr><td>Extern templates</td><td>N1987</td><td>7.0</td></tr><tr><td>Null pointer constant</td><td>N2431</td><td>7.0</td></tr><tr><td>Strongly-typed enums</td><td>N2347</td><td>7.0</td></tr><tr><td>Forward declarations for enums</td><td>N2764 DR1206</td><td>7.0</td></tr><tr><td>Standardized attribute syntax</td><td>N2761</td><td>7.0</td></tr><tr><td>Generalized constant expressions</td><td>N2235</td><td>7.0</td></tr><tr><td>Alignment support</td><td>N2341</td><td>7.0</td></tr><tr><td>Conditionally-support behavior</td><td>N1627</td><td>7.0</td></tr><tr><td>Changing undefined behavior into diagnosable errors</td><td>N1727</td><td>7.0</td></tr><tr><td>Delegating constructors</td><td>N1986</td><td>7.0</td></tr><tr><td>Inheriting constructors</td><td>N2540</td><td>7.0</td></tr><tr><td>Explicit conversion operators</td><td>N2437</td><td>7.0</td></tr><tr><td>New character types</td><td>N2249</td><td>7.0</td></tr><tr><td>Unicode string literals</td><td>N2442</td><td>7.0</td></tr><tr><td>Raw string literals</td><td>N2442</td><td>7.0</td></tr><tr><td>Universal character names in literals</td><td>N2170</td><td>7.0</td></tr><tr><td>User-defined literals</td><td>N2765</td><td>7.0</td></tr></table>

continues on next page

Table 23 – continued from previous page

<table><tr><td>Language Feature</td><td>C++11 Proposal</td><td>Available in nvcc (device code)</td></tr><tr><td>Standard Layout Types</td><td>N2342</td><td>7.0</td></tr><tr><td>Defaulted functions</td><td>N2346</td><td>7.0</td></tr><tr><td>Deleted functions</td><td>N2346</td><td>7.0</td></tr><tr><td>Extended friend declarations</td><td>N1791</td><td>7.0</td></tr><tr><td>Extending sizeof</td><td>N2253 DR850</td><td>7.0</td></tr><tr><td>Inline namespaces</td><td>N2535</td><td>7.0</td></tr><tr><td>Unrestricted unions</td><td>N2544</td><td>7.0</td></tr><tr><td>Local and unnamed types as template arguments</td><td>N2657</td><td>7.0</td></tr><tr><td>Range-based for</td><td>N2930</td><td>7.0</td></tr><tr><td>Explicit virtual overrides</td><td>N2928 N3206N3272</td><td>7.0</td></tr><tr><td>Minimal support for garbage collection and reachability-based leak detection</td><td>N2670</td><td>N/A (see Restrictions)</td></tr><tr><td>Allowing move constructors to throw [noexcept]</td><td>N3050</td><td>7.0</td></tr><tr><td>Defining move special member functions</td><td>N3053</td><td>7.0</td></tr><tr><td colspan="3">Concurrency</td></tr><tr><td>Sequence points</td><td>N2239</td><td></td></tr><tr><td>Atomic operations</td><td>N2427</td><td></td></tr><tr><td>Strong Compare and Exchange</td><td>N2748</td><td></td></tr><tr><td>Bidirectional Fences</td><td>N2752</td><td></td></tr><tr><td>Memory model</td><td>N2429</td><td></td></tr><tr><td>Data-dependency ordering: atomics and memory model</td><td>N2664</td><td></td></tr><tr><td>Propagating exceptions</td><td>N2179</td><td></td></tr><tr><td>Allow atomics use in signal handlers</td><td>N2547</td><td></td></tr><tr><td>Thread-local storage</td><td>N2659</td><td></td></tr><tr><td>Dynamic initialization and destruction with concurrency</td><td>N2660</td><td></td></tr><tr><td colspan="3">C99 Features in C++11</td></tr><tr><td>__func__ predefined identifier</td><td>N2340</td><td>7.0</td></tr><tr><td>C99 preprocessor</td><td>N1653</td><td>7.0</td></tr><tr><td>long long</td><td>N1811</td><td>7.0</td></tr><tr><td>Extended integral types</td><td>N1988</td><td></td></tr></table>

## 18.2. C++14 Language Features

The following table lists new language features that have been accepted into the C++14 standard.

Table 24: C++14 Language Features

<table><tr><td>Language Feature</td><td>C++14 Proposal</td><td>Available in nvcc (device code)</td></tr><tr><td>Tweak to certain C++ contextual conversions</td><td>N3323</td><td>9.0</td></tr><tr><td>Binary literals</td><td>N3472</td><td>9.0</td></tr><tr><td>Functions with deduced return type</td><td>N3638</td><td>9.0</td></tr><tr><td>Generalized lambda capture (init-capture)</td><td>N3648</td><td>9.0</td></tr><tr><td>Generic (polymorphic) lambda expressions</td><td>N3649</td><td>9.0</td></tr><tr><td>Variable templates</td><td>N3651</td><td>9.0</td></tr><tr><td>Relaxing requirements on constexpr functions</td><td>N3652</td><td>9.0</td></tr><tr><td>Member initializers and aggregates</td><td>N3653</td><td>9.0</td></tr><tr><td>Clarifying memory allocation</td><td>N3664</td><td></td></tr><tr><td>Sized deallocation</td><td>N3778</td><td></td></tr><tr><td>[ [deprecated ]] attribute</td><td>N3760</td><td>9.0</td></tr><tr><td>Single-quotation-mark as a digit separator</td><td>N3781</td><td>9.0</td></tr></table>

## 18.3. C++17 Language Features

All C++17 language features are supported in nvcc version 11.0 and later, subject to restrictions described here.

## 18.4. C++20 Language Features

All C++20 language features are supported in nvcc version 12.0 and later, subject to restrictions described here.

## 18.5. Restrictions

## 18.5.1. Host Compiler Extensions

Host compiler specific language extensions are not supported in device code.

\_\_Complex types are only supported in host code.

\_\_int128 type is supported in device code when compiled in conjunction with a host compiler that supports it.

\_\_float128 type is supported for devices with compute capability 10.0 and later, when compiled in conjunction with a host compiler that supports the type. A constant expression of \_\_float128 type may be processed by the compiler in a floating point representation with lower precision.

## 18.5.2. Preprocessor Symbols

## 18.5.2.1 \_\_CUDA\_ARCH\_\_

1. The type signature of the following entities shall not depend on whether \_\_CUDA\_ARCH\_\_ is defined or not, or on a particular value of \_\_CUDA\_ARCH\_\_:

▶ \_\_global\_\_ functions and function templates

▶ \_\_device\_\_ and \_\_constant\_\_ variables

▶ textures and surfaces

Example:

```c
#if !defined(__CUDA_ARCH__)
typedef int mytype;
#else
typedef double mytype;
#endif

__device__ mytype xxx;          // error: xxx's type depends on __CUDA_ARCH__
__global__ void foo(mytype in, // error: foo's type depends on __CUDA_ARCH__
                 mytype *ptr)
{
    *ptr = in;
}
```

2. If a \_\_global\_\_ function template is instantiated and launched from the host, then the function template must be instantiated with the same template arguments irrespective of whether \_\_CUDA\_ARCH\_\_ is defined and regardless of the value of \_\_CUDA\_ARCH\_\_

Example:

```txt
__device__ int result;
template <typename T>
__global__ void kern(T in)
{
    result = in;
}

__host__ __device__ void foo(void)
{
#if !defined(__CUDA_ARCH__)
    kern<<<1,1>>>(1);      // error: "kern<int>" instantiation only
                                // when __CUDA_ARCH__ is undefined!
#endif
}

int main(void)
{
    foo();
    cudaDeviceSynchronize();
    return 0;
}
```

3. In separate compilation mode, the presence or absence of a definition of a function or variable with external linkage shall not depend on whether \_\_CUDA\_ARCH\_\_ is defined or on a particular value of \_\_CUDA\_ARCH\_\_<sup>Page</sup> <sup>327,</sup> <sup>7</sup>.

Example:

```c
#if !defined(__CUDA_ARCH__)
void foo(void) { }                      // error: The definition of foo()
                                // is only present when __CUDA_ARCH__
                                // is undefined
#endif
```

4. In separate compilation, \_\_CUDA\_ARCH\_\_ must not be used in headers such that diferent objects could contain diferent behavior. Or, it must be guaranteed that all objects will compile for the same compute\_arch. If a weak function or template function is defined in a header and its behavior depends on \_\_CUDA\_ARCH\_\_, then the instances of that function in the objects could conflict if the objects are compiled for diferent compute arch.

For example, if an a.h contains:

```c
template<typename T>
__device__ T* getptr(void)
{
#if __CUDA_ARCH__ == 700
    return NULL; /* no address */
#else
    __shared__ T arr[256];
    return arr;
#endif
}
```

Then if a.cu and b.cu both include a.h and instantiate getptr for the same type, and b.cu expects a non-NULL address, and compile with:

```shell
nvcc -arch=compute_70 -dc a.cu
nvcc -arch=compute_80 -dc b.cu
nvcc -arch=sm_80 a.o b.o
```

At link time only one version of the getptr is used, so the behavior would depend on which version is chosen. To avoid this, either a.cu and b.cu must be compiled for the same compute arch, or \_\_CUDA\_ARCH\_\_ should not be used in the shared header function.

The compiler does not guarantee that a diagnostic will be generated for the unsupported uses of \_\_CUDA\_ARCH\_\_ described above.
````
