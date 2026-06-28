The \_\_forceinline\_\_ function qualifier can be used to force the compiler to inline the function.

The \_\_noinline\_\_ and \_\_forceinline\_\_ function qualifiers cannot be used together, and neither function qualifier can be applied to an inline function.

## 10.1.6. \_\_inline\_hint\_\_

The \_\_inline\_hint\_\_ qualifier enables more aggressive inlining in the compiler. Unlike \_\_forceinline\_\_, it does not imply that the function is inline. It can be used to improve inlining across modules when using LTO.

Neither the \_\_noinline\_\_ nor the \_\_forceinline\_\_ function qualifier can be used with the \_\_inline\_hint\_\_ function qualifier.

## 10.2. Variable Memory Space Specifiers

Variable memory space specifiers denote the memory location on the device of a variable.

An automatic variable declared in device code without any of the \_\_device\_\_, \_\_shared\_\_ and \_\_constant\_\_ memory space specifiers described in this section generally resides in a register. However in some cases the compiler might choose to place it in local memory, which can have adverse performance consequences as detailed in Device Memory Accesses.

## 10.2.1. \_\_device\_\_

The \_\_device\_\_ memory space specifier declares a variable that resides on the device.

At most one of the other memory space specifiers defined in the next three sections may be used together with \_\_device\_\_ to further denote which memory space the variable belongs to. If none of them is present, the variable:

▶ Resides in global memory space,

▶ Has the lifetime of the CUDA context in which it is created,

Has a distinct object per device,

▶ Is accessible from all the threads within the grid and from the host through the runtime library (cudaGetSymbolAddress() / cudaGetSymbolSize() / cudaMemcpyToSymbol() / cudaMemcpyFromSymbol()).

## 10.2.2. \_\_constant\_\_

The \_\_constant\_\_ memory space specifier, optionally used together with \_\_device\_\_, declares a variable that:

▶ Resides in constant memory space,

▶ Has the lifetime of the CUDA context in which it is created,

▶ Has a distinct object per device,

▶ Is accessible from all the threads within the grid and from the host through the runtime library (cudaGetSymbolAddress() / cudaGetSymbolSize() / cudaMemcpyToSymbol() / cudaMemcpyFromSymbol()).

The behavior of modifying a constant from the host while there is a concurrent grid that access that constant at any point of this grid’s lifetime is undefined.

## 10.2.3. \_\_shared\_\_

The \_\_shared\_\_ memory space specifier, optionally used together with \_\_device\_\_, declares a variable that:

▶ Resides in the shared memory space of a thread block,

▶ Has the lifetime of the block,

▶ Has a distinct object per block,

▶ Is only accessible from all the threads within the block,

Does not have a constant address.

When declaring a variable in shared memory as an external array such as

```txt
extern __shared__ float shared[];
```

the size of the array is determined at launch time (see Execution Configuration). All variables declared in this fashion, start at the same address in memory, so that the layout of the variables in the array must be explicitly managed through ofsets. For example, if one wants the equivalent of

```javascript
short array0[128];
float array1[64];
int array2[256];
```

in dynamically allocated shared memory, one could declare and initialize the arrays the following way:

```lisp
extern __shared__ float array[];
__device__ void func()      // __device__ or __global__ function
{
    short* array0 = (short*)array;
    float* array1 = (float*)&array0[128];
    int*   array2 =   (int*)&array1[64];
}
```

Note that pointers need to be aligned to the type they point to, so the following code, for example, does not work since array1 is not aligned to 4 bytes.

```lisp
extern __shared__ float array[];
__device__ void func()      // __device__ or __global__ function
{
    short* array0 = (short*)array;
    float* array1 = (float*)&array0[127];
}
```

Alignment requirements for the built-in vector types are listed in Table 7.

## 10.2.4. \_\_grid\_constant\_

The \_\_grid\_constant\_\_ annotation for compute architectures greater or equal to 7.0 annotates a const-qualified \_\_global\_\_ function parameter of non-reference type that:

▶ Has the lifetime of the grid,

▶ Is private to the grid, i.e., the object is not accessible to host threads and threads from other grids, including sub-grids,

▶ Has a distinct object per grid, i.e., all threads in the grid see the same address,

Is read-only, i.e., modifying a \_\_grid\_constant\_\_ object or any of its sub-objects is undefined behavior, including mutable members.

## Requirements:

Kernel parameters annotated with \_\_grid\_constant\_\_ must have const-qualified nonreference types.

▶ All function declarations must match with respect to any \_\_grid\_constant\_ parameters.

▶ A function template specialization must match the primary template declaration with respect to any \_\_grid\_constant\_\_ parameters.

▶ A function template instantiation directive must match the primary template declaration with respect to any \_\_grid\_constant\_\_ parameters.

If the address of a \_\_global\_\_ function parameter is taken, the compiler will ordinarily make a copy of the kernel parameter in thread local memory and use the address of the copy, to partially support C++ semantics, which allow each thread to modify its own local copy of function parameters. Annotating a \_\_global\_\_ function parameter with \_\_grid\_constant\_\_ ensures that the compiler will not create a copy of the kernel parameter in thread local memory, but will instead use the generic address of the parameter itself. Avoiding the local copy may result in improved performance.

```javascript
__device__ void unknown_function(S const&);
__global__ void kernel(const __grid_constant__ S s) {
    s.x += threadIdx.x;  // Undefined Behavior: tried to modify read-only memory

    // Compiler will _not_ create a per-thread thread local copy of "s":
    unknown_function(s);
}
```

## 10.2.5. \_\_managed

The \_\_managed\_\_ memory space specifier, optionally used together with \_\_device\_\_, declares a variable that:

