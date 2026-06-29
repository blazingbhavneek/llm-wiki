# Graph API Threading and Execution Constraints

## Thread Safety of Graph Objects

`cudaGraph_t` objects are not thread-safe. It is the responsibility of the user to ensure that multiple threads do not concurrently access the same `cudaGraph_t` object. Concurrent access to a single graph object from multiple threads must be avoided to prevent undefined behavior.

## Concurrency Constraints of Executable Graphs

An executable graph, represented by `cudaGraphExec_t`, cannot run concurrently with itself. If a `cudaGraphExec_t` is launched multiple times, each launch is ordered after previous launches of the same executable graph. This ensures that the execution of the graph is serialized with respect to itself, even if launched across different streams or contexts.

## Role of Streams in Graph Execution

Graph execution is performed within CUDA streams to facilitate ordering with other asynchronous work. However, the stream serves strictly for ordering purposes; it does not constrain the internal parallelism of the graph, nor does it affect where graph nodes execute within the graph structure. The internal execution order and parallelism are determined by the graph's dependencies, not the stream's execution order.

## References

- [CUDA_C_Programming_Guide:L2844-L2853]
