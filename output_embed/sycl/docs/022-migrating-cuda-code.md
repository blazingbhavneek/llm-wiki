# Migrating CUDA Code

Many readers of this book have likely encountered data parallel code written in CUDA. Some readers may even be CUDA experts! In this chapter we will describe some of the similarities between CUDA and SYCL, some of the differences, and useful tools and techniques to help migrate CUDA code effectively and efficiently to C++ with SYCL.

## Design Differences Between CUDA and SYCL

Before we dive into the details, it is first instructive to identify key design differences between CUDA and SYCL. This can provide useful background to inform why some differences exist, to understand which differences may disappear in time and which differences are likely to remain.

## Multiple Targets vs. Single Device Targets

One of the biggest design differences between CUDA and SYCL is the universe of devices they are designed to support. CUDA is designed to support GPU devices from a single device vendor, so most CUDA devices look relatively similar. As an example, all CUDA devices currently include texture sampling hardware and all CUDA devices currently support the same maximum work-group size. This reduces complexity, but also reduces where a CUDA application may run.

By contrast, SYCL is designed to support a diverse set of heterogeneous accelerators, including different devices from different device vendors. This flexibility gives SYCL programs the freedom to take advantage of the computing resources in a modern heterogeneous system; however, this flexibility does come at a modest cost. For example, as SYCL programmers we may need to enumerate the devices in the system, examine their properties, and choose which device or devices are best suited to run different parts of our program.

Of course, if our SYCL program does not intend to utilize all the computing resources in our system, various shortcuts exist to reduce code verbosity, such as standard device selectors. Figure 21-1 shows a basic SYCL sample that uses a queue for the default device, chosen by the SYCL implementation.

```cpp
// Declare an in-order SYCL queue for the default device
queue q{property::queue::in_order Little};
std::cout << "Running on device: "
       << q.get_device().get_info<info::device::name>()"
       << "\n";

int* buffer = malloc_host<int>(count, q);
q.fill(buffer, 0, count);

q.parallel_for(count, [=](auto id) {
    buffer[id] = id;
}).wait();
```

## Figure 21-1. Running a kernel on the default SYCL device

This SYCL code is very similar to the equivalent CUDA code, shown in Figure 21-2.

```cpp
CHAPTER 21 MIGRATING CUD

// The CUDA kernel is a separate function
__global__ void TestKernel(int* dst) {
    auto id = blockIdx.x * blockDim.x + threadIdx.x;
    dst[id] = id;
}

int main() {
    // CUDA uses device zero by default
    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, 0);
    std::cout << "Running on device: " << deviceProp.name << "\n";

    int* buffer = nullptr;
    cudaMallocHost(&buffer, count * sizeof(int));
    cudaMemset(buffer, 0, count * sizeof(int));

    TestKernel<<<count / 256, 256>>>(buffer);
    cudaDeviceSynchronize();
    // ...
```  
Figure 21-2. Running a kernel on the default CUDA device

Real-world SYCL code is usually more complicated. For example, many SYCL applications will enumerate and choose a specific device or a combination of devices to run on (refer to Chapter 2) by searching for specific device characteristics (refer to Chapter 12). Concise options exist when this complexity is not needed or desired, though, and SYCL is well designed to support the additional complexity when it is required.

## Aligning to C++ vs. Extending C++

Another important design difference between CUDA and SYCL is how they interact with other programming languages, especially C++. SYCL code is standard C++ code, without any language extensions. By learning to read, understand, and write C++ code, we are also able to read and understand SYCL code. Similarly, if a compiler can parse C++ code, it can also parse SYCL code.

CUDA made a different decision. Instead, CUDA extends C++ by adding new keywords and a special syntax to execute kernels. At times, the language extensions can be more concise, but they are also one more syntax to learn and remember, and the language extensions mean that CUDA code can only be compiled by a CUDA-enabled compiler.

To see this design difference in practice, notice how the SYCL example in Figure 21-1 uses a standard C++ lambda expression to represent the kernel code and a standard C++ function call to submit the kernel for execution. The CUDA example in Figure 21-2 instead uses a special \_global\_\_ keyword to identify the kernel code and a special <<< >>> syntax to submit the kernel for execution.

## Terminology Differences Between CUDA and SYCL

Now that we understand some of the key design differences between SYCL and CUDA we are almost ready to start examining specific similarities and differences. We have one more bit of background to take care of first, though: because CUDA and SYCL often use different terms for similar concepts, we need a decoder so we can meaningfully compare the two APIs, such as the summary in Figure 21-3.

<table><tr><td>Concept</td><td>SYCL Term</td><td>CUDA Term</td></tr><tr><td>A function that is executed in parallel on a device.</td><td>Kernel</td><td>Kernel</td></tr><tr><td>The N-dimensional parallel index space.</td><td>Range (generally), or ND-Range (with grouping)</td><td>Grid (always has grouping)</td></tr><tr><td>A kernel instance executing at a point in the parallel index space.</td><td>Work-Item</td><td>Thread</td></tr><tr><td>An application-defined group of kernel instances in the parallel index space that can communicate and synchronize.</td><td>Work-Group</td><td>Block</td></tr><tr><td>An implementation-defined group of kernel instances with additional communication and synchronization capabilities.</td><td>Sub-Group</td><td>Warp</td></tr><tr><td>Memory used to exchange data among instances in a group.</td><td>Local Memory</td><td>Shared Memory</td></tr><tr><td>Function used to synchronize instances in a group.</td><td>group_barrier()</td><td>__syncthreads(), __syncwarp(), coop_group.sync()</td></tr><tr><td>Object used to execute kernels or other work on a device.</td><td>Queue</td><td>Stream</td></tr></table>

Figure 21-3. CUDA and SYCL decoder ring

