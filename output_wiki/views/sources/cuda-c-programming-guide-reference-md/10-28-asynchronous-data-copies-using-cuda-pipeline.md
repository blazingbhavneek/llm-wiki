# 10.28. Asynchronous Data Copies using cuda::pipeline

Part of [Cuda C Programming Guide Reference](README.md). Source lines L9778-L10217.

- [cuda::pipeline Overview](../../../concepts/cuda-pipeline.md) — The cuda::pipeline synchronization object manages and overlaps asynchronous data movement with computation using a double-ended N-stage queue that processes work in FIFO order.
- [Single-Stage Asynchronous Data Copies using cuda::pipeline](../../../concepts/cuda-pipeline-single-stage.md) — Demonstrates using the cuda::pipeline API with a single stage to schedule asynchronous memory copies, allowing computation to overlap with data transfer.
- [Multi-Stage Asynchronous Data Copies using cuda::pipeline](../../../concepts/cuda-pipeline-multi-stage.md) — The cuda::pipeline feature enables CUDA kernels to overlap memory transfers with computation by managing a sequence of asynchronous memcpy operations across multiple stages.
- [Unified Pipeline Loop Pattern](../../../concepts/cuda-pipeline-unified-loop.md) — The Unified Pipeline Loop Pattern merges the prolog and epilog stages of a CUDA pipeline execution into a single nested loop structure, optimizing code conciseness while maintaining asynchronous memory transfers and computation overlap.
- [Specialized Producer/Consumer Roles in cuda::pipeline](../../../concepts/cuda-pipeline-specialized-roles.md) — The cuda::pipeline interface allows threads within a block to be assigned specific roles (producer, consumer, or both) to optimize memory transfer and computation overlap, with optimizations available for specific participation patterns.
- [cuda::pipeline Interface Requirements](../../../concepts/cuda-pipeline-interface-requirements.md) — The cuda::pipeline interface requires CUDA 11.0 or later, ISO C++ 2011 compatibility, and the inclusion of the <cuda/pipeline> header, with a C-like alternative available for non-C++11 environments.
- [Pipeline Primitives Interface](../../../concepts/cuda-pipeline-primitives-interface.md) — The Pipeline Primitives Interface provides a C-like API for managing memcpy_async operations, accessible via the <cuda_pipeline.h> header in ISO C++ 2011 compliant environments or <cuda_pipeline_primitives.h> otherwise.
- [__pipeline_memcpy_async Primitive](../../../entities/pipeline-memcpy-async.md)
- [__pipeline_commit Primitive](../../../entities/pipeline-commit.md)
- [__pipeline_wait_prior Primitive](../../../entities/pipeline-wait-prior.md)
- [__pipeline_arrive_on Primitive](../../../entities/pipeline-arrive-on.md)
