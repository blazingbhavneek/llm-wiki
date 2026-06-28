# Backend Interoperability

In this chapter we will learn about backend interoperability, a SYCL feature that can incrementally add SYCL to an application that is already using other data parallel techniques or APIs.

We will also learn how backend interoperability can be used by expert programmers familiar with low-level APIs to “peek behind the curtain” and use underlying data parallel APIs from SYCL programs directly. This provides direct access to API-specific features, when necessary, while retaining the portability and ease-of-use benefits of SYCL otherwise.

## What Is Backend Interoperability?

So far in this book we have referred to SYCL programs running on SYCL devices, but in practice many SYCL implementations build upon lowerlevel APIs such as OpenCL, Level Zero, CUDA, or others to access the parallel hardware in a system. When a SYCL implementation is built upon a lower-level API, we refer to the target API as a SYCL backend. Figure 20-1 shows the relationship between SYCL backends, platforms, and devices. Most SYCL implementations can run SYCL programs on multiple SYCL backends simultaneously to utilize all the parallel hardware in a system.

![](images/35ad5ab35b3289cff4bf75d2d64bb6f2e07c5032e67ae38cecfd069564145b5b.jpg)  
Figure 20-1. Relationship between SYCL backends, platforms, and devices

We can query the SYCL backends in a system by first querying the SYCL platforms and then querying the SYCL backend associated with each platform, as shown in Figure 20-2. The output from this program will depend on the number and type of SYCL devices in a system. If the same device is supported by different SYCL backends, it may enumerate as a SYCL device for each backend.

![](images/0bd2905f5bee855a13f10b18703df88c473c3fc98cec185d8a0fc08166e2c524.jpg)  
Figure 20-2. Querying the SYCL backend for a SYCL platform

The associated backend can be queried for most SYCL objects, not just for SYCL platforms. For example, we can also query the associated backend for a SYCL device, a SYCL context, or a SYCL queue.

Backend interoperability lets us use knowledge of the associated backend to interact with and manipulate underlying native backend objects that represent SYCL objects for the associated backend.

## When Is Backend Interoperability Useful?

Many SYCL programmers will never need to use backend interoperability. In fact, using backend interoperability may be undesirable; backend interoperability will frequently either make a program more complex because it requires multiple code paths for multiple SYCL backends, or it will make a program less portable because it will restrict execution to devices with a single associated backend.

Still, backend interoperability is a useful tool to have in our toolbox to solve some specific problems. In this section we will explore several common use cases where backend interoperability is useful.

## BACKEND INTEROPERABILITY IS LIKE AN INLINE ASSEMBLER

A useful mental model for backend interoperability is that backend interoperability is to SYCL as inline assembler is to C++ host code: backend interoperability is not necessary for learning SYCL or being productive with SYCL, and backend interoperability is often undesirable because it increases complexity or decreases portability. Nevertheless, it is a useful tool to have in our toolbox to solve specific problems.

## Adding SYCL to an Existing Codebase

The SYCL programs in this book are designed to teach specific SYCL concepts so they are intentionally straightforward and short. By contrast, most real-world software is large and complex, consisting of thousands or millions of lines of code, perhaps developed by many people over many years. Even if we wanted to do so, completely rewriting a large application to use SYCL may not be feasible.

One of the key benefits provided by backend interoperability is the ability to incrementally add SYCL to an existing codebase that is already using a low-level API, by creating SYCL objects from native backend objects for that API. For example, let’s say we have a large OpenCL application that creates an OpenCL context and OpenCL memory objects. Backend interoperability has templated functions like make\_context and make\_buffer which let us seamlessly create SYCL objects from these OpenCL objects. After creating SYCL objects from the OpenCL objects, they can be used by SYCL queues and SYCL kernels just like any other SYCL object, as shown in Figure 20-3.

```cpp
// Create SYCL objects from the native backend objects.
context c =
    make_context<backend::opencl>(openclContext);
device d = make_device<backend::opencl>(openclDevice);
buffer data_buf =
    make_buffer<backend::opencl, int>(openclBuffer, c);

// Now use the SYCL objects to create a queue and submit
// a kernel.
queue q{c, d};

q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};
    h.parallel_for(size, [=](id<1> i) {
        data_acc[i] = data_acc[i] + 1;
    });
}).wait();
```

Figure 20-3. Creating SYCL objects from OpenCL objects

The SYCL 2020 specification only defines interoperability with OpenCL backends, but SYCL implementations may provide interoperability with other backends via extensions. Figure 20-4 shows how SYCL objects may be created from Level Zero objects using the sycl\_ext\_oneapi\_backend\_ level\_zero extension.

```cpp
// Create SYCL objects from the native backend objects.
device d = make_device<backend::ext_oneapi_level_zero>(
    level0Device);
context c =
    make_context<backend::ext_oneapi_level_zero>(
        {level0Context,
            {d},
            ext::oneapi::level_zero::ownership::keep});
buffer data_buf =
    make_buffer<backend::ext_oneapi_level_zero, int>(
        {level0Ptr,
            ext::oneapi::level_zero::ownership::keep},
            c);

// Now use the SYCL objects to create a queue and submit
// a kernel.
queue q{c, d};

q.submit([&](handler& h) {
    accessor data_acc{data_buf, h};
    h.parallel_for(size, [=](id<1> i) {
        data_acc[i] = data_acc[i] + 1;
    });
}).wait();
```

## Figure 20-4. Creating SYCL objects from Level Zero objects

Notice that the parameters that are passed to create the SYCL objects are slightly different for the Level Zero backend. This will generally be true for any supported backend interoperability because each backend may require different information to properly create the SYCL object. Otherwise, the same make\_device, make\_context, and make\_buffer functions are used for both OpenCL and Level Zero backend interoperability.

Notice also that ownership is handled differently by each backend. For the OpenCL backend, the SYCL implementation uses the reference counting provided by OpenCL to manage the lifetimes of the native backend objects. For the Level Zero backend, the SYCL implementation must be explicitly told whether it should take ownership of the native backend object, or whether our application will keep ownership. If the SYCL implementation takes ownership of the native backend object, then the native backend object will be destroyed when the SYCL object is destroyed; otherwise, our application is responsible for freeing the native backend object directly.
