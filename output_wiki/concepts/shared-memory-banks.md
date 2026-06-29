# Shared Memory Banks and Conflicts

Shared memory is an on-chip memory resource that provides significantly higher bandwidth and lower latency compared to local or global memory [CUDA_C_Programming_Guide:L6484-L6485]. To achieve this high bandwidth, shared memory is divided into equally-sized memory modules known as **banks**, which can be accessed simultaneously [CUDA_C_Programming_Guide:L6486-L6487].

## Simultaneous Access and Bandwidth

When memory read or write requests target addresses that fall into distinct memory banks, the hardware can service these requests concurrently [CUDA_C_Programming_Guide:L6487-L6488]. Specifically, if $n$ addresses fall into $n$ distinct memory banks, the requests are serviced simultaneously, yielding an overall bandwidth that is $n$ times the bandwidth of a single module [CUDA_C_Programming_Guide:L6488-L6490].

## Bank Conflicts

A **bank conflict** occurs when two or more addresses in a single memory request fall into the same memory bank [CUDA_C_Programming_Guide:L6491-L6492]. In such cases, the hardware cannot service the requests simultaneously and must serialize them [CUDA_C_Programming_Guide:L6492].

The hardware resolves bank conflicts by splitting the original memory request into as many separate, conflict-free requests as necessary [CUDA_C_Programming_Guide:L6492-L6493]. This serialization decreases throughput by a factor equal to the number of separate memory requests generated [CUDA_C_Programming_Guide:L6493]. If the initial request results in $n$ separate memory requests, it is said to cause an **$n$-way bank conflict** [CUDA_C_Programming_Guide:L6493].

## Optimization

To achieve maximum performance, it is critical to understand how memory addresses map to memory banks and to schedule memory requests in a way that minimizes bank conflicts [CUDA_C_Programming_Guide:L6494-L6495]. The specific mapping rules and optimization strategies vary by device architecture and are detailed in the documentation for Compute Capability 5.x, 6.x, 7.x, 8.x, 9.0, 10.0, and 12.0 [CUDA_C_Programming_Guide:L6495].
