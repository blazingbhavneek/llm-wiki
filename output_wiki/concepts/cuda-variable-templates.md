# Variable Templates in CUDA

CUDA supports variable templates, allowing variables to be defined with template parameters. These can be declared with `__device__` or `__constant__` qualifiers to reside in device memory.

## Microsoft Host Compiler Restrictions

When using the Microsoft host compiler (typically on Windows), there are specific restrictions regarding const qualification in variable templates. A `__device__` or `__constant__` variable template cannot have a `const` qualified type [CUDA_C_Programming_Guide:L17952-L17983].

### Invalid Examples

The following examples result in errors when compiled with the Microsoft host compiler because the variable template itself has a `const` qualified type:

```c
// error: a __device__ variable template cannot
// have a const qualified type on Windows
template <typename T>
__device__ const T d1(2);

int *const x = nullptr;
// error: a __device__ variable template cannot
// have a const qualified type on Windows
template <typename T>
__device__ T *const d2(x);
```

### Valid Examples

It is permissible for the variable template to point to a const type, or for the type itself to be non-const. The following examples are valid:

```c
// OK
template <typename T>
__device__ const T *d3;
```

In this case, `d3` is a pointer to a const type, but the pointer itself is not const, and the variable template definition is valid.

### Usage

Variable templates can be instantiated and used within device functions. For example:

```c
__device__ void fn() {
    int t1 = d1<int>; // Error if d1 is defined as above

    int *const t2 = d2<int>; // Error if d2 is defined as above

    const int *t3 = d3<int>; // OK
}
```

Note that while `d3` is valid, `d1` and `d2` as defined in the invalid examples would cause compilation errors on Windows with the Microsoft host compiler. On other host compilers, these restrictions may not apply, but the const qualification rules still govern the semantics of the instantiated variables. [CUDA_C_Programming_Guide:L17952-L17983]
