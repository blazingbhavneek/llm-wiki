# Relaxed Constexpr

Experimental `-expt-relaxed-constexpr` flag enabling cross-execution space constexpr calls (host-to-device and device-to-host) when evaluated in constant-evaluation contexts.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19075-L19116

Citation: [CUDA_C_Programming_Guide:L19075-L19116]

````text

By default, the following cross-execution space calls are not supported:

1. Calling a \_\_device\_\_-only constexpr function from a \_\_host\_\_ function during host code generation phase (i.e, when \_\_CUDA\_ARCH\_\_ macro is undefined). Example:

```javascript
constexpr __device__ int D() { return 0; }
int main() {
    int x = D();  //ERROR: calling a __device__-only constexpr function
    from host code
}
```

2. Calling a \_\_host\_\_-only constexpr function from a \_\_device\_\_ or \_\_global\_\_ function, during device code generation phase (i.e. when \_\_CUDA\_ARCH\_\_ macro is defined). Example:

```txt
constexpr int H() { return 0; }
__device__ void dmain()
{
    int x = H();  //ERROR: calling a __host__-only constexpr function from
    device code
}
```

The experimental flag -expt-relaxed-constexpr can be used to relax this constraint. When this flag is specified, the compiler will support cross execution space calls described above, as follows:

1. A cross-execution space call to a constexpr function is supported if it occurs in a context that requires constant evaluation, e.g., in the initializer of a constexpr variable. Example:

```lisp
constexpr __host__ int H(int x) { return x+1; };
__global__ void doit() {
constexpr int val = H(1); // OK: call is in a context that
                                      // requires constant evaluation.
}

constexpr __device__ int D(int x) { return x+1; }
int main() {
constexpr int val = D(1); // OK: call is in a context that
                                      // requires constant evaluation.
}
```
````
