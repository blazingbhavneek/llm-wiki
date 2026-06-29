# CUDA Stream Capture Peer Access

## Overview

When using CUDA stream capture to record execution graphs, the system captures the state of memory allocations, including their accessibility properties. Specifically, the **allocation node** within the captured graph records the **peer accessibility** of the allocating memory pool at the exact time the capture occurs [CUDA_C_Programming_Guide:L16294-L16322].

## Key Behavior

### Immutable Accessibility Mappings

Once a `cudaMallocAsync` call is captured within a stream capture session, the peer accessibility mappings for that allocation are fixed in the resulting graph [CUDA_C_Programming_Guide:L16294-L16322].

*   **Recording State:** The graph node records the accessibility flags of the memory pool as they exist at the time of the `cudaMallocAsync` call [CUDA_C_Programming_Guide:L16294-L16322].
*   **Post-Capture Changes:** Altering the peer accessibility of the memory pool after the allocation has been captured **does not affect** the mappings that the graph will use for that specific allocation [CUDA_C_Programming_Guide:L16294-L16322].

### Example Scenario

The following example illustrates how different graphs capture different accessibility states for the same memory pool:

1.  **Initial State:** A memory pool (`memPool`) is resident and accessible on device 0.
2.  **Graph 1 Capture:**
    *   Stream capture begins.
    *   `cudaMallocAsync` is called to allocate `dptr1` from `memPool`.
    *   Stream capture ends.
    *   At this point, `memPool` is only accessible on device 0. Therefore, the graph node for `dptr1` records accessibility only for device 0 [CUDA_C_Programming_Guide:L16294-L16322].
3.  **Accessibility Change:**
    *   `cudaMemPoolSetAccess` is called to grant `memPool` accessibility on device 1 as well [CUDA_C_Programming_Guide:L16294-L16322].
4.  **Graph 2 Capture:**
    *   A new stream capture begins.
    *   `cudaMallocAsync` is called to allocate `dptr2` from `memPool`.
    *   Stream capture ends.
    *   At this point, `memPool` is accessible on both device 0 and device 1. Therefore, the graph node for `dptr2` records accessibility for both devices [CUDA_C_Programming_Guide:L16294-L16322].

### Implications

*   **Graph 1 (`dptr1`):** Even though the pool now has device 1 accessibility, the graph node for `dptr1` retains only device 0 accessibility. It will not automatically gain access to device 1 memory based on the pool's updated state [CUDA_C_Programming_Guide:L16294-L16322].
*   **Graph 2 (`dptr2`):** This graph captures the updated state, so its allocation node has both device 0 and device 1 accessibility [CUDA_C_Programming_Guide:L16294-L16322].

## Code Example

The following code snippet demonstrates the boilerplate for setting up access descriptors and the sequence of capture and modification operations [CUDA_C_Programming_Guide:L16294-L16322]:

```txt
// boilerplate for the access descs (only ReadWrite and Device access supported by
    the add node api)
accessDesc.flags = cudaMemAccessFlagsProtReadWrite;
accessDesc.location.type = cudaMemLocationTypeDevice;
accessDesc.location.id = 1;

// let memPool be resident and accessible on device 0

cudaStreamBeginCapture(stream);
cudaMallocAsync(&dptr1, size, memPool, stream);
cudaStreamEndCapture(stream, &graph1);

cudaMemPoolSetAccess(memPool, &accessDesc, 1);

cudaStreamBeginCapture(stream);
cudaMallocAsync(&dptr2, size, memPool, stream);
cudaStreamEndCapture(stream, &graph2);

//The graph node allocating dptr1 would only have the device 0 accessibility even
    though memPool now has device 1 accessibility.
//The graph node allocating dptr2 will have device 0 and device 1 accessibility,
    since that was the pool accessibility at the time of the cudaMallocAsync call.
```
