# Synchronous Calls

When a synchronous function is called, control is not returned to the host thread before the device has completed the requested task [CUDA_C_Programming_Guide:L3449-L3452]. 

Whether the host thread will then yield, block, or spin can be specified by calling `cudaSetDeviceFlags()` with some specific flags before any other CUDA call is performed by the host thread [CUDA_C_Programming_Guide:L3449-L3452].
