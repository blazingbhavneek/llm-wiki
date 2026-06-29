# Runtime Initialization

## Overview
The CUDA runtime manages global state that is initialized during host program initiation and destroyed during termination. As of CUDA 12.0, explicit initialization is required to ensure proper error handling and timing isolation [CUDA_C_Programming_Guide:L1236-L1248].

## Initialization Mechanisms
### Explicit Initialization (CUDA 12.0+)
In CUDA 12.0 and later, the `cudaInitDevice()` and `cudaSetDevice()` functions explicitly initialize the runtime and the primary context associated with the specified device [CUDA_C_Programming_Guide:L1236-L1248]. 

*   **cudaSetDevice()**: This function now explicitly initializes the runtime after changing the current device for the host thread. Previous versions of CUDA delayed runtime initialization on the new device until the first runtime call was made after `cudaSetDevice()` [CUDA_C_Programming_Guide:L1236-L1248].
*   **Error Checking**: Because initialization happens explicitly within `cudaSetDevice()`, it is critical to check the return value of this function for initialization errors [CUDA_C_Programming_Guide:L1236-L1248].

### Implicit Initialization
If `cudaInitDevice()` or `cudaSetDevice()` are not called, the runtime will implicitly use device 0 and self-initialize as needed to process other runtime API requests [CUDA_C_Programming_Guide:L1236-L1248]. Developers must account for this implicit initialization when timing runtime function calls or interpreting the error code from the first call into the runtime [CUDA_C_Programming_Guide:L1236-L1248].

### Historical Context (Pre-CUDA 12.0)
Before CUDA 12.0, `cudaSetDevice()` did not initialize the runtime. Applications often used the no-op runtime call `cudaFree(0)` to isolate runtime initialization from other API activity, both for timing and error handling purposes [CUDA_C_Programming_Guide:L1236-L1248].

## Primary Context
The runtime creates a CUDA context for each device in the system [CUDA_C_Programming_Guide:L1236-L1248]. This context is the primary context for the device and is initialized at the first runtime function that requires an active context on that device [CUDA_C_Programming_Guide:L1236-L1248].

*   **Sharing**: The primary context is shared among all host threads of the application [CUDA_C_Programming_Guide:L1236-L1248].
*   **JIT Compilation**: As part of context creation, device code is just-in-time (JIT) compiled if necessary and loaded into device memory [CUDA_C_Programming_Guide:L1236-L1248]. This process happens transparently [CUDA_C_Programming_Guide:L1236-L1248].
*   **Driver API Interoperability**: The primary context of a device can be accessed from the driver API if needed for interoperability [CUDA_C_Programming_Guide:L1236-L1248].

## Context Lifecycle
*   **Creation**: The primary context is created upon the first runtime function call requiring an active context on the device [CUDA_C_Programming_Guide:L1236-L1248].
*   **Destruction**: When a host thread calls `cudaDeviceReset()`, it destroys the primary context of the device that the host thread currently operates on [CUDA_C_Programming_Guide:L1236-L1248].
*   **Re-creation**: The next runtime function call made by any host thread that has the device as current will create a new primary context for that device [CUDA_C_Programming_Guide:L1236-L1248].

## Error Handling and Exceptions
*   **Non-Initializing Functions**: Runtime functions from the error handling and version management sections of the reference manual do not initialize the runtime [CUDA_C_Programming_Guide:L1236-L1248].
*   **Undefined Behavior**: The CUDA interfaces use global state that is initialized during host program initiation and destroyed during host program termination. The CUDA runtime and driver cannot detect if this state is invalid. Therefore, using any CUDA interfaces (implicitly or explicitly) during program initiation or termination after `main()` returns will result in undefined behavior [CUDA_C_Programming_Guide:L1236-L1248].

## See Also
*   [Context Creation]
*   [Just-in-Time Compilation]
*   [Interoperability between Runtime and Driver APIs]
*   [Device Selection]
