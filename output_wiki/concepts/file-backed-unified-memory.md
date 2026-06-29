# File-backed Unified Memory

Systems with full CUDA Unified Memory support allow the device to access any memory owned by the host process, enabling direct access to file-backed memory. This capability allows GPU kernels to read data directly from input files without explicit data transfers, as the memory is backed by a physical file or memory-backed files (as detailed in Inter-Process Communication with Unified Memory).

## Implementation Example

The following C code demonstrates how to map a file into memory and access it via a GPU kernel. The `kernel` function prints the first 8 characters of the mapped data.

```c
__global__ void kernel(const char* type, const char* data) {
    static const int n_char = 8;
    printf("%s - first %d characters: '', type, n_char);
    for (int i = 0; i < n_char; ++i) printf("%c", data[i]);
    printf("\n");
}
```

The host-side function `test_file_backed` opens the input file, retrieves its size, and maps it into memory using `mmap`. It then launches the kernel and synchronizes the device before cleaning up.

```c
void test_file_backed() {
    int fd = open(INPUT_FILE_NAME, O_RDONLY);
    ASSERT(fd >= 0, "Invalid file handle");
    struct stat file_stat;
    int status = fstat(fd, &file_stat);
    ASSERT(status >= 0, "Invalid file stats");
    char* mapped = (char*)mmap(0, file_stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    ASSERT(mapped != MAP_FAILED, "Cannot map file into memory");
    kernel<<<1, 1>>>("file-backed", mapped);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
    ASSERT(munmap(mapped, file_stat.st_size) == 0, "Cannot unmap file");
    ASSERT(close(fd) == 0, "Cannot close file");
}
```

## Limitations

Atomic accesses to file-backed memory are not supported on systems without the `hostNativeAtomicSupported` property. This limitation applies to systems with Linux HMM (Heterogeneous Memory Management) enabled [CUDA_C_Programming_Guide:L21546-L21584].
