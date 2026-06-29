# CUDA Extended Lambdas

CUDA extended lambdas are a feature of the NVIDIA CUDA compiler (`nvcc`) that allows explicit execution space annotations (such as `__device__` or `__host__ __device__`) within lambda expressions. This feature is enabled by passing the `--extended-lambda` flag to `nvcc` [CUDA_C_Programming_Guide:L18353-L18356]. When this flag is specified, the compiler defines the macro `__CUDACC_EXTENDED_LAMBDA__` [CUDA_C_Programming_Guide:L18356].

## Definition and Scope

An extended lambda is defined as either an extended `__device__` lambda or an extended `__host__ __device__` lambda [CUDA_C_Programming_Guide:L18360-L18362]. To be considered an extended lambda, the expression must be annotated explicitly with the execution space specifier after the lambda-introducer and before the optional lambda-declarator [CUDA_C_Programming_Guide:L18354-L18355].

Crucially, an extended lambda must be defined within the immediate or nested block scope of a `__host__` or `__host__ __device__` function [CUDA_C_Programming_Guide:L18361-L18362]. If a lambda is defined inside a `__device__` function, it is not considered an extended lambda, even if it carries explicit execution space annotations [CUDA_C_Programming_Guide:L18380-L18384]. Similarly, lambdas defined at namespace scope or outside of a host/host-device function context are not extended lambdas [CUDA_C_Programming_Guide:L18385-L18389].

If execution space annotations are not explicitly specified, they are computed based on the scopes enclosing the closure class, following standard C++11 support rules [CUDA_C_Programming_Guide:L18364-L18366].

## Type Traits

The compiler provides type traits to detect closure types for extended lambdas at compile time [CUDA_C_Programming_Guide:L18392-L18393]. These traits are available in all compilation modes, regardless of whether extended lambdas are enabled [CUDA_C_Programming_Guide:L18405-L18406].

*   `__nv_is_extended_device_lambda_closure_type(type)`: Returns true if the type is the closure class for an extended `__device__` lambda [CUDA_C_Programming_Guide:L18395-L18396].
*   `__nv_is_extended_device_lambda_with_preserved_return_type(type)`: Returns true if the type is the closure class for an extended `__device__` lambda defined with a trailing return type, provided the return type does not refer to any lambda parameter names [CUDA_C_Programming_Guide:L18397-L18399].
*   `__nv_is_extended_host_device_lambda_closure_type(type)`: Returns true if the type is the closure class for an extended `__host__ __device__` lambda [CUDA_C_Programming_Guide:L18400-L18401].

## Restrictions

The CUDA compiler replaces an extended lambda expression with an instance of a placeholder type defined in namespace scope before invoking the host compiler [CUDA_C_Programming_Guide:L18410-L18412]. This placeholder type requires taking the address of the function enclosing the original extended lambda expression [CUDA_C_Programming_Guide:L18412-L18414]. This mechanism imposes several restrictions:

### 1. Nesting Restrictions

*   **No Nested Extended Lambdas:** An extended lambda cannot be defined inside another extended lambda expression [CUDA_C_Programming_Guide:L18420-L18423].
*   **No Generic Lambda Nesting:** An extended lambda cannot be defined inside a generic lambda expression (a lambda with `auto` parameters) [CUDA_C_Programming_Guide:L18425-L18428].
*   **Outer Lambda Scope:** If an extended lambda is defined within nested lambda expressions, the outermost such lambda expression must be defined inside the immediate or nested block scope of a function [CUDA_C_Programming_Guide:L18430-L18435]. An extended lambda cannot be defined inside a lambda that is itself at namespace scope [CUDA_C_Programming_Guide:L18430-L18435].

### 2. Enclosing Function Requirements

The compiler computes an "enclosing function" for the extended lambda [CUDA_C_Programming_Guide:L18415-L18419]. This function is determined as follows:

1.  If the extended lambda is in the scope of a `__host__` or `__host__ __device__` function that is not an `operator()` of a lambda, that function is the enclosing function [CUDA_C_Programming_Guide:L18416-L18417].
2.  If the extended lambda is inside nested lambda `operator()`s, the enclosing function is the function `F` in whose scope the outermost of those lambda expressions is defined [CUDA_C_Programming_Guide:L18418-L18419]. If no such function exists, the enclosing function does not exist, and the lambda is invalid [CUDA_C_Programming_Guide:L18419].

### 3. Addressability Constraints

The enclosing function must be named, and its address must be takable [CUDA_C_Programming_Guide:L18437-L18438]. If the enclosing function is a class member, the following conditions must be met:

*   All classes enclosing the member function must have a name [CUDA_C_Programming_Guide:L18440-L18441].
*   The member function must not have private or protected access within its parent class [CUDA_C_Programming_Guide:L18442-L18443].
*   All enclosing classes must not have private or protected access within their respective parent classes [CUDA_C_Programming_Guide:L18444-L18445].

Additionally, it must be possible to take the address of the enclosing routine unambiguously at the point where the extended lambda is defined [CUDA_C_Programming_Guide:L18447-L18448]. Ambiguity can arise if, for example, a class typedef shadows a template type argument of the same name, causing the injected address expression to refer to the wrong function [CUDA_C_Programming_Guide:L18449-L18463].

## Usage in Templates

Extended lambdas can be used in the type arguments of `__global__` function template instantiation [CUDA_C_Programming_Guide:L18363]. This capability is supported by the placeholder type mechanism described above, which allows the compiler to handle the closure type correctly in device code contexts [CUDA_C_Programming_Guide:L18412-L18414].

## Related Features

### Polymorphic Function Wrappers

The `nvstd::function` class template, provided in the `nvfunctional` header, can store, copy, and invoke callable targets including lambda expressions [CUDA_C_Programming_Guide:L18273-L18275]. It supports both host and device code [CUDA_C_Programming_Guide:L18275].

*   Host `nvstd::function` instances cannot be initialized with `__device__` functions or functors with `__device__` `operator()` [CUDA_C_Programming_Guide:L18310-L18312].
*   Device `nvstd::function` instances cannot be initialized with `__host__` functions or functors with `__host__` `operator()` [CUDA_C_Programming_Guide:L18312-L18314].
*   `nvstd::function` instances cannot be passed from host to device code (or vice versa) at runtime [CUDA_C_Programming_Guide:L18315-L18316].
*   `nvstd::function` cannot be used as a parameter type in a `__global__` function launched from host code [CUDA_C_Programming_Guide:L18316-L18317].

### C++17 and C++20 Features

While not specific to extended lambdas, C++17 and C++20 features enabled by `nvcc` may interact with lambda usage:

*   **C++17:** Structured bindings cannot be declared with variable memory space specifiers (e.g., `__device__`) [CUDA_C_Programming_Guide:L18043-L18047].
*   **C++20:** Coroutines are not supported in device code [CUDA_C_Programming_Guide:L18130-L18132]. Modules are not supported in CUDA C++ [CUDA_C_Programming_Guide:L18110-L18112]. `consteval` functions allow cross-execution-space calls, permitting `__device__` functions to call `__host__ consteval` functions and vice versa [CUDA_C_Programming_Guide:L18134-L18140].
