# CDP2 Compatibility and Interoperability

CUDA Dynamic Parallelism (CDP) has two generations of interfaces: CDP1 (legacy) and CDP2 (new). Starting with CUDA 12.0, CDP2 is the default behavior. Understanding the compatibility between these versions is critical for managing compilation flags, device code restrictions, and cross-version launch constraints.

## Default Behavior and Compilation Flags

By default, functions compiled with CUDA 12.0 and newer use the CDP2 interface [CUDA_C_Programming_Guide:L14279-L14288]. Developers can opt-out of CDP2 on devices with compute capability less than 9.0 by compiling with the flag `-DCUDA_FORCE_CDP1_IF_SUPPORTED` [CUDA_C_Programming_Guide:L14279-L14288].

## Interface Selection by Compute Capability and Compilation

The interface used (CDP1 vs. CDP2) depends on both the target compute capability and how the function was compiled. The following table summarizes the behavior:

| Scenario | Function compiled with CUDA 12.0+ (Default) | Function compiled with pre-CUDA 12.0 or with `-DCUDA_FORCE_CDP1_IF_SUPPORTED`
| :--- | :--- | :---
| **Compilation Constraints** | Compile error if device code references `cudaDeviceSynchronize` [CUDA_C_Programming_Guide:L14279-L14288]. | Compile error if code references `cudaStreamTailLaunch` or `cudaStreamFireAndForget` [CUDA_C_Programming_Guide:L14279-L14288].<br>Compile error if device code references `cudaDeviceSynchronize` and code is compiled for `sm_90` or newer [CUDA_C_Programming_Guide:L14279-L14288].
| **Compute Capability < 9.0** | New interface (CDP2) is used [CUDA_C_Programming_Guide:L14279-L14288]. | Legacy interface (CDP1) is used [CUDA_C_Programming_Guide:L14279-L14288].
| **Compute Capability >= 9.0** | New interface (CDP2) is used [CUDA_C_Programming_Guide:L14279-L14288]. | New interface (CDP2) is used [CUDA_C_Programming_Guide:L14279-L14288].<br>If the function references `cudaDeviceSynchronize` in device code, `function load` returns `cudaErrorSymbolNotFound`. This can occur if code is compiled for compute capability < 9.0 but runs on devices >= 9.0 via JIT [CUDA_C_Programming_Guide:L14279-L14288].

## Simultaneous Execution and Feature Usage

Functions using CDP1 and CDP2 may be loaded and run simultaneously within the same CUDA context [CUDA_C_Programming_Guide:L14279-L14288]. Each version retains access to its specific features:

*   **CDP1 Functions**: Can use CDP1-specific features, such as `cudaDeviceSynchronize` [CUDA_C_Programming_Guide:L14279-L14288].
*   **CDP2 Functions**: Can use CDP2-specific features, such as tail launch (`cudaStreamTailLaunch`) and fire-and-forget launch (`cudaStreamFireAndForget`) [CUDA_C_Programming_Guide:L14279-L14288].

## Call Graph Restrictions

Strict separation is enforced between CDP1 and CDP2 functions within a single call graph. A function using CDP1 cannot launch a function using CDP2, and vice versa [CUDA_C_Programming_Guide:L14279-L14288].

If a function that would use CDP1 contains a function in its call graph that would use CDP2 (or vice versa), the `function load` operation will fail with `cudaErrorCdpVersionMismatch` [CUDA_C_Programming_Guide:L14279-L14288]. This ensures that mixed-version parallelism does not occur within a single kernel launch hierarchy.
