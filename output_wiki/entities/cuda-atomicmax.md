# atomicMax()

The `atomicMax()` function performs an atomic maximum operation. It reads the 32-bit or 64-bit word `old` located at the specified `address` in global or shared memory, computes the maximum of `old` and the input value `val`, and stores the result back to memory at the same address. These three operations (read, compute, write) are performed in one atomic transaction. The function returns the value of `old` that was previously stored at the address.

## Syntax

```cpp
int atomicMax(int* address, int val);
unsigned int atomicMax(unsigned int* address, unsigned int val);
unsigned long long int atomicMax(unsigned long long int* address, unsigned long long int val);
long long int atomicMax(long long int* address, long long int val);
```

## Parameters

- **address**: Pointer to the location in global or shared memory where the value is read from and written to.
- **val**: The value to compare against the existing value at `address`.

## Return Value

Returns the value previously stored at `address`.

## 64-bit Support

The 64-bit versions of `atomicMax()` (taking `unsigned long long int` or `long long int` arguments) are only supported by devices with compute capability 5.0 and higher.

## References

- CUDA C Programming Guide [CUDA_C_Programming_Guide:L7880-L7895]
