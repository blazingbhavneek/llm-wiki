# CUDA Driver API

The CUDA Driver API is a lower-level C Application Programming Interface (API) upon which the CUDA Runtime API is built [CUDA_C_Programming_Guide:L1115-L1115]. While most applications utilize the Runtime API for its concise code and implicit management of resources, the Driver API is accessible to applications that require an additional level of control over the CUDA device [CUDA_C_Programming_Guide:L1115-L1115].

## Core Concepts

The Driver API exposes lower-level concepts that map to host-side execution models:

*   **CUDA Contexts**: These serve as the analogue of host processes for the device [CUDA_C_Programming_Guide:L1115-L1115].
*   **CUDA Modules**: These serve as the analogue of dynamically loaded libraries for the device [CUDA_C_Programming_Guide:L1115-L1115].

When using the CUDA Runtime API, context and module management are handled implicitly, whereas the Driver API exposes these mechanisms explicitly to the application [CUDA_C_Programming_Guide:L1115-L1115].

## Interoperability

The CUDA Runtime API is interoperable with the Driver API [CUDA_C_Programming_Guide:L1115-L1115]. Consequently, applications that require specific features from the Driver API can default to using the Runtime API for general operations and invoke the Driver API only where necessary [CUDA_C_Programming_Guide:L1115-L1115].

## Driver Entry Point Access

The Driver API includes mechanisms for accessing function entry points dynamically, primarily through `cuGetProcAddress` [CUDA_C_Programming_Guide:L667-L683]. This section of the API documentation covers:

*   **Introduction**: Overview of driver entry point access [CUDA_C_Programming_Guide:L667-L683].
*   **Driver Function Typedefs**: Definitions for function pointers [CUDA_C_Programming_Guide:L667-L683].
*   **Driver Function Retrieval**: Methods for retrieving functions, including:
    *   Using the Driver API directly [CUDA_C_Programming_Guide:L667-L683].
    *   Using the Runtime API to access driver functions [CUDA_C_Programming_Guide:L667-L683].
    *   Retrieving per-thread default stream versions [CUDA_C_Programming_Guide:L667-L683].
    *   Accessing new CUDA features [CUDA_C_Programming_Guide:L667-L683].
*   **Guidelines**: Best practices for using `cuGetProcAddress`, including specific guidelines for Runtime API usage [CUDA_C_Programming_Guide:L667-L683].
*   **Error Handling**: Determining failure reasons for `cuGetProcAddress` calls [CUDA_C_Programming_Guide:L667-L683].

## API Structure

The Driver API documentation is structured into the following primary sections [CUDA_C_Programming_Guide:L667-L683]:

1.  **Context**: Management of CUDA contexts [CUDA_C_Programming_Guide:L667-L683].
2.  **Module**: Loading and managing device modules [CUDA_C_Programming_Guide:L667-L683].
3.  **Kernel Execution**: Launching and managing kernel execution [CUDA_C_Programming_Guide:L667-L683].
4.  **Interoperability**: Details on interacting between the Runtime and Driver APIs [CUDA_C_Programming_Guide:L667-L683].
5.  **Driver Entry Point Access**: Dynamic function retrieval and management [CUDA_C_Programming_Guide:L667-L683].

For a complete description of the Driver API, refer to the CUDA reference manual [CUDA_C_Programming_Guide:L1115-L1115].
