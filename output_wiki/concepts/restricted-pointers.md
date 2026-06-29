# Restricted Pointers (__restrict__)

nvcc supports restricted pointers via the `__restrict__` keyword [CUDA_C_Programming_Guide:L6757-L6759].

## Purpose

Restricted pointers were introduced in C99 to alleviate the aliasing problem that exists in C-type languages [CUDA_C_Programming_Guide:L6761-L6763]. This aliasing problem inhibits various compiler optimizations, including code re-ordering and common sub-expression elimination [CUDA_C_Programming_Guide:L6763].

## Mechanism

In standard C-type languages, pointers may be aliased, meaning that a write through one pointer could modify the data accessed by another [CUDA_C_Programming_Guide:L6779]. For example, if pointers `a`, `b`, and `c` are not restricted, the compiler cannot assume that writing to `c` does not overwrite elements of `a` or `b` [CUDA_C_Programming_Guide:L6780]. Consequently, the compiler cannot load `a[0]` and `b[0]` into registers, multiply them, and store the result to multiple locations (e.g., `c[0]` and `c[1]`) because the value of `a[0]` might change due to the write to `c[0]` [CUDA_C_Programming_Guide:L6781]. Similarly, the compiler cannot reorder computations involving `c` because preceding writes to `c` could alter the inputs for subsequent calculations [CUDA_C_Programming_Guide:L6782].

By applying the `__restrict__` keyword to pointer arguments, the programmer asserts to the compiler that these pointers do not alias [CUDA_C_Programming_Guide:L6784]. This means that writes through one restricted pointer will never overwrite the data pointed to by another restricted pointer [CUDA_C_Programming_Guide:L6785].

### Example

Without `__restrict__`, the compiler must treat potential aliasing conservatively:

```c
void foo(const float* a,
         const float* b,
         float* c)
{
    c[0] = a[0] * b[0];
    c[1] = a[0] * b[0];
    c[2] = a[0] * b[0] * a[1];
    c[3] = a[0] * a[1];
    c[4] = a[0] * b[0];
    c[5] = b[0];
    ...
}
```

With `__restrict__`, the compiler can optimize the code by caching loads and eliminating common sub-expressions:

```c
void foo(const float* __restrict__ a,
         const float* __restrict__ b,
         float* __restrict__ c)
{
    float t0 = a[0];
    float t1 = b[0];
    float t2 = t0 * t1;
    float t3 = a[1];
    c[0] = t2;
    c[1] = t2;
    c[4] = t2;
    c[2] = t2 * t3;
    c[3] = t0 * t3;
    c[5] = t1;
    ...
}
```

## Benefits

When `__restrict__` is applied, the compiler can freely reorder instructions and perform common sub-expression elimination while maintaining functional correctness identical to the abstract execution model [CUDA_C_Programming_Guide:L6788]. This results in:

*   A reduced number of memory accesses.
*   A reduced number of computations [CUDA_C_Programming_Guide:L6790].

## Caveats

The optimization benefits of `__restrict__` come with a trade-off: an increase in register pressure due to "cached" loads and common sub-expressions [CUDA_C_Programming_Guide:L6791].

Since register pressure is a critical issue in many CUDA codes, the use of restricted pointers can have a negative performance impact by reducing occupancy [CUDA_C_Programming_Guide:L6793]. Therefore, developers should evaluate the balance between optimization gains and register usage when applying `__restrict__`.

## Notes

*   All pointer arguments that participate in the optimization must be marked as restricted for the compiler to derive benefits [CUDA_C_Programming_Guide:L6787].
*   The `__restrict__` keyword is supported by nvcc [CUDA_C_Programming_Guide:L6757].
