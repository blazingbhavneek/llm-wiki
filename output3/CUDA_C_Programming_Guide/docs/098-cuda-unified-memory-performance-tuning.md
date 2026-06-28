On systems without CPU and GPU page tables: hardware coherency vs. software coherency, atomic accesses from the device to file-backed host memory are not supported. The following example code is valid on systems with CPU and GPU page tables: hardware coherency vs. software coherency but exhibits undefined behavior on other systems:

```cpp
#include <cuda/atomic>

#include <cstdio>
#include <fcntl.h>
#include <sys/mman.h>

#define ERR(msg, ...) { fprintf(stderr, msg, ##__VA_ARGS_); return EXIT_FAILURE; }

__global__ void kernel(int* ptr) {
    cuda::atomic_ref{*ptr}.store(2);
}

int main() {
    // this will be closed/deleted by default on exit
    FILE* tmp_file = tmpfile64();
    // need to allocate space in the file, we do this with posix_fallocate here
    int status = posix_fallocate(fileno(tmp_file), 0, 4096);
    if (status != 0) ERR("Failed to allocate space in temp file\n");
    int* ptr = (int*)mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE, fileno(tmp_file), 0);
    if (ptr == MAP_FAILED) ERR("Failed to map temp file\n");

    // initialize the value in our file-backed memory
    *ptr = 1;
    printf("Atom value: %d\n", *ptr);

    // device and host thread access ptr concurrently, using cuda::atomic_ref
    kernel<<<1, 1>>>(ptr);
    while (cuda::atomic_ref{*ptr}.load() != 2);
    // this will always be 2
    printf("Atom value: %d\n", *ptr);

    return EXIT_SUCCESS;
}
```

On systems without CPU and GPU page tables: hardware coherency vs. software coherency, atomic accesses to unified memory may incur page faults which can lead to significant latencies. Note that this is not the case for all GPU atomics to CPU memory on these systems: operations listed by nvidia-smi -q | grep "Atomic Caps Outbound" may avoid page faults.

On systems with CPU and GPU page tables: hardware coherency vs. software coherency, atomics between host and device do not require page faults, but may still fault for other reasons that any memory access can fault for.

## 24.2.2.5 Memcpy()/Memset() Behavior With Unified Memory

cudaMemcpy\*() and cudaMemset\*() accept any unified memory pointer as arguments.

For cudaMemcpy\*(), the direction specified as cudaMemcpyKind is a performance hint, which can have a higher performance impact if any of the arguments is a unified memory pointer.

Thus, it is recommended to follow the following performance advice:

▶ When the physical location of unified memory is known, use an accurate cudaMemcpyKind hint.

Prefer cudaMemcpyDefault over an inaccurate cudaMemcpyKind hint.

Always use populated (initialized) bufers: avoid using these APIs to initialize memory.

▶ Avoid using cudaMemcpy\*() if both pointers point to System-Allocated Memory: launch a kernel or use a CPU memory copy algorithm such as std::memcpy instead.

## 24.3. Unified memory on devices without full CUDA Unified Memory support
