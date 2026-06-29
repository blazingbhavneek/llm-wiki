# Single Thread Group

The single thread group is a cooperative group that represents the current thread. It is obtained using the `this_thread` function, which returns a `thread_block_tile<1>` object.

## API

The `this_thread` function is defined as:

```txt
thread_block_tile<1> this_thread();
```

## Usage

This group is commonly used in APIs that require a thread group context, such as asynchronous memory copies. For example, the `memcpy_async` function from the `cooperative_groups/memcpy_async.h` header can use the single thread group to copy data from a source to a destination:

```c
#include <cooperative_groups.h>
#include <cooperative_groups/memcpy_async.h>

cooperative_groups::memcpy_async(cooperative_groups::this_thread(), dest, src,
sizeof(int));
```

More detailed examples of using `this_thread` to perform asynchronous copies can be found in the "Single-Stage Asynchronous Data Copies using cuda::pipeline" and "Multi-Stage Asynchronous Data Copies using cuda::pipeline" sections of the CUDA C++ Programming Guide [CUDA_C_Programming_Guide:L12338-L12357].
