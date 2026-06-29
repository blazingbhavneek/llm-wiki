# Templates in CUDA

CUDA imposes specific restrictions on the types and templates that can be used as arguments in template instantiations within device code. These restrictions apply primarily to `__global__` function templates and `__device__`/`__constant__` variable templates.

## Restrictions on Template Arguments

A type or template cannot be used in the type, non-type, or template template argument of a `__global__` function template instantiation or a `__device__`/`__constant__` variable instantiation if any of the following conditions are met:

1. **Host-Only Definition**: The type or template is defined within a `__host__` or `__host__ __device__` scope. This ensures that device code does not rely on types that are not available or properly defined in the device execution environment.
2. **Private/Protected Class Members**: The type or template is a class member with private or protected access, and its parent class is not defined within a `__device__` or `__global__` function. This prevents device code from accessing restricted members of classes that are not fully available in the device context.
3. **Unnamed Types**: The type is unnamed. Unnamed types, such as local structs or closure types from lambdas, cannot be used as template arguments in device code.
4. **Compounded Types**: The type is compounded from any of the types listed above. If a type is derived from or composed of any restricted type, it inherits the restriction.

## Debugging Layout Mismatches

When working with templates in CUDA, it is important to ensure that the layout of types is consistent between host and device code. One way to debug suspected layout mismatches of a type `C` is to use `printf` to output the values of `sizeof(C)` and `offsetof(C, field)` in both host and device code. This can help identify discrepancies in how the compiler interprets the type's memory layout.

## Examples

### Example 1: Private Class Member

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
```

In this example, `inner_t` is a private member of `myClass`. Attempting to use `inner_t` as a template argument for `myKernel` results in an error because `inner_t` is not accessible from the device code.

### Example 2: Local and Closure Types (C++14)

```cpp
// C++14 only
template <typename T> __device__ T d1;

template <typename T1, typename T2> __device__ T1 d2;

void fn() {
    struct S1_t { };
    // error (C++14 only): S1_t is local to the function fn
    d1<S1_t> = {};

    auto lam1 = [] { };
    // error (C++14 only): a closure type cannot be used for
    // instantiating a variable template
    d2<int, decltype(lam1)> = 10;
}
```

In this example, `S1_t` is a local struct defined within the function `fn`, and `lam1` is a lambda with an unnamed closure type. Both are invalid as template arguments for `__device__` variable templates because they are not accessible or named in a way that allows device code to reference them.

## References

- [CUDA_C_Programming_Guide:L17354-L17401]
