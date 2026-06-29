# System-Allocated Memory: In-depth Examples

Systems with full CUDA Unified Memory support allow the device to access any memory owned by the host process interacting with the device [CUDA_C_Programming_Guide:L21411-L21545]. This section illustrates advanced use-cases for system-allocated memory, demonstrating how various memory allocation strategies and variable scopes can be accessed from CUDA kernels [CUDA_C_Programming_Guide:L21411-L21545].

The following examples utilize a simple kernel that prints the first 8 characters of an input character array to the standard output stream [CUDA_C_Programming_Guide:L21411-L21545]:

```c
__global__ void kernel(const char* type, const char* data) {
    static const int n_char = 8;
    printf("%s - first %d characters: ", type, n_char);
    for (int i = 0; i < n_char; ++i) printf("%c", data[i]);
    printf("\n");
}
```

## Malloc

Memory allocated via standard host `malloc` can be accessed directly by the device [CUDA_C_Programming_Guide:L21411-L21545]. The host copies data into the allocated heap memory and passes the pointer to the kernel [CUDA_C_Programming_Guide:L21411-L21545]:

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

## Managed Memory

Using `cudaMallocManaged` allocates memory that is automatically managed by the CUDA runtime, allowing seamless access from both host and device [CUDA_C_Programming_Guide:L21411-L21545]:

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

## Stack Variables

Stack variables defined within a host function can be passed to the device kernel, provided they are accessed via a pointer [CUDA_C_Programming_Guide:L21411-L21545]:

```c
void test_stack() {
    const char test_string[] = "Hello World";
    kernel<<<1, 1>>>("stack", test_string);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

## File-Scope Static Variables

Variables declared with `static` at file scope are accessible by the device when passed as arguments [CUDA_C_Programming_Guide:L21411-L21545]:

```c
void test_static() {
    static const char test_string[] = "Hello World";
    kernel<<<1, 1>>>("static", test_string);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

## Global-Scope Variables

Global-scope variables can also be accessed by the device, but with specific constraints regarding direct access [CUDA_C_Programming_Guide:L21411-L21545].

### Direct Access Limitation

Global variables without the `__managed__` specifier are declared as `__host__`-only by default. Consequently, most compilers will not allow these variables to be accessed directly in device code (`__device__` or `__global__`) [CUDA_C_Programming_Guide:L21411-L21545].

For example, the following kernel will cause a compilation error:

```cpp
// this variable is declared at global scope
int global_variable;

__global__ void kernel_uncompilable() {
    // this causes a compilation error: global (__host__) variables must not
    // be accessed from __device__ / __global__ code
    printf("%d\n", global_variable);
}
```

### Indirect Access via Pointer

On systems where `pageableMemoryAccess` is set to 1, the address of a global variable can be passed to the kernel, allowing the device to dereference it [CUDA_C_Programming_Guide:L21411-L21545]. The correct approach is to pass the address of the global variable as an argument:

```cpp
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

## Global-Scope Extern Variables

Global-scope `extern` variables can be accessed by the device, even if the memory is owned and managed by a third-party library that does not interact with CUDA [CUDA_C_Programming_Guide:L21411-L21545].

The `extern` variable is declared in the current translation unit and defined in a separate file (potentially a non-CUDA file) [CUDA_C_Programming_Guide:L21411-L21545]:

```c
// declared in separate file, see below
extern char* ext_data;

void test_extern() {
    kernel<<<1, 1>>>("extern", ext_data);
    ASSERT(cudaDeviceSynchronize() == cudaSuccess,
        "CUDA failed with '%s'", cudaGetErrorString(cudaGetLastError()));
}
```

The separate file manages the memory lifecycle using constructor and destructor attributes:

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

## Summary of Access Patterns

*   **Stack, File-Scope Static, and Global-Scope Variables**: These can only be accessed by the GPU through a pointer [CUDA_C_Programming_Guide:L21411-L21545]. Direct access in device code is restricted for non-managed global variables [CUDA_C_Programming_Guide:L21411-L21545].
*   **Extern Variables**: Can be accessed by the device even if the underlying memory is managed by external libraries unrelated to CUDA [CUDA_C_Programming_Guide:L21411-L21545].
*   **Managed Memory**: Provides the most seamless integration, handled automatically by the CUDA runtime [CUDA_C_Programming_Guide:L21411-L21545].
*   **Host Malloc**: Standard host-allocated memory is accessible to the device under full Unified Memory support [CUDA_C_Programming_Guide:L21411-L21545].

All examples require synchronization (`cudaDeviceSynchronize`) to ensure the kernel completes before proceeding or freeing memory [CUDA_C_Programming_Guide:L21411-L21545].
