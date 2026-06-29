# Namespace Reservations

Unless an exception is otherwise noted, it is undefined behavior to add any declarations or definitions to `cuda::`, `nv::`, `cooperative_groups::` or any namespace nested within [CUDA_C_Programming_Guide:L16886-L16937].

## Invalid Usage

Adding symbols directly to reserved namespaces or their nested namespaces is prohibited. For example, defining a struct or a function within the `cuda` namespace is invalid [CUDA_C_Programming_Guide:L16886-L16937]:

```cpp
namespace cuda{
    // Bad: class declaration added to namespace cuda
    struct foo{};

    // Bad: function definition added to namespace cuda
    cudaStream_t make_stream(){
        cudaStream_t s;
        cudaStreamCreate(&s);
        return s;
    }
} // namespace cuda
```

Similarly, adding definitions to namespaces nested within reserved namespaces is also invalid [CUDA_C_Programming_Guide:L16886-L16937]:

```cpp
namespace cuda{
    namespace utils{
        // Bad: function definition added to namespace nested within cuda
        cudaStream_t make_stream(){
            cudaStream_t s;
            cudaStreamCreate(&s);
            return s;
        }
    } // namespace utils
} // namespace cuda
```

Using a namespace directive to bring symbols from a non-reserved namespace into a reserved one is also considered equivalent to adding symbols to the reserved namespace at global scope and is therefore bad practice [CUDA_C_Programming_Guide:L16886-L16937]:

```cpp
namespace utils{
    namespace cuda{
        cudaStream_t make_stream(){
            cudaStream_t s;
            cudaStreamCreate(&s);
            return s;
        }
    } // namespace cuda
}

// Bad: Equivalent to adding symbols to namespace cuda at global scope
using namespace utils;
```

## Valid Usage

It is permissible to use the reserved namespace names nested within a non-reserved namespace [CUDA_C_Programming_Guide:L16886-L16937]:

```cpp
namespace utils{
    namespace cuda{
        // Okay: namespace cuda may be used nested within a non-reserved namespace
        cudaStream_t make_stream(){
            cudaStream_t s;
            cudaStreamCreate(&s);
            return s;
        }
    } // namespace cuda
} // namespace utils
```

In this case, the `cuda` namespace is a child of `utils`, not a direct child of the global scope, so it does not violate the reservation rules [CUDA_C_Programming_Guide:L16886-L16937].
