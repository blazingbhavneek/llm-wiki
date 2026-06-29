# atomicInc()

The `atomicInc()` function performs an atomic increment operation on a 32-bit word located at a specified memory address. It is designed for use in global or shared memory.

## Syntax

```cpp
unsigned int atomicInc(unsigned int* address,
                       unsigned int val);
```

## Description

The function reads the 32-bit word `old` located at the `address` in global or shared memory. It then computes the new value using the formula `((old >= val) ? 0 : (old+1))` and stores the result back to memory at the same address. These three operations (read, compute, store) are performed in one atomic transaction, ensuring thread safety.

The function returns the original value `old` that was read from memory before the update.

## Parameters

- **address**: A pointer to the 32-bit unsigned integer in global or shared memory to be updated.
- **val**: The limit value. If the current value at `address` is greater than or equal to `val`, the value is reset to 0; otherwise, it is incremented by 1.

## Return Value

Returns the old value of the 32-bit word at `address` before the atomic operation.

## Supported Types

- `unsigned int`

## References

- CUDA C Programming Guide, Section 10.14.1.6 [CUDA_C_Programming_Guide:L7896-L7905]
