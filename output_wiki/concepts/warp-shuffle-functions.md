# Warp Shuffle Functions (__shfl_sync)

Warp shuffle functions are intrinsics that allow threads within a warp to exchange data directly with each other without using shared memory. The primary functions are `__shfl_sync`, `__shfl_up_sync`, `__shfl_down_sync`, and `__shfl_xor_sync` [CUDA_C_Programming_Guide:L8670-L8670]. These functions are supported by devices with compute capability 5.0 or higher [CUDA_C_Programming_Guide:L8672-L8672].

## Deprecation of Non-Sync Variants

The non-synchronized variants (`__shfl`, `__shfl_up`, `__shfl_down`, and `__shfl_xor`) were deprecated in CUDA 9.0 for all devices [CUDA_C_Programming_Guide:L8674-L8674]. When targeting devices with compute capability 7.x or higher, these non-sync variants are no longer available, and their `_sync` counterparts must be used [CUDA_C_Programming_Guide:L8676-L8676].

## Function Signatures

The synchronized shuffle functions share a common signature structure, taking a mask, a variable, and addressing parameters, with an optional width parameter:

```cpp
T __shfl_sync(unsigned mask, T var, int srcLane, int width=warpSize);
T __shfl_up_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
T __shfl_down_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
T __shfl_xor_sync(unsigned mask, T var, int laneMask, int width=warpSize);
```

## Supported Data Types

The template type `T` can be:
*   `int`, `unsigned int`
*   `long`, `unsigned long`
*   `long long`, `unsigned long long`
*   `float`, `double`

Additionally, if the `cuda_fp16.h` header is included, `T` can also be `__half` or `__half2`. If the `cuda_bf16.h` header is included, `T` can also be `__nv_bfloat16` or `__nv_bfloat162` [CUDA_C_Programming_Guide:L8687-L8687].

## Operation and Behavior

The `__shfl_sync()` intrinsics permit exchanging a variable between threads within a warp without use of shared memory. The exchange occurs simultaneously for all active threads within the warp (and named in the mask), moving 4 or 8 bytes of data per thread depending on the type [CUDA_C_Programming_Guide:L8691-L8691].

Threads within a warp are referred to as lanes, with indices ranging from 0 to `warpSize-1` [CUDA_C_Programming_Guide:L8693-L8693]. There are four source-lane addressing modes:

1.  **Direct copy from indexed lane**: `__shfl_sync` retrieves the value from a specific lane ID [CUDA_C_Programming_Guide:L8697-L8697].
2.  **Copy from a lane with lower ID**: `__shfl_up_sync` shifts data up the warp [CUDA_C_Programming_Guide:L8701-L8701].
3.  **Copy from a lane with higher ID**: `__shfl_down_sync` shifts data down the warp [CUDA_C_Programming_Guide:L8705-L8705].
4.  **Copy from a lane based on bitwise XOR**: `__shfl_xor_sync` uses a butterfly addressing pattern [CUDA_C_Programming_Guide:L8709-L8709].

### The Mask Parameter

The `_sync` intrinsics require a `mask` argument indicating which threads are participating in the call. A bit representing the thread's lane ID must be set for each participating thread to ensure proper convergence before the intrinsic is executed by the hardware [CUDA_C_Programming_Guide:L8723-L8723]. Each calling thread must have its own bit set in the mask, and all non-exited threads named in the mask must execute the same intrinsic with the same mask; otherwise, the result is undefined [CUDA_C_Programming_Guide:L8723-L8723].

### The Width Parameter

All `__shfl_sync()` intrinsics take an optional `width` parameter that alters behavior. `width` must be a power of two in the range [1, `warpSize`] (i.e., 1, 2, 4, 8, 16, or 32). Results are undefined for other values [CUDA_C_Programming_Guide:L8713-L8713].

If `width` is less than `warpSize`, each subsection of the warp behaves as a separate entity with a starting logical lane ID of 0 [CUDA_C_Programming_Guide:L8715-L8715].

*   **`__shfl_sync`**: Returns the value of `var` held by the thread whose ID is `srcLane`. If `srcLane` is outside the range [0, `width`-1], the value returned corresponds to `var` held by `srcLane % width` [CUDA_C_Programming_Guide:L8715-L8715].
*   **`__shfl_up_sync`**: Calculates a source lane ID by subtracting `delta` from the caller’s lane ID. The value is shifted up by `delta` lanes. The source lane index will not wrap around the value of `width`, so effectively the lower `delta` lanes remain unchanged [CUDA_C_Programming_Guide:L8717-L8717].
*   **`__shfl_down_sync`**: Calculates a source lane ID by adding `delta` to the caller’s lane ID. The value is shifted down by `delta` lanes. The source lane index will not wrap around the value of `width`, so the upper `delta` lanes remain unchanged [CUDA_C_Programming_Guide:L8719-L8719].
*   **`__shfl_xor_sync`**: Calculates a source lane ID by performing a bitwise XOR of the caller’s lane ID with `laneMask`. This implements a butterfly addressing pattern used in tree reduction and broadcast. If `width` is less than `warpSize`, groups of `width` consecutive threads can access elements from earlier groups, but if they attempt to access later groups, their own value of `var` is returned [CUDA_C_Programming_Guide:L8721-L8721].

## Convergence and Safety

Threads may only read data from another thread which is actively participating in the `__shfl_sync()` command. If the target thread is inactive, the retrieved value is undefined [CUDA_C_Programming_Guide:L8711-L8711] [CUDA_C_Programming_Guide:L8725-L8725].

These intrinsics do not imply a memory barrier and do not guarantee any memory ordering [CUDA_C_Programming_Guide:L8727-L8727].
