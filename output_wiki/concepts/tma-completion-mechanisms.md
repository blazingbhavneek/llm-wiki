# TMA Completion Mechanisms

Tensor Memory Accelerator (TMA) data transfers are asynchronous, allowing the initiating thread to continue computing while the hardware asynchronously copies the data [CUDA_C_Programming_Guide:L10228-L10233]. Whether a data transfer occurs asynchronously in practice depends on the hardware implementation and may change in future versions [CUDA_C_Programming_Guide:L10228-L10233].

Bulk-asynchronous operations use specific completion mechanisms to signal that they have finished [CUDA_C_Programming_Guide:L10228-L10233]. The mechanism used depends on the direction of the data transfer:

## Global-to-Shared Reads
When an operation reads from global memory to shared memory, any thread in the block can wait for the data to be readable in shared memory by waiting on a Shared Memory Barrier (mbarrier) [CUDA_C_Programming_Guide:L10228-L10233].

## Shared-to-Global/Shared Writes
When a bulk-asynchronous operation writes data from shared memory to global memory or distributed shared memory, only the initiating thread can wait for the operation to have completed [CUDA_C_Programming_Guide:L10228-L10233]. This is accomplished using a bulk async-group based completion mechanism [CUDA_C_Programming_Guide:L10228-L10233].

## Supported Source-Destination Pairs
Table 8 details the supported source-destination pairs and their corresponding completion mechanisms for TMA operations. An empty cell indicates that a source-destination pair is not supported [CUDA_C_Programming_Guide:L10228-L10233].

**Table 8: Asynchronous copies with possible source and destinations memory spaces and completion mechanisms**

| Direction | Destination | Source | Completion mechanism (Bulk-asynchronous copy / TMA) |
| :--- | :--- | :--- | :--- |
| Global | Global | | |
| Global | Shared::cta | | Bulk async-group |
| Shared::cta | Global | Mbarrier | |
| Shared::cluster | Global | | Mbarrier (multicast) |
| Shared::cta | Shared::cluster | | Mbarrier |
| Shared::cta | Shared::cta | | |

*Note: The table above reflects the "Bulk-asynchronous copy (TMA)" column from the source documentation. For standard asynchronous copies, the completion mechanisms may differ (e.g., Async-group, mbarrier for Global to Shared::cta) [CUDA_C_Programming_Guide:L10228-L10233].*

Completion mechanisms and supported operations are also described in the PTX ISA [CUDA_C_Programming_Guide:L10228-L10233].
