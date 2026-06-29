# CUDA Extended Lambda Type Introspection

CUDA extended lambdas allow device code to be defined within host functions. However, the CUDA compiler handles these lambdas differently depending on whether they are accessed from host or device code, leading to specific limitations on type introspection in host contexts.

## Host-Side Introspection Limitations

When a `__device__` extended lambda is defined in host code, the CUDA compiler replaces it with a placeholder type defined in namespace scope [CUDA_C_Programming_Guide:L18758-L18797]. 

Unless the type trait `__nv_is_extended_device_lambda_with_preserved_return_type()` returns `true` for the closure type of the extended lambda, this placeholder type does not define an `operator()` function equivalent to the original lambda declaration [CUDA_C_Programming_Guide:L18758-L18797]. Consequently, attempting to determine the return type or parameter types of the `operator()` function using host-side type traits (such as `std::result_of` or `std::invoke_result`) may fail or produce incorrect results [CUDA_C_Programming_Guide:L18758-L18797]. This occurs because the code processed by the host compiler is semantically different from the input code processed by the CUDA compiler [CUDA_C_Programming_Guide:L18758-L18797].

### Example of Failure

The following example demonstrates a case where host-side introspection fails:

```cpp
#include <type_traits>

void foo(void) {
    auto lam1 = [] __device__ { return "10"; };

    // Error: attempt to extract the return type
    // of a __device__ lambda in host code
    std::result_of<decltype(lam1)()>::type xx1 = "abc";
}
```

In this case, `lam1` is a `__device__` lambda without a preserved return type, so the host compiler cannot correctly resolve its return type [CUDA_C_Programming_Guide:L18758-L18797].

## Conditions for Preserved Return Types

Introspection in host code is supported under two specific conditions:

1.  **`__host__ __device__` Lambdas:** The restriction does not apply to extended lambdas that are both host and device callable [CUDA_C_Programming_Guide:L18758-L18797].
2.  **Preserved Return Types:** The restriction does not apply to `__device__` extended lambdas for which `__nv_is_extended_device_lambda_with_preserved_return_type()` returns `true` [CUDA_C_Programming_Guide:L18758-L18797].

A `__device__` lambda typically has a preserved return type if its return type is explicitly specified and does not depend on the parameter types of the `operator()` in a way that prevents the compiler from determining it independently [CUDA_C_Programming_Guide:L18758-L18797].

### Examples of Success

**`__host__ __device__` Lambda:**

```cpp
auto lam2 = [] __host__ __device__ { return "10"; };

// OK : lam2 represents a __host__ __device__ extended lambda
std::result_of<decltype(lam2)()>::type xx2 = "abc";
```

**`__device__` Lambda with Explicit Return Type:**

```cpp
auto lam3 = [] __device__ () -> const char * { return "10"; };

// OK : lam3 represents a __device__ extended lambda with preserved return type
std::result_of<decltype(lam3)()>::type xx2 = "abc";
static_assert( std::is_same_v< std::result_of<decltype(lam3)()>::type, const char *> );
```

### Cases Where Return Type is Not Preserved

If a `__device__` lambda's trailing return type references the parameter types of the `operator()`, the return type is not preserved, and host-side introspection will fail [CUDA_C_Programming_Guide:L18758-L18797].

```cpp
const char& getRef(const char* p) { return *p; }

auto lam4 = [] __device__ (char x) -> decltype(getRef(&x)) { return 0; };
// lam4's return type is not preserved because it references the operator()'s
// parameter types in the trailing return type.
static_assert( ! __nv_is_extended_device_lambda_with_preserved_return_type(decltype(lam4)), "" );
```

## Device-Side Introspection

Unlike host code, it is permissible to introspect the return type or parameter types of the `operator()` function within device code [CUDA_C_Programming_Guide:L18758-L18797]. The limitations described above apply specifically to the host compiler's view of the placeholder type [CUDA_C_Programming_Guide:L18758-L18797].

## Related Traits

*   `__nv_is_extended_device_lambda_with_preserved_return_type`: A type trait that returns `true` if the closure type of an extended lambda has a preserved return type, allowing for correct host-side introspection [CUDA_C_Programming_Guide:L18758-L18797].
