Specifying read\_ony accessor mode, instead of read\_write, is especially useful when kernels are repeatedly launched inside a for-loop. If the access mode is read\_write, the kernels launched will be serialized, because one kernel should finish its computation and the data should be ready before the next kernel can be launched. On the other hand, if the access mode is read\_only, then the runtime can launch the kernels in parallel.

Note that the buffer declarations and kernels are launched inside a block. This will cause the buffers to go out of scope at the end of first kernel completion. This will trigger a copy of the contents from the device to the host. The second kernel is inside another block where new buffers are declared to the same memory and this will trigger a copy of this same memory again from the host to the device. This back-and-forth between host and device can be avoided by declaring the buffers once, ensuring that they are in scope during the lifetime of the memory pointed to by these buffers. A better way to write the code that avoids these unnecessary memory transfers is shown below.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Create 3 buffers, each holding N integers
    sycl::buffer<int> ABuf(&AData[0], N);
    sycl::buffer<int> BBuf(&BData[0], N);
    sycl::buffer<int> CBuf(&CData[0], N);

    // Kernel1
    Q.submit([&](auto &h) {
        // Create device accessors.
        // The property no_init lets the runtime know that the
        // previous contents of the buffer can be discarded.
        sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
        sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
        sycl::accessor aC(CBuf, h, sycl::write_only, sycl::no_init);

        h.parallel_for(N, [=](auto i) {
            aA[i] = 11;
            aB[i] = 22;
            aC[i] = 0;
        });
    });

    // Kernel2
    Q.submit([&](auto &h) {
        // Create device sycl::accessors
        sycl::accessor aA(ABuf, h, sycl::read_only);
```

```cpp
sycl::accessor aB(BBuf, h, sycl::read_only);
    sycl::accessor aC(CBuf, h);
    h.parallel_for(N, [=](auto i) { aC[i] += aA[i] + aB[i]; });
});

// The host accessor creation will ensure that a wait for kernel to finish
// is triggered and data from device to host is copied
sycl::host_accessor h_acc(CBuf);
for (int i = 0; i < N; i++) {
    printf("%d\n", h_acc[i]);
}

return 0;
}
```

The following example shows another way to run the same code with different scope blocking. In this case, there will not be a copy of buffers from host to device at the end of kernel1 and from host to device at the beginning of kernel2. The copy of all three buffers happens at the end of kernel2 when these buffers go out of scope.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    {
        // Create 3 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);
        sycl::buffer<int> CBuf(&CData[0], N);

        // Kernel1
        Q.submit([&](auto &h) {
            // Create device accessors.
            // The property no_init lets the runtime know that the
            // previous contents of the buffer can be discarded.
            sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aC(CBuf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(N, [=](auto i) {
                aA[i] = 11;
                aB[i] = 22;
                aC[i] = 0;
            });
        });

        // Kernel2
        Q.submit([&](auto &h) {
            // Create device accessors
            sycl::accessor aA(ABuf, h, sycl::read_only);
```

```cpp
sycl::accessor aB(BBuf, h, sycl::read_only);
    sycl::accessor aC(CBuf, h);
    h.parallel_for(N, [=](auto i) { aC[i] += aA[i] + aB[i]; });
});
}
// Since the buffers are going out of scope, they will have to be
// copied back from device to host and this will require a wait for
// all the kernels to finish and so no explicit wait is needed
for (int i = 0; i < N; i++) {
    printf("%d\n", CData[i]);
}

return 0;
}
```

