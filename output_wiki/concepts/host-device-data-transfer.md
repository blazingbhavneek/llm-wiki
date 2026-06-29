# Host-Device Data Transfer Optimization

Applications should strive to minimize data transfer between the host and the device to maximize performance [CUDA_C_Programming_Guide:L6395-L6406]. This section outlines strategies to reduce transfer overhead and improve bandwidth utilization.

## Minimizing Transfer Volume

One effective strategy to reduce data transfer is to move more computation from the host to the device. This may involve executing kernels that do not expose sufficient parallelism for full device efficiency, if doing so avoids copying intermediate data structures between host and device memory [CUDA_C_Programming_Guide:L6395-L6406]. Intermediate data can be created, operated on, and destroyed entirely within device memory without ever being mapped by the host or copied back [CUDA_C_Programming_Guide:L6395-L6406].

## Batching Transfers

Due to the fixed overhead associated with each transfer operation, batching many small transfers into a single large transfer consistently yields better performance than executing transfers individually [CUDA_C_Programming_Guide:L6395-L6406].

## Page-Locked Host Memory

On systems with a front-side bus, higher performance for data transfers between host and device is achieved by using page-locked host memory [CUDA_C_Programming_Guide:L6395-L6406]. Page-locked memory prevents the operating system from swapping the memory to disk, allowing for direct memory access (DMA) transfers [CUDA_C_Programming_Guide:L6395-L6406].

## Mapped Memory

Mapped page-locked memory allows data transfers to be performed implicitly when a kernel accesses the mapped memory, eliminating the need to explicitly allocate device memory and copy data between host and device [CUDA_C_Programming_Guide:L6395-L6406].

### Performance Considerations

For mapped memory to provide a performance benefit over explicit copies, the following conditions should be met:
*   Memory accesses must be coalesced, similar to accesses to global memory [CUDA_C_Programming_Guide:L6395-L6406].
*   The mapped memory should be read or written only once [CUDA_C_Programming_Guide:L6395-L6406].

If these conditions are satisfied, using mapped page-locked memory can be a win for performance [CUDA_C_Programming_Guide:L6395-L6406].

## Integrated Systems

On integrated systems where device memory and host memory are physically the same, explicit copies between host and device memory are superfluous [CUDA_C_Programming_Guide:L6395-L6406]. In such cases, mapped page-locked memory should be used instead [CUDA_C_Programming_Guide:L6395-L6406].

Applications can query whether a device is integrated by checking if the integrated device property is equal to 1 [CUDA_C_Programming_Guide:L6395-L6406].
