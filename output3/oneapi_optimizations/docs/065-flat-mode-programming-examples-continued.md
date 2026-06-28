## FLAT Mode Programming

As mentioned previously, the FLAT mode is the default mode on Intel<sup>®</sup> Data Center GPU Max Series. In FLAT mode, each stack is exposed as a root device. In this section, we present SYCL and OpenMP examples to demonstrate offloading in FLAT mode.

## Memory in FLAT Mode

Each stack has its own memory. A kernel offloaded to a stack will run on that stack and use the memory allocated on that stack.

A kernel running on a stack can access memory on other stacks in the same GPU card. However, accessing memory on a stack other than the stack it is running on will be slower.

• FLAT Mode Example - SYCL

• FLAT Mode Example - OpenMP

## FLAT Mode Example - SYCL

In this section, we use a simple vector addition example to show how to scale the performance using multiple devices in FLAT mode.

## Offloading to a single device (stack)

A first look at adding 2 vectors using one device or stack:

```txt
float *da;
    float *db;
    float *dc;
```

```cpp
da = (float *)sycl::malloc_device<float>(gsize, q);
db = (float *)sycl::malloc_device<float>(gsize, q);
dc = (float *)sycl::malloc_device<float>(gsize, q);
q.memcpy(da, ha, gsize);
q.memcpy(db, hb, gsize);

q.wait();

std::cout << "Offloading work to 1 device" << std::endl;

for (int i = 0; i < 16; i ++) {
    q.parallel_for(sycl::nd_range<1>(gsize, 1024),[=](auto idx) {
        int ind = idx.get_global_id();
        dc[ind] = da[ind] + db[ind];
    });
}

q.wait();

std::cout << "Offloaded work completed" << std::endl;

q.memcpy(hc, dc, gsize);
```

The above example adds two float vectors ha and hb and then saves the result in vector hc\`.

The example first allocates device memory for the 3 vectors, then copies the data from the host to the device before launching the kernels on the device to do vector addition. After the computation on the device completes, the result in vector dc on the device is copied to the vector hc on the host.

## Compilation and run commands:

```shell
$ icpx -fsycl flat_sycl_vec_add_single_device.cpp -o flat_sycl_vec_add_single_device
$ ./flat_sycl_vec_add_single_device
```

## Offloading to multiple devices (stacks)

We can scale up the performance of the above example if multiple devices are available.

The following example starts with enumerating all devices on the platform to make sure that at least 2 devices are available.

```cpp
auto plat = sycl::platform(sycl::gpu_selector_v);
auto devs = plat.get_devices();
auto ctxt = sycl::context(devs);

if (devs.size() < 2) {
    std::cerr << "No 2 GPU devices found" << std::endl;
    return -1;
}

std::cout << devs.size() << " GPU devices are found and 2 will be used" << std::endl;
sycl::queue q[2];
q[0] = sycl::queue(ctxt, devs[0], {sycl::property::queue::in_order()});
q[1] = sycl::queue(ctxt, devs[1], {sycl::property::queue::in_order()});
```

Next, the example allocates the vectors ha and hb on the host and partitions each vector into 2 parts. Then the first halves of the vectors ha and hb are copied to the first device, and the second halves are copied to the second device.

```lisp
constexpr size_t gsize = 1024 * 1024 * 1024L;
float *ha = (float *)(malloc(gsize * sizeof(float)));
float *hb = (float *)(malloc(gsize * sizeof(float)));
```

```c
float *hc = (float *)(malloc(gsize * sizeof(float)));

for (size_t i = 0; i < gsize; i++) {
    ha[i] = float(i);
    hb[i] = float(i + gsize);
}

float *da[2];
float *db[2];
float *dc[2];

size_t lsize = gsize / 2;

