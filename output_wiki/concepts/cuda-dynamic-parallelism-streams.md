# CUDA Dynamic Parallelism Streams

Streams in CUDA Dynamic Parallelism (CDP) including named, unnamed (NULL), fire-and-forget, and tail launch streams.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L13858-L13948

Citation: [CUDA_C_Programming_Guide:L13858-L13948]

````text
## 13.3.1.2 Streams

Both named and unnamed (NULL) streams are available from the device runtime. Named streams may be used by any thread within a grid, but stream handles may not be passed to other child/parent kernels. In other words, a stream should be treated as private to the grid in which it is created.

Similar to host-side launch, work launched into separate streams may run concurrently, but actual concurrency is not guaranteed. Programs that depend upon concurrency between child kernels are not supported by the CUDA programming model and will have undefined behavior.

The host-side NULL stream’s cross-stream barrier semantic is not supported on the device (see below for details). In order to retain semantic compatibility with the host runtime, all device streams must be created using the cudaStreamCreateWithFlags() API, passing the cudaStreamNonBlocking flag. The cudaStreamCreate() call is a host-runtime- only API and will fail to compile for the device.

As cudaStreamSynchronize() and cudaStreamQuery() are unsupported by the device runtime, a kernel launched into the cudaStreamTailLaunch stream should be used instead when the application needs to know that stream-launched child kernels have completed.

## 13.3.1.2.1 The Implicit (NULL) Stream

Within a host program, the unnamed (NULL) stream has additional barrier synchronization semantics with other streams (see Default Stream for details). The device runtime ofers a single implicit, unnamed stream shared between all threads in a thread block, but as all named streams must be created with the cudaStreamNonBlocking flag, work launched into the NULL stream will not insert an implicit dependency on pending work in any other streams (including NULL streams of other thread blocks).

## 13.3.1.2.2 The Fire-and-Forget Stream

The fire-and-forget named stream (cudaStreamFireAndForget) allows the user to launch fire-andforget work with less boilerplate and without stream tracking overhead. It is functionally identical to, but faster than, creating a new stream per launch, and launching into that stream.

Fire-and-forget launches are immediately scheduled for launch without any dependency on the completion of previously launched grids. No other grid launches can depend on the completion of a fireand-forget launch, except through the implicit synchronization at the end of the parent grid. So a tail launch or the next grid in parent grid’s stream won’t launch before a parent grid’s fire-and-forget work has completed.

```dart
// In this example, C2's launch will not wait for C1's completion
__global__ void P( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}
```

The fire-and-forget stream cannot be used to record or wait on events. Attempting to do so results in cudaErrorInvalidValue. The fire-and-forget stream is not supported when compiled with CUDA\_FORCE\_CDP1\_IF\_SUPPORTED defined. Fire-and-forget stream usage requires compilation to be in 64-bit mode.

## 13.3.1.2.3 The Tail Launch Stream

The tail launch named stream (cudaStreamTailLaunch) allows a grid to schedule a new grid for launch after its completion. It should be possible to to use a tail launch to achieve the same functionality as a cudaDeviceSynchronize() in most cases.

Each grid has its own tail launch stream. All non-tail launch work launched by a grid is implicitly synchronized before the tail stream is kicked of. I.e. A parent grid’s tail launch does not launch until the parent grid and all work launched by the parent grid to ordinary streams or per-thread or fire-andforget streams have completed. If two grids are launched to the same grid’s tail launch stream, the later grid does not launch until the earlier grid and all its descendent work has completed.

```txt
// In this example, C2 will only launch after C1 completes.
__global__ void P( ... ) {
    C1<<< ... , cudaStreamTailLaunch >>>( ... );
    C2<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

Grids launched into the tail launch stream will not launch until the completion of all work by the parent grid, including all other grids (and their descendants) launched by the parent in all non-tail launched streams, including work executed or launched after the tail launch.

```txt
// In this example, C will only launch after all X, F and P complete.
__global__ void P( ... ) {
    C<<< ... , cudaStreamTailLaunch >>>( ... );
    X<<< ... , cudaStreamPerThread >>>( ... );
    F<<< ... , cudaStreamFireAndForget >>>( ... )
}
```

The next grid in the parent grid’s stream will not be launched before a parent grid’s tail launch work has completed. In other words, the tail launch stream behaves as if it were inserted between its parent grid and the next grid in its parent grid’s stream.

```txt
// In this example, P2 will only launch after C completes.
__global__ void P1( ... ) {
    C<<< ... , cudaStreamTailLaunch >>>( ... );
}

__global__ void P2( ... ) {
}

int main ( ... ) {
    ...
    P1<<< ... >>>( ... );
    P2<<< ... >>>( ... );
    ...
}
```

Each grid only gets one tail launch stream. To tail launch concurrent grids, it can be done like the example below.

```txt
// In this example, C1 and C2 will launch concurrently after P's completion
__global__ void T( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}

__global__ void P( ... ) {
    ...
    T<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

The tail launch stream cannot be used to record or wait on events. Attempting to do so results in cudaErrorInvalidValue. The tail launch stream is not supported when compiled with CUDA\_FORCE\_CDP1\_IF\_SUPPORTED defined. Tail launch stream usage requires compilation to be in 64-bit mode.
````
