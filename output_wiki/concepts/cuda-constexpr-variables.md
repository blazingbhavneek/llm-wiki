# Constexpr Variables in CUDA

In CUDA C++, `constexpr` variables defined at namespace scope or as class static members that lack execution space annotations (such as `__device__`, `__constant__`, or `__shared__`) are treated as host code variables [CUDA_C_Programming_Guide:L17623-L17659].

## Usage in Device Code

While these variables are host-side entities, their values can be utilized in device code under specific conditions:

1.  **Scalar Types**: If the variable `V` is of a scalar type other than `long double` and is not `volatile`-qualified, its value can be directly used in device code [CUDA_C_Programming_Guide:L17623-L17659].
2.  **Non-Scalar Types**: If `V` is of a non-scalar type, its scalar elements can be accessed inside a `__device__` or `__host__ __device__` function, provided that the function call constitutes a constant expression [CUDA_C_Programming_Guide:L17623-L17659].

## Restrictions

Device source code is prohibited from taking a reference to or the address of such host `constexpr` variables [CUDA_C_Programming_Guide:L17623-L17659].

## Example

The following example illustrates valid and invalid uses of host `constexpr` variables within a `__device__` function:

```cpp
constexpr int xxx = 10;
constexpr int yyy = xxx + 4;
struct S1_t { static constexpr int qqq = 100; };

constexpr int host_arr[] = { 1, 2, 3};
constexpr __device__ int get(int idx) { return host_arr[idx]; }

__device__ int foo(int idx) {
    int v1 = xxx + yyy + S1_t::qqq; // OK: Direct use of scalar values
    const int &v2 = xxx; // error: reference to host constexpr variable
    const int *v3 = &xxx; // error: address of host constexpr variable
    const int &v4 = S1_t::qqq; // error: reference to host constexpr variable
    const int *v5 = &S1_t::qqq; // error: address of host constexpr variable

    v1 += get(2); // OK: 'get(2)' is a constant expression
    v1 += get(idx); // error: 'get(idx)' is not a constant expression
    v1 += host_arr[2]; // error: 'host_arr' does not have scalar type
    return v1;
}
```

In this example:
*   `xxx`, `yyy`, and `S1_t::qqq` are scalar host `constexpr` variables, so their values can be added directly to `v1` [CUDA_C_Programming_Guide:L17623-L17659].
*   Taking references (`v2`, `v4`) or addresses (`v3`, `v5`) of these variables results in compilation errors [CUDA_C_Programming_Guide:L17623-L17659].
*   The function `get(2)` is a constant expression because the argument is a literal, allowing its result to be used [CUDA_C_Programming_Guide:L17623-L17659].
*   `get(idx)` is not a constant expression because `idx` is a variable, and `host_arr[2]` fails because `host_arr` is an array (non-scalar type) [CUDA_C_Programming_Guide:L17623-L17659].