There is another way to write the kernel where a copy of the read-only variable on the host can be accessed on the device as part of variable capture in the lambda function defining the kernel, as shown below. The issue with this is that for every kernel invocation the data associated with vectors AData and BData have to be copied to the device.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;
constexpr int iters = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;
    sycl::buffer<int> CBuf(&CData[0], N);

    {
        // Create 2 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);

        // Kernel1
        Q.submit([&](auto &h) {
            // Create device accessors.
            // The property no_init lets the runtime know that the
            // previous contents of the buffer can be discarded.
            sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aC(CBuf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(N, [=](auto i) {
                aA[i] = 11;
                aB[i] = 22;
                aC[i] = 0;
            });
        });
    }

    for (int it = 0; it < iters; it++) {
        // Kernel2
```

```cpp
Q.submit([&](auto &h) {
    // Create device accessors
    sycl::accessor aC(CBuf, h);
    h.parallel_for(N, [=](auto i) { aC[i] += AData[i] + BData[i]; });
});
}

sycl::host_accessor h_acc(CBuf);
for (int i = 0; i < N; i++) {
    printf("%d\n", h_acc[i]);
}

return 0;
}
```

It is better to use a buffer and a read-only accessor to that buffer so that the vector is copied from host to device only once. In the following kernel, access to memory AData and BData is made through the ABuf and Bbuf on lines 38 and 39 and the declaration in lines 44 and 45 makes them read-only, which prevents them from being copied back to the host from the device when they go out of scope.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;
constexpr int iters = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;
    sycl::buffer<int> CBuf(&CData[0], N);

    {
        // Create 2 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);

        // Kernel1
        Q.submit([&](auto &h) {
            // Create device accessors.
            // The property no_init lets the runtime know that the
            // previous contents of the buffer can be discarded.
            sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
            sycl::accessor aC(CBuf, h, sycl::write_only, sycl::no_init);

            h.parallel_for(N, [=](auto i) {
                aA[i] = 11;
                aB[i] = 22;
                aC[i] = 0;
            });
        });
    }

    sycl::buffer<int> ABuf(&AData[0], N);
    sycl::buffer<int> BBuf(&BData[0], N);
```

```cpp
for (int it = 0; it < iters; it++) {
    // Kernel2
    Q.submit([&](auto &h) {
        // Create device accessors
        sycl::accessor aA(ABuf, h, sycl::read_only);
        sycl::accessor aB(BBuf, h, sycl::read_only);
        sycl::accessor aC(CBuf, h);
        h.parallel_for(N, [=](auto i) { aC[i] += aA[i] + aB[i]; });
    });
}

sycl::host_accessor h_acc(CBuf);
for (int i = 0; i < N; i++) {
    printf("%d\n", h_acc[i]);
}

return 0;
}
```

## Host/Device Coordination

Significant computation and communication resources exist between the host and accelerator devices, and care must be taken to ensure that they are effectively utilized.

In this section, we cover topics related to the coordination of host and accelerator processing.

• Asynchronous and Overlapping Data Transfers Between Host and Device

## Asynchronous and Overlapping Data Transfers Between Host and Device

An accelerator is a separate device from the host CPU and is attached with some form of bus, like PCIe\* or CXL\*. This bus, depending on its type, has a certain bandwidth through which the host and devices can transfer data. An accelerator needs some data from host to do computation, and overall performance of the system is dependent on how quickly this transfer can happen.

## Bandwidth Between Host and Device

Most current accelerators are connected to the host system through PCIe. Different generations of PCIe have increased the bandwidth over time, as shown in the table below.

PCIe bandwidth by generation

<table><tr><td>PCIe Version</td><td>Transfer Rate</td><td>Throughput</td></tr><tr><td>1.0</td><td>2.5 GT/s</td><td>0.250 GB/s</td></tr><tr><td>2.0</td><td>5.0 GT/s</td><td>0.500 GB/s</td></tr><tr><td>3.0</td><td>8.0 GT/s</td><td>0.985 GB/s</td></tr><tr><td>4.0</td><td>16.0 GT/s</td><td>1.969 GB/s</td></tr><tr><td>5.0</td><td>32.0 GT/s</td><td>3.938 GB/s</td></tr></table>

The local memory bandwidth of an accelerator is an order of magnitude higher than host-to-device bandwidth over a link like PCIe. For instance, HBM (High Bandwidth Memory) on modern GPUs can reach up to 900 GB/sec of bandwidth compared to an x16 PCIe, which can get 63 GB/s. So it is imperative to keep data in local memory and avoid data transfer from host to device or device to host as much as possible. This means that it is better to execute all the kernels on the accelerator to avoid data movement between accelerators or between host and accelerator even it means some kernels are not very efficiently executed on these accelerators.

Any intermediate data structures should be created and used on the device, as opposed to creating them on the host and moving them back and forth between host and accelerator. This is illustrated by the kernels shown here for reduction operations, where the intermediate results are created only on the device and never on the host. In kernel ComputeParallel1, a temporary accumulator is created on the host and all work-items put their intermediate results in it. This accumulator is brought back to the host and then further reduced (at line 37).

