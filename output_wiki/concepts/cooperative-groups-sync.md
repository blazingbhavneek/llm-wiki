# sync

Synchronizes all threads named in a group. Available as a member function or free function. Equivalent to calling barrier_arrive followed by barrier_wait.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12620-L12631

Citation: [CUDA_C_Programming_Guide:L12620-L12631]

````text
## 11.6.1.2 sync

```cpp
static void T::sync();
```

```txt
template <typename T>
void sync(T& group);
```

sync synchronizes the threads named in the group. Group type T can be any of the existing group types, as all of them support synchronization. Its available as a member function in every group type or as a free function taking a group as parameter. If the group is a grid\_group the kernel must have been launched using the appropriate cooperative launch APIs. Equivalent to T.barrier\_wait(T. barrier\_arrive()).
````
