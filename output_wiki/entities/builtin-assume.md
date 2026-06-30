# 10.18.2 __builtin_assume()

Compiler optimization hint. Allows compiler to assume Boolean argument is true. Undefined behavior if false at runtime. Unspecified behavior if argument has side effects.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8466-L8498

Citation: [CUDA_C_Programming_Guide:L8466-L8498]

````text

Three parameter version:

```txt
void * __builtin_assume_aligned (const void *exp, size_t align,
                     <integral type> offset)
```

Allows the compiler to assume that (char \*)exp - offset is aligned to at least align bytes, and returns the argument pointer.

Example:

```lisp
void *res = __builtin_assume_aligned(ptr, 32, 8); // compiler can assume
// '(char *)res - 8' is
// at least 32-byte aligned.
```

## 10.18.2. \_\_builtin\_assume()

```txt
void __builtin_assume(bool exp)
```

Allows the compiler to assume that the Boolean argument is true. If the argument is not true at run time, then the behavior is undefined. Note that if the argument has side efects, the behavior is unspecified.

Example:

```txt
__device__ int get(int *ptr, int idx) {
    __builtin_assume(idx <= 2);
    return ptr[idx];
}
````
