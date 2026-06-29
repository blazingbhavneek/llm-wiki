# CUDA SM ID and Warp ID

In the PTX assembly language, `%smid` and `%warpid` are special registers that provide identifiers for the current execution context.

## Volatility and Rescheduling

Both `%smid` and `%warpid` are defined as volatile values. This volatility arises because the CUDA device runtime may reschedule thread blocks onto different Streaming Multiprocessors (SMs) to more efficiently manage hardware resources [CUDA_C_Programming_Guide:L14251-L14253].

## Safety Implications

Due to this potential rescheduling, it is unsafe to rely upon `%smid` or `%warpid` remaining unchanged across the lifetime of a thread or thread block [CUDA_C_Programming_Guide:L14251-L14253]. Developers should avoid using these identifiers for state tracking or synchronization logic that persists beyond the immediate execution context of a warp or block on a specific SM.

## Aliases

- `%smid`
- `%warpid`
