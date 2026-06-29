# atomicMin()

The `atomicMin()` function performs an atomic minimum operation on a value located at a specified memory address. It reads the current 32-bit or 64-bit word `old` at `address` in global or shared memory, computes the minimum of `old` and the input `val`, and stores the result back to the same address. These three operations (read, compute, write) are performed in a single atomic transaction. The function returns the original value `old` that was located at the address before the operation.

## Syntax

```c
int atomicMin(int* address, int val);
unsigned int atomicMin(unsigned int* address, unsigned int val);
unsigned long long int atomicMin(unsigned long long int* address, unsigned long long int val);
long long int atomicMin(long long int* address, long long int val);
```

## Supported Types

The function supports the following integer types:
- `int`
- `unsigned int`
- `unsigned long long int`
- `long long int`

## 64-bit Support

The 64-bit versions of `atomicMin()` (i.e., those taking `unsigned long long int` or `long long int` arguments) are only supported by devices with compute capability 5.0 and higher. The 32-bit versions are supported on all devices that support atomic operations.

## References

- CUDA C Programming Guide [CUDA_C_Programming_Guide:L7864-L7879]