```cpp
float ComputeParallel1(sycl::queue &q, std::vector<float> &data) {
    const size_t data_size = data.size();
    float sum = 0;
    static float *accum = 0;

    if (data_size > 0) {
        const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
        int num_EUs =
            q.get_device().get_info<sycl::info::device::max_compute_units>();
        int vec_size =
            q.get_device()
                .get_info<sycl::info::device::native_vector_width_float>();
        int num_processing_elements = num_EUs * vec_size;
        int BATCH = (N + num_processing_elements - 1) / num_processing_elements;
        sycl::buffer<float> buf(data.data(), data.size(), props);
        sycl::buffer<float> accum_buf(accum, num_processing_elements, props);

        if (!accum)
            accum = new float[num_processing_elements];

        q.submit([&](auto &h) {
            sycl::accessor buf_acc(buf, h, sycl::read_only);
            sycl::accessor accum_acc(accum_buf, h, sycl::write_only, sycl::no_init);
            h.parallel_for(num_processing_elements, [=](auto index) {
                size_t glob_id = index[0];
                size_t start = glob_id * BATCH;
                size_t end = (glob_id + 1) * BATCH;
                if (end > N)
                    end = N;
                float sum = 0.0;
                for (size_t i = start; i < end; i++)
                    sum += buf_acc[i];
                accum_acc[glob_id] = sum;
            });
        });
        q.wait();
        sycl::host_accessor h_acc(accum_buf);
        for (int i = 0; i < num_processing_elements; i++)
            sum += h_acc[i];
    }
    return sum;
} // end ComputeParallel1
```

An alternative approach is to keep this temporary accumulator on the accelerator and launch another kernel with only one work-item, which will perform this final reduction operation on the device as shown in the following ComputeParallel2 kernel on line 36. Note that this kernel does not have much parallelism and so it is executed by just one work-item. On some platforms this might be better than transferring the data back to the host and doing the reduction there.

```cpp
float ComputeParallel2(sycl::queue &q, std::vector<float> &data) {
  const size_t data_size = data.size();
  float sum = 0;
  static float *accum = 0;

  if (data_size > 0) {
    const sycl::property_list props = {sycl::property::buffer::use_host_ptr() };
    int num_EUs =
      q.get_device().get_info<sycl::info::device::max_compute_units>();
    int vec_size =
      q.get_device()
        .get_info<sycl::info::device::native_vector_width_float>();
    int num_processing_elements = num_EUs * vec_size;
    int BATCH = (N + num_processing_elements - 1) / num_processing_elements;
    if (!accum)
      accum = new float[num_processing_elements];
    sycl::buffer<float> buf(data.data(), data.size(), props);
    sycl::buffer<float> accum_buf(accum, num_processing_elements, props);
    sycl::buffer<float> res_buf(&sum, 1, props);

    q.submit([&](auto &h) {
      sycl::accessor buf_acc(buf, h, sycl::read_only);
      sycl::accessor accum_acc(accum_buf, h, sycl::write_only, sycl::no_init);
      h.parallel_for(num_processing_elements, [=](auto index) {
        size_t glob_id = index[0];
        size_t start = glob_id * BATCH;
        size_t end = (glob_id + 1) * BATCH;
        if (end > N)
          end = N;
        float sum = 0.0;
        for (size_t i = start; i < end; i++)
          sum += buf_acc[i];
        accum_acc[glob_id] = sum;
      });
    });

    q.submit([&](auto &h) {
      sycl::accessor accum_acc(accum_buf, h, sycl::read_only);
      sycl::accessor res_acc(res_buf, h, sycl::write_only, sycl::no_init);
      h.parallel_for(1, [=](auto index) {
        res_acc[index] = 0;
        for (int i = 0; i < num_processing_elements; i++)
          res_acc[index] += accum_acc[i];
      });
    });
  }
  // Buffers go out of scope and data gets transferred from device to host return sum;
} // end ComputeParallel2
```

## Overlapping Data Transfer from Host to Device with Computation on Device

