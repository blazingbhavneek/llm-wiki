# CUDA Dynamic Parallelism (CDP1) Memory Footprint

The device runtime system software in CUDA Dynamic Parallelism version 1 (CDP1) reserves memory for various management purposes. This reserved memory is critical for the correct operation of nested kernel launches and synchronization [CUDA_C_Programming_Guide:L14918-L14925].

## Reserved Memory Components

The system utilizes two primary memory reservations:

1.  **Parent-Grid State Synchronization**: One reservation is used for saving parent-grid state during synchronization operations [CUDA_C_Programming_Guide:L14918-L14925].
2.  **Pending Launch Tracking**: A second reservation is dedicated to tracking pending grid launches [CUDA_C_Programming_Guide:L14918-L14925].

## Memory Allocation and Impact

The majority of the reserved memory is allocated as a backing store for parent kernel state, which is required when synchronizing on a child launch [CUDA_C_Programming_Guide:L14918-L14925].

### Capacity Requirements

The memory required for parent kernel state must conservatively support storing the state for the maximum number of live threads possible on the device [CUDA_C_Programming_Guide:L14918-L14925]. Consequently:

*   Each parent generation at which `cudaDeviceSynchronize()` is callable may require up to **860MB** of device memory [CUDA_C_Programming_Guide:L14918-L14925].
*   This requirement depends on the specific device configuration [CUDA_C_Programming_Guide:L14918-L14925].
*   This memory is unavailable for program use, even if it is not fully consumed [CUDA_C_Programming_Guide:L14918-L14925].

## Configuration

Configuration controls are available to reduce the size of these memory reservations. However, reducing the reservation size comes with certain launch limitations [CUDA_C_Programming_Guide:L14918-L14925]. For details on these controls, see Configuration Options (CDP1) [CUDA_C_Programming_Guide:L14918-L14925].

## Note on CDP2

For the memory footprint details specific to CUDA Dynamic Parallelism version 2 (CDP2), refer to the CDP2 version of the document [CUDA_C_Programming_Guide:L14918-L14925].
