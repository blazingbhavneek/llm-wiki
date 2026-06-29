# Memory Synchronization Domains

Memory Synchronization Domains are a feature introduced in the Hopper architecture with CUDA 12.0 that alleviates performance degradation caused by memory fence interference [CUDA_C_Programming_Guide:L2024-L2116]. This feature allows applications to isolate memory traffic, enabling the GPU to reduce the scope of memory operations waited on by fence instructions [CUDA_C_Programming_Guide:L2024-L2116].

## Memory Fence Interference

Memory fence interference occurs when CUDA applications experience degraded performance because memory fence or flush operations wait on more transactions than those strictly necessitated by the CUDA memory consistency model [CUDA_C_Programming_Guide:L2024-L2116]. This often arises from the cumulativity of system-scope operations [CUDA_C_Programming_Guide:L2024-L2116].

For example, consider a scenario where:
1. Thread 1 writes to a device-scope atomic `a` and a managed variable `x`.
2. Thread 2 waits on `a` and then writes to a system-scope atomic `b`.
3. Thread 3 (on CPU) waits on `b` and asserts `x == 1`.

The CUDA memory consistency model guarantees that the write to `x` by Thread 1 is visible to Thread 3 before the write to `b` by Thread 2 [CUDA_C_Programming_Guide:L2024-L2116]. However, because the system-scope fence on `b` is cumulative, it must ensure that all writes visible to Thread 2 (including `x` from Thread 1) are visible to Thread 3 [CUDA_C_Programming_Guide:L2024-L2116]. Since the GPU cannot distinguish at execution time which writes are guaranteed by the source-level model versus those visible only by chance timing, it conservatively waits on a wide net of in-flight memory operations [CUDA_C_Programming_Guide:L2024-L2116].

A common example of this interference is when a kernel performing local GPU computation implicitly flushes its writes upon completion to satisfy synchronizes-with relationships [CUDA_C_Programming_Guide:L2024-L2116]. This may unnecessarily wait on slower NVLink or PCIe writes from a parallel communication kernel (e.g., NCCL) running concurrently [CUDA_C_Programming_Guide:L2024-L2116].

## Isolating Traffic with Domains

To alleviate this interference, Hopper GPUs support Memory Synchronization Domains [CUDA_C_Programming_Guide:L2024-L2116]. Each kernel launch is assigned a domain ID, and writes and fences are tagged with this ID [CUDA_C_Programming_Guide:L2024-L2116]. A fence will only order writes that match its domain's ID [CUDA_C_Programming_Guide:L2024-L2116].

By placing communication kernels in a different domain than compute kernels, the GPU can reduce the net cast of a fence operation, waiting only on relevant local traffic rather than remote communication traffic [CUDA_C_Programming_Guide:L2024-L2116].

### Synchronization Rules

When using domains, specific rules apply to synchronization:
*   **Cross-Domain:** Ordering or synchronization between distinct domains on the same GPU requires system-scope fencing [CUDA_C_Programming_Guide:L2024-L2116]. This is necessary because cumulativity is satisfied by ensuring that cross-domain traffic is flushed to the system scope ahead of time [CUDA_C_Programming_Guide:L2024-L2116].
*   **Intra-Domain:** Within a single domain, device-scope fencing remains sufficient [CUDA_C_Programming_Guide:L2024-L2116].

This mechanism modifies the definition of `thread_scope_device`, but backward compatibility is maintained because kernels default to domain 0 [CUDA_C_Programming_Guide:L2024-L2116].

## Configuration and Usage

Domains are configured using launch attributes and can be queried via device attributes [CUDA_C_Programming_Guide:L2024-L2116].

### Querying Domain Count
The number of available domains can be queried using the device attribute `cudaDevAttrMemSyncDomainCount` [CUDA_C_Programming_Guide:L2024-L2116]. Hopper architecture GPUs support 4 domains [CUDA_C_Programming_Guide:L2024-L2116]. For portability, CUDA reports a count of 1 on devices prior to Hopper [CUDA_C_Programming_Guide:L2024-L2116].