Unlike the rest of this book where SYCL terminology was used consistently, this chapter may use the CUDA terms and the SYCL terms interchangeably.

## Similarities and Differences

This section describes some of the syntactic and behavioral similarities between SYCL and CUDA as well as places where SYCL and CUDA differ.

## Execution Model

Fundamentally, both SYCL and CUDA use the same data-parallel kernel execution model introduced in Chapter 4 and described throughout this book. The terminology may be slightly different, for example, SYCL refers to an ND-range and CUDA refers to a grid, but we can use our decoder ring in Figure 21-3 to translate key concepts from SYCL to CUDA and vice versa.

## In-Order vs. Out-of-Order Queues

Despite the many execution model similarities, several differences do exist. One difference is that CUDA streams are unconditionally in-order. This means that any kernel or memory operation submitted to a CUDA stream must complete before the next submitted kernel or memory copy operation can start. SYCL queues instead are out-of-order by default but may optionally be in-order by passing the in\_order queue property when the SYCL queue is created (refer to Chapter 8).

An in-order CUDA stream is simpler because it does not require explicit scheduling or dependence management. This simplicity means that CUDA applications typically do not use mechanisms like accessors or depends\_on to order operations in a stream. The in-order semantics also constrain execution, though, and do not offer any opportunity for overlapping execution of two commands in a single stream. Because a CUDA application cannot overlap execution of two commands in a single stream, when a CUDA application would like to (potentially) execute commands simultaneously, it will submit the commands to different CUDA streams, because commands in different CUDA streams may execute simultaneously.

This same pattern of submitting to multiple in-order queues to potentially execute kernels or memory operations simultaneously works in SYCL also, and many SYCL implementations and SYCL devices are

optimized to handle this case. Out-of-order SYCL queues provide an alternative mechanism to overlap execution with just a single queue, though, and many SYCL implementations and SYCL devices are optimized to handle this case as well.

Ultimately, whether to use multiple in-order SYCL queues or fewer out-of-order SYCL queues is a matter of personal preference and programming style, and we can choose whichever option makes the most sense for our SYCL programs. The SYCL examples in this chapter create in-order SYCL queues to stay as close to the equivalent CUDA examples as possible.

## Contiguous Dimension

Another difference that is likely to confuse novice and expert CUDA programmers alike concerns multidimensional SYCL ranges or CUDA grids: SYCL aligns its convention with multidimensional arrays in standard C++, so the last dimension is the contiguous dimension, also known as the unit-stride dimension or the fastest moving dimension. CUDA instead aligns to graphics conventions, so the first dimension is the contiguous dimension. Because of this difference, multidimensional SYCL ranges will appear to be transposed compared to the equivalent CUDA code, and the highest dimension of a SYCL id will correspond to the x-component of the comparable CUDA built-in variables, not the lowest dimension.

To demonstrate this difference, consider the CUDA example in Figure 21-4. In this example, each CUDA thread exchanges its value of threadIdx.x with its neighbor. Because the x-component is the fastest moving component in CUDA, we do not expect a CUDA thread’s value to match its neighbor thread’s value.

```txt
CHAPTER 21 MIGRATING CUDA CODE

__global__ void ExchangeKernel(int* dst) {
    auto index = get_global_linear_id(); // helper function
    auto fastest = threadIdx.x;
    auto neighbor = __shfl_xor_sync(0xFFFFFF, fastest, 1);
    dst[index] = neighbor;
}
...
dim3 threadsPerBlock(16, 2);
ExchangeKernel<<<1, threadsPerBlock>>>(buffer);
cudaDeviceSynchronize();
```

## Figure 21-4. x-component is the contiguous dimension in CUDA

The equivalent SYCL example is shown in Figure 21-5. Notice that in the SYCL example the ND-range is {2, 16} rather than (16, 2) in the CUDA example, so the parallel index space appears to be transposed. The SYCL example also describes the ND-range as a {2, 16} global range divided into work-groups of size {2, 16}, whereas the CUDA example describes a grid of one block with (16, 2) CUDA threads per block.

Additionally, notice that each SYCL work-item exchanges the value of its item.get\_local\_id(1) (not item.get\_local\_id(0)!) with its neighbor, because the last dimension is the fastest moving component in SYCL. In this SYCL example, we also do not expect a SYCL work-item’s value to match its neighbor work-item’s value.

```txt
q.parallel_for(nd_range<2>{{2, 16}, {2, 16}},
        [=](auto item) {
            auto index = item.get_global_linear_id();
            auto fastest = item.get_local_id(1);
            auto sg = item.get_sub_group();
            auto neighbor =
                permute_group_by_xor(sg, fastest, 1);
            buffer[index] = neighbor;
        })
    .wait();
```

## Figure 21-5. Last dimension is the contiguous dimension in SYCL

## Sub-Group Sizes (Warp Sizes)

There are a few more differences we can spot if we look carefully at these examples, specifically relating to the function used to exchange data with a neighbor.

The CUDA example uses the function \_\_shfl\_xor\_sync(0xFFFFFFFF, fastest, 1) to exchange data with a neighbor. For this function, the first argument 0xFFFFFFFF is a bitfield mask indicating the set of CUDA threads participating in the call. For CUDA devices, a 32-bit mask is sufficient, because the warp size is currently 32 for all CUDA devices.

The SYCL example uses the function permute\_group\_by\_xor(sg, fastest, 1) to exchange data with its neighbor. For this function, the first argument describes the set of work-items participating in the call. In this case, sg represents the entire sub-group. Because the set of work-items is specified by a group object rather than a bitfield mask, it can represent sets of arbitrary sizes. This flexibility is desirable because the sub-group size may be less than or greater than 32 for some SYCL devices.

