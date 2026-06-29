# Friend Functions

In CUDA C++, specific restrictions apply when declaring `__global__` functions or function templates as friends within a class or struct. A `__global__` function or function template cannot be defined inside a friend declaration.

While declaring a `__global__` function as a friend is permitted (provided it is not defined at that point), attempting to provide the function body within the friend declaration results in a compilation error.

## Example

The following code illustrates valid and invalid friend declarations for `__global__` functions:

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
```

In the example above, `foo1` and `foo2` are valid because they are merely declared as friends without providing their implementation. `foo3` and `foo4` cause errors because they attempt to define the `__global__` function body directly within the friend declaration.

[CUDA_C_Programming_Guide:L17243-L17266]
