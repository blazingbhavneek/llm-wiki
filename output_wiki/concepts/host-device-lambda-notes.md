# Host Device Lambda Notes

Behavioral notes on `__host__ __device__` lambdas, specifically regarding indirect function calls and host compiler inlining limitations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L18896-L18901

Citation: [CUDA_C_Programming_Guide:L18896-L18901]

````text
## 18.7.3. Notes on \_\_host\_\_ \_\_device\_\_ lambdas

Unlike \_\_device\_\_ lambdas, \_\_host\_\_ \_\_device\_\_ lambdas can be called from host code. As described earlier, the CUDA compiler replaces an extended lambda expression defined in host code with an instance of a named placeholder type. The placeholder type for an extended \_\_host \_device\_\_ lambda invokes the original lambda’s operator() with an indirect function call<sup>Page</sup> <sup>458,</sup> <sup>24</sup>.

The presence of the indirect function call may cause an extended \_\_host\_\_ \_\_device\_\_ lambda to be less optimized by the host compiler than lambdas that are implicitly or explicitly \_\_host\_\_ only. In the latter case, the host compiler can easily inline the body of the lambda into the calling context. But in case of an extended \_\_host\_\_ \_\_device\_\_ lambda, the host compiler encounters the indirect function call and may not be able to easily inline the original \_\_host\_\_ \_\_device\_\_ lambda body.
````
