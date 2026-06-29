# Variable Memory Space Specifiers

Variable memory space specifiers denote the memory location on the device of a variable [CUDA_C_Programming_Guide:L6621-L6631].

An automatic variable declared in device code without any of the `__device__`, `__shared__`, and `__constant__` memory space specifiers generally resides in a register. However, in some cases, the compiler might choose to place it in local memory, which can have adverse performance consequences [CUDA_C_Programming_Guide:L6621-L6631].

## __device__

The `__device__` memory space specifier declares a variable that resides on the device [CUDA_C_Programming_Guide:L6632-L6645].

At most one of the other memory space specifiers defined in the subsequent sections may be used together with `__device__` to further denote which memory space the variable belongs to [CUDA_C_Programming_Guide:L6632-L6645]. If none of them is present, the variable:

*   Resides in global memory space [CUDA_C_Programming_Guide:L6632-L6645].
*   Has the lifetime of the CUDA context in which it is created [CUDA_C_Programming_Guide:L6632-L6645].
*   Has a distinct object per device [CUDA_C_Programming_Guide:L6632-L6645].
*   Is accessible from all the threads within the grid and from the host through the runtime library (`cudaGetSymbolAddress()`, `cudaGetSymbolSize()`, `cudaMemcpyToSymbol()`, `cudaMemcpyFromSymbol()`) [CUDA_C_Programming_Guide:L6632-L6645].

## __constant__

The `__constant__` memory space specifier, optionally used together with `__device__`, declares a variable that:

*   Resides in constant memory space [CUDA_C_Programming_Guide:L6646-L6659].
*   Has the lifetime of the CUDA context in which it is created [CUDA_C_Programming_Guide:L6646-L6659].
*   Has a distinct object per device [CUDA_C_Programming_Guide:L6646-L6659].
*   Is accessible from all the threads within the grid and from the host through the runtime library (`cudaGetSymbolAddress()`, `cudaGetSymbolSize()`, `cudaMemcpyToSymbol()`, `cudaMemcpyFromSymbol()`) [CUDA_C_Programming_Guide:L6646-L6659].

The behavior of modifying a constant from the host while there is a concurrent grid that accesses that constant at any point of this grid’s lifetime is undefined [CUDA_C_Programming_Guide:L6646-L6659].

## __shared__

The `__shared__` memory space specifier, optionally used together with `__device__`, declares a variable that:

*   Resides in the shared memory space of a thread block [CUDA_C_Programming_Guide:L6660-L6712].
*   Has the lifetime of the block [CUDA_C_Programming_Guide:L6660-L6712].
*   Has a distinct object per block [CUDA_C_Programming_Guide:L6660-L6712].
*   Is only accessible from all the threads within the block [CUDA_C_Programming_Guide:L6660-L6712].
*   Does not have a constant address [CUDA_C_Programming_Guide:L6660-L6712].

When declaring a variable in shared memory as an external array, such as `extern __shared__ float shared[];`, the size of the array is determined at launch time [CUDA_C_Programming_Guide:L6660-L6712]. All variables declared in this fashion start at the same address in memory, so that the layout of the variables in the array must be explicitly managed through offsets [CUDA_C_Programming_Guide:L6660-L6712].

For example, if one wants the equivalent of:

```cpp
short array0[128];
float array1[64];
int array2[256];
```

in dynamically allocated shared memory, one could declare and initialize the arrays the following way:

```cpp
extern __shared__ float array[];
__device__ void func()      // __device__ or __global__ function
{
    short* array0 = (short*)array;
    float* array1 = (float*)&array0[128];
    int*   array2 =   (int*)&array1[64];
}
```

Pointers need to be aligned to the type they point to. For example, the following code does not work since `array1` is not aligned to 4 bytes:

```cpp
extern __shared__ float array[];
__device__ void func()      // __device__ or __global__ function
{
    short* array0 = (short*)array;
    float* array1 = (float*)&array0[127];
}
```

Alignment requirements for the built-in vector types are listed in Table 7 of the CUDA C++ Programming Guide [CUDA_C_Programming_Guide:L6660-L6712].

## __grid_constant__

The `__grid_constant__` annotation for compute architectures greater or equal to 7.0 annotates a const-qualified `__global__` function parameter of non-reference type that:

*   Has the lifetime of the grid [CUDA_C_Programming_Guide:L6713-L6736].
*   Is private to the grid, i.e., the object is not accessible to host threads and threads from other grids, including sub-grids [CUDA_C_Programming_Guide:L6713-L6736].
*   Has a distinct object per grid, i.e., all threads in the grid see the same address [CUDA_C_Programming_Guide:L6713-L6736].
*   Is read-only, i.e., modifying a `__grid_constant__` object or any of its sub-objects is undefined behavior, including mutable members [CUDA_C_Programming_Guide:L6713-L6736].

### Requirements

*   Kernel parameters annotated with `__grid_constant__` must have const-qualified nonreference types [CUDA_C_Programming_Guide:L6713-L6736].
*   All function declarations must match with respect to any `__grid_constant__` parameters [CUDA_C_Programming_Guide:L6713-L6736].
*   A function template specialization must match the primary template declaration with respect to any `__grid_constant__` parameters [CUDA_C_Programming_Guide:L6713-L6736].
*   A function template instantiation directive must match the primary template declaration with respect to any `__grid_constant__` parameters [CUDA_C_Programming_Guide:L6713-L6736].

If the address of a `__global__` function parameter is taken, the compiler will ordinarily make a copy of the kernel parameter in thread local memory and use the address of the copy, to partially support C++ semantics, which allow each thread to modify its own local copy of function parameters [CUDA_C_Programming_Guide:L6713-L6736]. Annotating a `__global__` function parameter with `__grid_constant__` ensures that the compiler will not create a copy of the kernel parameter in thread local memory, but will instead use the generic address of the parameter itself [CUDA_C_Programming_Guide:L6713-L6736]. Avoiding the local copy may result in improved performance [CUDA_C_Programming_Guide:L6713-L6736].

```cpp
__device__ void unknown_function(S const&);
__global__ void kernel(const __grid_constant__ S s) {
    s.x += threadIdx.x;  // Undefined Behavior: tried to modify read-only memory

    // Compiler will _not_ create a per-thread thread local copy of "s":
    unknown_function(s);
}
```

## __managed__

The `__managed__` memory space specifier, optionally used together with `__device__`, declares a variable that:

*   Can be referenced from both device and host code, for example, its address can be taken or it can be read or written directly from a device or host function [CUDA_C_Programming_Guide:L6737-L6756].
*   Has the lifetime of an application [CUDA_C_Programming_Guide:L6737-L6756].

See the `__managed__` Memory Space Specifier section for more details [CUDA_C_Programming_Guide:L6737-L6756].
