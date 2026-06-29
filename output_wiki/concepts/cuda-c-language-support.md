# CUDA C++ Language Support

CUDA C++ language support allows CUDA source files compiled with `nvcc` to include a mix of host code and device code. The CUDA front-end compiler aims to emulate the host compiler's behavior with respect to C++ input code, processing input source according to C++ ISO/IEC 14882:2003, C++ ISO/IEC 14882:2011, C++ ISO/IEC 14882:2014, or C++ ISO/IEC 14882:2017 specifications, while also emulating host compiler divergences from the ISO specification. The supported language is extended with CUDA-specific constructs and is subject to specific restrictions.

## Supported C++ Standards

CUDA supports features from C++11, C++14, C++17, and C++20. The support matrix for these features is detailed in the CUDA Programming Guide.

### C++11 Features

C++11 support includes features such as lambda expressions, `std::initializer_list`, rvalue references, `constexpr` functions and variables, inline namespaces, `thread_local`, and device-specific qualifiers like `__global__`, `__managed__`, and `__shared__`.

### C++14 Features

C++14 support includes functions with deduced return types and variable templates.

### C++17 Features

C++17 support includes inline variables and structured bindings.

### C++20 Features

C++20 support includes module support, coroutine support, the three-way comparison operator, and `consteval` functions.

## Restrictions

While CUDA supports a wide range of C++ features, there are significant restrictions on standard library usage, templates, exceptions, and specific device code constructs.

### General Restrictions

- **Host Compiler Extensions**: CUDA supports host compiler extensions.
- **Preprocessor Symbols**: Specific preprocessor symbols like `__CUDA_ARCH__` are available for device code.
- **Qualifiers**: Device memory space specifiers, the `__managed__` memory space specifier, and the volatile qualifier have specific behaviors and restrictions.
- **Pointers and Operators**: Restrictions apply to pointer usage and operators, including assignment and address operators.
- **RTTI and Exceptions**: Run Time Type Information (RTTI) and exception handling have limitations in device code.
- **Standard Library**: Usage of the standard library is restricted, particularly in device code.
- **Namespace Reservations**: Certain namespaces are reserved.

### Function Restrictions

- **External Linkage**: Functions with external linkage have specific constraints.
- **Implicitly-declared and non-virtual explicitly-defaulted functions**: These are subject to restrictions.
- **Function Parameters**: Restrictions apply to function parameters.
- **Static Variables within Function**: Static variables in device functions are restricted.
- **Function Pointers**: Usage of function pointers is limited.
- **Function Recursion**: Recursion is restricted in device code.
- **Friend Functions**: Friend functions have limitations.
- **Operator Functions**: Operator functions are subject to restrictions.
- **Allocation and Deallocation Functions**: Custom allocation and deallocation functions are restricted.

### Class Restrictions

- **Data Members**: Restrictions apply to data members in device classes.
- **Function Members**: Member functions have specific constraints.
- **Virtual Functions**: Virtual functions are restricted in device code.
- **Virtual Base Classes**: Virtual base classes are not supported in device code.
- **Anonymous Unions**: Anonymous unions have limitations.
- **Windows-Specific**: Windows-specific features may have additional restrictions.

### Template Restrictions

Templates are supported but with specific restrictions, particularly regarding device code.

### Other Restrictions

- **Trigraphs and Digraphs**: Support for trigraphs and digraphs is limited.
- **Const-qualified variables**: Restrictions apply to const-qualified variables in device code.
- **Long Double**: Support for `long double` is restricted.
- **Deprecation Annotation**: Deprecation annotations are supported.
- **Noreturn Annotation**: The `[[noreturn]]` annotation is supported.
- **[[likely]] / [[unlikely]] Standard Attributes**: These attributes are supported.
- **const and pure GNU Attributes**: GNU-specific attributes have restrictions.
- **_nv_pure__ Attribute**: The `_nv_pure__` attribute is supported.
- **Intel Host Compiler Specific**: Intel host compiler-specific features have limitations.

## Extended Lambdas

CUDA supports extended lambdas, which allow lambdas to be used in device code. This includes extended lambda type traits and specific restrictions on extended lambda usage. Notes on `__host__ __device__` lambdas and `*this` capture by value are also provided.

## Polymorphic Function Wrappers

CUDA supports polymorphic function wrappers, which allow for flexible function object usage in both host and device code.

## Code Samples

Code samples are provided for various C++ constructs, including data aggregation classes, derived classes, class templates, function templates, and functor classes.

## Legacy Notice

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## References

- [CUDA_C_Programming_Guide:L534-L620]
- [CUDA_C_Programming_Guide:L16486-L16493]
