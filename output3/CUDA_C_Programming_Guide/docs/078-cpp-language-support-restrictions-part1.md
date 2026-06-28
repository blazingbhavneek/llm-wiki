
## 18.5. Restrictions

## 18.5.1. Host Compiler Extensions

Host compiler specific language extensions are not supported in device code.

\_\_Complex types are only supported in host code.

\_\_int128 type is supported in device code when compiled in conjunction with a host compiler that supports it.

\_\_float128 type is supported for devices with compute capability 10.0 and later, when compiled in conjunction with a host compiler that supports the type. A constant expression of \_\_float128 type may be processed by the compiler in a floating point representation with lower precision.

## 18.5.2. Preprocessor Symbols

## 18.5.2.1 \_\_CUDA\_ARCH\_\_

1. The type signature of the following entities shall not depend on whether \_\_CUDA\_ARCH\_\_ is defined or not, or on a particular value of \_\_CUDA\_ARCH\_\_:

▶ \_\_global\_\_ functions and function templates

▶ \_\_device\_\_ and \_\_constant\_\_ variables

▶ textures and surfaces

Example:

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

2. If a \_\_global\_\_ function template is instantiated and launched from the host, then the function template must be instantiated with the same template arguments irrespective of whether \_\_CUDA\_ARCH\_\_ is defined and regardless of the value of \_\_CUDA\_ARCH\_\_

Example:

```txt
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

int main(void)
{
    foo();
    cudaDeviceSynchronize();
    return 0;
}
```

3. In separate compilation mode, the presence or absence of a definition of a function or variable with external linkage shall not depend on whether \_\_CUDA\_ARCH\_\_ is defined or on a particular value of \_\_CUDA\_ARCH\_\_<sup>Page</sup> <sup>327,</sup> <sup>7</sup>.

Example:

```c
#if !defined(__CUDA_ARCH__)
void foo(void) { }                      // error: The definition of foo()
                                // is only present when __CUDA_ARCH__
                                // is undefined
#endif
```

4. In separate compilation, \_\_CUDA\_ARCH\_\_ must not be used in headers such that diferent objects could contain diferent behavior. Or, it must be guaranteed that all objects will compile for the same compute\_arch. If a weak function or template function is defined in a header and its behavior depends on \_\_CUDA\_ARCH\_\_, then the instances of that function in the objects could conflict if the objects are compiled for diferent compute arch.

For example, if an a.h contains:

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

Then if a.cu and b.cu both include a.h and instantiate getptr for the same type, and b.cu expects a non-NULL address, and compile with:

```shell
nvcc -arch=compute_70 -dc a.cu
nvcc -arch=compute_80 -dc b.cu
nvcc -arch=sm_80 a.o b.o
```

At link time only one version of the getptr is used, so the behavior would depend on which version is chosen. To avoid this, either a.cu and b.cu must be compiled for the same compute arch, or \_\_CUDA\_ARCH\_\_ should not be used in the shared header function.

The compiler does not guarantee that a diagnostic will be generated for the unsupported uses of \_\_CUDA\_ARCH\_\_ described above.

## 18.5.3. Qualifiers

## 18.5.3.1 Device Memory Space Specifiers

The \_\_device\_\_, \_\_shared\_\_, \_\_managed\_\_ and \_\_constant\_\_ memory space specifiers are not allowed on:

▶ class, struct, and union data members,

formal parameters,

▶ non-extern variable declarations within a function that executes on the host.

The \_\_device\_\_, \_\_constant\_\_ and \_\_managed\_\_ memory space specifiers are not allowed on variable declarations that are neither extern nor static within a function that executes on the device.

A \_\_device\_\_, \_\_constant\_\_, \_\_managed\_\_ or \_\_shared\_\_ variable definition cannot have a class type with a non-empty constructor or a non-empty destructor. A constructor for a class type is considered empty at a point in the translation unit, if it is either a trivial constructor or it satisfies all of the following conditions:

▶ The constructor function has been defined.

▶ The constructor function has no parameters, the initializer list is empty and the function body is an empty compound statement.

▶ Its class has no virtual functions, no virtual base classes and no non-static data member initializers.

▶ The default constructors of all base classes of its class can be considered empty.

For all the nonstatic data members of its class that are of class type (or array thereof), the default constructors can be considered empty.

A destructor for a class is considered empty at a point in the translation unit, if it is either a trivial destructor or it satisfies all of the following conditions:

▶ The destructor function has been defined.

▶ The destructor function body is an empty compound statement.

▶ Its class has no virtual functions and no virtual base classes.

▶ The destructors of all base classes of its class can be considered empty.

▶ For all the nonstatic data members of its class that are of class type (or array thereof), the destructor can be considered empty.

When compiling in the whole program compilation mode (see the nvcc user manual for a description of this mode), \_\_device\_\_, \_\_shared\_\_, \_\_managed\_\_ and \_\_constant\_\_ variables cannot be defined as external using the extern keyword. The only exception is for dynamically allocated \_\_shared\_\_ variables as described in \_\_shared

When compiling in the separate compilation mode (see the nvcc user manual for a description of this mode), \_\_device\_\_, \_\_shared\_\_, \_\_managed\_\_ and \_\_constant\_\_ variables can be defined as external using the extern keyword. nvlink will generate an error when it cannot find a definition for an external variable (unless it is a dynamically allocated \_\_shared\_\_ variable).

## 18.5.3.2 \_\_managed\_\_ Memory Space Specifier

Variables marked with the \_\_managed\_\_ memory space specifier (“managed” variables) have the following restrictions:

▶ The address of a managed variable is not a constant expression.

A managed variable shall not have a const qualified type.

A managed variable shall not have a reference type.

▶ The address or value of a managed variable shall not be used when the CUDA runtime may not be in a valid state, including the following cases:

▶ In static/dynamic initialization or destruction of an object with static or thread local storage duration.

▶ In code that executes after exit() has been called (for example, a function marked with gcc’s “\_\_attribute\_\_((destructor))”).

▶ In code that executes when CUDA runtime may not be initialized (for example, a function marked with gcc’s “\_\_attribute\_\_((constructor))”).

▶ A managed variable cannot be used as an unparenthesized id-expression argument to a decltype() expression.

▶ Managed variables have the same coherence and consistency behavior as specified for dynamically allocated managed memory.
