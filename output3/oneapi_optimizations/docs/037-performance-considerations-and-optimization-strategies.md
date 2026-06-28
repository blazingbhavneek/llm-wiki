
Unified Shared Memory (USM). USM allows reading and writing of data with conventional pointers, in contrast to buffers where access to data is exclusively by API. USM has two commonly-used variants. Device allocations can only be accessed from the device and therefore require explicit movement of data between host and device. Shared allocations can be referenced from device or host, with the runtime automatically moving memory.

We illustrate the tradeoffs between choices by showing the same example program written with the three models. To highlight the issues, we use a program where a GPU and the host cooperatively compute, and therefore need to ship data back and forth.

We start by showing the serial computation below. Assume that we want to perform the loop at line 9 on the GPU and the loop on line 14 on the CPU. Both loops read and write the data array so data must move between host and GPU for each iteration of the loop in line 8.

```txt
void serial(int stride) {
  // Allocate and initialize data
  float *data = new float[data_size];
  init(data);

  timer it;

  for (int i = 0; i < time_steps; i++) {
    for (int j = 0; j < data_size; j++) {
      for (int k = 0; k < device_steps; k++)
        data[j] += 1.0;
    }

    for (int j = 0; j < data_size; j += stride)
      data[j] += 1.0;
  }
  put_elapsed_time(it);

  check(data);

  delete[] data;
} // serial
```

## Buffers

Below, we show the same computation using buffers to manage data. A buffer is created at line 3 and initialized by the init function. The init function is not shown. It accepts an accessor or a pointer. The parallel\_for executes the kernel defined on line 13. The kernel uses the device\_dataaccessor to read and write data in buffer\_data.

Note that the code does not specify the location of data. An accessor indicates when and where the data is needed, and the SYCL runtime moves the data to the device (if necessary) and then launches the kernel. The host\_accessor on line 21 indicates that the data will be read/written on the host. Since the kernel is also read/writing buffer\_data, the host\_accessor constructor waits for the kernel to complete and moves data to the host to perform the read/write on line 23. In the next iteration of the loop the accessor constructor on line 11 waits until the until the data is moved back to the device, which effectively delays launching the kernel.

```cpp
void buffer_data(int stride) {
  // Allocate buffer, initialize on host
  sycl::buffer<float> buffer_data{data_size};
  init(sycl::host_accessor(buffer_data, sycl::write_only, sycl::no_init));

  timer it;
  for (int i = 0; i < time_steps; i++) {

    // Compute on device
    q.submit([&](auto &h) {
      sycl::accessor device_data(buffer_data, h);

      auto compute = [=](auto id) {
        for (int k = 0; k < device_steps; k++)
          device_data[id] += 1.0;
      };
      h.parallel_for(data_size, compute);
```

```cpp
});

// Compute on host
sycl::host_accessor host_data(buffer_data);
for (int i = 0; i < data_size; i += stride)
    host_data[i] += 1.0;
}
put_elapsed_time(it);

const sycl::host_accessor h(buffer_data);
check(h);
} // buffer_data
```

## Performance Considerations

The data access on lines 15 and 23 appear to be simple array references, but they are implemented by the SYCL runtime with C++ operator overloading. The efficiency of accessor array references depends on the implementation. In practice, device code pays no overhead for overloading compared to direct memory references. The runtime does not know in advance which part of the buffer is accessed, so it must ensure all the data is on the device before the kernel begins. This is true today, but may change over time.

The same is not currently true for the host\_accessor. The runtime does not move all the data to the host. The array references are implemented with more complex code and are significantly slower than native C++ array references. While it is acceptable to reference a small amount of data, computationally intensive algorithms using host\_accessor pay a large performance penalty and should be avoided.

Another concern is concurrency. A host\_accessor can block kernels that reference the same buffer from launching, even if the accessor is not actively being used to read/write data. Limit the scope that contains the host\_accessor to the minimum possible. In this example, the host accessor on line 4 is destroyed after the init function returns and the host accessor on line 21 is destroyed at the end of each loop iteration.

## Shared Allocations

