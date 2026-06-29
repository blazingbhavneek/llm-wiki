# CUDA Shared Memory on Device

In CUDA C++, shared memory can be declared either as a statically sized file-scope or function-scoped variable, or as an `extern` variable with the size determined at runtime by the kernel’s caller via a launch configuration argument. Both types of declarations are valid under the device runtime [CUDA_C_Programming_Guide:L13977-L13985].

## Dynamic Shared Memory

When using dynamic shared memory, the size is specified at launch time. For example, a host function can launch a kernel with a specific shared memory size:

```cpp
void host_launch(int *data) {
    permute<<< 1, 256, 256*sizeof(int) >>>(256, data);
}
```

Inside the kernel, the shared memory is declared as an extern array:

```cpp
__global__ void permute(int n, int *data) {
    extern __shared__ int smem[];
    // ... usage of smem ...
}
```

## Recursive Launch Limitations

Shared memory cannot be passed directly to child kernels launched recursively. If a kernel launches another kernel that requires shared memory, the parent kernel must write its shared memory data back to global memory before the launch, and the child kernel must read from global memory [CUDA_C_Programming_Guide:L13995-L14007].

For instance, in a recursive permutation kernel:

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
```

In this example, the shared memory `smem` is used for intermediate computation, but before launching child kernels, the data is written back to global memory (`data`) because shared memory is not accessible to the child kernels [CUDA_C_Programming_Guide:L13995-L14007].