In this specific case, the CUDA example can be rewritten to use the more modern CUDA cooperative groups syntax rather than the older \_shfl\_xor\_sync syntax. The CUDA cooperative groups equivalent is shown in Figure 21-6. This version looks a lot more like the SYCL kernel and is a good example how the later versions of CUDA and SYCL 2020 are growing even closer together.

```cpp
__global__ void ExchangeKernelCoopGroups(int* dst) {
    namespace cg = cooperative_groups;
    auto index = cg::this_grid().thread_rank();
    auto fastest = threadIdx.x;
    auto warp = cg::tiled_partition<32>(cg::this_thread_block());
    auto neighbor = warp.shfl_xor(fastest, 1);
    dst[index] = neighbor;
}
```  
Figure 21-6. Exchanging data with CUDA cooperative groups

## Forward Progress Guarantees

We can find one more difference if we look very carefully at the examples in Figures 21-4 and 21-5, although this difference is more subtle. Once again, the difference is related to the \_\_shfl\_xor\_sync function used to exchange data with a neighbor, and in this case the difference is implied by the \_sync suffix on the function. The \_sync suffix indicates this function is synchronizing the CUDA threads, though this naturally may lead us to ask, why may the CUDA threads be unsynchronized in the first place, before calling this function?

In Chapters 15 and 16, we developed a mental model for a dataparallel kernel executing on a CPU or GPU where a group of work-items is processed simultaneously, in lockstep, using SIMD instructions. While this is a useful mental model for CPUs and GPUs from many vendors, it is not the only way a data-parallel kernel may be executed using SYCL or CUDA, and one of the cases where this mental model breaks is for newer CUDA devices supporting a feature called independent thread scheduling.

For CUDA devices with independent thread scheduling, the individual CUDA threads make progress independently, rather than as a group. These additional forward progress guarantees enable code patterns to execute safely on a CUDA device that may not execute correctly on a SYCL device without the stronger forward progress guarantees. The \_sync suffix on the \_shfl\_xor\_sync function was added in CUDA to clearly indicate that the function requires synchronization and to specify the CUDA threads that are synchronizing using the 32-bit mask.

Forward progress guarantees are an active topic in the SYCL community, and it is very likely that a future version of SYCL will add queries to determine the forward progress capabilities of a device, along with properties to specify the forward progress requirements of a kernel. For now, though, we should be aware that a syntactically correct SYCL program that was ported from CUDA may not execute correctly on all SYCL devices due to independent thread scheduling.

## Barriers

One final, subtle execution model difference we should be aware of concerns the CUDA \_\_syncthreads function compared to the SYCL group\_barrier equivalent. The CUDA \_\_syncthreads function synchronizes all non-exited CUDA threads in the thread block, whereas the SYCL group\_barrier function synchronizes all work-items in the workgroup. This means that a CUDA kernel will run correctly if some CUDA threads early exit before calling \_\_syncthreads, but there is no guarantee that a SYCL kernel like the one shown in Figure 21-7 will run correctly.

```cpp
std::cout << "WARNING: May deadlock on some devices!\n";
q.parallel_for(nd_range<1>{64, 64}, [=](auto item) {
    int id = item.get_global_id(0);
    if (id >= count) {
        return;  // early exit
    }
    group_barrier(item.get_group());
    buffer[id] = id;
}).wait();
```  
Figure 21-7. Possible SYCL barrier deadlock

In this case, the fix is straightforward: the range check can be moved after the group\_barrier, or in this specific case, the group\_barrier can be removed entirely. This is not always the case though, and other kernels may require restructuring to ensure all work-items always reach or always skip a group\_barrier.

## Memory Model

Fundamentally, both CUDA and SYCL use a similar weakly-ordered memory model. Luckily there are only a few memory model differences we need to keep in mind when we are migrating a CUDA kernel to SYCL.

## Barriers

By default, the CUDA \_\_syncthreads barrier function and the SYCL group\_barrier barrier function has the same effects on the memory model, assuming the group passed to the SYCL group\_barrier is a workgroup. Likewise, the CUDA \_\_syncwarp barrier function has the same effects as the SYCL group\_barrier barrier function, assuming the group passed to the SYCL group\_barrier is a sub-group.

The SYCL group\_barrier accepts an optional parameter to specify the fence\_scope for the barrier, but in most cases, this can be omitted. A wider scope can be passed to group\_barrier, such as memory\_scope::device, but this usually is not required, and it may cause the SYCL group\_barrier to be more expensive than the CUDA \_\_syncthreads barrier.

```txt
q.parallel_for(nd_range<1>{16, 16}, [=](auto item) {
    // Equivalent of __syncthreads, or
    // this_thread_block().sync():
        group_barrier(item.get_group());

    // Equivalent of __syncwarp, or
    // tiled_partition<32>(this_thread_block()).sync():
        group_barrier(item.get_sub_group());
}).wait();
```

## Figure 21-8. CUDA and SYCL barrier equivalents

The code in Figure 21-8 shows the equivalent barrier syntax for CUDA and SYCL. Notice how the newer CUDA cooperative groups syntax using this\_thread\_block and tiled\_partition has a sync function that is even closer to the SYCL group\_barrier. This is another good example how later versions of CUDA and SYCL 2020 are becoming more and more similar.

## Atomics and Fences

Both CUDA and SYCL support similar atomic operations, though as with barriers there are a few important differences we should be aware of. The most important difference concerns the default atomic memory order.

Many CUDA programs are written using an older C-like atomic syntax where the atomic function takes a pointer to memory, like atomicAdd. These atomic functions are relaxed atomics and operate at device scope. There are also suffixed versions of these atomic functions that operate at a different scope, such as atomicAdd\_system and atomicAdd\_block, but these are uncommon.

