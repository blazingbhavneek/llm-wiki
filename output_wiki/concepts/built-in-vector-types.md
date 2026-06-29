# Built-in Vector Types

CUDA provides a set of built-in vector types derived from basic integer and floating-point types. These types are implemented as structures, allowing individual components to be accessed via the fields `x`, `y`, `z`, and `w`, which correspond to the 1st, 2nd, 3rd, and 4th components, respectively [CUDA_C_Programming_Guide:L6816-L6828].

## Standard Vector Types

The standard vector types include variants for `char`, `short`, `int`, `long`, `longlong`, `float`, and `double` [CUDA_C_Programming_Guide:L6816-L6828].

### Constructors

Each vector type comes with a corresponding constructor function named `make_<type name>` [CUDA_C_Programming_Guide:L6816-L6828]. For example, the `int2` type has a constructor `make_int2`:

```cpp
int2 make_int2(int x, int y);
```

This function creates a vector of type `int2` with the specified values [CUDA_C_Programming_Guide:L6816-L6828].

### Alignment

The alignment requirements for these vector types are defined in the CUDA C Programming Guide's alignment table [CUDA_C_Programming_Guide:L6816-L6828].

## The dim3 Type

The `dim3` type is a specialized integer vector type based on `uint3` [CUDA_C_Programming_Guide:L6846-L6848]. It is primarily used to specify dimensions, such as grid and block dimensions in kernel launches [CUDA_C_Programming_Guide:L6846-L6848].

When defining a variable of type `dim3`, any component that is left unspecified is automatically initialized to 1 [CUDA_C_Programming_Guide:L6846-L6848]. This behavior simplifies the declaration of dimensions where certain axes are not explicitly needed (e.g., a 2D grid can be defined as `dim3 grid(10, 10)` where the z-dimension defaults to 1) [CUDA_C_Programming_Guide:L6846-L6848].

## Related Topics

- Alignment Requirements
- Kernel Launch Configuration
