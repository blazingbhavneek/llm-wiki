# CUDA Fire-and-Forget Stream

The fire-and-forget named stream (`cudaStreamFireAndForget`) allows the user to launch fire-and-forget work with less boilerplate and without stream tracking overhead [CUDA_C_Programming_Guide:L13872-L13875]. It is functionally identical to, but faster than, creating a new stream per launch and launching into that stream [CUDA_C_Programming_Guide:L13875-L13877].

## Behavior and Dependencies

Fire-and-forget launches are immediately scheduled for launch without any dependency on the completion of previously launched grids [CUDA_C_Programming_Guide:L13877-L13879]. No other grid launches can depend on the completion of a fire-and-forget launch, except through the implicit synchronization at the end of the parent grid [CUDA_C_Programming_Guide:L13879-L13882]. Consequently, a tail launch or the next grid in the parent grid’s stream will not launch before a parent grid’s fire-and-forget work has completed [CUDA_C_Programming_Guide:L13882-L13884].

For example, in the following code snippet, launch `C2` will not wait for the completion of `C1`:

```cpp
// In this example, C2's launch will not wait for C1's completion
__global__ void P( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}
```

## Limitations and Requirements

The fire-and-forget stream cannot be used to record or wait on events. Attempting to do so results in `cudaErrorInvalidValue` [CUDA_C_Programming_Guide:L13884-L13886].

Additionally, the fire-and-forget stream is not supported when compiled with `CUDA_FORCE_CDP1_IF_SUPPORTED` defined [CUDA_C_Programming_Guide:L13886-L13887]. Usage of the fire-and-forget stream requires compilation to be in 64-bit mode [CUDA_C_Programming_Guide:L13887].
