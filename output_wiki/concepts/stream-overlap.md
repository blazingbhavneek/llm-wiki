# Stream Overlap

Stream overlap refers to the ability of a GPU device to execute operations from different CUDA streams concurrently. The extent of this overlap is determined by both the hardware capabilities of the device and the specific sequence in which commands are issued to the streams.

## Factors Influencing Overlap

The amount of execution overlap between two streams depends on the order in which the commands are issued to each stream and whether or not the device supports [Overlap of Data Transfer and Kernel Execution](concept/kernel-data-overlap), [Concurrent Kernel Execution](concept/concurrent-kernels), and/or [Concurrent Data Transfers](concept/concurrent-transfers) [CUDA_C_Programming_Guide:L2253-L2274].

### Device Capabilities

1.  **Concurrent Data Transfers**: On devices that support concurrent data transfers, memory operations from different streams can overlap with each other. For example, a memory copy from host to device in one stream can overlap with a memory copy from device to host in another stream [CUDA_C_Programming_Guide:L2253-L2274].
2.  **Overlap of Data Transfer and Kernel Execution**: If the device supports this feature, memory transfers can overlap with kernel execution. This allows a kernel in one stream to execute while a memory transfer in another stream is ongoing [CUDA_C_Programming_Guide:L2253-L2274].
3.  **Concurrent Kernel Execution**: Devices that support this feature can execute kernels from different streams simultaneously [CUDA_C_Programming_Guide:L2253-L2274].

### Impact of Command Order

The order in which commands are issued significantly affects overlap, particularly on devices with limited concurrency capabilities.

*   **Devices without Concurrent Data Transfers**: On such devices, streams may not overlap at all if the command order forces serialization. For instance, if a memory copy from device to host is issued to stream[0] and a memory copy from host to device is issued to stream[1] *after* the first copy, the second copy can only start once the first has completed [CUDA_C_Programming_Guide:L2253-L2274].
*   **Optimized Command Order**: By restructuring code to issue all host-to-device transfers first, followed by kernel launches, and then device-to-host transfers, overlap can be maximized. In this pattern, a host-to-device transfer in stream[1] can overlap with a kernel launch in stream[0] (assuming the device supports overlap of data transfer and kernel execution) [CUDA_C_Programming_Guide:L2253-L2274].

## Example Scenario

Consider a code sample involving two streams where memory copies and kernels are launched. If the device supports concurrent data transfers, the memory copy from host to device issued to stream[1] can overlap with both the memory copy from device to host issued to stream[0] and the kernel launch issued to stream[0] (assuming the device also supports overlap of data transfer and kernel execution) [CUDA_C_Programming_Guide:L2253-L2274].

Conversely, if the device does not support concurrent data transfers, these operations may not overlap at all due to the serialization imposed by the command order [CUDA_C_Programming_Guide:L2253-L2274].
