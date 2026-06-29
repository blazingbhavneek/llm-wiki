# cuGraphAddMemsetNode

`cuGraphAddMemsetNode` is a function used to add a memset node to a CUDA graph. A key constraint of this API is that it does not work with memory allocated via the stream ordered allocator [CUDA_C_Programming_Guide:L15872-L15875].

Despite this limitation, memsets performed on allocations created by the stream ordered allocator can still be stream captured [CUDA_C_Programming_Guide:L15872-L15875].

## See Also

- CUDA Graphs
- Stream Ordered Allocator
