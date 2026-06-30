# Device Memory Space Specifiers

Restrictions and rules for device memory space specifiers, including constructor/destructor constraints and compilation mode differences.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16642-L16681

Citation: [CUDA_C_Programming_Guide:L16642-L16681]

````text
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
````
