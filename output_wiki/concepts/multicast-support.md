# Multicast Support

Multicast Object Management APIs provide a mechanism for applications to create Multicast Objects, which, in combination with Virtual Memory Management APIs, allow leveraging NVLINK SHARP on supported NVLINK-connected GPUs connected via NVSWITCH [CUDA_C_Programming_Guide:L15256-L15277]. NVLINK SHARP enables CUDA applications to utilize in-fabric computing to accelerate operations such as broadcast and reductions between GPUs [CUDA_C_Programming_Guide:L15256-L15277].

## Architecture and Teams

Multiple NVLINK-connected GPUs form a **Multicast Team** [CUDA_C_Programming_Guide:L15256-L15277]. Each GPU in the team backs up a Multicast Object with physical memory, resulting in N physical replicas for a team of N GPUs, with each replica local to its participating GPU [CUDA_C_Programming_Guide:L15256-L15277]. The `multimem` PTX instructions operate on mappings of Multicast Objects and work with all replicas of the object [CUDA_C_Programming_Guide:L15256-L15277].

## Workflow

To work with Multicast Objects, an application must follow these steps [CUDA_C_Programming_Guide:L15256-L15277]:

1.  **Query Multicast Support**: Determine if the hardware supports multicast operations.
2.  **Create a Multicast Handle**: Use `cuMulticastCreate` to generate a handle for the multicast object [CUDA_C_Programming_Guide:L15256-L15277].
3.  **Share the Handle**: Export the Multicast Handle using `cuMemExportToShareableHandle` and share it with all processes controlling GPUs that should participate in the Multicast Team [CUDA_C_Programming_Guide:L15256-L15277].
4.  **Add Devices**: Use `cuMulticastAddDevice` to add all participating GPUs to the Multicast Team [CUDA_C_Programming_Guide:L15256-L15277].
5.  **Bind Memory**: For each participating GPU, bind physical memory (allocated via `cuMemCreate`) to the Multicast Handle [CUDA_C_Programming_Guide:L15256-L15277]. All devices must be added to the Multicast Team before binding memory on any device [CUDA_C_Programming_Guide:L15256-L15277].
6.  **Map and Set Access**: Reserve an address range, map the Multicast Handle, and set access rights similar to regular Unicast mappings. Unicast and Multicast mappings to the same physical memory are supported [CUDA_C_Programming_Guide:L15256-L15277]. Developers should refer to the Virtual Aliasing Support section to ensure consistency between multiple mappings to the same physical memory [CUDA_C_Programming_Guide:L15256-L15277].
7.  **Execute**: Use `multimem` PTX instructions with the multicast mappings [CUDA_C_Programming_Guide:L15256-L15277].

## Usage and Examples

The `multi_node_p2p` example in the Multi GPU Programming Models GitHub repository provides a complete implementation using Fabric Memory and Multicast Objects to leverage NVLINK SHARP [CUDA_C_Programming_Guide:L15256-L15277]. This example demonstrates how higher-level programming models like NVSHMEM operate internally within a (multinode) NVLINK domain [CUDA_C_Programming_Guide:L15256-L15277].

This API is primarily intended for developers of libraries such as NCCL or NVSHMEM [CUDA_C_Programming_Guide:L15256-L15277]. Application developers are generally advised to use higher-level interfaces like MPI, NCCL, or NVSHMEM instead of interacting directly with the Multicast Object Management APIs [CUDA_C_Programming_Guide:L15256-L15277].
