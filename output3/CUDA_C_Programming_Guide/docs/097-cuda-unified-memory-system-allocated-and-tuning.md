
## 24.2.1. System-Allocated Memory: in-depth examples

Systems with full CUDA Unified Memory support allow the device to access any memory owned by the host process interacting with the device. This section shows a few advanced use-cases, using a kernel that simply prints the first 8 characters of an input character array to the standard output stream:

```c
__global__ void kernel(const char* type, const char* data) {
    static const int n_char = 8;
    printf("%s - first %d characters: '', type, n_char);
    for (int i = 0; i < n_char; ++i) printf("%c", data[i]);
    printf("\n");
}
```

The following tabs show various ways of how this kernel may be called:

## Malloc

```cpp
void test_malloc() {
    const char test_string[] = "Hello World";
    char* heap_data = (char*)malloc(sizeof(test_string));
    strncpy(heap_data, test_string, sizeof(test_string));
    kernel<<<1, 1>>>("malloc", heap_data);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
    free(heap_data);
}
```

## Managed

```cpp
void test_managed() {
    const char test_string[] = "Hello World";
    char* data;
    cudaMallocManaged(&data, sizeof(test_string));
    strncpy(data, test_string, sizeof(test_string));
    kernel<<<1, 1>>>("managed", data);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
    cudaFree(data);
}
```

## Stack variable

