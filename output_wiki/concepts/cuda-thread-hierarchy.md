# CUDA Thread Hierarchy

The CUDA programming model organizes parallel execution into a hierarchy of thread blocks and grids. This structure allows developers to map computational tasks to data domains such as vectors, matrices, or volumes using one-dimensional, two-dimensional, or three-dimensional indexing.

## Thread Blocks

A thread block is a group of threads that can cooperate by sharing data and synchronizing their execution. All threads within a block reside on the same streaming multiprocessor (SM) core and share its limited memory resources [CUDA_C_Programming_Guide:L887-L889].

### Thread Indices and IDs

For convenience, the built-in variable `threadIdx` is a 3-component vector, allowing threads to be identified using 1D, 2D, or 3D indices [CUDA_C_Programming_Guide:L860-L862]. The relationship between a thread's index and its unique thread ID is defined as follows:

*   **1D Block**: The thread index and thread ID are the same.
*   **2D Block**: For a block of size $(D_x, D_y)$, the thread ID of a thread with index $(x, y)$ is calculated as $x + y \times D_x$ [CUDA_C_Programming_Guide:L860-L862].
*   **3D Block**: For a block of size $(D_x, D_y, D_z)$, the thread ID of a thread with index $(x, y, z)$ is calculated as $x + y \times D_x + z \times D_x \times D_y$ [CUDA_C_Programming_Guide:L860-L862].

### Block Size Limits

Due to the shared memory and resource constraints of the SM, there is a limit to the number of threads per block. On current GPUs, a thread block may contain up to 1024 threads [CUDA_C_Programming_Guide:L887-L889]. A common choice for block dimensions is $16 \times 16$, resulting in 256 threads per block [CUDA_C_Programming_Guide:L924-L926].

## Thread Grids

Thread blocks are organized into a grid, which can be one-dimensional, two-dimensional, or three-dimensional [CUDA_C_Programming_Guide:L891-L893]. The number of blocks in a grid is typically determined by the size of the data being processed, which usually exceeds the number of processors in the system [CUDA_C_Programming_Guide:L891-L893].

### Grid and Block Configuration

The number of threads per block and the number of blocks per grid are specified during kernel invocation using the `<<<...>>>` syntax. These values can be of type `int` or `dim3` [CUDA_C_Programming_Guide:L891-L893].

To compute the global index of a thread within the entire grid, both the block index (`blockIdx`) and the block dimensions (`blockDim`) are used alongside the thread index. For example, in a 2D matrix addition kernel:

```c
int i = blockIdx.x * blockDim.x + threadIdx.x;
int j = blockIdx.y * blockDim.y + threadIdx.y;
```

This calculation ensures that each thread can uniquely identify its position in the global data space [CUDA_C_Programming_Guide:L900-L922].

### Execution Independence

Thread blocks are required to execute independently. They can be scheduled in any order, in parallel or in series, across any number of cores [CUDA_C_Programming_Guide:L924-L926]. This independence allows the CUDA runtime to scale execution across the available hardware cores without requiring explicit synchronization between different blocks [CUDA_C_Programming_Guide:L924-L926].

## Example: Matrix Addition

The following example demonstrates a 2D thread block and grid configuration for adding two matrices.

### Single Block Configuration

A simple implementation uses a single block containing $N \times N$ threads to process an $N \times N$ matrix:

```c
// Kernel definition
__global__ void MatAdd(float A[N][N], float B[N][N], float C[N][N]) {
    int i = threadIdx.x;
    int j = threadIdx.y;
    C[i][j] = A[i][j] + B[i][j];
}

int main() {
    // Kernel invocation with one block of N * N * 1 threads
    int numBlocks = 1;
    dim3 threadsPerBlock(N, N);
    MatAdd<<<numBlocks, threadsPerBlock>>>(A, B, C);
}
```

### Multi-Block Configuration

For larger matrices or to adhere to block size limits, the grid is divided into multiple blocks. Each thread calculates its global index using `blockIdx` and `blockDim`:

```c
// Kernel definition
__global__ void MatAdd(float A[N][N], float B[N][N], float C[N][N]) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    if (i < N && j < N)
        C[i][j] = A[i][j] + B[i][j];
}

int main() {
    // Kernel invocation
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);
    MatAdd<<<numBlocks, threadsPerBlock>>>(A, B, C);
}
```

This example assumes that the number of threads per grid in each dimension is evenly divisible by the number of threads per block in that dimension, although this is not a strict requirement [CUDA_C_Programming_Guide:L924-L926]. The grid is created with enough blocks to ensure one thread per matrix element [CUDA_C_Programming_Guide:L924-L926].

## References

*   [CUDA_C_Programming_Guide:L860-L862]
*   [CUDA_C_Programming_Guide:L866-L885]
*   [CUDA_C_Programming_Guide:L887-L889]
*   [CUDA_C_Programming_Guide:L891-L893]
*   [CUDA_C_Programming_Guide:L900-L922]
*   [CUDA_C_Programming_Guide:L924-L926]
