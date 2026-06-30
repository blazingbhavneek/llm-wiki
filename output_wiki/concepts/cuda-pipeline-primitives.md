# CUDA Pipeline Primitives Interface

C-like Pipeline Primitives Interface (__pipeline_memcpy_async, __pipeline_commit, __pipeline_wait_prior, __pipeline_arrive_on). Covers function signatures, usage requirements, race condition warnings, and barrier synchronization details.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L10149-L10217

Citation: [CUDA_C_Programming_Guide:L10149-L10217]

````text
## 10.28.4. Pipeline Primitives Interface

Pipeline primitives are a C-like interface for memcpy\_async functionality. The pipeline primitives interface is available by including the <cuda\_pipeline.h> header. When compiling without ISO C++ 2011 compatibility, include the <cuda\_pipeline\_primitives.h> header.

## 10.28.4.1 memcpy\_async Primitive

```txt
void __pipeline_memcpy_async(void* __restrict__ dst_shared,
                    const void* __restrict__ src_global,
                    size_t size_and_align,
                    size_t zfill=0);
```

▶ Request that the following operation be submitted for asynchronous evaluation:

```c
size_t i = 0;
for (; i < size_and_align - zfill; ++i) ((char*)dst_shared)[i] = ((char*)src_global)[i]; /* copy */
for (; i < size_and_align; ++i) ((char*)dst_shared)[i] = 0; /* zero-fill */
```

## ▶ Requirements:

▶ dst\_shared must be a pointer to the shared memory destination for the memcpy\_async.

▶ src\_global must be a pointer to the global memory source for the memcpy\_async.

▶ size\_and\_align must be 4, 8, or 16.

▶ zfill <= size\_and\_align.

▶ size\_and\_align must be the alignment of dst\_shared and src\_global.

▶ It is a race condition for any thread to modify the source memory or observe the destination memory prior to waiting for the memcpy\_async operation to complete. Between submitting a memcpy\_async operation and waiting for its completion, any of the following actions introduces a race condition:

Loading from dst\_shared.

▶ Storing to dst\_shared or src\_global.

▶ Applying an atomic update to dst\_shared or src\_global.

## 10.28.4.2 Commit Primitive

```javascript
void __pipeline_commit();
```

Commit submitted memcpy\_async to the pipeline as the current batch.

## 10.28.4.3 Wait Primitive

```txt
void __pipeline_wait_prior(size_t N);
```

▶ Let {0, 1, 2, ..., L} be the sequence of indices associated with invocations of \_\_pipeline\_commit() by a given thread.

▶ Wait for completion of batches at least up to and including L-N.

## 10.28.4.4 Arrive On Barrier Primitive

```txt
void __pipeline_arrive_on(__mbarrier_t* bar);
```

▶ bar points to a barrier in shared memory.

Increments the barrier arrival count by one, when all memcpy\_async operations sequenced before this call have completed, the arrival count is decremented by one and hence the net efect on the arrival count is zero. It is user’s responsibility to make sure that the increment on the arrival count does not exceed \_\_mbarrier\_maximum\_count().
````
