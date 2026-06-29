# CUDA C++11 Language Features

The NVIDIA CUDA compiler (`nvcc`) supports a wide range of language features accepted into the C++11 standard for device code. The following table lists these features, the corresponding ISO C++ committee proposal number, and the first version of `nvcc` that implemented support for device code [CUDA_C_Programming_Guide:L16494-L16513].

## C++11 Language Features

All features listed below are available in `nvcc` device code starting from version 7.0, unless otherwise noted [CUDA_C_Programming_Guide:L16494-L16513].

### Core Language and Templates

| Language Feature | C++11 Proposal | Available in nvcc (device code) |
| :--- | :--- | :--- |
| Rvalue references | N2118 | 7.0 |
| Rvalue references for *this | N2439 | 7.0 |
| Initialization of class objects by rvalues | N1610 | 7.0 |
| Non-static data member initializers | N2756 | 7.0 |
| Variadic templates | N2242 | 7.0 |
| Extending variadic template template parameters | N2555 | 7.0 |
| Initializer lists | N2672 | 7.0 |
| Static assertions | N1720 | 7.0 |
| auto-typed variables | N1984 | 7.0 |
| Multi-declarator auto | N1737 | 7.0 |
| Removal of auto as a storage-class specifier | N2546 | 7.0 |
| New function declarator syntax | N2541 | 7.0 |
| Lambda expressions | N2927 | 7.0 |
| Declared type of an expression | N2343 | 7.0 |
| Incomplete return types | N3276 | 7.0 |
| Right angle brackets | N1757 | 7.0 |
| Default template arguments for function templates | DR226 | 7.0 |
| Solving the SFINAE problem for expressions | DR339 | 7.0 |
| Alias templates | N2258 | 7.0 |
| Extern templates | N1987 | 7.0 |
| Null pointer constant | N2431 | 7.0 |
| Strongly-typed enums | N2347 | 7.0 |
| Forward declarations for enums | N2764 DR1206 | 7.0 |
| Standardized attribute syntax | N2761 | 7.0 |
| Generalized constant expressions | N2235 | 7.0 |
| Alignment support | N2341 | 7.0 |
| Conditionally-support behavior | N1627 | 7.0 |
| Changing undefined behavior into diagnosable errors | N1727 | 7.0 |
| Delegating constructors | N1986 | 7.0 |
| Inheriting constructors | N2540 | 7.0 |
| Explicit conversion operators | N2437 | 7.0 |
| New character types | N2249 | 7.0 |
| Unicode string literals | N2442 | 7.0 |
| Raw string literals | N2442 | 7.0 |
| Universal character names in literals | N2170 | 7.0 |
| User-defined literals | N2765 | 7.0 |
| Standard Layout Types | N2342 | 7.0 |
| Defaulted functions | N2346 | 7.0 |
| Deleted functions | N2346 | 7.0 |
| Extended friend declarations | N1791 | 7.0 |
| Extending sizeof | N2253 DR850 | 7.0 |
| Inline namespaces | N2535 | 7.0 |
| Unrestricted unions | N2544 | 7.0 |
| Local and unnamed types as template arguments | N2657 | 7.0 |
| Range-based for | N2930 | 7.0 |
| Explicit virtual overrides | N2928 N3206N3272 | 7.0 |
| Allowing move constructors to throw [noexcept] | N3050 | 7.0 |
| Defining move special member functions | N3053 | 7.0 |

### Concurrency

The following concurrency features are part of the C++11 standard but are not implemented in `nvcc` device code [CUDA_C_Programming_Guide:L16494-L16513].

| Language Feature | C++11 Proposal | Available in nvcc (device code) |
| :--- | :--- | :--- |
| Sequence points | N2239 | |
| Atomic operations | N2427 | |
| Strong Compare and Exchange | N2748 | |
| Bidirectional Fences | N2752 | |
| Memory model | N2429 | |
| Data-dependency ordering: atomics and memory model | N2664 | |
| Propagating exceptions | N2179 | |
| Allow atomics use in signal handlers | N2547 | |
| Thread-local storage | N2659 | |
| Dynamic initialization and destruction with concurrency | N2660 | |

### Minimal Support for Garbage Collection

| Language Feature | C++11 Proposal | Available in nvcc (device code) |
| :--- | :--- | :--- |
| Minimal support for garbage collection and reachability-based leak detection | N2670 | N/A (see Restrictions) |

### C99 Features in C++11

`nvcc` also supports specific C99 features adopted in C++11 [CUDA_C_Programming_Guide:L16494-L16513].

| Language Feature | C++11 Proposal | Available in nvcc (device code) |
| :--- | :--- | :--- |
| __func__ predefined identifier | N2340 | 7.0 |
| C99 preprocessor | N1653 | 7.0 |
| long long | N1811 | 7.0 |
| Extended integral types | N1988 | |
