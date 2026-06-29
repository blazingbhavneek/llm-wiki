# __managed__ and __shared__ Variables in CUDA

In CUDA programming, variables declared with the `__managed__` or `__shared__` storage qualifiers have specific restrictions regarding compile-time constants. These variables cannot be marked with the keyword `constexpr` [[CUDA_C_Programming_Guide:L17837-L17839]].

This restriction applies because `__managed__` variables reside in unified memory accessible by both host and device, and `__shared__` variables reside in shared memory accessible by threads within a block, neither of which aligns with the strict compile-time evaluation requirements of `constexpr` objects in this context.
