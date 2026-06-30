# Tail Self-Launch

Covers the ability of a device graph to enqueue itself for a tail launch using `cudaGetCurrentGraphExec()`. Allows device-side looping/recursion. Only one self-launch can be enqueued at a time.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3046-L3078

Citation: [CUDA_C_Programming_Guide:L3046-L3078]

````text
## 6.2.8.7.7.10 Tail Self-launch

It is possible for a device graph to enqueue itself for a tail launch, although a given graph can only have one self-launch enqueued at a time. In order to query the currently running device graph so that it can be relaunched, a new device-side function is added:

```javascript
cudaGraphExec_t cudaGetCurrentGraphExec();
```

This function returns the handle of the currently running graph if it is a device graph. If the currently executing kernel is not a node within a device graph, this function will return NULL.

Below is sample code showing usage of this function for a relaunch loop:

```javascript
__device__ int relaunchCount = 0;

__global__ void relaunchSelf() {
    int relaunchMax = 100;

    if (threadIdx.x == 0) {
```

(continues on next page)

```txt
if (relaunchCount < relaunchMax) {
    cudaGraphLaunch(cudaGetCurrentGraphExec(), cudaStreamGraphTailLaunch);
}

relaunchCount++;
}
}
```
````
