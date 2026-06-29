# atomicExch()

The `atomicExch()` function performs an atomic exchange operation on a memory location. It reads the current value from the specified address, stores a new value at that address, and returns the original value read. These read and write operations are performed as a single atomic transaction, ensuring that no other thread can modify the memory location between the read and the write.

## 32-bit and 64-bit Variants

Standard variants of `atomicExch()` support 32-bit and 64-bit data types. These functions operate on global or shared memory.

### Signatures

```cpp
int atomicExch(int* address, int val);
unsigned int atomicExch(unsigned int* address, unsigned int val);
unsigned long long int atomicExch(unsigned long long int* address, unsigned long long int val);
float atomicExch(float* address, float val);
```

### Behavior

For these types, `atomicExch()` reads the 32-bit or 64-bit word `old` located at the `address` in global or shared memory and stores `val` back to memory at the same address. The function returns `old`.

## 128-bit Variant (Template)

A template-based variant exists for 128-bit atomic operations.

### Signature

```cpp
template<typename T> T atomicExch(T* address, T val);
```

### Requirements

The type `T` must meet the following requirements:

*   `sizeof(T) == 16` (128-bit size)
*   `alignof(T) >= 16` (16-byte alignment)
*   `std::is_trivially_copyable<T>::value == true` (trivially copyable)
*   For C++03 and older: `std::is_default_constructible<T>::value == true` (default constructible)

### Hardware Support

The 128-bit `atomicExch()` is only supported by devices with compute capability 9.x and higher.

## References

*   CUDA C Programming Guide: [CUDA_C_Programming_Guide:L7834-L7863]
