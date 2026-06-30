# Unified Memory Performance Tuning

Provides general advice for tuning Unified Memory performance: understanding paging, keeping data local, tuning for transfer granularity, and carefully using performance hints to avoid overhead.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21603-L21614

Citation: [CUDA_C_Programming_Guide:L21603-L21614]

````text
## 24.2.2. Performance Tuning

In order to achieve good performance with Unified Memory, it is important to:

▶ Understand how paging works on your system, and how to avoid unnecessary page faults.

▶ Understand the various mechanisms allowing you to keep data local to the accessing processor.

▶ Consider tuning your application for the granularity of memory transfers of your system.

As general advice, Performance Hints might provide improved performance, but using them incorrectly might degrade performance compared to the default behavior. Also note that any hint has a performance cost associated with it on the host, thus useful hints must at the very least improve performance enough to overcome this cost.
````
