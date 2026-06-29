# Device Launch Mechanics

Device graphs can be launched from both the host and the device via `cudaGraphLaunch()`, which has the same signature on the device as on the host [CUDA_C_Programming_Guide:L2927-L2932]. Device graphs are launched via the same handle on the host and the device [CUDA_C_Programming_Guide:L2927-L2932].

When launching a device graph from the device, it must be launched from another graph [CUDA_C_Programming_Guide:L2927-L2932]. Device-side graph launch is per-thread, and multiple launches may occur from different threads at the same time [CUDA_C_Programming_Guide:L2927-L2932]. Consequently, the user will need to select a single thread from which to launch a given graph [CUDA_C_Programming_Guide:L2927-L2932].
