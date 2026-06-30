# Unified Memory Performance Hints

Introduces performance hints (cudaMemPrefetchAsync, cudaMemAdvise, etc.) that allow applications to provide CUDA with additional information to optimize data placement and migration without altering application semantics.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21193-L21200

Citation: [CUDA_C_Programming_Guide:L21193-L21200]

````text
## 24.1.2.8 Performance Hints

The following sections describes the available unified memory performance hints, which may be used on all Unified Memory, for example, CUDA Managed memory or, on systems with full CUDA Unified Memory support, also all System-Allocated Memory. These APIs are hints, that is, they do not impact the semantics of applications, only their peformance. That is, they can be added or removed anywhere on any application without impacting its results.

CUDA Unified Memory may not always have all the information necessary to make the best performance decisions related to unified memory. These performance hints enable the application to provide CUDA with more information.

Note that applications should only use these hints if they improve their performance.
````
