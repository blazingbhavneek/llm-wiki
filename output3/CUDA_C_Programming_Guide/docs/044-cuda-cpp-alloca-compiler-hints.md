## 10.17. Alloca Function

## 10.17.1. Synopsis

```c
__host__ __device__ void * alloca(size_t size);
```

## 10.17.2. Description

The alloca() function allocates size bytes of memory in the stack frame of the caller. The returned value is a pointer to allocated memory, the beginning of the memory is 16 bytes aligned when the function is invoked from device code. The allocated memory is automatically freed when the caller to alloca() is returned.

Note: On Windows platform, <malloc.h> must be included before using alloca(). Using alloca() may cause the stack to overflow, user needs to adjust stack size accordingly.

It is supported with compute capability 5.2 or higher.

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

## 10.18.4. \_\_builtin\_expect()

```txt
long __builtin_expect (long exp, long c)
```

Indicates to the compiler that it is expected that exp == c, and returns the value of exp. Typically used to indicate branch prediction information to the compiler.

Example:

```txt
// indicate to the compiler that likely "var == 0",
// so the body of the if-block is unlikely to be
// executed at run time.
if (__builtin_expect (var, 0))
    doit ();
```

## 10.18.5. \_\_builtin\_unreachable()

```txt
void __builtin_unreachable(void)
```

Indicates to the compiler that control flow never reaches the point where this function is being called from. The program has undefined behavior if the control flow does actually reach this point at run time.

Example:

```txt
// indicates to the compiler that the default case label is never reached.
switch (in) {
case 1: return 4;
case 2: return 10;
default: __builtin_unreachable();
}
```

## 10.18.6. Restrictions

\_\_assume() is only supported when using cl.exe host compiler. The other functions are supported on all platforms, subject to the following restrictions:

▶ If the host compiler supports the function, the function can be invoked from anywhere in translation unit.

Otherwise, the function must be invoked from within the body of a \_\_device\_\_/ \_\_global\_\_function, or only when the \_\_CUDA\_ARCH\_\_ macro is defined<sup>5</sup>.

## 10.19. Warp Vote Functions
