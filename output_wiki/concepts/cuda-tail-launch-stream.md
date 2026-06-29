# CUDA Tail Launch Stream

The tail launch named stream, identified by the constant `cudaStreamTailLaunch`, allows a CUDA grid to schedule a new grid for launch after its own completion [CUDA_C_Programming_Guide:L13888-L13948]. It serves as an implicit synchronization point, enabling functionality similar to `cudaDeviceSynchronize()` in most cases [CUDA_C_Programming_Guide:L13888-L13948].

## Behavior and Synchronization

Each grid possesses its own tail launch stream. All work launched by a grid into non-tail launch streams is implicitly synchronized before the tail stream is triggered [CUDA_C_Programming_Guide:L13888-L13948]. Specifically, a parent grid's tail launch does not execute until the parent grid and all work launched by the parent grid to ordinary streams, per-thread streams, or fire-and-forget streams have completed [CUDA_C_Programming_Guide:L13888-L13948].

If multiple grids are launched into the same grid's tail launch stream, the later grid will not launch until the earlier grid and all its descendant work have completed [CUDA_C_Programming_Guide:L13888-L13948]. The tail launch stream effectively behaves as if it were inserted between the parent grid and the next grid in the parent grid's stream [CUDA_C_Programming_Guide:L13888-L13948].

### Examples

**Sequential Tail Launches:**
In this example, grid `C2` will only launch after `C1` completes, as both are launched into the tail launch stream of the parent grid `P` [CUDA_C_Programming_Guide:L13888-L13948]:

```cpp
__global__ void P( ... ) {
    C1<<< ... , cudaStreamTailLaunch >>>( ... );
    C2<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

**Synchronization with Other Streams:**
Grid `C` will only launch after all work from `X` (per-thread), `F` (fire-and-forget), and `P` (the parent grid itself) has completed [CUDA_C_Programming_Guide:L13888-L13948]:

```cpp
__global__ void P( ... ) {
    C<<< ... , cudaStreamTailLaunch >>>( ... );
    X<<< ... , cudaStreamPerThread >>>( ... );
    F<<< ... , cudaStreamFireAndForget >>>( ... )
}
```

**Synchronization with Parent Stream:**
Grid `P2` will only launch after `C` (launched via tail launch from `P1`) completes [CUDA_C_Programming_Guide:L13888-L13948]:

```cpp
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

## Concurrent Launches

Each grid is limited to one tail launch stream. To launch concurrent grids after the parent grid completes, one can use the tail launch stream to launch a helper grid that subsequently launches multiple grids into fire-and-forget streams [CUDA_C_Programming_Guide:L13888-L13948]. In the following example, `C1` and `C2` will launch concurrently after `P` completes [CUDA_C_Programming_Guide:L13888-L13948]:

```cpp
__global__ void T( ... ) {
    C1<<< ... , cudaStreamFireAndForget >>>( ... );
    C2<<< ... , cudaStreamFireAndForget >>>( ... );
}

__global__ void P( ... ) {
    ...
    T<<< ... , cudaStreamTailLaunch >>>( ... );
}
```

## Limitations and Requirements

*   **Events:** The tail launch stream cannot be used to record or wait on events. Attempting to do so results in `cudaErrorInvalidValue` [CUDA_C_Programming_Guide:L13888-L13948].
*   **Compilation Mode:** Usage of the tail launch stream requires compilation in 64-bit mode [CUDA_C_Programming_Guide:L13888-L13948].
*   **Feature Flags:** The tail launch stream is not supported when compiled with `CUDA_FORCE_CDP1_IF_SUPPORTED` defined [CUDA_C_Programming_Guide:L13888-L13948].
