# 11.6.4. Execution control

Part of [Cuda C Programming Guide Reference](README.md). Source lines L13107-L13542.

- [exclusive_scan_update](../../../concepts/exclusive-scan-update.md) — exclusive_scan_update is a cooperative groups function that performs an exclusive scan over thread inputs while atomically updating a shared counter with the total sum, enabling dynamic buffer space allocation.
- [invoke_one](../../../concepts/invoke-one.md) — The `invoke_one` and `invoke_one_broadcast` collective functions in the CUDA cooperative groups library select a single arbitrary thread from a group to execute a function, with the latter distributing the result to all threads.
- [Grid Synchronization](../../../concepts/grid-synchronization.md) — Grid synchronization enables inter-thread block synchronization within a kernel using cooperative groups, requiring specific launch configurations and device support.
- [Cluster Launch Control](../../../concepts/cluster-launch-control.md) — Cluster Launch Control, introduced in Compute Capability 10.0, is a CUDA feature that enables thread blocks to cancel the launch of other pending thread blocks, facilitating work-stealing while maintaining reduced launch overheads and supporting preemption.
