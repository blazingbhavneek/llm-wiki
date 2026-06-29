# CUDA Dynamic Parallelism (CDP1) SM Id and Warp Id

In the context of CUDA Dynamic Parallelism 1 (CDP1), the PTX instructions for reading the Streaming Multiprocessor ID (`%smid`) and Warp ID (`%warpid`) are defined as **volatile** values [CUDA_C_Programming_Guide:L14972-L14977].

This volatility arises because the device runtime may reschedule thread blocks onto different Streaming Multiprocessors (SMs) to manage resources more efficiently [CUDA_C_Programming_Guide:L14972-L14977]. Consequently, it is unsafe to rely upon `%smid` or `%warpid` remaining unchanged across the lifetime of a thread or thread block [CUDA_C_Programming_Guide:L14972-L14977].

For the CDP2 version of these registers, refer to the documentation section on SM Id and Warp Id (CDP2).
