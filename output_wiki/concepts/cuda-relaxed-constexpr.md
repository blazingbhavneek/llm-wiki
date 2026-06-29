# CUDA Relaxed Constexpr

The `-expt-relaxed-constexpr` flag enables cross-execution space calls to `constexpr` functions in contexts that require constant evaluation. By default, the CUDA compiler restricts such calls between host and device execution spaces to prevent ambiguity during code generation phases.

## Default Behavior

Without the `-expt-relaxed-constexpr` flag, the following cross-execution space calls are not supported:

1. **Host calling Device**: Calling a `__device__`-only `constexpr` function from a `__host__` function during the host code generation phase (when the `__CUDA_ARCH__` macro is undefined). For example:

   ```cpp
   constexpr __device__ int D() { return 0; }
   int main() {
       int x = D();  // ERROR: calling a __device__-only constexpr function from host code
   }
   ```

2. **Device/Global calling Host**: Calling a `__host__`-only `constexpr` function from a `__device__` or `__global__` function during the device code generation phase (when the `__CUDA_ARCH__` macro is defined). For example:

   ```cpp
   constexpr int H() { return 0; }
   __device__ void dmain() {
       int x = H();  // ERROR: calling a __host__-only constexpr function from device code
   }
   ```

## Relaxed Behavior

When the `-expt-relaxed-constexpr` flag is specified, the compiler supports cross-execution space calls if they occur in a context that requires constant evaluation, such as the initializer of a `constexpr` variable.

### Examples

**Device constexpr called from Host:**

```cpp
constexpr __device__ int D(int x) { return x+1; }
int main() {
    constexpr int val = D(1); // OK: call is in a context that requires constant evaluation.
}
```

**Host constexpr called from Device:**

```cpp
constexpr __host__ int H(int x) { return x+1; };
__global__ void doit() {
    constexpr int val = H(1); // OK: call is in a context that requires constant evaluation.
}
```

In these relaxed scenarios, the compiler can resolve the function call at compile time because the value is required to be a constant expression, eliminating the need for runtime execution across execution spaces.

## References

- [CUDA_C_Programming_Guide:L19074-L19116]
