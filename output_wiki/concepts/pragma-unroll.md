# #pragma unroll

The `#pragma unroll` directive allows developers to explicitly control the loop unrolling behavior of the compiler for specific loops [CUDA_C_Programming_Guide:L11705-L11705].

## Syntax and Usage

The directive must be placed immediately before the loop it applies to, and it only affects that specific loop [CUDA_C_Programming_Guide:L11707-L11707]. It is optionally followed by an integral constant expression (ICE) [CUDA_C_Programming_Guide:L11707-L11707].

## Behavior

The behavior of the pragma depends on the presence and value of the optional ICE [CUDA_C_Programming_Guide:L11707-L11707]:

*   **No ICE**: If no ICE is provided, the loop will be completely unrolled if its trip count is constant [CUDA_C_Programming_Guide:L11707-L11707].
*   **ICE = 1**: The compiler will not unroll the loop [CUDA_C_Programming_Guide:L11707-L11707].
*   **Invalid ICE**: The pragma will be ignored if the ICE evaluates to a non-positive integer or to an integer greater than the maximum value representable by the `int` data type [CUDA_C_Programming_Guide:L11707-L11707].

## Default Behavior

By default, the compiler automatically unrolls small loops that have a known trip count [CUDA_C_Programming_Guide:L11707-L11707]. The `#pragma unroll` directive is used to override or specify this behavior for any given loop [CUDA_C_Programming_Guide:L11707-L11707].
