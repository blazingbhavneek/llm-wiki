## 10.15. Address Space Predicate Functions

The functions described in this section have unspecified behavior if the argument is a null pointer.

## 10.15.1. \_\_isGlobal()

```c
__device__ unsigned int __isGlobal(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in global memory space, otherwise returns 0.

## 10.15.2. \_\_isShared()

```c
__device__ unsigned int __isShared(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in shared memory space, otherwise returns 0.

## 10.15.3. \_\_isConstant()

```txt
__device__ unsigned int __isConstant(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in constant memory space, otherwise returns 0.

## 10.15.4. \_\_isGridConstant()

```txt
__device__ unsigned int __isGridConstant(const void *ptr);
```

Returns 1 if ptr contains the generic address of a kernel parameter annotated with \_\_grid\_constant\_\_, otherwise returns 0. Only supported for compute architectures greater than or equal to 7.x or later.

## 10.15.5. \_\_isLocal()

```c
__device__ unsigned int __isLocal(const void *ptr);
```

Returns 1 if ptr contains the generic address of an object in local memory space, otherwise returns 0.

## 10.16. Address Space Conversion Functions

CUDA C++ pointers (T\*) can access CUDA C++ objects independently of where these objects are stored. For example, an int\* can access int objects independently of whether they are stored in global or shared memory.

The Address Space Conversion Functions below enable converting CUDA C++ pointers from and to other representations. This is required, among others, to interoperate with certain PTX instructions, or to exploit properties of these other representations for performance optimizations.

As an example of interoperating with certain PTX instructions, an ld.shared.u32 r0, [addr]; PTX instruction expects addr to refer to the shared space. A CUDA C++ program with a CUDA C++ uint32\_t\* pointer to an object in \_\_shared\_\_ memory, needs to convert this pointer to the shared space before passing it to such a PTX instruction by calling \_\_cvta\_generic\_to\_shared as follows:

```txt
__shared__ uint32_t x;
x = 42;
void* p = &x;
size_t sp = __cvta_generic_to_shared(p);
uint32_t o;
asm volatile("ld.shared.u32 %0, [%1];" : "=r"(o) : "l"(sp) : "memory");
assert(o == 42);
```

A common program optimization that exploits properties of these other address representations is reducing data-structure size by leveraging that the address ranges of shared, local, and const spaces is smaller than 32-bit, which allows programs to store 32-bit addresses instead of 64-bit pointers. To obtain the 32-bit integer representation of these addresses, it sufices to truncate it by performing an unsigned 64-bit integer to unsigned 32-bit integer cast:

```c
__shared__ int x;
void* p = &x;
uint32_t smem32 = __cvta_generic_to_shared(p);
```

To obtain a generic address from such a 32-bit integer representation, it sufices to zero-extend the address back to an unsigned 64-bit integer before calling the corresponding address space conversion function:

```c
size_t smem64 = smem32;
void* q = __cvta_shared_to_generic(smem64);
assert(p == q);
```

A roundtrip from an input generic space pointer to its 32-bit integer representation and back to an output generic space pointer is guaranteed to return an output pointer that is equivalent to the input pointer of the roundtrip for the spaces listed above.

## 10.16.1. \_\_cvta\_generic\_to\_global()

```c
__device__ size_t __cvta_generic_to_global(const void *ptr);
```

Returns the result of executing the PTXcvta.to.global instruction on the generic address denoted by ptr.

## 10.16.2. \_\_cvta\_generic\_to\_shared()

```c
__device__ size_t __cvta_generic_to_shared(const void *ptr);
```

Returns the result of executing the PTXcvta.to.shared instruction on the generic address denoted by ptr.

## 10.16.3. \_\_cvta\_generic\_to\_constant()

```c
__device__ size_t __cvta_generic_to_constant(const void *ptr);
```

Returns the result of executing the PTXcvta.to.const instruction on the generic address denoted by ptr.

## 10.16.4. \_\_cvta\_generic\_to\_local()

```c
__device__ size_t __cvta_generic_to_local(const void *ptr);
```

Returns the result of executing the PTXcvta.to.local instruction on the generic address denoted by ptr.

## 10.16.5. \_\_cvta\_global\_to\_generic()

```c
__device__ void * __cvta_global_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.global instruction on the value provided by rawbits.

## 10.16.6. \_\_cvta\_shared\_to\_generic()

```c
__device__ void * __cvta_shared_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.shared instruction on the value provided by rawbits.

## 10.16.7. \_\_cvta\_constant\_to\_generic()

```c
__device__ void * __cvta_constant_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.const instruction on the value provided by rawbits.

## 10.16.8. \_\_cvta\_local\_to\_generic()

```c
__device__ void * __cvta_local_to_generic(size_t rawbits);
```

Returns the generic pointer obtained by executing the PTXcvta.local instruction on the value provided by rawbits.
