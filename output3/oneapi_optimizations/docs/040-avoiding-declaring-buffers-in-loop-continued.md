
1. sycl\_ext\_oneapi\_copy\_optimize

2. Intel Compiler Extension Routines to OpenMP (C/C++)

3. Environment Variables — oneAPI DPC++ Compiler Documentation

## Avoiding Declaring Buffers in a Loop

When kernels are repeatedly launched inside a for-loop, you can prevent repeated allocation and freeing of a buffer by declaring the buffer outside the loop. Declaring a buffer inside the loop introduces repeated hostto-device and device-to-host memory copies.

In the following example, the kernel is repeatedly launched inside a for-loop. The buffer C is used as a temporary array, where it is used to hold values in an iteration, and the values assigned in one iteration are not used in any other iteration. Since the buffer C is declared inside the for-loop, it is allocated and freed in every loop iteration. In addition to the allocation and freeing of the buffer, the memory associated with the buffer is redundantly transferred from host to device and device to host in each iteration.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 25;
constexpr int STEPS = 100000;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

    // Create 2 buffers, each holding N integers
    sycl::buffer<int> ABuf(&AData[0], N);
    sycl::buffer<int> BBuf(&BData[0], N);

    Q.submit([&](auto &h) {
        // Create device accessors.
        // The property no_init lets the runtime know that the
        // previous contents of the buffer can be discarded.
        sycl::accessor aA(ABuf, h, sycl::write_only, sycl::no_init);
        sycl::accessor aB(BBuf, h, sycl::write_only, sycl::no_init);
        h.parallel_for(N, [=](auto i) {
```

```cpp
aA[i] = 10;
aB[i] = 20;
});
});

for (int j = 0; j < STEPS; j++) {
    sycl::buffer<int> CBuf(&CData[0], N);
    Q.submit([&](auto &h) {
        // Create device accessors.
        sycl::accessor aA(ABuf, h);
        sycl::accessor aB(BBuf, h);
        sycl::accessor aC(CBuf, h);
        h.parallel_for(N, [=](auto i) {
            aC[i] = (aA[i] < aB[i]) ? -1 : 1;
            aA[i] += aC[i];
            aB[i] -= aC[i];
        });
    });
} // end for

// Create host accessors.
const sycl::host_accessor haA(ABuf);
const sycl::host_accessor haB(BBuf);
printf("%d %d\n", haA[N / 2], haB[N / 2]);

return 0;
}
```

A better approach would be to declare the buffer C before the for-loop, so that it is allocated and freed only once, resulting in improved performance by avoiding the redundant data transfers between host and device. The following kernel shows this change.

```cpp
#include <stdio.h>
#include <sycl/sycl.hpp>

constexpr int N = 25;
constexpr int STEPS = 100000;

int main() {

    int AData[N];
    int BData[N];
    int CData[N];

    sycl::queue Q;

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
        h.parallel_for(N, [=](auto i) {
            aA[i] = 10;
```

```cpp
aB[i] = 20;
});
});

for (int j = 0; j < STEPS; j++) {
    Q.submit([&](auto &h) {
        // Create device accessors.
        sycl::accessor aA(ABuf, h);
        sycl::accessor aB(BBuf, h);
        sycl::accessor aC(CBuf, h);
        h.parallel_for(N, [=](auto i) {
            aC[i] = (aA[i] < aB[i]) ? -1 : 1;
            aA[i] += aC[i];
            aB[i] -= aC[i];
        });
    });
} // end for

// Create host accessors.
const sycl::host_accessor haA(ABuf);
const sycl::host_accessor haB(BBuf);
printf("%d %d\n", haA[N / 2], haB[N / 2]);

return 0;
}
```
