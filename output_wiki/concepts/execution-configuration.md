# Execution Configuration

Any call to a `__global__` function must specify an execution configuration [CUDA_C_Programming_Guide:L11535-L11535]. This configuration defines the dimension of the grid and blocks that will be used to execute the function on the device, as well as the associated stream [CUDA_C_Programming_Guide:L11535-L11535].

## Syntax

The execution configuration is specified by inserting an expression of the form `<<< Dg, Db, Ns, S >>>` between the function name and the parenthesized argument list [CUDA_C_Programming_Guide:L11537-L11537]. The arguments to the execution configuration are evaluated before the actual function arguments [CUDA_C_Programming_Guide:L11559-L11559].

### Parameters

*   **Dg**: This parameter is of type `dim3` and specifies the dimension and size of the grid, such that `Dg.x * Dg.y * Dg.z` equals the number of blocks being launched [CUDA_C_Programming_Guide:L11539-L11539].
*   **Db**: This parameter is of type `dim3` and specifies the dimension and size of each block, such that `Db.x * Db.y * Db.z` equals the number of threads per block [CUDA_C_Programming_Guide:L11541-L11541].
*   **Ns**: This parameter is of type `size_t` and specifies the number of bytes in shared memory that is dynamically allocated per block for this call in addition to the statically allocated memory [CUDA_C_Programming_Guide:L11543-L11543]. This dynamically allocated memory is used by any variables declared as an external array as mentioned in `__shared__` [CUDA_C_Programming_Guide:L11543-L11543]. `Ns` is an optional argument which defaults to 0 [CUDA_C_Programming_Guide:L11543-L11543].
*   **S**: This parameter is of type `cudaStream_t` and specifies the associated stream [CUDA_C_Programming_Guide:L11545-L11545]. `S` is an optional argument which defaults to 0 [CUDA_C_Programming_Guide:L11545-L11545].

## Constraints

The function call will fail if `Dg` or `Db` are greater than the maximum sizes allowed for the device as specified in Compute Capabilities [CUDA_C_Programming_Guide:L11561-L11561]. Additionally, the call will fail if `Ns` is greater than the maximum amount of shared memory available on the device, minus the amount of shared memory required for static allocation [CUDA_C_Programming_Guide:L11561-L11561].
