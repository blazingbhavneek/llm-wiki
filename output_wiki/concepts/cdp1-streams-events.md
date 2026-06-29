# CDP1 Streams and Events

In the Contextual Device Programming version 1 (CDP1) model, CUDA Streams and Events provide mechanisms to control dependencies between grid launches. This functionality applies equally to resources created on the host and those created on the device [CUDA_C_Programming_Guide:L14333-L14342].

## Host vs. Device Scope

The scope of a stream or event determines its validity and behavior:

*   **Device-Created Resources**: Streams and events created on the device serve the same purpose as host-created ones: controlling execution order and dependencies [CUDA_C_Programming_Guide:L14333-L14342].
*   **Host-Created Resources**: Streams and events created on the host have **undefined behavior** when used within any kernel [CUDA_C_Programming_Guide:L14333-L14342].
*   **Parent/Child Grids**: Streams and events created by a parent grid have **undefined behavior** if used within a child grid [CUDA_C_Programming_Guide:L14333-L14342].

## Thread Block Scope and Synchronization

Streams and events created within a grid exist within **thread block scope** [CUDA_C_Programming_Guide:L14333-L14342].

*   **Undefined Behavior**: Using a stream or event outside of the thread block where it was created results in undefined behavior [CUDA_C_Programming_Guide:L14333-L14342].
*   **Implicit Synchronization**: All work launched by a thread block is implicitly synchronized when the block exits [CUDA_C_Programming_Guide:L14333-L14342].
*   **Dependency Resolution**: Work launched into streams is included in this implicit synchronization, with all dependencies resolved appropriately upon block exit [CUDA_C_Programming_Guide:L14333-L14342].

## Execution Order

Grids launched into the same stream execute in order [CUDA_C_Programming_Guide:L14333-L14342]. Events may be used to create dependencies between streams, ensuring that specific operations complete before subsequent ones begin [CUDA_C_Programming_Guide:L14333-L14342].

## Note on CDP2

For the CDP2 version of the document, refer to the "Streams and Events" section in that specific context [CUDA_C_Programming_Guide:L14333-L14342].
