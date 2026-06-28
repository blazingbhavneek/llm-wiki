## 10.14.3. Other atomic functions

## 10.14.3.1 \_\_nv\_atomic\_load()

```c
__device__ void __nv_atomic_load(T* ptr, T* ret, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It loads the value where ptr points to and writes the value to where ret points to.

This is a generic atomic load, which means that T can be any data type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_RELEASE or \_\_NV\_ATOMIC\_ACQ\_REL.

## 10.14.3.2 \_\_nv\_atomic\_load\_n()

```c
__device__ T __nv_atomic_load_n(T* ptr, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It loads the value where ptr points to and returns this value.

This is a non-generic atomic load, which means that T can only be an integral type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_RELEASE or \_\_NV\_ATOMIC\_ACQ\_REL.

## 10.14.3.3 \_\_nv\_atomic\_store()

\_device\_\_ void \_\_nv\_atomic\_store(T\* ptr, T\* val, int order, int scope = \_\_NV\_THREAD\_ , SCOPE\_SYSTEM);

This atomic function is introduced in CUDA 12.8. It reads the value where val points to and stores to where ptr points to.

This is a generic atomic load, which means that T can be any data type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_CONSUME, \_\_NV\_ATOMIC\_ACQUIRE or \_\_NV\_ATOMIC\_ACQ\_REL.

## 10.14.3.4 \_\_nv\_atomic\_store\_n()

```txt
__device__ void __nv_atomic_store_n(T* ptr, T val, int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function is introduced in CUDA 12.8. It stores val to where ptr points to.

This is a non-generic atomic load, which means that T can only be an integral type that is size of 1, 2, 4, 8 or 16 bytes.

The atomic operation with memory order and thread scope is supported on the architecture sm\_60 and higher.

16-byte data type is supported on the architecture sm\_70 and higher.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables. order cannot be \_\_NV\_ATOMIC\_CONSUME, \_\_NV\_ATOMIC\_ACQUIRE or \_\_NV\_ATOMIC\_ACQ\_REL.

## 10.14.3.5 \_\_nv\_atomic\_thread\_fence()

```c
__device__ void __nv_atomic_thread_fence (int order, int scope = __NV_THREAD_SCOPE_SYSTEM);
```

This atomic function establishes an ordering between memory accesses requested by this thread based on the specified memory order. And the thread scope parameter specifies the set of threads that may observe the ordering efect of this operation.

The thread scope of cluster is supported on the architecture sm\_90 and higher.

The arguments order and scope need to be integer literals, i.e., the arguments cannot be variables.