The SYCL atomic syntax is a little different and is based on std::atomic\_ref from C++20 (refer to Chapter 19 for details about the SYCL atomic\_ref class and how it compares to std::atomic\_ref). If we want our SYCL atomic to be equivalent to the CUDA atomicAdd function, we will want to declare our SYCL atomic\_ref to have a similar memory\_ order::relaxed memory order and memory\_scope::device scope, as shown in Figure 21-9.

```rust
q.parallel_for(count, [=](auto id) {
    // The SYCL atomic_ref must specify the default order
    // and default scope as part of the atomic_ref type. To
    // match the behavior of the CUDA atomicAdd we want a
    // relaxed atomic with device scope:
    atomic_ref<int, memory_order::relaxed,
            memory_scope::device>
        aref(*buffer);

    // When no memory order is specified, the defaults are
    // used:
    aref.fetch_add(1);

    // We can also specify the memory order and scope as
    // part of the atomic operation:
    aref.fetch_add(1, memory_order::relaxed,
            memory_scope::device);
});

Figure 21-9. CUDA and SYCL atomic equivalents
```

Newer CUDA code may use the cuda::atomic\_ref class from the CUDA C++ Standard Library. The cuda::atomic\_ref class looks more like the SYCL atomic\_ref class, but there are some important differences to be aware of with it, also:

The scope is optional for a CUDA atomic\_ref, but defaults to the entire system if unspecified. The SYCL atomic\_ref must specify an atomic scope in all cases.

The default atomic order for a CUDA atomic\_ref is unconditionally sequential consistency, whereas the SYCL atomic\_ref may specify a different default atomic order. By specifying a default atomic order, our SYCL code can be more concise and use convenience operators like += even when the atomic order is something other than sequential consistency.

There is one final concern we need to keep in mind when our code or algorithm requires atomics: some atomic operations and atomic scopes are not required by the SYCL specification and may not be supported by all SYCL devices. This is also true for CUDA devices, but it is especially important to remember for SYCL due to the diversity of SYCL devices. Please refer to Chapter 12 for more detail on how to query properties of a SYCL device and to Chapter 19 for descriptions of the atomic capabilities that may be supported by a SYCL device or context.

## Other Differences

This section describes a few other miscellaneous differences to keep in mind when we are porting CUDA code to SYCL.

## Item Classes vs. Built-In Variables

One of the bigger stylistic differences between CUDA and SYCL is the way kernel instances identify their location in the N-dimensional parallel index space. Recall from Chapter 4 that every SYCL kernel must take an item, an nd\_item, an id, or in some cases an integral argument identifying the work-item in the parallel index space. The item and nd\_item classes can also be used to query information about the parallel index space itself, such as the global range, the local range, and the different groups that the work-item belongs to.

CUDA kernels do not include any arguments to identify the CUDA thread in the parallel index space. Instead, CUDA threads use built-in variables such as blockIdx and threadIdx to identify the location in the parallel index space and built-in variables such as gridDim and blockDim to represent information about the parallel index space itself. Newer CUDA kernels that use cooperative groups can also construct certain cooperative groups implicitly by calling built-in functions like this\_thread\_block.

This is usually only a syntactic difference that does not functionally affect the code we can write, though it does mean that SYCL kernels may pass an item or an nd\_item to called functions in more cases, say if a called function needs to know the work-item index.

## Contexts

Another conceptual difference between CUDA and SYCL is the idea of a SYCL context. Recall that a SYCL context is an object that stores the state of a SYCL application for a set of SYCL devices. As an example, a SYCL context may store information about memory allocations or compiled programs. Contexts are an important concept to a SYCL application because a single SYCL application may support devices from multiple vendors, perhaps using multiple backend APIs.

In most cases our SYCL programs can be blissfully unaware that contexts exist, and most of the example programs in this book do not create or manipulate contexts. If we do choose to create additional SYCL contexts in our programs though, either implicitly or explicitly, we need to be careful not to use context-specific SYCL objects from one context with a different SYCL context. At best, careless use of multiple contexts may cause our programs to run inefficiently, say if we end up compiling our SYCL kernels multiple times, once for each context. At worst, mixing SYCL objects across contexts may result in undefined behavior, causing our programs to become non-portable or executing improperly on some backends or devices.

For completeness, note that CUDA has a concept of contexts as well, though CUDA contexts are only exposed by the lower-level CUDA driver APIs. Most CUDA programs do not create or manipulate contexts, either.

## Error Checking

One final difference to consider relates to error checking and error handling. Because of CUDA’s C heritage, errors in CUDA are returned via error codes from CUDA function calls. For most CUDA functions, a failing error code indicates an error in the function returning the error, such as an incorrect parameter to the function. For some other CUDA functions though, like cudaDeviceSynchronize, the error value can also return asynchronous errors that occurred on the device.

SYCL also has synchronous and asynchronous errors, though both types of errors are reported using SYCL exceptions rather than return values from SYCL functions. Please refer to Chapter 5 for more information about error detection and error handling in SYCL.

## Features in CUDA That Aren’t In SYCL… Yet!

So far, we have described cases where features are in both CUDA and SYCL but are expressed differently. This section describes several features that are in CUDA but that do not (currently) have equivalents in SYCL. This is not an exhaustive list, but it is intended to describe some of the features that are commonly used by CUDA applications that may require more effort when migrating to SYCL.

Please note that vendor-specific features are an important part of the standardization process, regardless of whether they are extensions to a standard or defined in a completely vendor-specific API. Vendor-specific features provide important implementation experience and allow a feature to prove its value before it is refined and incorporated into a standard. Many of these features are already in active development for inclusion into the SYCL standard, and some may already be available as extensions to the standard.

## GET INVOLVED!

