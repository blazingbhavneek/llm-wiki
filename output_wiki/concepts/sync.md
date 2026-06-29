# sync

The `sync` function synchronizes the threads named in the specified group. It is available as both a member function for every group type and as a free function that takes a group as a parameter.

## Syntax

As a member function:

```cpp
static void T::sync();
```

As a free function:

```cpp
template <typename T>
void sync(T& group);
```

## Behavior

The `sync` function is equivalent to calling `T.barrier_wait(T.barrier_arrive())` [CUDA_C_Programming_Guide:L12617-L12631].

## Requirements

*   **Group Types**: The group type `T` can be any of the existing group types, as all of them support synchronization [CUDA_C_Programming_Guide:L12617-L12631].
*   **Grid Groups**: If the group is a `grid_group`, the kernel must have been launched using the appropriate cooperative launch APIs [CUDA_C_Programming_Guide:L12617-L12631].

## See Also

*   `barrier_arrive`
*   `barrier_wait`
