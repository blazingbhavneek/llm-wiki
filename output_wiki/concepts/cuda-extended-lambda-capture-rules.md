# CUDA Extended Lambda Capture Rules

CUDA extended lambdas (lambdas marked with `__device__` or `__host__ __device__`) have specific restrictions on how variables are captured compared to standard C++ lambdas. These rules ensure that the closure type can be correctly represented and initialized in both host and device code.

## General Capture Rules

### Value-Only Capture
Variables in an extended lambda can only be captured by value. By-reference capture is not supported for extended lambdas, regardless of whether they are `__device__` or `__host__ __device__` [CUDA_C_Programming_Guide:L18642-L18736].

In the code sent to the host compiler, the captured variable is passed by value to a sequence of helper functions before being used to direct-initialize the field of the class type representing the closure type [CUDA_C_Programming_Guide:L18642-L18736]. This differs from the C++ standard, which specifies that the captured variable is used directly to direct-initialize the field [CUDA_C_Programming_Guide:L18642-L18736].

### Type Restrictions
The type of the captured variable cannot involve:
* Types that are local to a function (except for closure types of extended lambdas).
* Private or protected class members [CUDA_C_Programming_Guide:L18642-L18736].

For `__host__ __device__` extended lambdas, the types used in the return or parameter types of the lambda's `operator()` are also subject to these restrictions [CUDA_C_Programming_Guide:L18642-L18736].

### Variadic Arguments
A function parameter that is an element of a variadic argument pack cannot be captured [CUDA_C_Programming_Guide:L18642-L18736].

## Array Capture

### Dimension Limits
A variable of array type cannot be captured if the number of array dimensions is greater than 7 [CUDA_C_Programming_Guide:L18642-L18736].

### Initialization and Element Types
For a variable of array type, the closure type’s array field is first default-initialized, and then each element of the array field is copy-assigned from the corresponding element of the captured array variable [CUDA_C_Programming_Guide:L18642-L18736]. Consequently, the array element type must be default-constructible and copy-assignable in host code [CUDA_C_Programming_Guide:L18642-L18736].

## Init-Capture Limitations

Init-capture (e.g., `[x = value]`) support varies by lambda type:
* **`__device__` extended lambdas**: Init-capture is supported, except when the init-capture is of array type or of type `std::initializer_list` [CUDA_C_Programming_Guide:L18642-L18736].
* **`__host__ __device__` extended lambdas**: Init-capture is not supported [CUDA_C_Programming_Guide:L18642-L18736].

## constexpr and Literal Type Restrictions

The function call operator for an extended lambda is not `constexpr`. Therefore, the closure type for an extended lambda is not a literal type, and the `constexpr` and `consteval` specifiers cannot be used in the declaration of an extended lambda [CUDA_C_Programming_Guide:L18642-L18736].

## Capture in `if-constexpr` Blocks

A variable cannot be implicitly captured inside an `if-constexpr` block lexically nested inside an extended lambda, unless:
1. It has already been implicitly captured earlier outside the `if-constexpr` block, or
2. It appears in the explicit capture list for the extended lambda [CUDA_C_Programming_Guide:L18642-L18736].

### Example

```cpp
void foo(void) {
  // OK: an init-capture is allowed for an extended __device__ lambda.
  auto lam1 = [x = 1] __device__ () { return x; };

  // Error: an init-capture is not allowed for an extended __host__ __device__ lambda.
  auto lam2 = [x = 1] __host__ __device__ () { return x; };

  int a = 1;
  // Error: an extended __device__ lambda cannot capture variables by reference.
  auto lam3 = [&a] __device__ () { return a; };

  // Error: by-reference capture is not allowed for an extended __device__ lambda.
  auto lam4 = [&x = a] __device__ () { return x; };

  struct S1_t { };
  S1_t s1;
  // Error: a type local to a function cannot be used in the type of a captured variable.
  auto lam6 = [s1] __device__ () { };

  // Error: an init-capture cannot be of type std::initializer_list.
  auto lam7 = [x = {11}] __device__ () { };

  std::initializer_list<int> b = {11,22,33};
  // Error: an init-capture cannot be of type std::initializer_list.
  auto lam8 = [x = b] __device__ () { };

  // Error scenario (lam9) and supported scenarios (lam10, lam11) for capture within 'if-constexpr' block
  int yyy = 4;
  auto lam9 = [=] __device__ {
    int result = 0;
    if constexpr(false) {
      // Error: An extended __device__ lambda cannot first-capture 'yyy' in constexpr-if context
      result += yyy;
    }
    return result;
  };

  auto lam10 = [yyy] __device__ {
    int result = 0;
    if constexpr(false) {
      // OK: 'yyy' already listed in explicit capture list for the extended lambda
      result += yyy;
    }
    return result;
  };

  auto lam11 = [=] __device__ {
    int result = yyy;
    if constexpr(false) {
      // OK: 'yyy' already implicit captured outside the 'if-constexpr' block
      result += yyy;
    }
    return result;
  };
}
```
