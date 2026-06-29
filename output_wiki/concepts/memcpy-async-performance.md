# memcpy_async Performance Guidance

Performance guidance for `memcpy_async` is primarily relevant for devices with compute capability 8.x, where the pipeline mechanism is shared among CUDA threads within the same warp. This sharing causes batches of `memcpy_async` to be entangled within a warp, impacting performance under specific circumstances, particularly regarding alignment, type requirements, and warp divergence.

## Alignment Requirements

On devices with compute capability 8.0, the `cp.async` family of instructions supports copying 4, 8, and 16 bytes at a time. To achieve optimal performance, specific alignment constraints must be met.

### Ideal Alignment
For best performance when using the `memcpy_async` API, an alignment of 128 bytes is required for both the shared memory and global memory pointers [CUDA_C_Programming_Guide:L9700-L9777].

### Minimum Alignment for Asynchronous Implementation
If the size provided to `memcpy_async` is a multiple of 4, 8, or 16, and both pointers are aligned to a 4, 8, or 16-byte boundary, `memcpy_async` can be implemented using exclusively asynchronous memory operations [CUDA_C_Programming_Guide:L9700-L9777].

### Runtime Overhead for Lower Alignments
For pointers to values with alignment requirements of 1 or 2 bytes, it is often impossible to prove at compile time that the pointers are aligned to higher boundaries. This necessitates runtime alignment checks, which increase code size and add runtime overhead [CUDA_C_Programming_Guide:L9700-L9777].

### Proving Alignment
The `cuda::aligned_size_t<size_t Align>(size_t size)` shape can be used to supply proof that both pointers are aligned to an `Align` boundary and that the size is a multiple of `Align` [CUDA_C_Programming_Guide:L9700-L9777]. This is passed as an argument where the `memcpy_async` APIs expect a Shape:

```cpp
cuda::memcpy_async(group, dst, src, cuda::aligned_size_t<16>(N * block.size()), pipeline);
```

If the proof provided is incorrect, the behavior is undefined [CUDA_C_Programming_Guide:L9700-L9777].

## Trivially Copyable Types

On compute capability 8.0 devices, `memcpy_async` relies on the `cp.async` family of instructions. If the pointer types passed to `memcpy_async` do not point to **TriviallyCopyable** types, the copy constructor of each output element must be invoked. In such cases, `cp.async` instructions cannot be used to accelerate the operation [CUDA_C_Programming_Guide:L9700-L9777].

## Warp Entanglement Effects

Because the pipeline mechanism is shared among threads in the same warp, the sequence of `memcpy_async` batches is shared across the warp. This leads to "warp entanglement," where divergence affects commit, wait, and arrive-on operations.

### Commit Operation
The commit operation is coalesced such that the pipeline sequence is incremented once for all converged threads invoking the operation [CUDA_C_Programming_Guide:L9700-L9777].

*   **Fully Converged Warp:** The sequence is incremented by one.
*   **Fully Diverged Warp:** The sequence is incremented by 32 (one for each thread) [CUDA_C_Programming_Guide:L9700-L9777].

Let $PB$ be the warp-shared pipeline’s actual sequence of batches, and $TB$ be a thread’s perceived sequence. An index in a thread’s perceived sequence ($BT_n$) always aligns to an equal or larger index in the actual warp-shared sequence ($BP_m$), such that $BT_n \le BP_m$ where $n \le m$. The sequences are equal only when all commit operations are invoked from converged threads [CUDA_C_Programming_Guide:L9700-L9777].

### Wait Operation
Threads invoke `pipeline_consumer_wait_prior<N>()` or `pipeline::consumer_wait()` to wait for batches in their perceived sequence $TB$ to complete [CUDA_C_Programming_Guide:L9700-L9777].

`pipeline_consumer_wait_prior<N>()` waits for batches in the actual sequence up to and including $PL-N$. Since $TL \le PL$, waiting for batch $PL-N$ includes waiting for batch $TL-N$. Consequently, if $TL < PL$ (due to divergence), the thread will unintentionally wait for additional, more recent batches than necessary [CUDA_C_Programming_Guide:L9700-L9777]. In an extreme fully-diverged warp example, each thread could wait for all 32 batches [CUDA_C_Programming_Guide:L9700-L9777].

### Arrive-On Operation
Warp divergence affects the number of times an `arrive_on(bar)` operation updates the barrier [CUDA_C_Programming_Guide:L9700-L9777]:

*   **Fully Converged Warp:** The barrier is updated once.
*   **Fully Diverged Warp:** 32 individual updates are applied to the barrier [CUDA_C_Programming_Guide:L9700-L9777].

## Best Practices

To avoid over-waiting and minimize barrier updates, it is recommended that `commit` and `arrive-on` invocations are performed by converged threads [CUDA_C_Programming_Guide:L9700-L9777].

If code preceding these operations causes thread divergence, the warp should be re-converged using `__syncwarp()` before invoking `commit` or `arrive-on` operations [CUDA_C_Programming_Guide:L9700-L9777].

## See Also

*   Pipeline Interface
*   Pipeline Primitives Interface