```c
void test_stack() {
    const char test_string[] = "Hello World";
    kernel<<<1, 1>>>("stack", test_string);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

## File-scope static variable

```txt
void test_static() {
    static const char test_string[] = "Hello World";
    kernel<<<1, 1>>>("static", test_string);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

## Global-scope variable

```txt
const char global_string[] = "Hello World";

void test_global() {
    kernel<<<1, 1>>>("global", global_string);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

Global-scope extern variable

```txt
// declared in separate file, see below
extern char* ext_data;

void test_extern() {
    kernel<<<1, 1>>>("extern", ext_data);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

```c
/** This may be a non-CUDA file */
char* ext_data;
static const char global_string[] = "Hello World";

void __attribute__ ((constructor)) setup(void) {
    ext_data = (char*)malloc(sizeof(global_string));
    strncpy(ext_data, global_string, sizeof(global_string));
}

void __attribute__ ((destructor)) tear_down(void) {
    free(ext_data);
}
```

The first three tabs above show the example as already detailed in the Programming Model section. The next three tabs show various ways a file-scope or global-scope variable can be accessed from the device.

Note that for the extern variable, it could be declared and its memory owned and managed by a thirdparty library, which does not interact with CUDA at all.

Also note that stack variables as well as file-scope and global-scope variables can only be accessed through a pointer by the GPU. In this specific example, this is convenient because the character array is already declared as a pointer: const char\*. However, consider the following example with a globalscope integer:

```cpp
// this variable is declared at global scope
int global_variable;

__global__ void kernel_uncompilable() {
    // this causes a compilation error: global (__host__) variables must not
    // be accessed from __device__ / __global__ code
    printf("%d\n", global_variable);
}

// On systems with pageableMemoryAccess set to 1, we can access the address
// of a global variable. The below kernel takes that address as an argument
__global__ void kernel(int* global_variable_addr) {
    printf("%d\n", *global_variable_addr);
}
int main() {
    kernel<<<1, 1>>>(&global_variable);
    ...
    return 0;
}
```

In the example above, we need to ensure to pass a pointer to the global variable to the kernel instead of directly accessing the global variable in the kernel. This is because global variables without the \_\_managed\_\_ specifier are declared as \_\_host\_\_-only by default, thus most compilers won’t allow using these variables directly in device code as of now.

## 24.2.1.1 File-backed Unified Memory

Since systems with full CUDA Unified Memory support allow the device to access any memory owned by the host process, they can directly access file-backed memory.

Here, we show a modified version of the initial example shown in the previous section to use filebacked memory in order to print a string from the GPU, read directly from an input file. In the following example, the memory is backed by a physical file, but the example applies to memory-backed files, too, as detailed in the section on Inter-Process Communication (IPC) with Unified Memory.

```c
__global__ void kernel(const char* type, const char* data) {
    static const int n_char = 8;
    printf("%s - first %d characters: '', type, n_char);
    for (int i = 0; i < n_char; ++i) printf("%c", data[i]);
    printf("\n");
}
```

```c
void test_file_backed() {
    int fd = open(INPUT_FILE_NAME, O_RDONLY);
```

(continues on next page)

```txt
ASSERT(fd >= 0, "Invalid file handle");
struct stat file_stat;
int status = fstat(fd, &file_stat);
ASSERT(status >= 0, "Invalid file stats");
char* mapped = (char*)mmap(0, file_stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
ASSERT(mapped != MAP_FAILED, "Cannot map file into memory");
kernel<<<1, 1>>>(file-backed", mapped);
ASSERT(cudaDeviceSynchronize() == cudaSuccess,
    "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
ASSERT(munmap(mapped, file_stat.st_size) == 0, "Cannot unmap file");
ASSERT(close(fd) == 0, "Cannot close file");
}
```

Note that on systems without the hostNativeAtomicSupported property, including systems with Linux HMM enabled, atomic accesses to file-backed memory are not supported.

## 24.2.1.2 Inter-Process Communication (IPC) with Unified Memory

Note: As of now, using IPC with Unified Memory can have significant performance implications.

Many applications prefer to manage one GPU per process, but still need to use Unified Memory, for example for over-subscription, and access it from multiple GPUs.

CUDA IPC (see Interprocess Communication) does not support Managed Memory: handles to this type of memory may not be shared through any of the mechanisms discussed in this section. On systems with full CUDA Unified Memory support, System-Allocated Memory is Inter-Process Communication (IPC) capable. Once access to System-Allocated Memory has been shared with other processes, the same Programming Model applies, similar to File-backed Unified Memory.

See the following references for more information on various ways of creating IPC-capable System-Allocated Memory under Linux:

▶ mmap with MAP\_SHARED

▶ POSIX IPC APIs

1 Linux memfd\_create

Note that it is not possible to share memory between diferent hosts and their devices using this technique.

## 24.2.2. Performance Tuning

In order to achieve good performance with Unified Memory, it is important to:

▶ Understand how paging works on your system, and how to avoid unnecessary page faults.

▶ Understand the various mechanisms allowing you to keep data local to the accessing processor.

▶ Consider tuning your application for the granularity of memory transfers of your system.

As general advice, Performance Hints might provide improved performance, but using them incorrectly might degrade performance compared to the default behavior. Also note that any hint has a performance cost associated with it on the host, thus useful hints must at the very least improve performance enough to overcome this cost.

## 24.2.2.1 Memory Paging and Page Sizes

Many of the sections for unified memory performance tuning assume prior knowledge on virtual addressing, memory pages and page sizes. This section attempts to define all necessary terms and explain why paging matters for performance.

All currently supported systems for Unified Memory use a virtual address space: this means that memory addresses used by an application represent a virtual location which might be mapped to a physical location where the memory actually resides.

All currently supported processors, including both CPUs and GPUs, additionally use memory paging. Because all systems use a virtual address space, there are two types of memory pages:

Virtual pages: this represents a fixed-size contiguous chunk of virtual memory per process tracked by the operating system, which can be mapped into physical memory. Note that the virtual page is linked to the mapping: for example, a single virtual address might be mapped into physical memory using diferent page sizes.

Physical pages: this represents a fixed-size contiguous chunk of memory the processor’s main Memory Management Unit (MMU) supports and into which a virtual page can be mapped.

Currently, all x86\_64 CPUs use 4KiB physical pages. Arm CPUs support multiple physical page sizes - 4KiB, 16KiB, 32KiB and 64KiB - depending on the exact CPU. Finally, NVIDIA GPUs support multiple physical page sizes, but prefer 2MiB physical pages or larger. Note that these sizes are subject to change in future hardware.

The default page size of virtual pages usually corresponds to the physical page size, but an application may use diferent page sizes as long as they are supported by the operating system and the hardware. Typically, supported virtual page sizes must be powers of 2 and multiples of the physical page size.

The logical entity tracking the mapping of virtual pages into physical pages will be referred to as a page table, and each mapping of a given virtual page with a given virtual size to physical pages is called a page table entry (PTE). All supported processors provide specific caches for the page table to speed up the translation of virtual addresses to physical addresses. These caches are called translation lookaside bufers (TLBs).

There are two important aspects for performance tuning of applications:

▶ the choice of virtual page size,

whether the system ofers a combined page table used by both CPUs and GPUs, or separate page tables for each CPU and GPU individually.

## 24.2.2.1.1 Choosing the right page size

In general, small page sizes lead to less (virtual) memory fragmentation but more TLB misses, whereas larger page sizes lead to more memory fragmentation but less TLB misses. Additionally, memory migration is generally more expensive with larger page sizes compared to smaller page sizes, because we typically migrate full memory pages. This can cause larger latency spikes in an application using large page sizes. See also the next section for more details on page faults.

One important aspect for performance tuning is that TLB misses are generally significantly more expensive on the GPU compared to the CPU. This means that if a GPU thread frequently accesses random locations of Unified Memory mapped using a small enough page size, it might be significantly slower compared to the same accesses to Unified Memory mapped using a large enough page size. While a similar efect might occur for a CPU thread randomly accessing a large area of memory mapped using a small page size, the slowdown is less pronounced, meaning that the application might want to trade-of this slowdown with having less memory fragmentation.

Note that in general, applications should not tune their performance to the physical page size of a given processor, since physical page sizes are subject to change depending on the hardware. The advice above only applies to virtual page sizes.

## 24.2.2.1.2 CPU and GPU page tables: hardware coherency vs. software coherency

Note: In the remainder of the performance tuning documentation, we will refer to systems with a combined page table for both CPUs and GPUs as hardware coherent systems. Systems with separate page tables for CPUs and GPUs are referred to as software coherent.

Hardware coherent systems such as NVIDIA Grace Hopper ofer a logically combined page table for both CPUs and GPUs. This is important because in order to access System-Allocated Memory from the GPU, the GPU uses whichever page table entry was created by the CPU for the requested memory. If that page table entry uses the default CPU page size of 4KiB or 64KiB, accesses to large virtual memory areas will cause significant TLB misses, thus significant slowdowns.

See the section on configuring huge pages for examples on how to ensure System-Allocated Memory uses large enough page sizes to avoid this type of issue.

On the other hand, on systems where the CPUs and GPUs each have their own logical page table, diferent performance tuning aspects should be considered: in order to guarantee coherency, these systems usually use page faults in case a processor accesses a memory address mapped into the physical memory of a diferent processor. Such a page fault means that:

▶ it needs to be ensured that the currently owning processor (where the physical page currently resides) cannot access this page anymore, either by deleting the page table entry or updating it.

▶ it needs to be ensured that the processor requesting access can access this page, either by creating a new page table entry or updating and existing entry, such that it becomes valid/active.

the physical page backing this virtual page must be moved/migrated to the processor requesting access: this can be an expensive operation, and the amount of work is proportional to the page size.

Overall, hardware coherent systems provide significant performance benefits compared to software coherent systems in cases where frequent concurrent accesses to the same memory page are made by both CPU and GPU threads:

▶ less page-faults: these systems do not need to use page-faults for emulating coherency or migrating memory,

less contention: these systems are coherent at cache-line granularity instead of page-size granularity, that is, when there is contention from multiple processors within a cache line, only the cache line is exchanged which is much smaller than the smallest page-size, and when the diferent processors access diferent cache-lines within a page, then there is no contention.

This impacts the performance of the following scenarios:

▶ Atomic updates to the same address concurrently from both CPUs and GPUs.

Signaling a GPU thread from a CPU thread or vice-versa.

## 24.2.2.2 Direct Unified Memory Access from host

Some devices have hardware support for coherent reads, stores and atomic accesses from the host on GPU-resident unified memory. These devices have the attribute cudaDevAttrDirectManaged-MemAccessFromHost set to 1. Note that all hardware coherent systems have this attribute set for NVLink-connected devices. On these systems, the host has direct access to GPU-resident memory without page faults and data migration (see Data Usage Hints for more details on memory usage hints). Note that with CUDA Managed Memory, the cudaMemAdviseSetAccessedBy hint with location type cudaMemLocationTypeHost is necessary to enable this direct access without page faults.

Consider an example code below:

## System Allocator

```txt
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}
void test_malloc() {
    int *ret = (int*)malloc(1000 * sizeof(int));
    // for shared page table systems, the following hint is not necessary
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directManagedMemAccessFromHost=1:
CPU accesses GPU memory directly without migrations
                                // directManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    free(ret);
}
```

## Managed

```cpp
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}

void test_managed() {
    int *ret;
    cudaMallocManaged(&ret, 1000 * sizeof(int));
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);  // set direct access hint

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directedManagedMemAccessFromHost=1:
CPU accesses GPU memory directly without migrations
                                // directedManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directedManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directedManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    cudaFree(ret);
}
```

After write kernel is completed, ret will be created and initialized in GPU memory. Next, the CPU will access ret followed by append kernel using the same ret memory again. This code will show diferent behavior depending on the system architecture and support of hardware coherency:

▶ On systems with directManagedMemAccessFromHost=1: CPU accesses to the managed bufer will not trigger any migrations; the data will remain resident in GPU memory and any subsequent GPU kernels can continue to access it directly without inflicting faults or migrations.

▶ On systems with directManagedMemAccessFromHost=0: CPU accesses to the managed bufer will page fault and initiate data migration; any GPU kernel trying to access the same data first time will page fault and migrate pages back to GPU memory.

## 24.2.2.3 Host Native Atomics

Some devices, including NVLink-connected devices in hardware coherent systems, support hardwareaccelerated atomic accesses to CPU-resident memory. This implies that atomic accesses to host memory do not have to be emulated with a page fault. For these devices, the attribute cudaDevAttrHostNativeAtomicSupported is set to 1.

## 24.2.2.4 Atomic accesses & synchronization primitives

CUDA Unified Memory supports all atomic operations available to host and device threads, enabling all threads to cooperate by concurrently accessing the same shared memory location. The CUDA C++ standard library provides many heterogeneous synchronization primitives tuned for concurrent use between host and device threads, including cuda::atomic, cuda::atomic\_ref, cuda::barrier, cuda::semaphore, among many others.
