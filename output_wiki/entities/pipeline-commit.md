# __pipeline_commit Primitive

The `__pipeline_commit` function is used to commit previously submitted `memcpy_async` operations to the pipeline, designating them as the current batch.

## Syntax

```cpp
void __pipeline_commit();
```

## Description

This function finalizes the submission of asynchronous memory copy operations that were initiated via `memcpy_async`. It ensures that these operations are processed as a distinct batch within the pipeline execution model.

## References

- CUDA C Programming Guide [CUDA_C_Programming_Guide:L10191-L10196]
