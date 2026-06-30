# atomicExch()

Performs an atomic exchange operation on 16-bit, 32-bit, 64-bit, and 128-bit types in global or shared memory. Stores a new value and returns the old value.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L7834-L7863

Citation: [CUDA_C_Programming_Guide:L7834-L7863]

````text
## 10.14.1.3 atomicExch()

```txt
int atomicExch(int* address, int val);
unsigned int atomicExch(unsigned int* address,
                    unsigned int val);
unsigned long long int atomicExch(unsigned long long int* address,
                    unsigned long long int val);
float atomicExch(float* address, float val);
```

reads the 32-bit or 64-bit word old located at the address address in global or shared memory and stores val back to memory at the same address. These two operations are performed in one atomic transaction. The function returns old.

```txt
template<typename T> T atomicExch(T* address, T val);
```

reads the 128-bit word old located at the address address in global or shared memory and stores val back to memory at the same address. These two operations are performed in one atomic transaction. The function returns old. The type T must meet the following requirements:

```cpp
sizeof(T) == 16
alignof(T) >= 16
std::is_trivially_copyable<T>::value == true
// for C++03 and older
std::is_default_constructible<T>::value == true
```

So, T must be 128-bit and properly aligned, be trivially copyable, and on C++03 or older, it must also be default constructible.

The 128-bit atomicExch() is only supported by devices of compute capability 9.x and higher.
````
