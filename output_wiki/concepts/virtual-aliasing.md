# Virtual Aliasing Support

Describes creating multiple virtual memory mappings (proxies) to the same allocation via cuMemMap, and handling coherence/fencing with fence.proxy.alias.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L15142-L15196

Citation: [CUDA_C_Programming_Guide:L15142-L15196]

````text
## 14.5. Virtual Aliasing Support

The Virtual Memory Management APIs provide a way to create multiple virtual memory mappings or “proxies” to the same allocation using multiple calls to cuMemMap with diferent virtual addresses, socalled virtual aliasing. Unless otherwise noted in the PTX ISA, writes to one proxy of the allocation are considered inconsistent and incoherent with any other proxy of the same memory until the writing device operation (grid launch, memcpy, memset, and so on) completes. Grids present on the GPU prior to a writing device operation but reading after the writing device operation completes are also considered to have inconsistent and incoherent proxies.

For example, the following snippet is considered undefined, assuming device pointers A and B are virtual aliases of the same memory allocation:

```txt
__global__ void foo(char *A, char *B) {
  *A = 0x1;
  printf("%d\n", *B);    // Undefined behavior!  *B can take on either
// the previous value or some value in-between.
}
```

The following is defined behavior, assuming these two kernels are ordered monotonically (by streams or events).

```txt
__global__ void foo1(char *A) {
    *A = 0x1;
}

__global__ void foo2(char *B) {
    printf("%d\n", *B);      // *B == *A == 0x1 assuming foo2 waits for foo1
// to complete before launching
```

(continues on next page)

(continued from previous page)

```txt
}
cudaMemcpyAsync(B, input, size, stream1);    // Aliases are allowed at
// operation boundaries
foo1<<<1,1,0,stream1>>>(A);                  // allowing foo1 to access A.
cudaEventRecord(event, stream1);
cudaStreamWaitEvent(stream2, event);
foo2<<<1,1,0,stream2>>>(B);
cudaStreamWaitEvent(stream3, event);
cudaMemcpyAsync(output, B, size, stream3);   // Both launches of foo2 and
                                // cudaMemcpy (which both
                                // read) wait for foo1 (which writes)
                                // to complete before proceeding
```

If accessing same allocation through diferent “proxies” is required in the same kernel a fence.proxy. alias can be used between the two accesses. The above example can thus be made legal with inline PTX assembly:

```lisp
__global__ void foo(char *A, char *B) {
    *A = 0x1;
    asm volatile ("fence.proxy.alias;" ::: "memory");
    printf("%d\n", *B);      // *B == *A == 0x1
}
```
````
