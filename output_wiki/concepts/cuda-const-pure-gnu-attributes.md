# Const and Pure GNU Attributes in CUDA

The `const` and `pure` GNU attributes are supported for both host and device functions, provided the language dialect and host compiler also support these attributes (e.g., when using the `g++` host compiler) [CUDA_C_Programming_Guide:L17489-L17519].

## Attribute Behavior

These attributes inform the device code optimizer about the function's interaction with mutable state, such as memory [CUDA_C_Programming_Guide:L17489-L17519].

### Pure Attribute

For a device function annotated with the `pure` attribute, the device code optimizer assumes that the function does not change any mutable state visible to caller functions (e.g., memory) [CUDA_C_Programming_Guide:L17489-L17519].

### Const Attribute

For a device function annotated with the `const` attribute, the device code optimizer assumes that the function does not access or change any mutable state visible to caller functions (e.g., memory) [CUDA_C_Programming_Guide:L17489-L17519].

## Example

The following example demonstrates the use of the `const` attribute to enable common subexpression elimination by the optimizer [CUDA_C_Programming_Guide:L17489-L17519]:

```cpp
__attribute__((const)) __device__ int get(int in);

__device__ int doit(int in) {
    int sum = 0;

    // because 'get' is marked with 'const' attribute
    // device code optimizer can recognize that the
    // second call to get() can be commoned out.
    sum = get(in);
    sum += get(in);

    return sum;
}
```

In this case, since `get` is marked as `const`, the optimizer recognizes that the second call to `get(in)` returns the same value as the first and can optimize the code accordingly [CUDA_C_Programming_Guide:L17489-L17519].
