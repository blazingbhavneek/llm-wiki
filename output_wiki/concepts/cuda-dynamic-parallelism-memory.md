# CUDA Dynamic Parallelism Memory Declarations

Memory space handling in CDP including device, constant, texture, surface, shared, and symbol addresses.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L13964-L14013

Citation: [CUDA_C_Programming_Guide:L13964-L14013]

````text

## 13.3.1.6 Memory Declarations

## 13.3.1.6.1 Device and Constant Memory

Memory declared at file scope with \_\_device\_\_ or \_\_constant\_\_ memory space specifiers behaves identically when using the device runtime. All kernels may read or write device variables, whether the kernel was initially launched by the host or device runtime. Equivalently, all kernels will have the same view of \_\_constant\_\_s as declared at the module scope.

## 13.3.1.6.2 Textures and Surfaces

CUDA supports dynamically created texture and surface objects<sup>7</sup>, where a texture object may be created on the host, passed to a kernel, used by that kernel, and then destroyed from the host. The device runtime does not allow creation or destruction of texture or surface objects from within device code, but texture and surface objects created from the host may be used and passed around freely on the device. Regardless of where they are created, dynamically created texture objects are always valid and may be passed to child kernels from a parent.

Note: The device runtime does not support legacy module-scope (i.e., Fermi-style) textures and surfaces within a kernel launched from the device. Module-scope (legacy) textures may be created from the host and used in device code as for any kernel, but may only be used by a top-level kernel (i.e., the one which is launched from the host).

## 13.3.1.6.3 Shared Memory Variable Declarations

In CUDA C++ shared memory can be declared either as a statically sized file-scope or function-scoped variable, or as an extern variable with the size determined at runtime by the kernel’s caller via a launch configuration argument. Both types of declarations are valid under the device runtime.

```txt
__global__ void permute(int n, int *data) {
    extern __shared__ int smem[];
    if (n <= 1)
        return;

    smem[threadIdx.x] = data[threadIdx.x];
    __syncthreads();

    permute_data(smem, n);
    __syncthreads();

    // Write back to GMEM since we can't pass SMEM to children.
    data[threadIdx.x] = smem[threadIdx.x];
    __syncthreads();

    if (threadIdx.x == 0) {
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data);
        permute<<< 1, 256, n/2*sizeof(int) >>>(n/2, data+n/2);
    }
}

void host_launch(int *data) {
    permute<<< 1, 256, 256*sizeof(int) >>>(256, data);
}
```

## 13.3.1.6.4 Symbol Addresses

Device-side symbols (i.e., those marked \_\_device\_\_) may be referenced from within a kernel simply via the & operator, as all global-scope device variables are in the kernel’s visible address space. This also applies to \_\_constant\_\_ symbols, although in this case the pointer will reference read-only data.

Given that device-side symbols can be referenced directly, those CUDA runtime APIs which reference symbols (e.g., cudaMemcpyToSymbol() or cudaGetSymbolAddress()) are redundant and hence not supported by the device runtime. Note this implies that constant data cannot be altered from within a running kernel, even ahead of a child kernel launch, as references to \_\_constant\_\_ space are readonly.
````
