
## Using Sub-group Block Load/Store

Memory loads/stores are vectorized. Each lane of a vector load/store instruction has its own address and data. Both addresses and data take register space. For example:

```cpp
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
            [=](sycl::nd_item<1> it) {
                int i = it.get_global_linear_id();
                data[i] = data2[i];
            });
});
```

The memory loads and stores in the statement:

```txt
``data[i] = data2[i];``
```

are vectorized and each vector lane has its own address. Assuming the SIMD width or the sub-group size is 16, total register space for addresses of the 16 lanes is 128 bytes. If each GRF register is 32-byte wide, 4 GRF registers are needed for the addresses.

Noticing the addresses are contiguous, we can use sub-group block load/store built-ins to save register space for addresses:

```c
constexpr int N = 1024 * 1024;
int *data = sycl::malloc_shared<int>(N, q);
int *data2 = sycl::malloc_shared<int>(N, q);
```

```cpp
memset(data2, 0xFF, sizeof(int) * N);

auto e = q.submit([&](auto &h) {
    h.parallel_for(sycl::nd_range(sycl::range{N}, sycl::range{32}),
        [=](sycl::nd_item<1> it) [[intel::reqd_sub_group_size(16)]] {
        auto sg = it.get_sub_group();

        int base =
            (it.get_group(0) * 32 +
            sg.get_group_id()[0] * sg.get_local_range()[0]);

        auto load_ptr = get_multi_ptr(&(data2[base + 0]));
        int x = sg.load(load_ptr);

        auto store_ptr = get_multi_ptr(&(data[base + 0]));
        sg.store(store_ptr, x);
    });
});
```

The statements:

```javascript
` ` x = sg.load(global_ptr(&(data2[base + 0])), sg.store(global_ptr(&(data[base + 0])), x);``
```

each loads/stores a contiguous block of memory and the compiler will compile these 2 statements into special memory block load/store instructions. And because it is a contiguous memory block, we only need the starting address of the block. So 8, instead of 128, bytes of actual register space, or at most 1 register, is used for the address for each block load/store.
