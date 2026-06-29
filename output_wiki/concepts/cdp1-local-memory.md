# CDP1 Local Memory

In the context of CUDA Dynamic Parallelism version 1 (CDP1), local memory serves as private storage for an executing thread. This storage is not visible outside of the thread in which it is created [CUDA_C_Programming_Guide:L14441-L14471].

## Restrictions on Child Kernel Launches

It is illegal to pass a pointer to local memory as a launch argument when launching a child kernel. Attempting to dereference such a local memory pointer from within the child kernel results in undefined behavior [CUDA_C_Programming_Guide:L14441-L14471].

For example, the following code is illegal because `x_array` is created in the parent's local memory:

```cpp
int x_array[10];      // Creates x_array in parent's local memory
child_launch<<< 1, 1 >>>(x_array);
```

If `x_array` is accessed by `child_launch`, the behavior is undefined [CUDA_C_Programming_Guide:L14441-L14471].

## Correct Allocation Practices

Programmers must be aware that the compiler may place variables into local memory, which can sometimes be difficult to detect. As a general rule, all storage passed to a child kernel should be allocated explicitly from the global-memory heap. This can be achieved using `cudaMalloc()`, `new()`, or by declaring `__device__` storage at global scope [CUDA_C_Programming_Guide:L14441-L14471].

### Valid Example

The following example demonstrates correct usage, where `value` is global storage:

```dart
// Correct - "value" is global storage
__device__ int value;
__device__ void x() {
    value = 5;
    child<<< 1, 1 >>>(&value);
}
```

### Invalid Example

The following example is invalid because `value` is local storage:

```dart
// Invalid - "value" is local storage
__device__ void y() {
    int value = 5;
    child<<< 1, 1 >>>(&value);
}
```

## See Also

For the CDP2 version of this document, see Local Memory, above [CUDA_C_Programming_Guide:L14441-L14471].
