# __pipeline_arrive_on Primitive

The `__pipeline_arrive_on` function is a synchronization primitive used to manage barriers in shared memory for asynchronous memory copy operations.

## Syntax

```cpp
void __pipeline_arrive_on(__mbarrier_t* bar);
```

## Parameters

* `bar`: A pointer to an `__mbarrier_t` structure representing a barrier located in shared memory.

## Description

When `__pipeline_arrive_on` is called, it immediately increments the barrier's arrival count by one. Subsequently, once all `memcpy_async` operations that were sequenced before this call have completed, the function decrements the arrival count by one. Consequently, the net effect on the arrival count is zero [CUDA_C_Programming_Guide:L10208-L10217].

## Constraints

It is the user's responsibility to ensure that the increment on the arrival count does not exceed the value returned by `__mbarrier_maximum_count()` [CUDA_C_Programming_Guide:L10208-L10217].

## See Also

* `__mbarrier_t`
* `memcpy_async`
* `__mbarrier_maximum_count`
