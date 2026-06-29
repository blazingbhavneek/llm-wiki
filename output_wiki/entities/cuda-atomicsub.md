# atomicSub()

The `atomicSub()` function performs an atomic subtraction operation on a 32-bit word located at a specified memory address. It is available for both signed and unsigned 32-bit integers.

## Syntax

```c
int atomicSub(int* address, int val);
unsigned int atomicSub(unsigned int* address, unsigned int val);
```

## Description

The function reads the 32-bit word `old` located at the `address` in global or shared memory, computes `(old - val)`, and stores the result back to memory at the same address. These three operations (read, compute, write) are performed in one atomic transaction, ensuring that no other thread can modify the value between the read and the write.

The function returns the original value (`old`) that was stored at the address before the subtraction occurred.

## Supported Types

- `int` (signed 32-bit integer)
- `unsigned int` (unsigned 32-bit integer)

## Memory Scope

The `address` parameter must point to memory located in either global or shared memory [CUDA_C_Programming_Guide:L7824-L7833].

## Example Usage

```c
int* data = ...; // Pointer to global or shared memory
int val = 5;

// Atomically subtract 5 from *data
int old_value = atomicSub(data, val);

// old_value now holds the value of *data before the subtraction
```

## See Also

- `atomicAdd()`
- `atomicAnd()`
- `atomicOr()`
- `atomicXor()`

## References

- CUDA C Programming Guide, Section 10.14.1.2 [CUDA_C_Programming_Guide:L7824-L7833]
