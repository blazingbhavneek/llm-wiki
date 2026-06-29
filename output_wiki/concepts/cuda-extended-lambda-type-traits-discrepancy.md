# CUDA Extended Lambda Type Traits Discrepancy

When an extended `__device__` or `__host__ __device__` lambda expression is compiled, the CUDA compiler replaces it with an instance of a placeholder type in the code sent to the host compiler [CUDA_C_Programming_Guide:L18858-L18893]. This placeholder type may define C++ special member functions, such as constructors and destructors [CUDA_C_Programming_Guide:L18858-L18893].

As a result, certain standard C++ type traits may return different results for the closure type of the extended lambda when evaluated by the CUDA frontend compiler versus the host compiler [CUDA_C_Programming_Guide:L18858-L18893].

## Affected Type Traits

The following standard C++ type traits are affected by this discrepancy:

*   `std::is_trivially_copyable`
*   `std::is_trivially_constructible`
*   `std::is_trivially_copy_constructible`
*   `std::is_trivially_move_constructible`
*   `std::is_trivially_destructible` [CUDA_C_Programming_Guide:L18858-L18893]

## Usage Constraints

Care must be taken to avoid using the results of these type traits in contexts where the host and device code generation diverge. Specifically, these results should not be used in:

*   `__global__` function template instantiation
*   `__device__` variable template instantiation
*   `__constant__` variable template instantiation
*   `__managed__` variable template instantiation [CUDA_C_Programming_Guide:L18858-L18893]

## Example

The following example demonstrates a scenario where using `std::is_trivially_copyable` on an extended lambda's closure type in a `__global__` template instantiation can lead to errors, as the CUDA frontend compiler and the host compiler may disagree on the trait's value [CUDA_C_Programming_Guide:L18858-L18893].

```cpp
template <bool b>
void __global__ foo() { printf("hi"); }

template <typename T>
void dolaunch() {
    // ERROR: this kernel launch may fail, because CUDA frontend compiler
    // and host compiler may disagree on the result of
    // std::is_trivially_copyable() trait on the closure type of the
    // extended lambda
    foo<std::is_trivially_copyable<T>::value><<<1,1>>>();
    cudaDeviceSynchronize();
}

int main() {
    int x = 0;
    auto lam1 = [=] __host__ __device__ () { return x; };
    dolaunch<decltype(lam1)>();
}
```