da[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
db[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
dc[0] = (float *)sycl::malloc_device<float>(lsize, q[0]);
q[0].memcpy(da[0], ha, lsize);
q[0].memcpy(db[0], hb, lsize);

da[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
db[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
dc[1] = (float *)sycl::malloc_device<float)((lsize + gsize % 2), q[1]);
q[1].memcpy(da[1], ha + lsize, lsize + gsize % 2);
q[1].memcpy(db[1], hb + lsize, lsize + gsize % 2);

q[0].wait();
q[1].wait();
```

Once the data is available on the two devices, the vector addition kernels are launched on each device and the devices execute the kernels in parallel. After the computations on both devices complete, the results are copied from both the devices to the host.

```cpp
for (int i = 0; i < 16; i ++) {
    q[0].parallel_for(sycl::nd_range<1>(lsize, 1024), [=] (auto idx) {
        int ind = idx.get_global_id();
        dc[0][ind] = da[0][ind] + db[0][ind];
    });
    q[1].parallel_for(sycl::nd_range<1>(lsize + gsize % 2, 1024), [=] (auto idx) {
        int ind = idx.get_global_id();
        dc[1][ind] = da[1][ind] + db[1][ind];
    });
}

q[0].wait();
q[1].wait();

std::cout << "Offloaded work completed" << std::endl;

q[0].memcpy(hc, dc[0], lsize);
q[1].memcpy(hc + lsize, dc[1], lsize + gsize % 2);

q[0].wait();
q[1].wait();
```

Compilation and run commands:

```shell
$ icpx -fsycl flat_sycl_vec_add.cpp -o flat_sycl_vec_add
$ ./flat_sycl_vec_add
```

Note that this example uses 2 devices. It can easily be extended to use more than 2 devices if more than 2 devices are available. We leave this as an exercise.

## FLAT Mode Example - OpenMP

As previously mentioned, in FLAT mode, the stacks are exposed as devices.

Offloading to a single device (stack)

In this scheme, the default root device which is device 0 is used to offload. See code example below:

```c
int device_id = omp_get_default_device();

#pragma omp target teams distribute parallel for device(device_id) map(...)
for (int i = 0, i < N; i++) {
    ...
}
```

## Offloading to multiple devices (stacks)

In this scheme, we have multiple root devices (stacks) on which the code will run; the stacks may belong to one or more GPU cards. See code example below:

```txt
int num_devices = omp_get_num_devices();

#pragma omp parallel for
for (int device_id = 0; device_id < num_devices; device_id++) {

    #pragma omp target teams distribute parallel for device(device_id) map(...)
    for (int i = lb(device_id); I < ub(device_id); i++) {
        ...
    }
}
```

We present below a full OpenMP program that offloads to multiple devices (stacks) in FLAT mode.

## OpenMP Example

In the following program, flat\_openmp\_01.cpp, the array A is initialized on the device. First, we determine the number of devices (stacks) available, and then use the devices (stacks) to initialize different chunks of the array. The OpenMP device clause on the target pragma is used to specify which stack to use for a particular chunk. (If no device clause is specified, then the code will run on stack 0.)

omp\_get\_num\_devices() returns the total number of devices (stacks) that are available. For example, on a 4-card system with 2 stacks each, the routine will return 8.

```c
#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

#define SIZE 320

int num_devices = omp_get_num_devices();
int chunksize = SIZE/num_devices;

int main(void)
{
    int *A;
    A = new int[sizeof(int) * SIZE];

    printf ("num_devices = %d\n", num_devices);
```

```c
for (int i = 0; i < SIZE; i++)
    A[i] = -9;

#pragma omp parallel for
for (int id = 0; id < num_devices; id++) {
    #pragma omp target teams distribute parallel for device(id) \
        map(tofrom: A[id * chunksize : chunksize])
    for (int i = id * chunksize; i < (id + 1) * chunksize; i++) {
        A[i] = i;
    }
}

for (int i = 0; i < SIZE; i++)
    if (A[i] != i)
        printf ("Error in: %d\n", A[i]);
    else
        printf ("%d\n", A[i]);
```

Compilation command:

```shell
\$ icpx -fiopenmp -fopenmp-targets=spir64 flat_openmp_01.cpp
```

## Run command:

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY ./a.out
```

## Notes:

• OMP\_TARGET\_OFFLOAD=MANDATORY is used to make sure that the target region will run on the GPU. The program will fail if a GPU is not found.

• There is no need to specify ZE\_FLAT\_DEVICE\_HIERARCHY=FLAT with the run command, since FLAT mode is the default.

Running on a system with a single GPU card (2 stacks in total):

sycl-ls shows that there are 2 devices (corresponding to the 2 stacks):

```txt
\$ sycl-ls
[level_zero:gpu][level_zero:0] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:1] ... Intel(R) Data Center GPU Max 1550 1.3
[opencl:gpu][opencl:0] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:1] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
```

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 2 devices (corresponding to the 2 stacks) have been found.

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 2 root devices, 2 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0
Target LEVEL_ZERO RTL --> -- 1
```

Running on a system with 4 GPU cards (8 stacks in total)

sycl-ls shows that there are 8 devices (corresponding to the 8 stacks):

```txt
\$ sycl-ls
[level_zero:gpu][level_zero:0] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:1] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:2] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:3] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:4] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:5] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:6] ... Intel(R) Data Center GPU Max 1550 1.3
[level_zero:gpu][level_zero:7] ... Intel(R) Data Center GPU Max 1550 1.3
[opencl:gpu][opencl:0] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:1] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:2] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:3] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:4] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:5] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:6] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
[opencl:gpu][opencl:7] ... Intel(R) Data Center GPU Max 1550 OpenCL 3.0 NEO
```

We add LIBOMPTARGET\_DEBUG=1 to the run command to get libomptarget.so debug information.

```txt
$ OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_DEBUG=1 ./a.out >& libomptarget_debug.log
```

We see the following in libomptarget\_debug.log, showing that 8 devices (corresponding to the 8 stacks) have been found:

```txt
Target LEVEL_ZERO RTL --> Found a GPU device, Name = Intel(R) Data Center GPU Max 1550
Target LEVEL_ZERO RTL --> Found 8 root devices, 8 total devices.
Target LEVEL_ZERO RTL --> List of devices (DeviceID[.SubID[.CCSID]])
Target LEVEL_ZERO RTL --> -- 0
Target LEVEL_ZERO RTL --> -- 1
Target LEVEL_ZERO RTL --> -- 2
Target LEVEL_ZERO RTL --> -- 3
Target LEVEL_ZERO RTL --> -- 4
Target LEVEL_ZERO RTL --> -- 5
Target LEVEL_ZERO RTL --> -- 6
Target LEVEL_ZERO RTL --> -- 7
```
