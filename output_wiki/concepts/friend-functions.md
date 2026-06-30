# Friend Functions

Restrictions on defining __global__ functions or templates in friend declarations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17237-L17264

Citation: [CUDA_C_Programming_Guide:L17237-L17264]

````text

It is not allowed to take the address of a \_\_device\_\_ function in host code.

## 18.5.10.6 Function Recursion

\_\_global\_\_ functions do not support recursion.

## 18.5.10.7 Friend Functions

A \_\_global\_\_ function or function template cannot be defined in a friend declaration.

Example:

```c
struct S1_t {
  friend __global__
  void foo1(void);  // OK: not a definition
  template<typename T>
  friend __global__
  void foo2(void); // OK: not a definition

  friend __global__
  void foo3(void) { } // error: definition in friend declaration

  template<typename T>
  friend __global__
  void foo4(void) { } // error: definition in friend declaration
};
````
