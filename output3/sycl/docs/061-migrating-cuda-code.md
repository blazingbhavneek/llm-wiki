
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
