
## Level Zero

Level Zero is the low-level interface that enables oneAPI libraries to exploit the hardware capabilities of target devices. This section provides an insight into the architectural design followed in the Intel® Graphics Compute Runtime for oneAPI Level Zero. Implementation details and optimization guidelines are explained, as well as a description of the different features available for the different supported platforms.

• Immediate Command Lists

## Immediate Command Lists

## Introduction

Immediate command lists is a feature provided by Level-Zero specification to allow for very low latency submission usage models. In this scheme, commands appended on the command list such as launching a kernel or performing a memory copy are immediately submitted to the device for execution. This is different from a regular command list where multiple commands can be stitched and submitted together for execution .

Distinctions between an immediate command list compared to a regular command list include (but not limited to) the following:

• An immediate command list is an implicit command queue and is therefore created using a command queue descriptor.

• Commands appended to an immediate command list are submitted for execution immediately on the device.

• Immediate command lists are not required to be closed or reset.

• Synchronization of immediate command lists cannot be performed via zeCommandQueueSynchronize or zeFenceHostSynchronize as there is no command queue handle associated with the immediate command list. Recommendation is to use events to confirm commands submitted to the immediate command list have completed.

Since the intention of immediate command lists is to primarily provide a razor thin submission interface to the device, they are well suited to be used in workloads which have tendency to launch small or short running kernels and also need to run multiple iterations of such kernels. Examples of workloads with such characteristics can be found in HPC environments and also ML/DL frameworks.

## Programming Model

Following code shows how to create an immediate command list and submitting a kernel with it. Synchronization is achieved by querying the event status.

```matlab
ze_command_queue_desc_t cmdQueueDesc = {ZE_STRUCTURE_TYPE_COMMAND_QUEUE_DESC};
cmdQueueDesc.pNext = nullptr;
cmdQueueDesc.flags = 0;
cmdQueueDesc.priority = ZE_COMMAND_QUEUE_PRIORITY_NORMAL;
cmdQueueDesc.ordinal = queueGroupOrdinal;
cmdQueueDesc.index = 0;
```

```cpp
cmdQueueDesc.mode = ZE_COMMAND_QUEUE_MODE_ASYNCHRONOUS;
zeCommandListCreateImmediate(context, device, &cmdQueueDesc, &cmdList);

zeCommandListAppendLaunchKernel(cmdList, kernel, &dispatchTraits,
                          events[0], 0, nullptr);
// If Async mode, use event for sync
zeEventHostSynchronize(events[0], std::numeric_limits<uint64_t>::max() - 1);
```

Immediate command lists may also be used to implement in-order queues. In this case, commands submitted to the list are chained together using events, as seen below.

```cpp
zeCommandListAppendMemoryCopy(cmdList, deviceBuffer, hostBuffer, allocSize,
                          events[0],
                          0, nullptr);

zeCommandListAppendMemoryCopy(cmdList, stackBuffer, deviceBuffer, allocSize,
                          events[1],
                          1,
                          &events[0]);

zeEventHostSynchronize(events[1], std::numeric_limits<uint64_t>::max() - 1));
```

As with regular lists, immediate command lists may also be synchronous. In this case, synchronization is performed implicitly and each command submitted to the list is immediately submitted, and is guaranteed to have completed upon return from the call.

```txt
ze_command_queue_desc_t cmdQueueDesc = {ZE_STRUCTURE_TYPE_COMMAND_QUEUE_DESC};
cmdQueueDesc.pNext = nullptr;
cmdQueueDesc.flags = 0;
cmdQueueDesc.priority = ZE_COMMAND_QUEUE_PRIORITY_NORMAL;
cmdQueueDesc.ordinal = queueGroupOrdinal;
cmdQueueDesc.index = 0;
cmdQueueDesc.mode = ZE_COMMAND_QUEUE_MODE_SYNCHRONOUS;
zeCommandListCreateImmediate(context, device, &cmdQueueDesc, &cmdList);

zeCommandListAppendLaunchKernel(cmdList, kernel, &dispatchTraits,
                                nullptr, 0, nullptr);

// At this point, kernel has been executed
```

For more code samples, please refer compute-benchmarks repository https://github.com/intel/compute benchmarks. Scenarios such as create\_command\_list\_immediate\_l0.cpp and execute\_command\_list\_immediate\_l0.cpp serve as good starting points.
