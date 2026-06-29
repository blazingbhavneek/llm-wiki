# atomicDec()

## Description

The `atomicDec()` function performs an atomic decrement operation on a 32-bit word located at a specified address in global or shared memory. This operation is executed as a single atomic transaction, ensuring thread safety without the need for explicit locking mechanisms.

## Syntax

```cpp
unsigned int atomicDec(unsigned int* address,
                       unsigned int val);
```

## Parameters

- **address**: A pointer to the 32-bit word in global or shared memory to be modified.
- **val**: The value used to determine the decrement logic.

## Return Value

The function returns the old value of the 32-bit word located at `address` before the operation was performed.

## Behavior

Let `old` be the value read from `address`. The function computes the new value using the following logic:

```cpp
new_val = ((old == 0) || (old > val)) ? val : (old - 1);
```

The computed `new_val` is then stored back to `address`. The three operations (read, compute, store) are performed atomically.

## Supported Types

- `unsigned int`

## References

- CUDA C Programming Guide: Section 10.14.1.7 [CUDA_C_Programming_Guide:L7906-L7914]
