# 10.18.1 __builtin_assume_aligned()

Compiler optimization hint. Allows compiler to assume pointer is aligned to at least align bytes. Returns argument pointer. Supports two-parameter and three-parameter versions (with offset).

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8437-L8465

Citation: [CUDA_C_Programming_Guide:L8437-L8465]

````text

## 10.17.3. Example

```txt
__device__ void foo(unsigned int num) {
    int4 *ptr = (int4 *)alloca(num * sizeof(int4));
    // use of ptr
    ...
}
```

## 10.18. Compiler Optimization Hint Functions

The functions described in this section can be used to provide additional information to the compiler optimizer.

## 10.18.1. \_\_builtin\_assume\_aligned()

```txt
void * __builtin_assume_aligned (const void *exp, size_t align)
```

Allows the compiler to assume that the argument pointer is aligned to at least align bytes, and returns the argument pointer.

Example:

```txt
void *res = __builtin_assume_aligned(ptr, 32); // compiler can assume 'res' is
// at least 32-byte aligned
```
````
