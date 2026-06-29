# CUDA Runtime Memory Footprint

The CUDA device runtime system software reserves a portion of device memory for various management purposes. A primary component of this reservation is dedicated to tracking pending grid launches [CUDA_C_Programming_Guide:L14224-L14229].

## Configuration

Configuration controls are available to reduce the size of this memory reservation. However, reducing the footprint may result in certain launch limitations [CUDA_C_Programming_Guide:L14224-L14229]. For specific details on these controls and their implications, refer to the Configuration Options section of the documentation [CUDA_C_Programming_Guide:L14224-L14229].
