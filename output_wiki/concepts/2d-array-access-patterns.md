# Two-Dimensional Array Access Patterns

A common global memory access pattern involves threads accessing elements of a 2D array. For a thread with index $(t_x, t_y)$, the address to access one element of a 2D array of width $width$, located at address $BaseAddress$ of type $type^*$, is calculated as [CUDA_C_Programming_Guide:L6456-L6467]:

```txt
BaseAddress + width * ty + tx
```

For these accesses to be fully coalesced, both the width of the thread block and the width of the array must be a multiple of the warp size [CUDA_C_Programming_Guide:L6456-L6467].

In particular, this means that an array whose width is not a multiple of this size will be accessed much more efficiently if it is actually allocated with a width rounded up to the closest multiple of this size and its rows padded accordingly [CUDA_C_Programming_Guide:L6456-L6467]. The `cudaMallocPitch()` and `cuMemAllocPitch()` functions and associated memory copy functions enable programmers to write non-hardware-dependent code to allocate arrays that conform to these constraints [CUDA_C_Programming_Guide:L6456-L6467].
