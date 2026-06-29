# Operators

## Assignment Operator

Specific restrictions apply to the assignment operator for certain types of variables in CUDA C++:

* **__constant__ variables**: These can only be assigned from host code through runtime functions (Device Memory). They cannot be assigned from device code [CUDA_C_Programming_Guide:L16853-L16866].
* **__shared__ variables**: These cannot have an initialization as part of their declaration [CUDA_C_Programming_Guide:L16853-L16866].
* **Built-in variables**: It is not allowed to assign values to any of the built-in variables defined in Built-in Variables [CUDA_C_Programming_Guide:L16853-L16866].

## Address Operator

It is not allowed to take the address of any of the built-in variables defined in Built-in Variables [CUDA_C_Programming_Guide:L16853-L16866].
