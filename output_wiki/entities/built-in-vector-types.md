# Built-in Vector Types

Describes built-in vector types (char, short, int, long, float, double, dim3) derived from basic types, their component accessors (x, y, z, w), constructors, and alignment requirements.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6816-L6869

Citation: [CUDA_C_Programming_Guide:L6816-L6869]

````text
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

Built-in variables specify the grid and block dimensions and the block and thread indices. They are only valid within functions that are executed on the device.

## 10.4.1. gridDim

This variable is of type dim3 (see dim3) and contains the dimensions of the grid.

## 10.4.2. blockIdx

This variable is of type uint3 (see char, short, int, long, longlong, float, double) and contains the block index within the grid.

## 10.4.3. blockDim

This variable is of type dim3 (see dim3) and contains the dimensions of the block.

## 10.4.4. threadIdx

This variable is of type uint3 (see char, short, int, long, longlong, float, double) and contains the thread index within the block.
````
