# CDP1 Device-Side Kernel Launch

Device-Side Kernel Launch (CDP1) allows kernels to be launched from the device using the standard CUDA launch syntax. This capability is distinct from CDP2, which utilizes specific Kernel Launch APIs [CUDA_C_Programming_Guide:L14496-L14513].

## Syntax

Kernels are launched from the device using the following syntax:

```erlang
kernel_name<<< Dg, Db, Ns, S >>>([kernel arguments]);
```

## Parameters

*   **Dg**: Of type `dim3`, specifies the dimensions and size of the grid [CUDA_C_Programming_Guide:L14496-L14513].
*   **Db**: Of type `dim3`, specifies the dimensions and size of each thread block [CUDA_C_Programming_Guide:L14496-L14513].
*   **Ns**: Of type `size_t`, specifies the number of bytes of shared memory that is dynamically allocated per thread block for this call, in addition to statically allocated memory. This is an optional argument that defaults to 0 [CUDA_C_Programming_Guide:L14496-L14513].
*   **S**: Of type `cudaStream_t`, specifies the stream associated with this call. The stream must have been allocated in the same thread block where the call is being made. This is an optional argument that defaults to 0 [CUDA_C_Programming_Guide:L14496-L14513].
