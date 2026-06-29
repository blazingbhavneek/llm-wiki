# CUDA Dynamic Parallelism (CDP1) Shared Memory

In CUDA C++, shared memory can be declared either as a statically sized file-scope or function-scoped variable, or as an `extern` variable with the size determined at runtime by the kernel’s caller via a launch configuration argument. Both types of declarations are valid under the device runtime in the context of CUDA Dynamic Parallelism version 1 (CDP1) [CUDA_C_Programming_Guide:L14602-L14633].

## Limitations and Workarounds

A key constraint in CDP1 is that shared memory cannot be passed directly to child kernels. To utilize shared memory data in a child kernel, the parent kernel must first write the data back to global memory [CUDA_C_Programming_Guide:L14602-L14633].

### Example Implementation

The following example demonstrates a recursive `permute` kernel that uses shared memory. It writes data to shared memory, processes it, and then writes it back to global memory before launching child kernels [CUDA_C_Programming_Guide:L14602-L14633]:

```cpp
__global__ void permute(int n, int *data) {
    extern __shared__ int smem[];
    if (n <= 1)
        return;

    smem[threadIdx.x] = data[threadIdx.x];
    __syncthreads();

    permute_data(smem, n);
    __syncthreads();

    // Write back to GMEM since we can't pass SMEM to children.
    data[threadIdx.x] = smem[threadIdx.x];
    __syncthreads();

    if (threadIdx.x == 0) {
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data);
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data+n/2);
    }
}

void host_launch(int *data) {
    permute<<< 1, 256, 256*sizeof(int) >>>(256, data);
}
```

## See Also

For the CDP2 version of shared memory variable declarations, see the relevant section in the CUDA C++ Programming Guide [CUDA_C_Programming_Guide:L14602-L14633].
