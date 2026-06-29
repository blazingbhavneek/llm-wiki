# thread_block Group

The `thread_block` datatype is part of the Cooperative Groups extension, designed to explicitly represent the thread block concept within CUDA kernels [CUDA_C_Programming_Guide:L12059-L12063]. It is derived from the more generic `thread_group` datatype, which supports a wider class of thread groupings [CUDA_C_Programming_Guide:L12108-L12110].

## Construction

A `thread_block` object is constructed using the `this_thread_block()` function [CUDA_C_Programming_Guide:L12065-L12067].

```cpp
thread_block g = this_thread_block();
```

## Public Member Functions

The `thread_block` class provides several static member functions for synchronization and querying thread/block properties [CUDA_C_Programming_Guide:L12069-L12093].

### Synchronization

*   **`static void sync()`**: Synchronizes all threads named in the group. This is functionally equivalent to calling `g.barrier_wait(g.barrier_arrive())` [CUDA_C_Programming_Guide:L12071-L12073].
*   **`barrier_arrive()`**: Returns an `arrival_token` representing the thread's arrival at the block barrier [CUDA_C_Programming_Guide:L12075-L12076].
*   **`barrier_wait(arrival_token&& t)`**: Waits for the thread block barrier, taking the arrival token returned from `barrier_arrive()` as an rvalue reference [CUDA_C_Programming_Guide:L12078-L12079].

### Thread and Block Information

*   **`static unsigned int thread_rank()`**: Returns the rank of the calling thread within the range `[0, num_threads)` [CUDA_C_Programming_Guide:L12081-L12082].
*   **`static dim3 group_index()`**: Returns the 3-dimensional index of the block within the launched grid [CUDA_C_Programming_Guide:L12083-L12084].
*   **`static dim3 thread_index()`**: Returns the 3-dimensional index of the thread within the launched block [CUDA_C_Programming_Guide:L12085-L12086].
*   **`static dim3 dim_threads()`**: Returns the dimensions of the launched block in units of threads [CUDA_C_Programming_Guide:L12087-L12088].
*   **`static unsigned int num_threads()`**: Returns the total number of threads in the group [CUDA_C_Programming_Guide:L12089-L12090].

### Legacy Aliases

For compatibility, the following legacy member functions are provided as aliases [CUDA_C_Programming_Guide:L12092-L12095]:

*   **`static unsigned int size()`**: Alias for `num_threads()`, returning the total number of threads in the group [CUDA_C_Programming_Guide:L12092-L12093].
*   **`static dim3 group_dim()`**: Alias for `dim_threads()`, returning the dimensions of the launched block [CUDA_C_Programming_Guide:L12094-L12095].

## Usage Example

The following example demonstrates loading data from global memory into shared memory and synchronizing the block using `thread_block` [CUDA_C_Programming_Guide:L12097-L12105].

```cpp
/// Loading an integer from global into shared memory
__global__ void kernel(int *globalInput) {
    __shared__ int x;
    thread_block g = this_thread_block();
    // Choose a leader in the thread block
    if (g.thread_rank() == 0) {
        // load from global into shared for all threads to work with
        x = (*globalInput);
    }
    // After loading data into shared memory, you want to synchronize
    // if all threads in your thread block need to see it
    g.sync(); // equivalent to __syncthreads();
}
```

## Important Constraints

All threads in the group must participate in collective operations; otherwise, the behavior is undefined [CUDA_C_Programming_Guide:L12107].
