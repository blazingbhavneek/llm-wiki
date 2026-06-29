# Dynamic Parallelism Memory Model

The Dynamic Parallelism (CDP) memory model defines how parent and child grids interact with various memory spaces on the GPU. The primary distinction is that global and constant memory are shared between parent and child grids, whereas local and shared memory are private to their respective execution contexts.

## Global Memory Coherence and Consistency

Parent and child grids share the same global memory storage, but they have distinct local and shared memory [CUDA_C_Programming_Guide:L13732-L13734]. Access to global memory is coherent, but consistency guarantees between parent and child are weak [CUDA_C_Programming_Guide:L13739-L13743].

### Visibility Rules

There is only one point in time when a child grid's view of memory is fully consistent with the parent thread: at the moment the child grid is invoked by the parent [CUDA_C_Programming_Guide:L13739-L13743].

*   **Parent to Child:** All global memory operations in the parent thread prior to the child grid’s invocation are visible to the child grid [CUDA_C_Programming_Guide:L13739-L13743].
*   **Child to Parent:** Modifications made by threads in the child grid are not guaranteed to become available to the parent grid upon the child's completion. With the removal of `cudaDeviceSynchronize()`, it is no longer possible to directly access modifications made by child threads from the parent grid [CUDA_C_Programming_Guide:L13739-L13743].

To access modifications made by a child grid before the parent grid exits, a kernel must be launched into the `cudaStreamTailLaunch` stream [CUDA_C_Programming_Guide:L13739-L13743].

### Example

The following example illustrates these semantics. The `parent_launch` kernel initializes `data` and synchronizes threads. Thread 0 then launches `child_launch` and a tail-launch kernel.

```lisp
__global__ void tail_launch(int *data) {
    data[threadIdx.x] = data[threadIdx.x]+1;
}

__global__ void child_launch(int *data) {
    data[threadIdx.x] = data[threadIdx.x]+1;
}

__global__ void parent_launch(int *data) {
    data[threadIdx.x] = threadIdx.x;

    __syncthreads();

    if (threadIdx.x == 0) {
        child_launch<<< 1, 256 >>>(data);
        tail_launch<<< 1, 256, 0, cudaStreamTailLaunch >>>(data);
    }
}

void host_launch(int *data) {
    parent_launch<<< 1, 256 >>>(data);
}
```

In this scenario:
1.  The child grid executing `child_launch` is guaranteed to see the modifications to `data` made before it was launched [CUDA_C_Programming_Guide:L13739-L13743].
2.  Due to the `__syncthreads()` call, the child will see `data[0]=0`, `data[1]=1`, ..., `data[255]=255` [CUDA_C_Programming_Guide:L13739-L13743].
3.  The child grid returns at an implicit synchronization, but its modifications are never guaranteed to be visible to the parent grid directly [CUDA_C_Programming_Guide:L13739-L13743].
4.  To access modifications made by `child_launch`, the `tail_launch` kernel is launched into the `cudaStreamTailLaunch` stream [CUDA_C_Programming_Guide:L13739-L13743].

## Zero-Copy Memory

Zero-copy system memory has identical coherence and consistency guarantees to global memory, following the semantics detailed above [CUDA_C_Programming_Guide:L13770-L13772]. A kernel may not allocate or free zero-copy memory, but may use pointers to zero-copy memory passed in from the host program [CUDA_C_Programming_Guide:L13770-L13772].

## Constant Memory

Constants may not be modified from the device; they may only be modified from the host [CUDA_C_Programming_Guide:L13773-L13776]. However, the behavior of modifying a constant from the host while there is a concurrent grid accessing that constant at any point during its lifetime is undefined [CUDA_C_Programming_Guide:L13773-L13776].

## Shared and Local Memory

Shared and local memory are private to a thread block or thread, respectively, and are not visible or coherent between parent and child grids [CUDA_C_Programming_Guide:L13777-L13784].

### Restrictions

*   **Undefined Behavior:** Referencing an object in shared or local memory outside the scope in which it belongs results in undefined behavior and may cause an error [CUDA_C_Programming_Guide:L13777-L13784].
*   **Compiler Warnings:** The NVIDIA compiler attempts to warn if it detects that a pointer to local or shared memory is being passed as an argument to a kernel launch [CUDA_C_Programming_Guide:L13777-L13784].
*   **Runtime Checks:** Programmers can use the `__isGlobal()` intrinsic to determine if a pointer references global memory and is safe to pass to a child launch [CUDA_C_Programming_Guide:L13777-L13784].
*   **Async Memory Functions:** Calls to `cudaMemcpy*Async()` or `cudaMemset*Async()` may invoke new child kernels to preserve stream semantics. Passing shared or local memory pointers to these APIs is illegal and will return an error [CUDA_C_Programming_Guide:L13777-L13784].

### Local Memory Specifics

Local memory is private storage for an executing thread and is not visible outside that thread [CUDA_C_Programming_Guide:L13785-L13788]. It is illegal to pass a pointer to local memory as a launch argument when launching a child kernel; dereferencing such a pointer from a child results in undefined behavior [CUDA_C_Programming_Guide:L13785-L13788].

#### Examples

**Illegal (Local Memory):**
```cpp
int x_array[10];          // Creates x_array in parent's local memory
child_launch<<< 1, 1 >>>(x_array);
```
Accessing `x_array` by `child_launch` results in undefined behavior [CUDA_C_Programming_Guide:L13789-L13795].

**Correct (Global Memory):**
```dart
// Correct - "value" is global storage
__device__ int value;
__device__ void x() {
    value = 5;
    child<<< 1, 1 >>>(&value);
}
```

**Illegal (Local Memory in Device Function):**
```dart
// Invalid - "value" is local storage
__device__ void y() {
    int value = 5;
    child<<< 1, 1 >>>(&value);
}
```

## Texture Memory

Writes to the global memory region over which a texture is mapped are incoherent with respect to texture accesses [CUDA_C_Programming_Guide:L13817-L13818]. Coherence for texture memory is enforced at the invocation of a child grid and when a child grid completes [CUDA_C_Programming_Guide:L13817-L13818].

*   **Parent to Child:** Writes to memory prior to a child kernel launch are reflected in texture memory accesses of the child [CUDA_C_Programming_Guide:L13817-L13818].
*   **Child to Parent:** Writes to memory by a child are never guaranteed to be reflected in the texture memory accesses by a parent [CUDA_C_Programming_Guide:L13817-L13818].

Concurrent accesses by parent and child may result in inconsistent data [CUDA_C_Programming_Guide:L13817-L13818]. As with global memory, the only way to access modifications made by threads in the child grid before the parent grid exits is via a kernel launched into the `cudaStreamTailLaunch` stream [CUDA_C_Programming_Guide:L13817-L13818].

## Best Practices

It is sometimes difficult for a programmer to be aware of when a variable is placed into local memory by the compiler [CUDA_C_Programming_Guide:L13797-L13806]. As a general rule, all storage passed to a child kernel should be allocated explicitly from the global-memory heap, either with `cudaMalloc()`, `new()`, or by declaring `__device__` storage at global scope [CUDA_C_Programming_Guide:L13797-L13806].
