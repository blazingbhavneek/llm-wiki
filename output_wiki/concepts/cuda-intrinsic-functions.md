# CUDA Intrinsic Functions

CUDA intrinsic functions are specialized device code functions that provide faster, though less accurate, implementations of standard mathematical operations. These functions are prefixed with double underscores (e.g., `__sinf`) to distinguish them from standard library functions [CUDA_C_Programming_Guide:L16450-L16459].

## Characteristics

*   **Device Code Only**: Intrinsic functions can only be used in device code [CUDA_C_Programming_Guide:L16450-L16459].
*   **Performance vs. Accuracy**: They map to fewer native instructions, resulting in faster execution at the cost of reduced accuracy and potentially different special case handling compared to their standard counterparts [CUDA_C_Programming_Guide:L16450-L16459].

## Compiler Options

The NVIDIA compiler provides the `-use_fast_math` option, which automatically forces the compilation of specific standard functions to their intrinsic counterparts [CUDA_C_Programming_Guide:L16450-L16459]. Enabling this flag affects the accuracy of the affected functions and may alter how special cases are handled [CUDA_C_Programming_Guide:L16450-L16459].

## Affected Functions

The following table lists standard functions and their corresponding intrinsic equivalents, which are affected by the `-use_fast_math` flag [CUDA_C_Programming_Guide:L16450-L16459]:

| Operator/Function | Device Function |
| :--- | :--- |
| `x/y` | `__fdividef(x,y)` |
| `sinf(x)` | `__sinf(x)` |
| `cosf(x)` | `__cosf(x)` |
| `tanf(x)` | `__tanf(x)` |
| `sincosf(x,sptr,cptr)` | `__sincosf(x,sptr,cptr)` |
| `logf(x)` | `__logf(x)` |
| `log2f(x)` | `__log2f(x)` |
| `log10f(x)` | `__log10f(x)` |
| `expf(x)` | `__expf(x)` |
| `exp10f(x)` | `__exp10f(x)` |
| `powf(x,y)` | `__powf(x,y)` |
| `tanhf(x)` | `__tanhf(x)` |

## Best Practices

While `-use_fast_math` offers a global switch for performance optimization, a more robust approach is to selectively replace standard mathematical function calls with intrinsic functions only where performance gains are critical and the reduced accuracy or changed special case handling is acceptable [CUDA_C_Programming_Guide:L16450-L16459].
