# CUDA Dynamic Parallelism CDP2 vs CDP1

Differences, compatibility, and interoperability between the new (CDP2) and legacy (CDP1) CUDA Dynamic Parallelism interfaces.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L14254-L14283

Citation: [CUDA_C_Programming_Guide:L14254-L14283]

````text

## 13.4.3.1.6 ECC Errors

No notification of ECC errors is available to code within a CUDA kernel. ECC errors are reported at the host side once the entire launch tree has completed. Any ECC errors which arise during execution of a nested program will either generate an exception or continue execution (depending upon error and configuration).

## 13.5. CDP2 vs CDP1

This section summarises the diferences between, and the compatibility and interoperability of, the new (CDP2) and legacy (CDP1) CUDA Dynamic Parallelism interfaces. It also shows how to opt-out of the CDP2 interface on devices of compute capability less than 9.0.

## 13.5.1. Diferences Between CDP1 and CDP2

Explicit device-side synchronization is no longer possible with CDP2 or on devices of compute capability 9.0 or higher. Implicit synchronization (such as tail launches) must be used instead.

Attempting to query or set cudaLimitDevRuntimeSyncDepth (or CU\_LIMIT\_DEV\_RUNTIME\_SYNC\_DEPTH) with CDP2 or on devices of compute capability 9.0 or higher results in cudaErrorUnsupportedLimit.

CDP2 no longer has a virtualized pool for pending launches that don’t fit in the fixed-sized pool. cudaLimitDevRuntimePendingLaunchCount must be set to be large enough to avoid running out of launch slots.

For CDP2, there is a limit to the total number of events existing at once (note that events are destroyed only after a launch completes), equal to twice the pending launch count. cudaLimitDevRuntimePendingLaunchCount must be set to be large enough to avoid running out of event slots.

Streams are tracked per grid with CDP2 or on devices of compute capability 9.0 or higher, not per thread block. This allows work to be launched into a stream created by another thread block. Attempting to do so with the CDP1 results in cudaErrorInvalidValue.

CDP2 introduces the tail launch (cudaStreamTailLaunch) and fire-and-forget (cudaStreamFireAndForget) named streams.

CDP2 is supported only under 64-bit compilation mode.

## 13.5.2. Compatibility and Interoperability

CDP2 is the default. Functions can be compiled with -DCUDA\_FORCE\_CDP1\_IF\_SUPPORTED to opt-out of using CDP2 on devices of compute capability less than 9.0.

<table><tr><td></td><td>Function compiler with CUDA 12.0 and newer (default)</td><td>Function compiled with pre-CUDA 12.0 or with CUDA 12.0 and newer with -DCUDA_FORCE_CDP1_IF_SUPPORTED specified</td></tr><tr><td>Compilation</td><td>Compile error if device code references cudaDeviceSynchronize.</td><td>Compile error if code references cudaStream-TailLaunch or cudaStreamFireAndForget. Compile error if device code references cudaDeviceSynchronize and code is compiled for sm_90 or newer.</td></tr><tr><td>Compute capability &lt; 9.0</td><td>New interface is used.</td><td>Legacy interface is used.</td></tr><tr><td>Compute capability 9.0 and higher</td><td>New interface is used.</td><td>New interface is used. If function references cudaDeviceSynchronize in device code, function load returns cudaErrorSymbolNotFound (this could happen if the code is compiled for devices of compute capability less than 9.0, but run on devices of compute capability 9.0 or higher using JIT).</td></tr></table>
````
