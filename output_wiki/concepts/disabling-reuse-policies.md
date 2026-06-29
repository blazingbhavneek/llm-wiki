# Disabling Reuse Policies

While controllable reuse policies generally improve memory reuse, users may choose to disable them to maintain deterministic behavior or avoid unexpected serialization. Disabling these policies shifts the responsibility of synchronization to the user.

## Reasons for Disabling

There are two primary reasons for disabling reuse policies:

1.  **Run-to-Run Variance**: Allowing opportunistic reuse, such as `cudaMemPoolReuseAllowOpportunistic`, introduces variance in allocation patterns. This variance is based on the interleaving of CPU and GPU execution, which can lead to non-deterministic behavior across different runs [CUDA_C_Programming_Guide:L15665-L15669].
2.  **Non-Deterministic Serialization**: Internal dependency insertion, such as `cudaMemPoolReuseAllowInternalDependencies`, can serialize work in unexpected ways. This may occur when the user would prefer to explicitly synchronize an event or stream on allocation failure rather than relying on the library's internal dependency management [CUDA_C_Programming_Guide:L15665-L15669].

## Implications

When reuse policies are disabled, the user must handle allocation failures explicitly. This typically involves synchronizing on an event or stream to ensure proper ordering and resource availability, rather than relying on the automatic reuse mechanisms provided by the memory pool [CUDA_C_Programming_Guide:L15665-L15669].
