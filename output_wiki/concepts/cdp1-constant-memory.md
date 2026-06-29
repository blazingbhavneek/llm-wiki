# CDP1 Constant Memory

In the context of CUDA Dynamic Parallelism version 1 (CDP1), constant memory behaves with specific immutability and inheritance rules that distinguish it from other memory spaces.

## Immutability

Constant memory variables, declared with the `__constant__` qualifier, are immutable from the device side. They cannot be modified by any kernel execution, including both parent and child kernels [CUDA_C_Programming_Guide:L14424-L14426]. Consequently, the values of all `__constant__` variables must be set from the host program prior to the launch of any kernel that accesses them [CUDA_C_Programming_Guide:L14426].

## Inheritance by Child Kernels

A key feature of CDP1 constant memory is automatic inheritance. Constant memory is inherited automatically by all child kernels from their respective parent kernels [CUDA_C_Programming_Guide:L14427]. This ensures that child kernels have access to the same constant data as the parent without requiring explicit copying or passing of constant memory pointers.

## Address Semantics

Taking the address of a constant memory object from within a kernel thread follows the same semantics as in standard CUDA programs [CUDA_C_Programming_Guide:L14428]. Furthermore, passing the pointer to a constant memory object from a parent kernel to a child kernel, or vice versa, is naturally supported [CUDA_C_Programming_Guide:L14429].

## Relationship to Zero Copy Memory

Constant memory is distinct from Zero Copy memory, which is covered in the preceding section (13.6.1.2.1.2). While Zero Copy memory shares coherence and consistency guarantees with global memory, constant memory is defined by its immutability and automatic inheritance properties [CUDA_C_Programming_Guide:L14418-L14420].

## Note on CDP2

The documentation for CDP1 constant memory refers readers to the "Constant Memory" section for the CDP2 version of the document, indicating that behavior or semantics may differ in later versions of dynamic parallelism [CUDA_C_Programming_Guide:L14422-L14423].
