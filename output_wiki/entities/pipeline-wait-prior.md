# __pipeline_wait_prior Primitive

The `__pipeline_wait_prior` function is a synchronization primitive used in CUDA pipeline management to ensure that previous batches have been processed before proceeding.

## Syntax

```cpp
void __pipeline_wait_prior(size_t N);
```

## Description

Let `{0, 1, 2, ..., L}` be the sequence of indices associated with invocations of `__pipeline_commit()` by a given thread [CUDA_C_Programming_Guide:L10198-L10207].

The function waits for the completion of batches at least up to and including index `L-N` [CUDA_C_Programming_Guide:L10198-L10207]. This allows a thread to synchronize with the progress of the pipeline relative to its own commit history.

## Parameters

- **N**: The offset from the last committed batch index `L`. The function ensures that all batches with indices `<= L-N` are complete.

## See Also

- `__pipeline_commit`
- `__pipeline_async`
