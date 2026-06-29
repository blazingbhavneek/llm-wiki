# Virtual Functions in CUDA

Virtual functions in CUDA are subject to specific constraints regarding execution spaces and object lifetime to ensure correct behavior. These restrictions apply to both host and device code interactions.

## Execution Space Constraints

### Matching Specifiers
When a function in a derived class overrides a virtual function in a base class, the execution space specifiers (i.e., `__host__`, `__device__`) on the overridden and overriding functions must match [CUDA_C_Programming_Guide:L17284-L17320].

### Object Passing Restrictions
It is not allowed to pass as an argument to a `__global__` function an object of a class with virtual functions [CUDA_C_Programming_Guide:L17284-L17320].

### Cross-Space Invocation
Invoking a virtual function on an object across different execution spaces leads to undefined behavior:

*   If an object is created in host code, invoking a virtual function for that object in device code has undefined behavior [CUDA_C_Programming_Guide:L17284-L17320].
*   If an object is created in device code, invoking a virtual function for that object in host code has undefined behavior [CUDA_C_Programming_Guide:L17284-L17320].

## Example

The following example illustrates these restrictions using managed memory:

```txt
struct S1 { virtual __host__ __device__ void foo() { } };

__managed__ S1 *ptr1, *ptr2;

__managed__ __align__(16) char buf1[128];
__global__ void kern() {
    ptr1->foo();      // error: virtual function call on a object
                      //          created in host code.
    ptr2 = new(buf1) S1();
}

int main(void) {
    void *buf;
    cudaMallocManaged(&buf, sizeof(S1), cudaMemAttachGlobal);
    ptr1 = new (buf) S1();
    kern<<<1,1>>>();
    cudaDeviceSynchronize();
    ptr2->foo();  // error: virtual function call on an object
                      //          created in device code.
}
```

## Additional Constraints

See Windows-Specific for additional constraints when using the Microsoft host compiler [CUDA_C_Programming_Guide:L17284-L17320].
