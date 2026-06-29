# cuda::pipeline Overview

CUDA provides the `cuda::pipeline` synchronization object to manage and overlap asynchronous data movement with computation [CUDA_C_Programming_Guide:L9778-L9784]. The API documentation for `cuda::pipeline` is provided in the libcudacxx API [CUDA_C_Programming_Guide:L9778-L9784].

## Concept

A pipeline object is a double-ended N stage queue with a head and a tail, and is used to process work in a first-in first-out (FIFO) order [CUDA_C_Programming_Guide:L9778-L9784].

## Member Functions

The pipeline object has the following member functions to manage the stages of the pipeline [CUDA_C_Programming_Guide:L9778-L9784]:

### Producer Operations

*   **`producer_acquire`**: Acquires an available stage in the pipeline internal queue [CUDA_C_Programming_Guide:L9778-L9784].
*   **`producer_commit`**: Commits the asynchronous operations issued after the `producer_acquire` call on the currently acquired stage of the pipeline [CUDA_C_Programming_Guide:L9778-L9784].

### Consumer Operations

*   **`consumer_wait`**: Waits for completion of all asynchronous operations on the oldest stage of the pipeline [CUDA_C_Programming_Guide:L9778-L9784].
*   **`consumer_release`**: Releases the oldest stage of the pipeline to the pipeline object for reuse. The released stage can then be acquired by the producer [CUDA_C_Programming_Guide:L9778-L9784].
