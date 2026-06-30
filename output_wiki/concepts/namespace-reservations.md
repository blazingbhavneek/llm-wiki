# Namespace Reservations

Rules prohibiting additions to reserved CUDA namespaces, with examples of valid/invalid usage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16886-L16937

Citation: [CUDA_C_Programming_Guide:L16886-L16937]

````text

## 18.5.9. Namespace Reservations

Unless an exception is otherwise noted, it is undefined behavior to add any declarations or definitions to cuda::, nv::, cooperative\_groups:: or any namespace nested within.

Examples:

```cpp
namespace cuda{
    // Bad: class declaration added to namespace cuda
    struct foo{};

    // Bad: function definition added to namespace cuda
```

(continues on next page)

(continued from previous page)

```cpp
cudaStream_t make_stream(){
    cudaStream_t s;
    cudaStreamCreate(&s);
    return s;
}
} // namespace cuda

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

// Bad: Equivalent to adding symbols to namespace cuda at global scope
using namespace utils;
```
````
