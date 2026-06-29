# CDP1 Zero Copy Memory

## Overview

Zero-copy memory in the context of CUDA Direct Compute and Peer-to-Peer (CDP1) operations provides a memory allocation that is accessible by both the host and the device without explicit data transfers. This mechanism ensures that the memory behaves consistently with standard global memory from a coherence perspective.

## Key Characteristics

### Coherence and Consistency

Zero-copy memory maintains identical coherence and consistency properties to global memory. This means that reads and writes to zero-copy memory are visible to both the host and the device in a manner consistent with the CUDA memory model for global memory [CUDA_C_Programming_Guide:L14405-L14414].

### Allocation Constraints

A critical constraint of zero-copy memory is that it cannot be allocated or freed by device code. Allocation and deallocation must be performed by the host. This restriction ensures that memory management remains under host control, preventing potential race conditions or inconsistencies that could arise from device-side memory management operations [CUDA_C_Programming_Guide:L14405-L14414].

## Usage Example

The following code snippet illustrates a host function launching a parent kernel, which may interact with zero-copy memory. Note that the memory pointer `data` is managed by the host before the launch [CUDA_C_Programming_Guide:L14405-L14414]:

```cpp
void host_launch(int *data) {
    parent_launch<<< 1, 256 >>>(data);
}
```

## Caveats

- **Device Code Limitations**: Device code cannot allocate or free zero-copy memory. Any attempt to do so is unsupported.
- **Fallback Behavior**: In cases where research reports fail to provide comprehensive context, deterministic fallbacks based on direct source evidence should be used. Page writers must stay close to the source evidence to ensure accuracy [CUDA_C_Programming_Guide:L14405-L14414].

## Related Terms

- Global Memory
- CUDA Direct Compute and Peer-to-Peer (CDP)
- Unified Memory
