# Device Memory Space Specifiers

The `__device__`, `__shared__`, `__managed__`, and `__constant__` memory space specifiers are used to define variables with specific memory spaces in CUDA. There are strict restrictions on where these specifiers can be applied, particularly regarding class types, function parameters, and variable linkage.

## Restrictions on Usage

The `__device__`, `__shared__`, `__managed__`, and `__constant__` memory space specifiers are **not allowed** on:

*   Class, struct, and union data members.
*   Formal parameters of functions.
*   Non-`extern` variable declarations within a function that executes on the host.

Additionally, the `__device__`, `__constant__`, and `__managed__` memory space specifiers are **not allowed** on variable declarations that are neither `extern` nor `static` within a function that executes on the device.

## Class Type Requirements

A variable definition using `__device__`, `__constant__`, `__managed__`, or `__shared__` cannot have a class type with a non-empty constructor or a non-empty destructor. The compiler determines if a constructor or destructor is "empty" based on specific criteria.

### Empty Constructor

A constructor for a class type is considered empty at a point in the translation unit if it is either a trivial constructor or satisfies all of the following conditions:

1.  The constructor function has been defined.
2.  The constructor function has no parameters, the initializer list is empty, and the function body is an empty compound statement.
3.  Its class has no virtual functions, no virtual base classes, and no non-static data member initializers.
4.  The default constructors of all base classes of its class can be considered empty.
5.  For all nonstatic data members of its class that are of class type (or arrays thereof), the default constructors can be considered empty.

### Empty Destructor

A destructor for a class is considered empty at a point in the translation unit if it is either a trivial destructor or satisfies all of the following conditions:

1.  The destructor function has been defined.
2.  The destructor function body is an empty compound statement.
3.  Its class has no virtual functions and no virtual base classes.
4.  The destructors of all base classes of its class can be considered empty.
5.  For all nonstatic data members of its class that are of class type (or arrays thereof), the destructor can be considered empty.

## Linkage and Compilation Modes

The ability to define these variables as external using the `extern` keyword depends on the compilation mode.

### Whole Program Compilation Mode

When compiling in whole program compilation mode, `__device__`, `__shared__`, `__managed__`, and `__constant__` variables **cannot** be defined as external using the `extern` keyword. The only exception is for dynamically allocated `__shared__` variables.

### Separate Compilation Mode

When compiling in separate compilation mode, `__device__`, `__shared__`, `__managed__`, and `__constant__` variables **can** be defined as external using the `extern` keyword. In this mode, `nvlink` will generate an error if it cannot find a definition for an external variable, unless it is a dynamically allocated `__shared__` variable.

## References

[CUDA_C_Programming_Guide:L16642-L16681]
