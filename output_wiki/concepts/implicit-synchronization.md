# Implicit Synchronization

Operations from different streams cannot run concurrently if a CUDA operation on the NULL stream is submitted between them, unless non-blocking streams are used. Guidelines recommend issuing independent operations first and delaying synchronization.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2243-L2252

Citation: [CUDA_C_Programming_Guide:L2243-L2252]

````text
## 6.2.8.5.4 Implicit Synchronization

Two operations from diferent streams cannot run concurrently if any CUDA operation on the NULL stream is submitted in-between them, unless the streams are non-blocking streams (created with the cudaStreamNonBlocking flag).

Applications should follow these guidelines to improve their potential for concurrent kernel execution:

▶ All independent operations should be issued before dependent operations,

▶ Synchronization of any kind should be delayed as long as possible.
````