Some GPUs provide specialized engines for copying data from host to device. Effective utilization of them will ensure that the host-to-device data transfer can be overlapped with execution on the device. In the following example, a block of memory is divided into chunks and each chunk is transferred to the accelerator (line 57), processed (line 60), and the result (line 63) is brought back to the host. These chunks of three tasks are independent, so they can be processed in parallel depending on availability of hardware resources. In systems where there are copy engines that can be used to transfer data between host and device, we can see that the operations from different loop iterations can execute in parallel. The parallel execution can manifest in two ways:

• Between two memory copies, where one is executed by the GPU Vector Engines and one by a copy engine, or both are executed by copy engines.

• Between a memory copy and a compute kernel, where the memory copy is executed by the copy engine and the compute kernel by the GPU Vector Engines.

```cpp
#include <sycl/sycl.hpp>

#define NITERS 10
#define KERNEL_ITERS 10000
#define NUM_CHUNKS 10
#define CHUNK_SIZE 10000000

class Timer {
public:
    Timer() : start_(std::chrono::steady_clock::now()) {}

    double Elapsed() {
        auto now = std::chrono::steady_clock::now();
        return std::chrono::duration_cast<Duration>(now - start_).count();
    }

private:
    using Duration = std::chrono::duration<double>;
    std::chrono::steady_clock::time_point start_;
};

int main() {
    const int num_chunks = NUM_CHUNKS;
    const int chunk_size = CHUNK_SIZE;
    const int iter = NITERS;

    sycl::queue q;

    // Allocate and initialize host data
    float *host_data[num_chunks];
    for (int c = 0; c < num_chunks; c++) {
        host_data[c] = sycl::malloc_host<float>(chunk_size, q);
        float val = c;
        for (int i = 0; i < chunk_size; i++)
            host_data[c][i] = val;
    }
    std::cout << "Allocated host data\n";

    // Allocate and initialize device memory
    float *device_data[num_chunks];
    for (int c = 0; c < num_chunks; c++) {
        device_data[c] = sycl::malloc_device<float>(chunk_size, q);
        float val = 1000.0;
```

```cpp
q.fill<float>(device_data[c], val, chunk_size);
}
q.wait();
std::cout << "Allocated device data\n";

Timer timer;
for (int it = 0; it < iter; it++) {
    for (int c = 0; c < num_chunks; c++) {
        auto add_one = [=](auto id) {
            for (int i = 0; i < KERNEL_ITERS; i++)
                device_data[c][id] += 1.0;
        };
        // Copy-in not dependent on previous event
        auto copy_in =
            q.memcpy(device_data[c], host_data[c], sizeof(float) * chunk_size);
        // Compute waits for copy_in
        auto compute = q.parallel_for(chunk_size, copy_in, add_one);
        auto cg = [=](auto &h) {
            h.depends_on(compute);
            h.memcpy(host_data[c], device_data[c], sizeof(float) * chunk_size);
        };
        // Copy out waits for compute
        auto copy_out = q.submit(cg);
    }

    q.wait();
}
auto elapsed = timer.Elapsed() / iter;
for (int c = 0; c < num_chunks; c++) {
    for (int i = 0; i < chunk_size; i++) {
        if (host_data[c][i] != (float)((c + KERNEL_ITERS * iter))) {
            std::cout << "Mismatch for chunk: " << c << " position: " << i
                << " expected: " << c + 10000 << " got: " << host_data[c][i]
                << "\n";
            break;
        }
    }
}
std::cout << "Time = " << elapsed << " usecs\n";
}
```

In the timeline picture below, which is collected using onetrace, we can see that copy-ins from upcoming iterations overlap with the execution of compute kernel. Also, we see multiple copy-ins executing in parallel on multiple copy engines.

## Copy Overlaps with Compute Kernel Execution

![](images/5d6eab966ea8f26d92d19941ef4225298c369d7071b8c49282a28c270e0720e3.jpg)  
In the example above, we cannot have two kernels (even though they are independent) executing concurrently because we only have one GPU. (It is possible to partition the GPU into smaller chunks and execute different kernels concurrently on them.)

## Using Multiple Heterogeneous Devices

Most accelerators reside in a server that has a significant amount of compute resources in it. For instance, a typical server can have up to eight sockets, with each socket containing over 50 cores. SYCL provides the ability to treat the CPUs and the accelerators uniformly to distribute work among them. It is the responsibility of the programmer to ensure a balanced distribution of work among the heterogeneous compute resources in the platform.

