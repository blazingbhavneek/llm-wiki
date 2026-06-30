# 10.18.3 __assume()

Compiler optimization hint. Allows compiler to assume Boolean argument is true. Undefined behavior if false at runtime. Unspecified behavior if argument has side effects.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8499-L8516

Citation: [CUDA_C_Programming_Guide:L8499-L8516]

````text
```

## 10.18.3. \_\_assume()

```lisp
void __assume(bool exp)
```

Allows the compiler to assume that the Boolean argument is true. If the argument is not true at run time, then the behavior is undefined. Note that if the argument has side efects, the behavior is unspecified.

## Example:

```lisp
__device__ int get(int *ptr, int idx) {
    __assume(idx <= 2);
    return ptr[idx];
}
```
````
