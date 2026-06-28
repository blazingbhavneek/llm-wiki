
## Synchronization among Threads in a Kernel

There are a variety of ways in which the work-items in a kernel can synchronize to exchange data, update data, or cooperate with each other to accomplish a task in a specific order. These are:

Accessor classes specify acquisition and release of buffer and image data structures. Depending on where they are created and destroyed, the runtime generates appropriate data transfers and synchronization primitives.

Atomic operations

SYCL devices support a restricted subset of C++ atomics.

Fences

Fence primitives are used to order loads and stores. Fences can have acquire semantics, release semantics, or both.

<sup>•</sup> Barriers

Barriers are used to synchronize sets of work-items within individual groups.

Hierarchical parallel dispatch

In the hierarchical parallelism model of describing computations, synchronization within the work-group is made explicit through multiple instances of the parallel\_for\_work\_item function call, rather than through the use of explicit work-group barrier operations.

```txt
- Device event
```

Events are used inside kernel functions to wait for asynchronous operations to complete.

In many cases, any of the preceding synchronization events can be used to achieve the same functionality, but with significant differences in efficiency and performance.

• Atomic Operations

• Local Barriers vs Global Atomics

## Atomic Operations