## Overlapping Compute on Various Devices

SYCL provides access to different kinds of devices through abstraction of device selectors. Queues can be created for each of the devices, and kernels can be submitted to them for execution. All kernel submits in SYCL are non-blocking, which means that once the kernel is submitted to a queue for execution, the host does not wait for it to finish unless waiting on the queue is explicitly requested. This allows the host to do some work itself or initiate work on other devices while the kernel is executing on the accelerator.

The host CPU can be treated as an accelerator and the SYCL can submit kernels to it for execution. This is completely independent and orthogonal to the job done by the host to orchestrate the kernel submission and creation. The underlying operating system manages the kernels submitted to the CPU accelerator as another process and uses the same openCL/Level0 runtime mechanisms to exchange information with the host device.

The following example shows a simple vector add operation that works on a single GPU device.

```cpp
size_t VectorAdd1(sycl::queue &q, const IntArray &a, const IntArray &b,
            IntArray &sum, int iter) {
    sycl::range num_items{a.size()};

    sycl::buffer a_buf(a);
    sycl::buffer b_buf(b);
    sycl::buffer sum_buf(sum.data(), num_items);
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < iter; i++) {
```

```cpp
auto e = q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items,
            [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
});
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add1 completed on device - took "
        << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd1
```

In the following kernel the input vector is split into two parts and computation is done on two different accelerators (one CPU and one GPU) that can execute concurrently. Care must be taken to ensure that the kernels, in addition to be being submitted, are actually launched on the devices to get this parallelism. The actual time that a kernel is launched can be substantially later than when it was submitted by the host. The implementation decides the time to launch the kernels based on some heuristics to maximize metrics like utilization, throughput, or latency. For instance, in the case of the OpenCL backend, on certain platforms one needs to explicitly issue a clFlush (as shown on line 41) on the queue to launch the kernels on the accelerators.

```cpp
size_t VectorAdd2(sycl::queue &q1, sycl::queue &q2, const IntArray &a,
                    const IntArray &b, IntArray &sum, int iter) {
    sycl::range num_items{a.size() / 2};

    auto start = std::chrono::steady_clock::now();
    {
        sycl::buffer a1_buf(a.data(), num_items);
        sycl::buffer b1_buf(b.data(), num_items);
        sycl::buffer sum1_buf(sum.data(), num_items);

        sycl::buffer a2_buf(a.data() + a.size() / 2, num_items);
        sycl::buffer b2_buf(b.data() + a.size() / 2, num_items);
        sycl::buffer sum2_buf(sum.data() + a.size() / 2, num_items);
        for (int i = 0; i < iter; i++) {

            q1.submit([&](auto &h) {
                // Input accessors
                sycl::accessor a_acc(a1_buf, h, sycl::read_only);
                sycl::accessor b_acc(b1_buf, h, sycl::read_only);
                // Output accessor
                sycl::accessor sum_acc(sum1_buf, h, sycl::write_only, sycl::no_init);

                h.parallel_for(num_items,
                    [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
            });
        // do the work on host
        q2.submit([&](auto &h) {
            // Input accessors
            sycl::accessor a_acc(a2_buf, h, sycl::read_only);
            sycl::accessor b_acc(b2_buf, h, sycl::read_only);
            // Output accessor
```

```cpp
sycl::accessor sum_acc(sum2_buf, h, sycl::write_only, sycl::no_init);

h.parallel_for(num_items,
            [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
    });
}
// On some platforms this explicit flush of queues is needed
// to ensure the overlap in execution between the CPU and GPU
// cl_command_queue cq = q1.get();
// clFlush(cq);
// cq=q2.get();
// clFlush(cq);
}
q1.wait();
q2.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector add2 completed on device - took "
          << (end - start).count() << " u-secs\n";
return ((end - start).count());
} // end VectorAdd2
```

Checking the running time of the above two kernels, it can be seen that the application runs almost twice as fast as before since it has more hardware resources dedicated to solving the problem. In order to achieve good balance, you will have to split the work in proportion to the capability of the accelerator, instead of distributing it evenly as was done in the above example.
