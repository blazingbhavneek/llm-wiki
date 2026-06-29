# Local Memory

Local memory is a memory space in CUDA devices used to store automatic variables that the compiler cannot place in registers. It resides in device memory, meaning it shares the high latency and low bandwidth characteristics of global memory [CUDA_C_Programming_Guide:L6468-L6483].

## When Local Memory is Used

The compiler places variables in local memory under specific conditions, typically when register space is exhausted or when variable size exceeds register capacity [CUDA_C_Programming_Guide:L6468-L6483]. Common scenarios include:

*   **Register Spilling:** If a kernel uses more registers than available, variables may be spilled to local memory [CUDA_C_Programming_Guide:L6468-L6483].
*   **Large Variables:** Large structures or arrays that would consume excessive register space are placed in local memory [CUDA_C_Programming_Guide:L6468-L6483].
*   **Dynamic Indexing:** Arrays indexed with non-constant quantities that the compiler cannot optimize into registers [CUDA_C_Programming_Guide:L6468-L6483].

Additionally, some mathematical function implementations may access local memory [CUDA_C_Programming_Guide:L6468-L6483].

## Access Patterns and Performance

Local memory accesses have the same high latency and low bandwidth as global memory accesses [CUDA_C_Programming_Guide:L6468-L6483]. However, the memory organization allows for coalescing under specific conditions [CUDA_C_Programming_Guide:L6468-L6483].

*   **Coalescing:** Consecutive 32-bit words are accessed by consecutive thread IDs [CUDA_C_Programming_Guide:L6468-L6483].
*   **Optimal Access:** Accesses are fully coalesced if all threads in a warp access the same relative address, such as the same index in an array or the same member in a structure [CUDA_C_Programming_Guide:L6468-L6483].

## Caching

On devices with compute capability 5.x and higher, local memory accesses are cached in the L2 cache, similar to global memory accesses [CUDA_C_Programming_Guide:L6468-L6483].

## Detection and Verification

Developers can verify if variables are placed in local memory through several methods [CUDA_C_Programming_Guide:L6468-L6483]:

1.  **PTX Assembly:** Compiling with the `-ptx` or `-keep` option allows inspection of the PTX code. Variables in local memory are declared using the `.local` mnemonic and accessed via `ld.local` and `st.local` instructions [CUDA_C_Programming_Guide:L6468-L6483].
2.  **Cubin Object:** Subsequent compilation phases may move variables to local memory if they exceed register limits. Using `cuobjdump` on the cubin object can reveal these placements [CUDA_C_Programming_Guide:L6468-L6483].
3.  **Compiler Output:** Compiling with `--ptxas-options=-v` reports the total local memory usage per kernel (lmem) [CUDA_C_Programming_Guide:L6468-L6483].