Next we show the same algorithm implemented with shared allocations. Data is allocated on line 2. Accessors are not needed because USM-allocated data can be referenced with conventional allows pointers. Therefore, the array references on lines 10 and 15 can be implemented with simple indexing. The parallel\_for on line 12 ends with a wait to ensure the kernel finishes before the host accesses data on line 15. Similar to buffers, the SYCL runtime ensures that all the data is resident on the device before launching a kernel. And like buffers, shared allocations are not copied to the host unless it is referenced. The first time the host references data, there is an operating system page fault, a page of data is copied from device to host, and execution continues. Subsequent references to data on the same page execute at full speed. When a kernel is launched, all of the host-resident pages are flushed back to the device.

```cpp
void shared_usm_data(int stride) {
    float *data = sycl::malloc_shared<float>(data_size, q);
    init(data);

    timer it;

    for (int i = 0; i < time_steps; i++) {
        auto compute = [=](auto id) {
            for (int k = 0; k < device_steps; k++)
                data[id] += 1.0;
        };
        q.parallel_for(data_size, compute).wait();

        for (int k = 0; k < data_size; k += stride)
            data[k] += 1.0;
```

```cpp
}
q.wait();
put_elapsed_time(it);

check(data);

sycl::free(data, q);
} // shared_usm_data
```

## Performance Considerations

Compared to buffers, data references are simple pointers and perform well. However, servicing page faults to bring data to the host incurs overhead in addition to the cost of transferring data. The impact on the application depends on the reference pattern. Sparse random access has the highest overhead and linear scans through data have lower impact from page faults.

Since all synchronization is explicit and under programmer control, concurrency is not an issue for a well designed program.

## Device Allocations

The same program with device allocation can be found below. With device allocation, data can only be directly accessed on the device and must be explicitly copied to the host, as is done on line 21. All synchronization between device and host are explicit. Line 21 ends with a wait so the host code will not execute until the asynchronous copy finishes. The queue definition is not shown but uses an in-order queue so the memcpy on line 21 waits for the parallel\_for on line 18 to complete.

```cpp
void device_usm_data(int stride) {
  // Allocate and initialize host data
  float *host_data = new float[data_size];
  init(host_data);

  // Allocate device data
  float *device_data = sycl::malloc_device<float>(data_size, q);

  timer it;

  for (int i = 0; i < time_steps; i++) {
    // Copy data to device and compute
    q.memcpy(device_data, host_data, sizeof(float) * data_size);
    auto compute = [=](auto id) {
      for (int k = 0; k < device_steps; k++)
        device_data[id] += 1.0;
    };
    q.parallel_for(data_size, compute);

    // Copy data to host and compute
    q.memcpy(host_data, device_data, sizeof(float) * data_size).wait();
    for (int k = 0; k < data_size; k += stride)
      host_data[k] += 1.0;
  }
  q.wait();
  put_elapsed_time(it);

  check(host_data);
```

```cpp
sycl::free(device_data, q);
    delete[] host_data;
} // device_usm_data
```

## Performance Considerations

Both data movement and synchronization are explicit and under the full control of the programmer. Array references are array references on the host, so it has neither the page faults overhead of shared allocations, nor the overloading overhead associated with buffers. Shared allocations only transfer data that the host actually references, with a memory page granularity. In theory, device allocations allow on-demand movement of any granularity. In practice, fine-grained, asynchronous movement of data can be complex and most programmers simply move the entire data structure once. The requirement for explicit data movement and synchronization makes the code more complicated, but device allocations can provide the best performance.

## Avoiding Moving Data Back and Forth between Host and Device

The cost of moving data between host and device is quite high, especially in the case of discrete accelerators. So it is very important to avoid data transfers between host and device as much as possible. In some situations it may be required to bring the data that was computed by a kernel on the accelerator to the host and do some operation on it and send it back to the device for further processing. In such situation we will end up paying for the cost of device to host transfer and then again host to device transfer.

Consider the following example, where one kernel produces data through some operation (in this case vector add) into a new vector. This new vector is then transformed into a third vector by applying a function on each value and this third vector is finally fed as input into another kernel for some additional computation. This form of computation is quite common and occurs in many domains where algorithms are iterative and output from one computation needs to be fed as input into another computation. In machine learning, for example, models are structured as layers of computations, and output of one layer is input to the next layer.

