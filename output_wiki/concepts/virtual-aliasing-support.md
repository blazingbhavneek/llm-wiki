# Virtual Aliasing Support

Virtual Aliasing Support is provided by the Virtual Memory Management APIs, which allow the creation of multiple virtual memory mappings, or "proxies," to the same memory allocation. This is achieved by making multiple calls to `cuMemMap` with different virtual addresses [CUDA_C_Programming_Guide:L15142-L15196].

## Consistency and Coherence

By default, unless otherwise noted in the PTX ISA, writes to one proxy of an allocation are considered inconsistent and incoherent with any other proxy of the same memory until the writing device operation completes. A writing device operation includes grid launches, memory copies (`memcpy`), and memory sets (`memset`) [CUDA_C_Programming_Guide:L15142-L15196].

This inconsistency also applies to grids present on the GPU prior to a writing device operation but reading after that operation completes [CUDA_C_Programming_Guide:L15142-L15196].

### Undefined Behavior

Accessing the same allocation through different proxies within the same kernel without synchronization results in undefined behavior. For example, if device pointers `A` and `B` are virtual aliases of the same memory allocation, the following code is undefined because `*B` may reflect either the previous value or an intermediate value [CUDA_C_Programming_Guide:L15142-L15196]:

```cpp
__global__ void foo(char *A, char *B) {
  *A = 0x1;
  printf("%d\n", *B);    // Undefined behavior!
}
```

## Enforcing Consistency

Consistency between virtual aliases can be enforced using two primary methods: PTX fence instructions or stream/event synchronization.

### Using `fence.proxy.alias`

If accessing the same allocation through different proxies is required within the same kernel, the `fence.proxy.alias` PTX instruction can be used between the two accesses to ensure coherence [CUDA_C_Programming_Guide:L15142-L15196]. The previous example can be made legal with inline PTX assembly as follows [CUDA_C_Programming_Guide:L15142-L15196]:

```cpp
__global__ void foo(char *A, char *B) {
    *A = 0x1;
    asm volatile ("fence.proxy.alias;" ::: "memory");
    printf("%d\n", *B);      // *B == *A == 0x1
}
```

### Using Stream/Event Synchronization

Defined behavior can also be achieved by ordering kernels monotonically using streams or events. In this scenario, subsequent kernels or operations wait for the writing kernel to complete before accessing the aliased memory [CUDA_C_Programming_Guide:L15142-L15196].

Example of defined behavior using streams and events [CUDA_C_Programming_Guide:L15142-L15196]:

```cpp
__global__ void foo1(char *A) {
    *A = 0x1;
}

__global__ void foo2(char *B) {
    printf("%d\n", *B);      // *B == *A == 0x1 assuming foo2 waits for foo1
}

// ... setup code ...
cudaMemcpyAsync(B, input, size, stream1);    // Aliases are allowed at operation boundaries
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

In this example, `foo2` and the subsequent `cudaMemcpyAsync` wait for `foo1` (the writer) to complete before proceeding, ensuring that the read operations see the written value [CUDA_C_Programming_Guide:L15142-L15196].
