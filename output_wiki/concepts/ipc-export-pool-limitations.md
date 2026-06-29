# IPC Export Pool Limitations

## Overview
Memory pools exported via Inter-Process Communication (IPC) have specific limitations regarding memory management and reclamation. These constraints are enforced at the driver level rather than the CUDA runtime level, meaning the behavior is controlled by the underlying driver implementation.

## Key Limitations

### Inability to Release Physical Blocks
IPC pools do not currently support the mechanism to release physical memory blocks back to the operating system. This limitation impacts standard memory pool management APIs that rely on physical memory reclamation.

### Impact on Memory Pool APIs
Due to the inability to release physical blocks, specific CUDA memory pool APIs behave as follows:

*   **`cudaMemPoolTrimTo`**: This API acts as a **no-op**. It does not release memory back to the system, as the underlying physical blocks cannot be freed from the IPC pool context.
*   **`cudaMemPoolAttrReleaseThreshold`**: This attribute is **effectively ignored**. Setting a release threshold does not trigger the expected behavior of releasing memory blocks back to the OS because the IPC pool architecture does not support this operation.

## Driver Dependency
The behavior described above is controlled by the **driver**, not the CUDA runtime. Consequently, these limitations may change in future driver updates as the underlying implementation evolves. Users should not rely on these APIs for memory reclamation in IPC contexts and should be aware that behavior is subject to change based on the installed driver version.

## References
- [CUDA_C_Programming_Guide:L15847-L15849]
