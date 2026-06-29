# CUDA Dynamic Parallelism (CDP1) Including Device Runtime API

When working with CUDA Dynamic Parallelism, developers utilize the device runtime API to launch kernels from within other kernels. Similar to the host-side runtime API, prototypes for the CUDA device runtime API are included automatically during program compilation. There is no need to include `cuda_device_runtime_api.h` explicitly [CUDA_C_Programming_Guide:L14797-L14798].

This automatic inclusion simplifies the development process by ensuring that necessary function declarations are available without manual header management.
