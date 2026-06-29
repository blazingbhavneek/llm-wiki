# Dynamic Parallelism Streams and Events

CUDA Streams and Events provide mechanisms to control dependencies between grid launches. This functionality is available both on the host and on the device, allowing for fine-grained synchronization and ordering of parallel work.

## Host vs. Device Scope

Streams and events created on the device serve the same purpose as those created on the host: managing execution order and dependencies [CUDA_C_Programming_Guide:L13706-L13713].

### Grid-Scoped Streams and Events

Streams and events created within a grid exist within that grid's scope [CUDA_C_Programming_Guide:L13706-L13713]. Key characteristics include:

*   **Undefined Behavior Outside Scope:** Using a stream or event created within a grid outside of that grid results in undefined behavior [CUDA_C_Programming_Guide:L13706-L13713].
*   **Implicit Synchronization:** All work launched by a grid, including work launched into streams, is implicitly synchronized when the grid exits [CUDA_C_Programming_Guide:L13706-L13713]. This ensures that all dependencies are resolved appropriately before the grid terminates [CUDA_C_Programming_Guide:L13706-L13713].
*   **Modification Constraints:** The behavior of operations on a stream that has been modified outside of grid scope is undefined [CUDA_C_Programming_Guide:L13706-L13713].

### Host-Scoped Streams and Events

Streams and events created on the host have undefined behavior when used within any kernel [CUDA_C_Programming_Guide:L13706-L13713].

### Parent-Child Grid Relationships

The scoping rules extend to hierarchical grid launches. Streams and events created by a parent grid have undefined behavior if used within a child grid [CUDA_C_Programming_Guide:L13706-L13713].

## Execution Order and Dependencies

*   **In-Order Execution:** Grids launched into the same stream execute in order [CUDA_C_Programming_Guide:L13706-L13713].
*   **Inter-Stream Dependencies:** Events may be used to create dependencies between streams, allowing for complex synchronization patterns [CUDA_C_Programming_Guide:L13706-L13713].

## Caveats

*   Research reports for this topic have encountered context length limitations, so this page relies directly on the source evidence [CUDA_C_Programming_Guide:L13706-L13713].
*   Strict adherence to scope boundaries is required; violating scope rules leads to undefined behavior [CUDA_C_Programming_Guide:L13706-L13713].
