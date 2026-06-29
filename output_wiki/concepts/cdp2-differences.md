# CDP2 Differences

CUDA Dynamic Parallelism version 2 (CDP2), introduced with compute capability 9.0 and higher, differs significantly from CDP1 in synchronization mechanisms, resource management, and stream handling.

## Synchronization

Explicit device-side synchronization is no longer possible with CDP2 or on devices of compute capability 9.0 or higher [CUDA_C_Programming_Guide:L14262-L14278]. Developers must use implicit synchronization methods, such as tail launches, to ensure execution order [CUDA_C_Programming_Guide:L14262-L14278].

Attempting to query or set the `cudaLimitDevRuntimeSyncDepth` (or `CU_LIMIT_DEV_RUNTIME_SYNC_DEPTH`) limit with CDP2 or on compute capability 9.0+ devices results in `cudaErrorUnsupportedLimit` [CUDA_C_Programming_Guide:L14262-L14278].

## Resource Management

CDP2 no longer utilizes a virtualized pool for pending launches that exceed the fixed-size pool capacity [CUDA_C_Programming_Guide:L14262-L14278]. Instead, the `cudaLimitDevRuntimePendingLaunchCount` must be configured to a sufficiently large value to avoid running out of launch slots [CUDA_C_Programming_Guide:L14262-L14278].

There is a limit on the total number of events that can exist simultaneously, which is equal to twice the pending launch count [CUDA_C_Programming_Guide:L14262-L14278]. Events are destroyed only after a launch completes [CUDA_C_Programming_Guide:L14262-L14278]. Consequently, `cudaLimitDevRuntimePendingLaunchCount` must also be set large enough to prevent running out of event slots [CUDA_C_Programming_Guide:L14262-L14278].

## Stream Tracking

In CDP2, streams are tracked per grid rather than per thread block [CUDA_C_Programming_Guide:L14262-L14278]. This change allows work to be launched into a stream created by a different thread block [CUDA_C_Programming_Guide:L14262-L14278]. Attempting to launch work into a stream created by another thread block using CDP1 results in `cudaErrorInvalidValue` [CUDA_C_Programming_Guide:L14262-L14278].

## New Stream Types

CDP2 introduces two new named stream types:
*   **Tail launch** (`cudaStreamTailLaunch`)
*   **Fire-and-forget** (`cudaStreamFireAndForget`)

## Compilation Requirements

CDP2 is supported only under 64-bit compilation mode [CUDA_C_Programming_Guide:L14262-L14278].
