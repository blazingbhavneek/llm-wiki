## Buffer Accessor Modes

In SYCL, a buffer provides an abstract view of memory that can be accessed by the host or a device. A buffer cannot be accessed directly through the buffer object. Instead, we must create an accessor object that allows us to access the buffer’s data.

The access mode describes how we intend to use the memory associated with the accessor in the program. The accessor’s access modes are used by the runtime to create an execution order for the kernels and perform data movement. This will ensure that kernels are executed in an order intended by the programmer. Depending on the capabilities of the underlying hardware, the runtime can execute kernels concurrently if the dependencies do not give rise to dependency violations or race conditions.

For better performance, make sure that the access modes of accessors reflect the operations performed by the kernel. The compiler will flag an error when a write is done on an accessor which is declared as read\_only. But the compiler does not change the declaration of an accessor form read\_write to read if no write is done in the kernel.

The following example shows three kernels. The first kernel initializes the A, B, and C buffers, so we specify that the access modes for these buffers is write\_only. The second kernel reads the A and B buffers, and reads and writes the C buffer, so we specify that the access mode for the A and B buffers is read\_only, and the access mode for the C buffer is read\_write.

The read\_only access mode informs the runtime that the data needs to be available on the device before the kernel can begin executing, but the data need not be copied from the device to the host at the end of the computation.

If this second kernel were to use read\_write for A and B instead of read\_only, then the memory associated with A and B is copied from the device to the host at the end of kernel execution, even though the data has not been modified by the device. Moreover, read\_write creates unnecessary dependencies. If another kernel that reads A or B is submitted within this block, this new kernel cannot start until the second kernel has completed.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 100;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Kernel1
    {
        // Create 3 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);
        sycl::buffer<int> CBuf(&CData[0], N);

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
    } // end Kernel1

    // Kernel2
    {
        // Create 3 buffers, each holding N integers
        sycl::buffer<int> ABuf(&AData[0], N);
        sycl::buffer<int> BBuf(&BData[0], N);
        sycl::buffer<int> CBuf(&CData[0], N);

        Q.submit([&](auto &h) {
            // Create device accessors
            sycl::accessor aA(ABuf, h, sycl::read_only);
            sycl::accessor aB(BBuf, h, sycl::read_only);
            sycl::accessor aC(CBuf, h);
            h.parallel_for(N, [=](auto i) { aC[i] += aA[i] + aB[i]; });
        });
    } // end Kernel2

    // Buffers are destroyed and so CData is updated and can be accessed
```

```c
for (int i = 0; i < N; i++) {
    printf("%d\n", CData[i]);
}

return 0;
}
```

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