### Logical and Physical Domains
CUDA provides a layer of abstraction between logical and physical domains to ease application composition [CUDA_C_Programming_Guide:L2024-L2116].
*   **Logical Domains:** Defined by `cudaLaunchMemSyncDomainDefault` and `cudaLaunchMemSyncDomainRemote` [CUDA_C_Programming_Guide:L2024-L2116]. The remote domain is intended for kernels performing remote memory access to isolate their traffic from local kernels [CUDA_C_Programming_Guide:L2024-L2116].
*   **Physical Domains:** The actual hardware domains (0-3 on Hopper) [CUDA_C_Programming_Guide:L2024-L2116].

### Launch Attributes
Domains are controlled via two main attributes:
1.  **`cudaLaunchAttributeMemSyncDomain`**: Selects the logical domain for a specific kernel launch (e.g., `cudaLaunchKernelEx`) [CUDA_C_Programming_Guide:L2024-L2116].
2.  **`cudaLaunchAttributeMemSyncDomainMap`**: Maps logical domains to physical domains [CUDA_C_Programming_Guide:L2024-L2116]. This can be set at the stream level using `cudaStreamSetAttribute` [CUDA_C_Programming_Guide:L2024-L2116].

The default mapping maps the default logical domain to physical domain 0 and the remote logical domain to physical domain 1 (on GPUs with more than 1 domain) [CUDA_C_Programming_Guide:L2024-L2116].

### Usage Patterns
*   **Stream-Level Mapping:** Applications can partition parallel streams by mapping different logical domains to different physical domains per stream [CUDA_C_Programming_Guide:L2024-L2116].
*   **Library Integration:** Libraries like NCCL 2.16+ tag launches with the remote domain, providing beneficial use patterns out of the box without requiring changes in higher-level frameworks [CUDA_C_Programming_Guide:L2024-L2116].

### CUDA Graphs
These attributes are exposed uniformly on CUDA streams, individual launches using `cudaLaunchKernelEx`, and kernel nodes in CUDA graphs [CUDA_C_Programming_Guide:L2024-L2116]. When a graph is captured, both attributes are copied to the graph nodes [CUDA_C_Programming_Guide:L2024-L2116]. Graphs take both attributes from the node itself, meaning domain-related attributes set on the stream into which the graph is launched are not used during the graph's execution [CUDA_C_Programming_Guide:L2024-L2116].

### Example Code

Launching a kernel with the remote logical domain:
```cpp
cudaLaunchAttribute domainAttr;
domainAttr.id = cudaLaunchAttrMemSyncDomain;
domainAttr.val = cudaLaunchMemSyncDomainRemote;
cudaLaunchConfig_t config;
// Fill out other config fields
config.attrs = &domainAttr;
config.numAttrs = 1;
cudaLaunchKernelEx(&config, myKernel, kernelArg1, kernelArg2...);
```

Setting a mapping for a stream (default mapping illustration):
```cpp
cudaLaunchAttributeValue mapAttr;
mapAttr.memSyncDomainMap.default_ = 0;
mapAttr.memSyncDomainMap.remote = 1;
cudaStreamSetAttribute(stream, cudaLaunchAttributeMemSyncDomainMap, &mapAttr);
```

Mapping different streams to different physical domains:
```cpp
cudaLaunchAttributeValue mapAttr;
mapAttr.memSyncDomainMap.default_ = 0;
mapAttr.memSyncDomainMap.remote = 0;
cudaStreamSetAttribute(streamA, cudaLaunchAttributeMemSyncDomainMap, &mapAttr);
mapAttr.memSyncDomainMap.default_ = 1;
mapAttr.memSyncDomainMap.remote = 1;
cudaStreamSetAttribute(streamB, cudaLaunchAttributeMemSyncDomainMap, &mapAttr);
```