Feedback from users and developers is another important part of the standardization process. If you have an idea for a new feature, or if you have found an extension or a feature from another API valuable, please consider becoming involved! SYCL is an open standard and many SYCL implementations are open source, making it easy to participate in the growing SYCL community.

## Global Variables

Although programmers are told early on to never use global variables, sometimes a global variable is the right tool for the job. We might choose to use a global variable to store a useful constant, or a lookup table, or some other value that we would like to be accessible to all the work-items executing our data parallel kernel.

CUDA supports global variables in different address spaces and therefore with different lifetimes. For example, a CUDA program can declare a \_\_device\_\_ global variable in the global memory space that is unique for each device. These global variables can be set by or read from the host and accessed by all the CUDA threads executing a kernel. A CUDA program can also declare a \_\_shared\_\_ global variable in the CUDA shared memory space (remember, this is the equivalent of a variable declared in SYCL local memory) that is unique for every CUDA block and can only be accessed by the CUDA threads in that block.

SYCL does not support global variables in device code yet, though there are extensions in the works to provide similar functionality.

## Cooperative Groups

As described earlier in this chapter, recent versions of CUDA support cooperative groups, which provide an alternative syntax for collective operations like barriers and shuffle functions. The SYCL group object and the SYCL group algorithms library have many similarities to CUDA cooperative groups, but some key differences remain.

The biggest difference is that the SYCL group functions currently work only on the predefined SYCL work-group and sub-group classes, whereas CUDA cooperative groups are more flexible. For example, a CUDA program may create fixed-size tiled\_partition groups that divide an existing group into a set of smaller groups, or a CUDA program may represent the set of CUDA threads in a CUDA warp that are currently active as a coalesced\_group.

A CUDA program may additionally create cooperative groups that are larger than a work-group. For example, a CUDA program may create a grid\_group representing all the CUDA threads in the grid (equivalently, all the work-items in the global range), or a cluster\_group representing all the CUDA threads in a thread block cluster. To effectively use these newer and larger groups, a CUDA kernel must be launched using special host API functions to ensure that all the CUDA threads in a grid may cooperate, or to specify the thread block cluster dimensions.

SYCL does not support all the cooperative group types in CUDA yet, though there are extensions in the works to add additional group types to SYCL. The introduction of the group object and group algorithms in SYCL 2020 has SYCL well positioned to support this functionality.

## Matrix Multiplication Hardware

The final feature we will describe in this section is access to matrix multiplication hardware, also referred to as matrix multiply and accumulate (MMA) hardware, tensor cores, or systolic arrays. These are all different names for dedicated hardware engines that are purposebuilt to accelerate the matrix multiplication operations that are key to many artificial intelligence (AI) workloads. If we want to customize these workloads, it is important that we have access to matrix multiplication hardware in our data parallel kernels to achieve peak performance.

CUDA provides access to matrix multiplication hardware via warp matrix multiplication and accumulation (WMMA) functions. These functions effectively allow the CUDA threads in a warp (equivalently, work-items in a sub-group) to cooperate to perform a matrix multiply and accumulate operation on smaller matrix tiles. The elements of these matrix tiles can be 32-bit floats or 64-bit doubles for some devices and algorithms, but more commonly use lower-precision types like as 8-bit chars, 16-bit halfs, or specialized AI types like bfloat16s (bf16).

Both CUDA and SYCL are actively evolving their support for matrix multiplication hardware. This is a good example of how different vendors will add support for their vendor-specific functionality via vendor-specific mechanisms initially, then a feature will be refined, and common best practices will be added to the standard.

## Porting Tools and Techniques

Luckily, when we choose to migrate an application from CUDA to SYCL, it does not need to be a manual process, and we can use tools to automate parts of the migration. This section will describe one of these tools and techniques to assist with migration.

## Migrating Code with dpct and SYCLomatic

In this section we will describe the DPC++ Compatibility Tool (dpct) and the related open source SYCLomatic tool. We will use dpct to automatically migrate a CUDA sample to SYCL, though the concepts described in this section apply equally well to SYCLomatic.

Figure 21-10 shows the important parts of the simple CUDA sample we will be migrating. This sample reverses blocks of a buffer. This is not a very useful sample in practice, but it has interesting cases that our automigration tool will need to handle, such as a CUDA shared memory global variable, a barrier, a device query, memory allocation and initialization, the kernel dispatch itself, and some basic error checking.

```cpp
__shared__ int scratch[256];
__global__ void Reverse(int* ptr, size_t size) {
    auto gid = blockIdx.x * blockDim.x + threadIdx.x;
    auto lid = threadIdx.x;

    scratch[lid] = ptr[gid];
    __syncthreads();
    ptr[gid] = scratch[256 - lid - 1];
}

int main() {
    std::array<int, size> data;
    std::iota(data.begin(), data.end(), 0);

    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, 0);
    std::cout << "Running on device: " << deviceProp.name << "\n";

    int* ptr = nullptr;
    cudaMalloc(&ptr, size * sizeof(int));
    cudaMemcpy(ptr, data.data(), size * sizeof(int),
            cudaMemcpyDefault);
    Reverse<<<size / 256, 256>>>(ptr, size);
    cudaError_t result = cudaDeviceSynchronize();
    if (result != cudaSuccess) {
        std::cout << "An error occurred!\n";
    }
    // ...
```

## Figure 21-10. A simple CUDA program we will automatically migrate

## Running dpct

Because this is a simple example, we can simply invoke dpct and pass the CUDA source file we would like to migrate. For more complicated scenarios, dpct can be invoked as part of the application build process to identify the CUDA source files to migrate. Please refer to the links at the end of this chapter for more information and additional training material.

