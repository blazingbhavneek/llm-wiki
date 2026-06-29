# atomicCAS()

The `atomicCAS()` function performs an atomic Compare And Swap operation. It reads the old value located at the specified address in global or shared memory, computes the result based on a comparison, and stores the result back to memory at the same address. These three operations (read, compare, store) are performed in one atomic transaction.

## Function Signatures

The function supports 16-bit, 32-bit, and 64-bit integer types, as well as a template version for 128-bit types.

### 16-bit, 32-bit, and 64-bit

```c
unsigned short int atomicCAS(unsigned short int *address,
                             unsigned short int compare,
                             unsigned short int val);

int atomicCAS(int* address, int compare, int val);

unsigned int atomicCAS(unsigned int* address,
                       unsigned int compare,
                       unsigned int val);

unsigned long long int atomicCAS(unsigned long long int* address,
                                 unsigned long long int compare,
                                 unsigned long long int val);
```

### 128-bit (Template)

```cpp
template<typename T> T atomicCAS(T* address, T compare, T val);
```

## Operation

For all supported types, the function performs the following logic:

1. Reads the old value `old` located at the address `address` in global or shared memory.
2. Computes `(old == compare ? val : old)`.
3. Stores the result back to memory at the same address.
4. Returns the original `old` value.

## 128-bit Support Requirements

The 128-bit template version of `atomicCAS()` has specific requirements for the type `T`:

*   `sizeof(T) == 16`
*   `alignof(T) >= 16`
*   `std::is_trivially_copyable<T>::value == true`
*   For C++03 and older: `std::is_default_constructible<T>::value == true`

Thus, `T` must be 128-bit, properly aligned, trivially copyable, and default constructible (on C++03 and older).

## Hardware Support

The 128-bit `atomicCAS()` is only supported by devices of compute capability 9.x and higher [CUDA_C_Programming_Guide:L7915-L7954].

## See Also

*   Atomic Functions
*   Compute Capability
