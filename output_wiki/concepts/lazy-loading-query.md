# Querying Lazy Loading Status

To determine whether the user has enabled Lazy Loading for CUDA modules, the `cuModuleGetLoadingMode` function can be used. This function retrieves the current loading mode setting.

## Prerequisites

CUDA must be initialized before calling this function. This is typically done by calling `cuInit`.

## API Usage

The function signature is:

```cpp
CUresult cuModuleGetLoadingMode(CUmoduleLoadingMode* mode)
```

- `mode`: A pointer to a `CUmoduleLoadingMode` variable that will receive the current loading mode.

## Example

The following code snippet demonstrates how to query the lazy loading status after initializing the CUDA driver:

```cpp
#include "cuda.h"
#include "assert.h"
#include "iostream"

int main() {
    CUmoduleLoadingMode mode;

    // Initialize CUDA
    assert(CUDA_SUCCESS == cuInit(0));
    
    // Query the loading mode
    assert(CUDA_SUCCESS == cuModuleGetLoadingMode(&mode));

    // Print the result
    std::cout << "CUDA Module Loading Mode is " << ((mode == CU_MODULE_LAZY_LOADING) ? "lazy" : "eager") << std::endl;

    return 0;
}
```

In this example, the program checks if the `mode` variable equals `CU_MODULE_LAZY_LOADING` to determine if lazy loading is active.

[CUDA_C_Programming_Guide:L22136-L22158]