When we run dpct on our sample CUDA source file, we may see output like that shown in Figure 21-11. We can make several observations from this output. First, our file was processed successfully, which is great! There were a few warnings though, indicating cases that dpct was not able to able to migrate. For our example, all three warnings are due to the error checking differences between CUDA and SYCL. For our program, dpct was able to generate SYCL code that will behave correctly when the program does not generate an error, but it was not able to migrate the error checking.

The error checking warning is a good example how migration tools like dpct and SYCLomatic will not be able to migrate everything. We should expect to review and adjust the migrated code to address any migration issues, or to otherwise improve the migrated SYCL code for maintainability, portability, or performance.

```txt
\$ dpct source_file.cu
NOTE: Could not auto-detect compilation database for file
'source_file.cu' in '/path/to/your/file' or any parent directory.
The directory "dpct_output" is used as "out-root"
Processing: /path/to/your/file/source_file.cu
/path/to/your/file/source_file.cu:38:5: warning: DPCT1001:0: The
statement could not be removed.
    std::cout << "An error occurred!\n";
    ^
/path/to/your/file/source_file.cu:37:3: warning: DPCT1000:1: Error
handling if-stmt was detected but could not be rewritten.
    if (result != cudaSuccess) {
    ^
/path/to/your/file/source_file.cu:36:24: warning: DPCT1003:2: Migrated
API does not return error code. (*, 0) is inserted. You may need to
rewrite this code.
    cudaError_t result = cudaDeviceSynchronize();
    ^
Processed 1 file(s) in -in-root folder "/path/to/your/file"
```

## Figure 21-11. Sample dpct output when migrating this CUDA program

For this example, though, we can use the migrated code as-is. Figure 21-12 shows how to compile our migrated code using the DPC++ compiler with NVIDIA GPU support and then shows successful execution of our migrated program on an Intel GPU, an Intel CPU, and an NVIDIA GPU. Note, if we were to run the migrated program on a different system with different devices, the output may look different, or it may fail to run if the selected device does not exist in the system.

```txt
$ icpx -fsycl -fsycl-targets=spir64,nvptx64-nvidia-cuda \
    migrated.cpp -o migrated
$ ./migrated
Running on device: Intel(R) UHD Graphics 770
Success.
$ ONEAPI_DEVICE_SELECTOR=opencl:cpu ./migrated
Running on device: 12th Gen Intel(R) Core(TM) i9-12900K
Success.
$ ONEAPI_DEVICE_SELECTOR=ext_oneapi_cuda:gpu ./migrated
Running on device: NVIDIA GeForce RTX 3060
Success.
```  
Figure 21-12. Compiling and running our migrated CUDA program

## Examining the dpct Output

If we examine the migrated output, we can see that dpct handled many of the differences described in this chapter. For example, in the generated SYCL kernel shown in Figure 21-13, we see that the \_\_shared\_\_ global variable scratch was turned into a local memory accessor and passed into the kernel. We can also see that the built-in variables blockIdx and threadIdx were replaced by calls into an instance of the nd\_item class and that the differing conventions for the contiguous dimension were properly handled, for example, by replacing the use of threadIdx.x with a call to item\_gt1.get\_local\_id(2).

## Chapter 21 Migrating CUDA Code

```cpp
void Reverse(int *ptr, size_t size,
            const sycl::nd_item<3> &item_ct1,
            int *scratch) {
    auto gid =
        item_ct1.get_group(2) * item_ct1.get_local_range(2) +
        item_ct1.get_local_id(2);
    auto lid = item_ct1.get_local_id(2);

    scratch[lid] = ptr[gid];
    item_ct1.barrier(sycl::access::fence_space::local_space);
    ptr[gid] = scratch[256 - lid - 1];
}
```

## Figure 21-13. SYCL kernel migrated from CUDA

We can also see that dpct handled some of the host code differences by using several dpct utility functions, such as for the migrated device query shown in Figure 21-14. These helper functions are intended to be used by migrated code only. For portability and maintainability, we should prefer to use standard SYCL APIs directly for our additional development.

```cpp
dpct::device_info deviceProp;
dpct::dev_mgr::instance().get_device(0).get_device_info(
    deviceProp);
std::cout << "Running on device: "
        << deviceProp.get_name() << "\n";
```

## Figure 21-14. SYCL device name query migrated from CUDA

In general, though, the SYCL code that dpct generates is readable and the mapping between the CUDA code and the migrated SYCL code is clear. Even though additional hand-editing is often required, using automated tools like dpct or SYCLomatic can save time and reduce errors during migration.

## Summary

In this chapter, we described how to migrate an application from CUDA to SYCL to enable an application to run on any SYCL device, including CUDA devices by using SYCL compilers with CUDA support.

We started by looking at the many similarities between CUDA and SYCL programs, terminology aside. We saw how CUDA and SYCL fundamentally use the same kernel-based approach to parallelism, with a similar execution model and memory model, making it relatively straightforward to migrate a CUDA program to SYCL. We also explored a few places where CUDA and SYCL have subtle syntactic or behavioral differences and are therefore good to keep in mind as we are migrating our CUDA applications to SYCL. We also described several features that are in CUDA but are not in SYCL (yet!), and we described how vendor-specific features are an important part of the standardization process.

Finally, we examined several tools to automate parts of the migration process and we used the dpct tool to automatically migrate a simple CUDA example to SYCL. We saw how the tool migrated most of the code automatically, producing functionally correct and readable code. We were able to run the migrated SYCL example on different SYCL devices after migration, even though additional reviewing and editing may be required for more complex applications.

## For More Information

Migrating CUDA code to SYCL is a popular topic and there are many other resources available to learn more. Here are two resources the authors have found helpful:

• General information and tutorials showing how to migrate from CUDA to SYCL (tinyurl.com/cuda2sycl)

• Getting Started Guide for the DPC++ Compatibility Tool (tinyurl.com/startDPCpp)

