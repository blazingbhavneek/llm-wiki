# __managed__ Memory Space Specifier

Variables marked with the `__managed__` memory space specifier, commonly referred to as "managed" variables, are allocated in a unified memory space that is accessible by both the host CPU and one or more GPUs [CUDA_C_Programming_Guide:L16682-L16762]. These variables share the same coherence and consistency behavior as dynamically allocated managed memory [CUDA_C_Programming_Guide:L16682-L16762].

## Restrictions and Constraints

Managed variables are subject to several strict limitations regarding their type, initialization, and usage contexts [CUDA_C_Programming_Guide:L16682-L16762]:

### Type Qualifications
*   **No Constant Type:** A managed variable shall not have a `const` qualified type [CUDA_C_Programming_Guide:L16682-L16762].
*   **No Reference Type:** A managed variable shall not have a reference type [CUDA_C_Programming_Guide:L16682-L16762].
*   **Non-Constant Address:** The address of a managed variable is not a constant expression [CUDA_C_Programming_Guide:L16682-L16762]. Consequently, it cannot be used as an unparenthesized id-expression argument to a `decltype()` expression [CUDA_C_Programming_Guide:L16682-L16762].

### Initialization and Lifetime
The address or value of a managed variable must not be used when the CUDA runtime may not be in a valid state [CUDA_C_Programming_Guide:L16682-L16762]. Specifically, accessing managed variables is prohibited in the following scenarios [CUDA_C_Programming_Guide:L16682-L16762]:
*   Static or dynamic initialization of an object with static or thread-local storage duration [CUDA_C_Programming_Guide:L16682-L16762].
*   Destruction of an object with static or thread-local storage duration [CUDA_C_Programming_Guide:L16682-L16762].
*   Code that executes after `exit()` has been called (e.g., functions marked with GCC's `__attribute__((destructor))`) [CUDA_C_Programming_Guide:L16682-L16762].
*   Code that executes when the CUDA runtime may not be initialized (e.g., functions marked with GCC's `__attribute__((constructor))`) [CUDA_C_Programming_Guide:L16682-L16762].

### Linkage and Scope
*   **Host Functions:** A managed variable declaration without `extern` linkage is not allowed within a function that executes on the host [CUDA_C_Programming_Guide:L16682-L16762].
*   **Device Functions:** A managed variable declaration without `extern` or `static` linkage is not allowed within a function that executes on the device [CUDA_C_Programming_Guide:L16682-L16762].

### Multi-GPU Behavior
When a CUDA program containing managed variables runs on an execution platform with multiple GPUs, the variables are allocated only once, rather than being allocated per GPU [CUDA_C_Programming_Guide:L16682-L16762].

## Examples of Usage

The following examples illustrate legal and illegal uses of managed variables [CUDA_C_Programming_Guide:L16682-L16762]:

### Legal Usage
```c
// OK: Basic managed variable declaration
__device__ __managed__ int xxx = 10;

// OK: Accessing managed variable in device code
__global__ void kern(int *ptr)
{
    assert(ptr == &xxx);    // OK
    xxx = 20;               // OK
}

// OK: Accessing managed variable in host code after synchronization
int main(void)
{
    int *ptr = &xxx;        // OK
    kern<<<1,1>>>(ptr);
    cudaDeviceSynchronize(); // OK
    xxx++;                  // OK
    
    // OK: Using parenthesized expression with decltype
    decltype((xxx)) zzz = 10;
}
```

### Illegal Usage
```c
// Error: Use of managed variable in static initialization
int *ptr = &xxx;

// Error: Use of managed variable in dynamic initialization
struct S1_t {
    int field;
    S1_t(void) : field(xxx) { };
};
S1_t temp1;

// Error: Use of managed variable in destructor of static object
struct S2_t {
    ~S2_t(void) { xxx = 10; }
};
S2_t temp2;

// Error: Const qualified type
__device__ __managed__ const int yyy = 10;

// Error: Reference type
__device__ __managed__ int &zzz = xxx;

// Error: Address of managed variable is not a constant expression
template <int *addr> struct S3_t { };
S3_t<&xxx> temp;

// Error: Managed variable used as unparenthesized argument to decltype
decltype(xxx) qqq;
```
