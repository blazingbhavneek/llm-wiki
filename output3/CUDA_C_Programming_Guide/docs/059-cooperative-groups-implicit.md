## 11.3.1. Composition Example

To illustrate the concept of groups, this example attempts to perform a block-wide sum reduction. Previously, there were hidden constraints on the implementation when writing this code:

```lisp
__device__ int sum(int *x, int n) {
    // ...
    __syncthreads();
    return total;
}

__global__ void parallel_kernel(float *x) {
    // ...
    // Entire thread block must call sum
    sum(x, n);
}
```

All threads in the thread block must arrive at the \_\_syncthreads() barrier, however, this constraint is hidden from the developer who might want to use sum(…). With Cooperative Groups, a better way of writing this would be:

```lisp
__device__ int sum(const thread_block& g, int *x, int n) {
    // ...
    g.sync()
    return total;
}

__global__ void parallel_kernel(...) {
```

(continues on next page)

```txt
// ...
    // Entire thread block must call sum
    thread_block tb = this_thread_block();
    sum(tb, x, n);
    // ...
}
```

(continued from previous page)

## 11.4. Group Types

## 11.4.1. Implicit Groups

Implicit groups represent the launch configuration of the kernel. Regardless of how your kernel is written, it always has a set number of threads, blocks and block dimensions, a single grid and grid dimensions. In addition, if the multi-device cooperative launch API is used, it can have multiple grids (single grid per device). These groups provide a starting point for decomposition into finer grained groups which are typically HW accelerated and are more specialized for the problem the developer is solving.

Although you can create an implicit group anywhere in the code, it is dangerous to do so. Creating a handle for an implicit group is a collective operation—all threads in the group must participate. If the group was created in a conditional branch that not all threads reach, this can lead to deadlocks or data corruption. For this reason, it is recommended that you create a handle for the implicit group upfront (as early as possible, before any branching has occurred) and use that handle throughout the kernel. Group handles must be initialized at declaration time (there is no default constructor) for the same reason and copy-constructing them is discouraged.

## 11.4.1.1 Thread Block Group

Any CUDA programmer is already familiar with a certain group of threads: the thread block. The Cooperative Groups extension introduces a new datatype, thread\_block, to explicitly represent this concept within the kernel.

class thread\_block;

Constructed via:

```javascript
thread_block g = this_thread_block();
```

## Public Member Functions:

static void sync(): Synchronize the threads named in the group, equivalent to g. barrier\_wait(g.barrier\_arrive())

thread\_block::arrival\_token barrier\_arrive(): Arrive on the thread\_block barrier, returns a token that needs to be passed into barrier\_wait(). More details here

void barrier\_wait(thread\_block::arrival\_token&& t): Wait on the thread\_block barrier, takes arrival token returned from barrier\_arrive() as an rvalue reference. More details here

static unsigned int thread\_rank(): Rank of the calling thread within [0, num\_threads) static dim3 group\_index(): 3-Dimensional index of the block within the launched grid

static dim3 thread\_index(): 3-Dimensional index of the thread within the launched block static dim3 dim\_threads(): Dimensions of the launched block in units of threads static unsigned int num\_threads(): Total number of threads in the group

Legacy member functions (aliases):

static unsigned int size(): Total number of threads in the group (alias of num\_threads())

static dim3 group\_dim(): Dimensions of the launched block (alias of dim\_threads())

## Example:

```txt
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

Note: that all threads in the group must participate in collective operations, or the behavior is undefined.

Related: The thread\_block datatype is derived from the more generic thread\_group datatype, which can be used to represent a wider class of groups.

## 11.4.1.2 Cluster Group

This group object represents all the threads launched in a single cluster. Refer to Thread Block Clusters. The APIs are available on all hardware with Compute Capability 9.0+. In such cases, when a non-cluster grid is launched, the APIs assume a 1x1x1 cluster.

class cluster\_group;

Constructed via:

```javascript
cluster_group g = this_cluster();
```

## Public Member Functions:

static void sync(): Synchronize the threads named in the group, equivalent to g. barrier\_wait(g.barrier\_arrive())

static cluster\_group::arrival\_token barrier\_arrive(): Arrive on the cluster barrier, returns a token that needs to be passed into barrier\_wait(). More details here

static void barrier\_wait(cluster\_group::arrival\_token&& t): Wait on the cluster barrier, takes arrival token returned from barrier\_arrive() as a rvalue reference. More details here

static unsigned int thread\_rank(): Rank of the calling thread within [0, num\_threads)

static unsigned int block\_rank(): Rank of the calling block within [0, num\_blocks)

static unsigned int num\_threads(): Total number of threads in the group

static unsigned int num\_blocks(): Total number of blocks in the group

static dim3 dim\_threads(): Dimensions of the launched cluster in units of threads

static dim3 dim\_blocks(): Dimensions of the launched cluster in units of blocks

static dim3 block\_index(): 3-Dimensional index of the calling block within the launched cluster

static unsigned int query\_shared\_rank(const void \*addr): Obtain the block rank to which a shared memory address belongs

static T\* map\_shared\_rank(T \*addr, int rank): Obtain the address of a shared memory variable of another block in the cluster

Legacy member functions (aliases):

static unsigned int size(): Total number of threads in the group (alias of num\_threads())

## 11.4.1.3 Grid Group

This group object represents all the threads launched in a single grid. APIs other than sync() are available at all times, but to be able to synchronize across the grid, you need to use the cooperative launch API.

class grid\_group;

Constructed via:

```txt
grid_group g = this_grid();
```

## Public Member Functions:

bool is\_valid() const: Returns whether the grid\_group can synchronize

void sync() const: Synchronize the threads named in the group, equivalent to g. barrier\_wait(g.barrier\_arrive())

grid\_group::arrival\_token barrier\_arrive(): Arrive on the grid barrier, returns a token that needs to be passed into barrier\_wait(). More details here

void barrier\_wait(grid\_group::arrival\_token&& t): Wait on the grid barrier, takes arrival token returned from barrier\_arrive() as a rvalue reference. More details here

static unsigned long long thread\_rank(): Rank of the calling thread within [0, num\_threads)

static unsigned long long block\_rank(): Rank of the calling block within [0, num\_blocks)

static unsigned long long cluster\_rank(): Rank of the calling cluster within [0, num\_clusters)

static unsigned long long num\_threads(): Total number of threads in the group

static unsigned long long num\_blocks(): Total number of blocks in the group

static unsigned long long num\_clusters(): Total number of clusters in the group

static dim3 dim\_blocks(): Dimensions of the launched grid in units of blocks

static dim3 dim\_clusters(): Dimensions of the launched grid in units of clusters

static dim3 block\_index(): 3-Dimensional index of the block within the launched grid

static dim3 cluster\_index(): 3-Dimensional index of the cluster within the launched grid

Legacy member functions (aliases):

static unsigned long long size(): Total number of threads in the group (alias of num\_threads())

static dim3 group\_dim(): Dimensions of the launched grid (alias of dim\_blocks())
