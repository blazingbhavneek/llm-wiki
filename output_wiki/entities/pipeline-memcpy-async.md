# __pipeline_memcpy_async Primitive

Documentation for the __pipeline_memcpy_async primitive, which requests an asynchronous copy operation. It details the parameters (dst_shared, src_global, size_and_align, zfill), the required alignment, and race condition warnings regarding source/destination memory access.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Could not extract valid JSON from LLM response.

## Source CUDA_C_Programming_Guide:L10153-L10189

Citation: [CUDA_C_Programming_Guide:L10153-L10189]

````text
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
````

## Source CUDA_C_Programming_Guide:L10190-L10190

Citation: [CUDA_C_Programming_Guide:L10190-L10190]

````text
## 10.28.4.2 Commit Primitive
````
