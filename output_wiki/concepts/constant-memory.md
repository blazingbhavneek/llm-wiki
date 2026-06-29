# Constant Memory

Constant memory is a specialized memory space that resides in device memory and is cached in the constant cache [CUDA_C_Programming_Guide:L6494-L6501].

When a read request is issued, the system splits it into as many separate requests as there are different memory addresses in the initial request [CUDA_C_Programming_Guide:L6494-L6501]. This splitting decreases throughput by a factor equal to the number of separate requests generated [CUDA_C_Programming_Guide:L6494-L6501].

The resulting requests are serviced at the throughput of the constant cache if there is a cache hit, or at the throughput of device memory otherwise [CUDA_C_Programming_Guide:L6494-L6501].
