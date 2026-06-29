# Windows-Specific Class Layout Constraints

When compiling CUDA code with the Microsoft Visual C++ (MSVC) host compiler, a fundamental incompatibility exists between the class layout rules used by the CUDA compiler and those used by the host compiler. This discrepancy can lead to undefined behavior when objects are shared between host and device execution spaces.

## ABI Divergence

The CUDA compiler follows the IA64 ABI for class layout, whereas the Microsoft host compiler does not adhere to this standard [CUDA_C_Programming_Guide:L17332-L17353]. Consequently, the CUDA compiler may compute the class layout and size differently than the Microsoft host compiler for specific types [CUDA_C_Programming_Guide:L17332-L17353].

## Affected Types

Let $T$ denote a pointer to member type, or a class type that satisfies any of the following conditions:

* $T$ has virtual functions.
* $T$ has a virtual base class.
* $T$ has multiple inheritance with more than one direct or indirect empty base class.
* All direct and indirect base classes $B$ of $T$ are empty, and the type of the first field $F$ of $T$ uses $B$ in its definition, such that $B$ is laid out at offset 0 in the definition of $F$ [CUDA_C_Programming_Guide:L17332-L17353].

Let $C$ denote $T$ or a class type that has $T$ as a field type or as a base class type [CUDA_C_Programming_Guide:L17332-L17353].

## Safe Usage

As long as the type $C$ is used exclusively in host code or exclusively in device code, the program should work correctly [CUDA_C_Programming_Guide:L17332-L17353].

## Undefined Behavior

Passing an object of type $C$ between host and device code results in undefined behavior. This includes:

* Passing an object of type $C$ as an argument to a `__global__` function.
* Passing an object of type $C$ through `cudaMemcpy*()` calls [CUDA_C_Programming_Guide:L17332-L17353].

Additionally, the following scenarios result in undefined behavior:

* Accessing an object of type $C$ or any subobject in device code, or invoking a member function in device code, if the object is created in host code [CUDA_C_Programming_Guide:L17332-L17353].
* Accessing an object of type $C$ or any subobject in host code, or invoking a member function in host code, if the object is created in device code [CUDA_C_Programming_Guide:L17332-L17353].