▶ Can be referenced from both device and host code, for example, its address can be taken or it can be read or written directly from a device or host function.

▶ Has the lifetime of an application.

See \_\_managed\_\_ Memory Space Specifier for more details.

## 10.2.6. \_\_restrict\_\_

nvcc supports restricted pointers via the \_\_restrict\_\_ keyword.

Restricted pointers were introduced in C99 to alleviate the aliasing problem that exists in C-type languages, and which inhibits all kind of optimization from code re-ordering to common sub-expression elimination.

Here is an example subject to the aliasing issue, where use of restricted pointer can help the compiler to reduce the number of instructions:

```txt
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

In C-type languages, the pointers a, b, and c may be aliased, so any write through c could modify elements of a or b. This means that to guarantee functional correctness, the compiler cannot load a[0] and b[0] into registers, multiply them, and store the result to both c[0] and c[1], because the results would difer from the abstract execution model if, say, a[0] is really the same location as c[0]. So the compiler cannot take advantage of the common sub-expression. Likewise, the compiler cannot just reorder the computation of c[4] into the proximity of the computation of c[0] and c[1] because the preceding write to c[3] could change the inputs to the computation of c[4].

By making a, b, and c restricted pointers, the programmer asserts to the compiler that the pointers are in fact not aliased, which in this case means writes through c would never overwrite elements of a or b. This changes the function prototype as follows:

```c
void foo(const float* __restrict__ a,
        const float* __restrict__ b,
        float* __restrict__ c);
```

Note that all pointer arguments need to be made restricted for the compiler optimizer to derive any benefit. With the \_\_restrict\_\_ keywords added, the compiler can now reorder and do common sub-expression elimination at will, while retaining functionality identical with the abstract execution model:

```lisp
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

The efects here are a reduced number of memory accesses and reduced number of computations. This is balanced by an increase in register pressure due to “cached” loads and common subexpressions.

Since register pressure is a critical issue in many CUDA codes, use of restricted pointers can have negative performance impact on CUDA code, due to reduced occupancy.

## 10.3. Built-in Vector Types

## 10.3.1. char, short, int, long, longlong, float, double

These are vector types derived from the basic integer and floating-point types. They are structures and the 1st, 2nd, 3rd, and 4th components are accessible through the fields x, y, z, and w, respectively. They all come with a constructor function of the form make\_<type name>; for example,

```txt
int2 make_int2(int x, int y);
```

which creates a vector of type int2 with value(x, y).

The alignment requirements of the vector types are detailed in Table 7.

Table 7: Alignment Requirements

<table><tr><td>Type</td><td>Alignment</td></tr><tr><td>char1, uchar1</td><td>1</td></tr><tr><td>char2, uchar2</td><td>2</td></tr><tr><td>char3, uchar3</td><td>1</td></tr><tr><td>char4, uchar4</td><td>4</td></tr><tr><td>short1, ushort1</td><td>2</td></tr><tr><td>short2, ushort2</td><td>4</td></tr></table>

continues on next page

Table 7 – continued from previous page

<table><tr><td>Type</td><td>Alignment</td></tr><tr><td>short3, ushort3</td><td>2</td></tr><tr><td>short4, ushort4</td><td>8</td></tr><tr><td>int1, uint1</td><td>4</td></tr><tr><td>int2, uint2</td><td>8</td></tr><tr><td>int3, uint3</td><td>4</td></tr><tr><td>int4, uint4</td><td>16</td></tr><tr><td>long1, ulong1</td><td>4 if sizeof(long) is equal to sizeof(int) 8, otherwise</td></tr><tr><td>long2, ulong2</td><td>8 if sizeof(long) is equal to sizeof(int), 16, otherwise</td></tr><tr><td>long3, ulong3</td><td>4 if sizeof(long) is equal to sizeof(int), 8, otherwise</td></tr><tr><td>long $4^3$ </td><td rowspan="2">16</td></tr><tr><td>long4_16a</td></tr><tr><td>long4_32a</td><td>32</td></tr><tr><td>ulong $4^{Page\ 167,\ 3}$ </td><td rowspan="2">16</td></tr><tr><td>ulong4_16a</td></tr><tr><td>ulong4_32a</td><td>32</td></tr><tr><td>longlong1, ulonglong1</td><td>8</td></tr><tr><td>longlong2, ulonglong2</td><td>16</td></tr><tr><td>longlong3, ulonglong3</td><td>8</td></tr><tr><td>longlong $4^{Page\ 167,\ 3}$ </td><td rowspan="2">16</td></tr><tr><td>longlong4_16a</td></tr><tr><td>longlong4_32a</td><td>32</td></tr><tr><td>ulonglong $4^{Page\ 167,\ 3}$ </td><td rowspan="2">16</td></tr><tr><td>ulonglong4_16a</td></tr><tr><td>ulonglong4_32a</td><td>32</td></tr><tr><td>float1</td><td>4</td></tr><tr><td>float2</td><td>8</td></tr><tr><td>float3</td><td>4</td></tr><tr><td>float4</td><td>16</td></tr><tr><td>double1</td><td>8</td></tr><tr><td>double2</td><td>16</td></tr><tr><td>double3</td><td>8</td></tr></table>

continues on next page

Table 7 – continued from previous page

<table><tr><td>Type</td><td>Alignment</td></tr><tr><td>double4Page 167, 3</td><td rowspan="2">16</td></tr><tr><td>double4_16a</td></tr><tr><td>double4_32a</td><td>32</td></tr></table>

## 10.3.2. dim3

This type is an integer vector type based on uint3 that is used to specify dimensions. When defining a variable of type dim3, any component left unspecified is initialized to 1.

## 10.4. Built-in Variables
