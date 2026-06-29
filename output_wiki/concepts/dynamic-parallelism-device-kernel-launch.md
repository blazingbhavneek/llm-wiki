# Dynamic Parallelism Device-Side Kernel Launch

Kernels may be launched from the device using the standard CUDA `<<< >>>` syntax [CUDA_C_Programming_Guide:L13830-L13836].

## Syntax

The syntax for launching a kernel from the device is:

```erlang
kernel_name<<< Dg, Db, Ns, S >>>([kernel arguments]);
```

[CUDA_C_Programming_Guide:L13830-L13836]

## Parameters

- **Dg**: Of type `dim3`, specifies the dimensions and size of the grid [CUDA_C_Programming_Guide:L13837-L13844].
- **Db**: Of type `dim3`, specifies the dimensions and size of each thread block [CUDA_C_Programming_Guide:L13837-L13844].
- **Ns**: Of type `size_t`, specifies the number of bytes of shared memory that is dynamically allocated per thread block for this call in addition to statically allocated memory. `Ns` is an optional argument that defaults to 0 [CUDA_C_Programming_Guide:L13837-L13844].
- **S**: Of type `cudaStream_t`, specifies the stream associated with this call. The stream must have been allocated in the same grid where the call is being made. `S` is an optional argument that defaults to the NULL stream [CUDA_C_Programming_Guide:L13837-L13844].

## Caveats

- The research report for this page was generated as a deterministic fallback due to a subagent error; content is strictly derived from the assigned source evidence [CUDA_C_Programming_Guide:L13830-L13836].
