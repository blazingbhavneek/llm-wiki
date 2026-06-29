# Bind Memory to Multicast Objects

After a Multicast Object has been created and all participating devices have been added to the Multicast Object, it needs to be backed with physical memory allocated with `cuMemCreate` for each device [CUDA_C_Programming_Guide:L15326-L15331].

The binding is performed using the `cuMulticastBindMem` function [CUDA_C_Programming_Guide:L15326-L15331].

## Function Signature

```c
cuMulticastBindMem(mcHandle, mcOffset, memHandle, memOffset, size, 0 /*flags*/);
```

## Parameters

- **mcHandle**: The handle to the Multicast Object.
- **mcOffset**: The offset within the Multicast Object.
- **memHandle**: The handle to the physical memory allocated via `cuMemCreate`.
- **memOffset**: The offset within the physical memory.
- **size**: The size of the memory region to bind.
- **flags**: Flags for the binding operation (typically 0). [CUDA_C_Programming_Guide:L15326-L15331]
