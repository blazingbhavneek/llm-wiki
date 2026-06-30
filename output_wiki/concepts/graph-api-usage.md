# Graph API Usage Guidelines

Covers thread-safety rules for `cudaGraph_t` (not thread-safe, user responsibility), concurrency limits for `cudaGraphExec_t` (cannot run concurrently with itself, ordered launches), and the role of streams for ordering without constraining internal graph parallelism.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2844-L2853

Citation: [CUDA_C_Programming_Guide:L2844-L2853]

````text
## 6.2.8.7.6 Using Graph APIs

cudaGraph\_t objects are not thread-safe. It is the responsibility of the user to ensure that multiple threads do not concurrently access the same cudaGraph\_t.

A cudaGraphExec\_t cannot run concurrently with itself. A launch of a cudaGraphExec\_t will be ordered after previous launches of the same executable graph.

Graph execution is done in streams for ordering with other asynchronous work. However, the stream is for ordering only; it does not constrain the internal parallelism of the graph, nor does it afect where graph nodes execute.

See Graph API.
````
