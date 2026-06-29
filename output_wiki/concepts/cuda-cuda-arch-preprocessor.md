# CUDA __CUDA_ARCH__ Preprocessor Symbol

The `__CUDA_ARCH__` preprocessor symbol is defined by the CUDA compiler (`nvcc`) when compiling code for the device. It allows developers to write code that behaves differently depending on whether it is being compiled for the host (CPU) or the device (GPU), or to differentiate between specific GPU architectures.

However, because CUDA code is often compiled in separate compilation modes and linked together, or because host code may instantiate device templates, the use of `__CUDA_ARCH__` is subject to strict restrictions to prevent linker errors and undefined behavior.

## Restrictions on Type Signatures

The type signature of certain entities must remain consistent regardless of whether `__CUDA_ARCH__` is defined or what its value is. Specifically, the following entities shall not have type signatures that depend on `__CUDA_ARCH__`:

*   `__global__` functions and function templates
*   `__device__` and `__constant__` variables
*   Textures and surfaces

If the type of a variable or parameter changes based on `__CUDA_ARCH__`, the compiler will generate an error. For example, the following code is invalid because the type of `xxx` and the parameters of `foo` depend on the definition of `__CUDA_ARCH__`:

```c
#if !defined(__CUDA_ARCH__)
typedef int mytype;
#else
typedef double mytype;
#endif

__device__ mytype xxx;          // error: xxx's type depends on __CUDA_ARCH__
__global__ void foo(mytype in, // error: foo's type depends on __CUDA_ARCH__
                 mytype *ptr)
{
    *ptr = in;
}
```

## Template Instantiation Consistency

When a `__global__` function template is instantiated and launched from the host, the template arguments used for instantiation must be identical regardless of whether `__CUDA_ARCH__` is defined. This ensures that the device code generated matches the host's expectations.

For example, the following code results in an error because the instantiation of `kern<int>` only occurs when `__CUDA_ARCH__` is undefined (i.e., on the host):

```cpp
__device__ int result;
template <typename T>
__global__ void kern(T in)
{
    result = in;
}

__host__ __device__ void foo(void)
{
#if !defined(__CUDA_ARCH__)
    kern<<<1,1>>>(1);      // error: "kern<int>" instantiation only
                                // when __CUDA_ARCH__ is undefined!
#endif
}
```

## Separate Compilation and External Linkage

In separate compilation mode, the presence or absence of a definition for a function or variable with external linkage must not depend on `__CUDA_ARCH__`. This prevents linker conflicts where one object file provides a definition and another does not, or where different definitions are provided.

The following code is invalid because the definition of `foo` is only present when `__CUDA_ARCH__` is undefined:

```c
#if !defined(__CUDA_ARCH__)
void foo(void) { }                      // error: The definition of foo()
                                // is only present when __CUDA_ARCH__
                                // is undefined
#endif
```

## Header Usage and Compute Architecture Conflicts

`__CUDA_ARCH__` must not be used in headers in a way that causes different compilation units to contain different behaviors, unless it is guaranteed that all objects will compile for the same `compute_arch`. 

If a weak function or template function is defined in a header and its behavior depends on `__CUDA_ARCH__`, instances of that function in different objects may conflict if those objects are compiled for different compute architectures. At link time, only one version of the function is typically used, leading to potential logical errors if the wrong version is selected.

For example, consider a header `a.h`:

```c
template<typename T>
__device__ T* getptr(void)
{
#if __CUDA_ARCH__ == 700
    return NULL; /* no address */
#else
    __shared__ T arr[256];
    return arr;
#endif
}
```

If `a.cu` and `b.cu` both include `a.h` and instantiate `getptr` for the same type, but are compiled for different architectures:

```shell
nvcc -arch=compute_70 -dc a.cu
nvcc -arch=compute_80 -dc b.cu
nvcc -arch=sm_80 a.o b.o
```

`a.cu` will generate a version of `getptr` that returns `NULL`, while `b.cu` will generate a version that returns a shared memory array. If `b.cu` expects a non-NULL address, the link-time selection of one version over the other will cause undefined behavior.

To avoid this, either:
1.  All compilation units must be compiled for the same compute architecture.
2.  `__CUDA_ARCH__` should not be used in shared header functions.

## Compiler Diagnostics

The CUDA compiler does not guarantee that a diagnostic (warning or error) will be generated for all unsupported uses of `__CUDA_ARCH__` described above. Developers must adhere to these rules manually to ensure correct program behavior.

## References

[CUDA_C_Programming_Guide:L16542-L16639]