![](images/2f9728d753ff200163fe6b25f46323dce7378e461458a77fe2dce907b64309b9.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Future Direction of SYCL

Take a moment now to feel the peace and calm of knowing that we have covered programming using C++ with SYCL. All the pieces have fallen into place.

We’ve endeavored to ensure that the code samples in previous chapters use standard SYCL 2020 functionality and execute on a wide range of hardware, and the few places we used extensions (e.g., interoperability and FPGA-specific extensions), we call it out. However, the future-looking code shown in this epilogue does not compile with any compiler as of mid-2023.

In this epilogue, we speculate on the future. Our crystal ball can be a bit difficult to read—this epilogue comes without any warranty. Some of the predictions we made in the first edition of this book came true, but others did not.

This epilogue provides a sneak peek of upcoming SYCL features and DPC++ extensions that we are very excited about. We offer no guarantees that the code samples printed in this epilogue compile: some may already be compatible with a compiler released after the book, while others may compile only after some massaging of syntax. Some features may be released as extensions or incorporated into future versions of SYCL, while others may remain experimental features indefinitely. The code samples in the GitHub repository associated with this book may be updated to use new syntax as it evolves. Likewise, we will have an erratum for the

book, which may get additions made from time to time. We recommend checking for updates in these two places (code repository and book errata—links can be found early in Chapter 1).

## Closer Alignment with C++11, C++14, and C++17

Maintaining close alignment between SYCL and C++ has two advantages. First, it enables SYCL to leverage the newest and greatest features of C++ to improve developer productivity. Second, it increases the chances of heterogeneous programming features introduced in SYCL successfully influencing the future direction of C++.

SYCL 1.2.1 was based on C++11, and many of the biggest improvements to the interfaces of SYCL 2020 are only possible because of language features introduced in C++14 (e.g., generic lambdas) and C++17 (e.g., class template argument deduction—CTAD). We expect SYCL and C++ to grow closer over time, and there are several exciting efforts already underway.

The C++ Standard Template Library (STL) contains several algorithms which correspond to the parallel patterns discussed in Chapter 17. The algorithms in the STL typically apply to sequences specified by pairs of iterators and—starting with C++17—support an execution policy argument denoting whether they should be executed sequentially or in parallel. The standard allows for implementations to define their own execution policies, too, and the oneAPI DPC++ Library (oneDPL) covered in Chapter 18 leverages such a custom execution policy to enable algorithms to execute on SYCL devices. The result is a high-productivity approach to programming heterogeneous devices—if an application can be expressed solely using functionality of the STL algorithms, oneDPL makes it possible to make use of the accelerators in our systems without writing a single line of SYCL kernel code! There are still open questions about how the STL algorithms should interact with certain SYCL concepts (e.g., buffers), and how to ensure that all the standard library classes we might want (e.g., std::complex, std::atomic) are available in device code, but oneDPL is the first step on a long path toward unifying our host and device code.

## Adopting Features from C++20, C++23 and Beyond

The SYCL specification deliberately trails behind C++ to ensure that the features it uses have broad compiler support. However, SYCL committee members—many of whom are also involved in ISO C++ committees—are keeping a close eye on how future versions of C++ are developing.

Adopting C++ or SYCL features we discuss here that are not finalized yet into a specification could be a mistake—features may change significantly before making it into a standard. Nevertheless, there are a number of features under discussion that may change the way that future SYCL programs look and behave which are worth discussing.

Some of the features in SYCL 2020 were informed by C++20 (e.g., std::atomic\_ref) and others were pre-adopted into the sycl:: namespace (e.g., std::bit\_cast, std::span). As we move toward the next official release of SYCL, we expect to align with C++20 more closely and incorporate the most useful parts of it. For example, C++20 introduced some additional thread synchronization routines in the form of std::latch and std::barrier; we already explored in Chapter 19 how similar interfaces could be used to define device-wide barriers, and it may make sense to reexamine sub-group and work-group barriers in the context of the new C++20 syntax as well.

One of the most exciting features in C++23 is mdspan, a non-owning view of data that provides both multidimensional array syntax for pointers and an AccessorPolicy as an extension point for controlling access to the underlying data. These semantics are very similar to those of SYCL

accessors, and mdspan would enable accessor-like syntax to be used for both buffers and USM allocations, as shown in Figure EP-1.

```cpp
queue q;
constexpr int N = 4;
constexpr int M = 2;
int* data = malloc_shared<int>(N * M, q);

stackx::mdspan<int, N, M> view{data};
q.parallel_for(range<2>{N, M}, [=](id<2> idx) {
    int i = idx[0];
    int j = idx[1];
    view(i, j) = i * M + j;
}).wait();
```

Figure EP-1. Attaching accessor-like indexing to a USM pointer using mdspan

Hopefully it is only a matter of time until SYCL officially supports mdspan. In the meantime, we recommend that interested readers experiment with the open source production-quality reference implementation available as part of the Kokkos project.

## Mixing SPMD and SIMD Programming

Another exciting, proposed feature for C++ is the std::simd class template, which seeks to provide a portable interface for explicit vector parallelism in C++. Adopting this interface would provide a clear distinction between the two different uses of vector types described in Chapter 11: uses of vector types for programmer convenience and uses of vector types by ninja programmers for low-level performance tuning. The presence of support for both SPMD and SIMD programming styles within the same language also raises some interesting questions: how should we declare which style a kernel uses, and should we be able to mix and match styles within the same kernel?

We have started to explore potential answers to this question in the form of a DPC++ extension (sycl\_ext\_oneapi\_invoke\_simd), which provides a new invoke\_simd function (modelled on std::invoke) that allows developers to call explicitly vectorized (SIMD) code from within an SPMD kernel. The call to invoke\_simd acts as a clear boundary between the two execution models implied by the two programming styles and defines how data should flow between them. The code in Figure EP-2 shows a very simple example of invoke\_simd’s usage, calling out to a function that expects to receive a combination of scalar and vector (simd) arguments.

```cpp
// Function expects one vector argument (x) and one scalar
// argument (n)
simd<float, 8> scale(simd<float, 8> x, float n) {
  return x * n;
}

q.parallel_for(..., sycl::nd_item<1> it)
    [[sycl::reqd_sub_group_size(8)]] {
  // In SPMD code, each work-item has its own x and n
  // variables
  float x = ...;
  float n = ...;

  // Invoke SIMD function (scale) using work-items in the
  // sub-group x values from each work-item are combined
  // into a simd<float, 8>
  // The value of n is defined to be the
  // same (uniform) across all work-items
  // Returned simd<float, 8> is unpacked
  sycl::sub_group sg = it.get_sub_group();
  float y = invoke_simd(sg, scale, x, uniform(n));
});
```

## Figure EP-2. A simple example of invoking a SIMD function from a SPMD kernel

The approach taken by invoke\_simd has several advantages. First, there can be no nasty surprises— functions with a different execution model are invoked explicitly, and the user is responsible for describing how to marshal data back and forth. Second, the mechanism allows

for fine-grained specialization—it is possible to write just a few lines of explicitly vectorized code (e.g., for performance tuning) without having to throw away the rest of our SPMD code. Finally, it is straightforward to extend—invoke\_simd itself can be extended to support new groups or new argument mappings via simple overloading, and similar invoke\_\* functions could be introduced to handle interoperability with different contexts (e.g., code written in a language that isn’t SYCL).

## Address Spaces

The introduction of generic address space support in SYCL 2020 has the potential to greatly simplify many codes, by allowing us to use regular C++ pointers without worrying about what kind of memory is being used. Many modern architectures provide hardware support for the generic address space, and so we can expect code using regular C++ pointers to work across a wide variety of machines and with minimal performance overhead.

However, there are some (older, or more special purpose) architectures on which generic address space support is a more complicated story. Some hardware may use different instructions to access different kinds of memory, requiring compilers to identify a concrete address space at compile time (i.e., to generate the correct instructions). There may also be SYCL backends incapable of representing a generic address space (e.g., OpenCL 1.2). SYCL 2020 makes allowances for such hardware and backends via a set of inference rules for deducing address spaces.

The address space deduction rules were inherited from SYCL 1.2.1, and the SYCL 2020 specification includes a note that the rules will be revisited in a future version of SYCL. Although it is unclear at the time of writing exactly how these rules will change, SYCL’s long-term thinking is clear: in most cases, we should not be concerned with address space management and should trust the compiler and hardware to do the right thing.

## Specialization Mechanism

There are plans to introduce compile-time queries enabling kernels to be specialized based on properties (aspects) of the targeted device (e.g., the device type, support for a specific extension, the size of work-group local memory, the sub-group size selected by the compiler). Such queries require a new kind of constant expression not currently present in C++— they are not necessarily constexpr when the host code is compiled but become constexpr when the target device becomes known.

The exact mechanism used to expose this “device-constant expression” concept is still being designed. We expect it to build on the specialization constants feature introduced in SYCL 2020 and to look and behave similarly to the code shown in Figure EP-3.

```cpp
h.parallel_for(range{1}, [=](id<1> idx) {
  if_device_has<aspect::cpu>([&]() {
    /* Code specialized for CPUs */
    out << "On a CPU!" << endl;
  }).else_if_device_has<aspect::gpu>([&]() {
    /* Code specialized for GPUs */
    out << "On a GPU!" << endl;
  });
});
```

Figure EP-3. Specializing kernel code based on device aspects at kernel compile time

## Compile-Time Properties

SYCL allows the behavior of certain classes (e.g., buffers, accessors) to be modified by passing a property list into the constructor. These properties are already very powerful, but their power is limited by the fact that the properties passed to a constructor are not known until runtime. Allowing for certain properties to be declared at compile time has the potential to significantly improve performance, by reducing the number of runtime checks and by enabling compilers to aggressively specialize both host and device code in the presence of specific properties.

The DPC++ compiler supports an experimental extension for compiletime properties (sycl\_ext\_oneapi\_properties), and it already enables a wide variety of other extensions:

Pointers annotated with information extending beyond just address spaces, which could inform the future of sycl::multi\_ptr (sycl\_ext\_oneapi\_annotated\_ptr)

Kernel configuration controls, which could replace C++ attributes and increase the capabilities of libraryonly SYCL implementations (sycl\_ext\_oneapi\_kernel\_ properties)

Descriptions of desired memory behavior and access controls (sycl\_ext\_oneapi\_device\_global, sycl\_ext\_ oneapi\_prefetch)

Our early experience with compile-time properties has been very positive, and we’re finding more and more potential use cases for them all the time. Given their wide applicability, we are keen to see some version of compile-time properties adopted in a future SYCL specification.

## Summary

There is already a lot of excitement around SYCL, and this is just the beginning! We (as a community) have a long path ahead of us, and it will take significant continued effort to distill the best practices for heterogeneous programming and to design new language features that strike the desired balance between performance, portability, and productivity.

We need your help! If your favorite feature of C++ (or any other programming language) is missing from SYCL, please reach out to us. Together, we can shape the future direction of SYCL and C++.

## For More Information

• Khronos SYCL Registry, www.khronos.org/ registry/SYCL

• H. Carter Edwards et al., “mdspan: A Non-Owning Multidimensional Array Reference,” wg21.link/p0009

• D. Hollman et al., “Production-Quality mdspan Implementation,” github.com/kokkos/mdspan

• Intel DPC++ Compiler Extensions, tinyurl.com/ syclextend

## Index