```cpp
double myFunc1(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()};
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessors
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(num_items,
                [=](auto id) { sum_acc[id] = a_acc[id] + b_acc[id]; });
        });
```

```cpp
{
    sycl::host_accessor h_acc(sum_buf);
    for (size_t j = 0; j < a.size(); j++)
        if (h_acc[j] > 10)
            h_acc[j] = 1;
        else
            h_acc[j] = 0;
}

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto id) {
        res_acc[id] = sum_acc[id] * c_acc[id] + d_acc[id];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
} // end myFunc1
```

Instead of bringing the data to the host and applying the function to the data and sending it back to the device, you can create a kernel3 to execute this function on the device, as shown in the following example. The kernel kernel3 operates on the intermediate data in accum\_buf in between kernel1 and kernel2, avoiding the round trip of data transfer between the device and the host.

```cpp
double myFunc2(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()} {
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(num_items,
                [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
```

```cpp
});

// kernel3
q.submit([&](auto &h) {
    sycl::accessor sum_acc(sum_buf, h, sycl::read_write);
    h.parallel_for(num_items, [=](auto id) {
        if (sum_acc[id] > 10)
            sum_acc[id] = 1;
        else
            sum_acc[id] = 0;
    });
});

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto i) {
        res_acc[i] = sum_acc[i] * c_acc[i] + d_acc[i];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
// end myFunc2
```

There are other ways to optimize this example. For instance, the clipping operation in kernel3 can be merged into the computation of kernel1 as shown below. This is kernel fusion and has the added advantage of not launching a third kernel. The SYCL compiler cannot do this kind of optimization. In some specific domains like machine learning, there are graph compilers that operate on the ML models and fuse the operations, which has the same impact.

```cpp
double myFunc3(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;
    AlignedVector<int> sum(a.size(), alloc);

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()};
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);
    sycl::buffer sum_buf(sum.data(), num_items, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
```

```cpp
// Output accessor
sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

h.parallel_for(num_items, [=](auto i) {
    int t = a_acc[i] + b_acc[i];
    if (t > 10)
        sum_acc[i] = 1;
    else
        sum_acc[i] = 0;
});
});

// kernel2
q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor sum_acc(sum_buf, h, sycl::read_only);
    sycl::accessor c_acc(c_buf, h, sycl::read_only);
    sycl::accessor d_acc(d_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items, [=](auto i) {
        res_acc[i] = sum_acc[i] * c_acc[i] + d_acc[i];
    });
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
// end myFunc3
```

We can take this kernel fusion one level further and fuse both kernel1 and kernel2 as shown in the code below. This gives very good performance since it avoids the intermediate accum\_buf completely, saving memory in addition to launching an additional kernel. Most of the performance benefit in this case is due to improvement in locality of memory references.

```cpp
double myFunc4(sycl::queue &q, AlignedVector<int> &a, AlignedVector<int> &b,
        AlignedVector<int> &res, int iter) {
    sycl::range num_items{a.size()};
    VectorAllocator<int> alloc;

    const sycl::property_list props = {sycl::property::buffer::use_host_ptr()}  
    sycl::buffer a_buf(a, props);
    sycl::buffer b_buf(b, props);
    sycl::buffer c_buf(b, props);
    sycl::buffer d_buf(b, props);
    sycl::buffer res_buf(res, props);

    Timer timer;
    for (int i = 0; i < iter; i++) {
        // kernel1
        q.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a_buf, h, sycl::read_only);
            sycl::accessor b_acc(b_buf, h, sycl::read_only);
            sycl::accessor c_acc(c_buf, h, sycl::read_only);
            sycl::accessor d_acc(d_buf, h, sycl::read_only);
            // Output accessor
            sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);
```

```javascript
h.parallel_for(num_items, [=](auto i) {
    int t = a_acc[i] + b_acc[i];
    if (t > 10)
        res_acc[i] = c_acc[i] + d_acc[i];
    else
        res_acc[i] = d_acc[i];
});
});
q.wait();
}
double elapsed = timer.Elapsed() / iter;
return (elapsed);
} // end myFunc4
```

## Optimizing Data Transfers
