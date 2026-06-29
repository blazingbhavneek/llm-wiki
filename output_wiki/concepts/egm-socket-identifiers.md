# EGM Socket Identifiers (NUMA)

## Overview

EGM (Explicit Global Memory) relies on NUMA (Non-Uniform Memory Access) socket identifiers to determine optimal memory placement and access patterns. In NUMA architectures, system memory is divided into multiple nodes, where each node consists of its own processors and memory. The operating system assigns a unique identifier, known as the `numaID`, to each node [CUDA_C_Programming_Guide:L22222-L22222].

## EGM Usage

EGM uses the NUMA node identifier assigned by the operating system to associate devices with their closest host node [CUDA_C_Programming_Guide:L22224-L22224]. It is important to distinguish this identifier from the device ordinal; the NUMA ID specifically reflects the proximity to the host node rather than the device's index within a list [CUDA_C_Programming_Guide:L22224-L22224].

## Accessing the Identifier

Users can retrieve the host node's NUMA identifier for a specific device by calling `cuDeviceGetAttribute` with the `CU_DEVICE_ATTRIBUTE_HOST_NUMA_ID` attribute type [CUDA_C_Programming_Guide:L22224-L22224].

### Example Code

The following code snippet demonstrates how to obtain the NUMA ID for a given device ordinal:

```c
int numaId;
cuDeviceGetAttribute(&numaId, CU_DEVICE_ATTRIBUTE_HOST_NUMA_ID, deviceOrdinal);
```

[CUDA_C_Programming_Guide:L22226-L22228]
