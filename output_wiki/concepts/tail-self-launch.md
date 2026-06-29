# Tail Self-Launch

Tail self-launch is a feature in CUDA that allows a device graph to enqueue itself for execution. This capability enables recursive or iterative patterns within device-side graphs, where a graph can trigger its own subsequent execution.

## Key Constraints

*   **Single Enqueue Limit**: A given graph can only have one self-launch enqueued at any given time [CUDA_C_Programming_Guide:L3046-L3078].

## API: `cudaGetCurrentGraphExec`

To facilitate tail self-launching, CUDA provides a device-side function to query the handle of the currently executing graph.

### `cudaGraphExec_t cudaGetCurrentGraphExec()`

This function returns the `cudaGraphExec_t` handle of the currently running device graph [CUDA_C_Programming_Guide:L3046-L3078].

*   **Return Value**: If the currently executing kernel is a node within a device graph, it returns the graph's execution handle [CUDA_C_Programming_Guide:L3046-L3078].
*   **Null Case**: If the currently executing kernel is not a node within a device graph, the function returns `NULL` [CUDA_C_Programming_Guide:L3046-L3078].

## Usage Example

The following example demonstrates a device kernel that uses `cudaGetCurrentGraphExec()` to relaunch itself up to a maximum count using `cudaStreamGraphTailLaunch`.

```cpp
__device__ int relaunchCount = 0;

__global__ void relaunchSelf() {
    int relaunchMax = 100;

    if (threadIdx.x == 0) {
        if (relaunchCount < relaunchMax) {
            // Enqueue the current graph for tail launch
            cudaGraphLaunch(cudaGetCurrentGraphExec(), cudaStreamGraphTailLaunch);
        }
        relaunchCount++;
    }
}
```

In this pattern, `cudaGetCurrentGraphExec()` retrieves the handle of the graph currently executing the `relaunchSelf` kernel, allowing it to be relaunched via `cudaGraphLaunch` with the `cudaStreamGraphTailLaunch` flag [CUDA_C_Programming_Guide:L3046-L3078].
