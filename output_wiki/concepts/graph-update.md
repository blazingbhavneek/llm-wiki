# Graph Update

Work submission using CUDA graphs is separated into three distinct stages: definition, instantiation, and execution [CUDA_C_Programming_Guide:L2670-L2675]. In scenarios where the workflow remains static, the overhead of definition and instantiation is amortized over many executions, providing a performance advantage over streams [CUDA_C_Programming_Guide:L2675-L2678]. A graph serves as a snapshot of a workflow, including kernels, parameters, and dependencies, optimized for rapid replay [CUDA_C_Programming_Guide:L2678-L2681].

When the workflow changes, the graph becomes out of date and must be modified [CUDA_C_Programming_Guide:L2681-L2683]. Major structural changes, such as alterations to topology or node types, require re-instantiation of the source graph because topology-related optimization techniques must be reapplied [CUDA_C_Programming_Guide:L2683-L2687]. However, repeated instantiation can reduce overall performance benefits [CUDA_C_Programming_Guide:L2687-L2689].

To address cases where only node parameters (e.g., kernel parameters, `cudaMemcpy` addresses) change while the graph topology remains identical, CUDA provides a lightweight mechanism known as **Graph Update** [CUDA_C_Programming_Guide:L2689-L2694]. This allows certain node parameters to be modified in-place without rebuilding the entire graph, which is significantly more efficient than re-instantiation [CUDA_C_Programming_Guide:L2694-L2697].

## Update Mechanisms

CUDA provides two mechanisms for updating instantiated graph parameters: **Whole Graph Update** and **Individual Node Update** [CUDA_C_Programming_Guide:L2697-L2700].

### Whole Graph Update

The `cudaGraphExecUpdate()` function allows an instantiated graph (the "original graph") to be updated with parameters from a topologically identical graph (the "updating" graph) [CUDA_C_Programming_Guide:L2700-L2704].

**Requirements for Whole Graph Update:**
*   The topology of the updating graph must be identical to the original graph used to instantiate the `cudaGraphExec_t` [CUDA_C_Programming_Guide:L2704-L2706].
*   The order in which dependencies are specified must match [CUDA_C_Programming_Guide:L2706-L2707].
*   CUDA must consistently order sink nodes (nodes with no dependencies) [CUDA_C_Programming_Guide:L2707-L2709].

To ensure deterministic pairing of nodes between the original and updating graphs, the following rules must be followed [CUDA_C_Programming_Guide:L2710-L2713]:
1.  For any capturing stream, API calls must be made in the same order, including event waits and other API calls not directly corresponding to node creation [CUDA_C_Programming_Guide:L2713-L2717].
2.  API calls manipulating a graph node’s incoming edges (including captured stream APIs, node add APIs, and edge addition/removal APIs) must be made in the same order [CUDA_C_Programming_Guide:L2717-L2722]. Dependencies specified in arrays must also maintain their order [CUDA_C_Programming_Guide:L2722-L2724].
3.  Sink node ordering must be consistent. Operations affecting sink node ordering include node add APIs, edge removals that result in a sink node, `cudaStreamUpdateCaptureDependencies()`, and `cudaStreamEndCapture()` [CUDA_C_Programming_Guide:L2724-L2733].

Whole graph update is more convenient when a large number of nodes are being updated or when the graph topology is unknown to the caller (e.g., resulting from stream capture of a library call) [CUDA_C_Programming_Guide:L2733-L2737].

### Individual Node Update

Individual node update allows the user to explicitly update the parameters of specific nodes [CUDA_C_Programming_Guide:L2737-L2739]. This approach is preferred when the number of changes is small and the user possesses the handles to the nodes requiring updates [CUDA_C_Programming_Guide:L2739-L2742].

Individual node update skips topology checks and comparisons for unchanged nodes, making it more efficient in many cases compared to whole graph update [CUDA_C_Programming_Guide:L2742-L2745]. It also allows for enabling and disabling individual nodes without affecting their current parameters [CUDA_C_Programming_Guide:L2745-L2747].

## Execution and Timing

Updates take effect the next time the graph is launched [CUDA_C_Programming_Guide:L2747-L2749]. Updates do not impact previous graph launches, even if they are still running at the time of the update [CUDA_C_Programming_Guide:L2749-L2752]. A graph may be updated and relaunched repeatedly, allowing multiple updates/launches to be queued on a stream [CUDA_C_Programming_Guide:L2752-L2755].

## Limitations

Not all graph components can be updated. The following restrictions apply:

### Kernel Nodes
*   The owning context of the function cannot change [CUDA_C_Programming_Guide:L2755-L2757].
*   A node whose function originally did not use CUDA dynamic parallelism cannot be updated to a function which uses CUDA dynamic parallelism [CUDA_C_Programming_Guide:L2757-L2760].

### `cudaMemset` and `cudaMemcpy` Nodes
*   The CUDA device(s) to which the operand(s) was allocated/mapped cannot change [CUDA_C_Programming_Guide:L2760-L2762].
*   The source/destination memory must be allocated from the same context as the original source/destination memory [CUDA_C_Programming_Guide:L2762-L2765].
*   Only 1D `cudaMemset`/`cudaMemcpy` nodes can be changed [CUDA_C_Programming_Guide:L2765-L2767].
*   Changing either the source or destination memory type (e.g., `cudaPitchedPtr`, `cudaArray_t`) or the type of transfer (`cudaMemcpyKind`) is not supported [CUDA_C_Programming_Guide:L2767-L2770].

### External Semaphore Wait and Record Nodes
*   Changing the number of semaphores is not supported [CUDA_C_Programming_Guide:L2770-L2772].

### Conditional Nodes
*   The order of handle creation and assignment must match between the graphs [CUDA_C_Programming_Guide:L2772-L2774].
*   Changing node parameters is not supported (e.g., number of graphs in the conditional, node context) [CUDA_C_Programming_Guide:L2774-L2777].
*   Changing parameters of nodes within the conditional body graph is subject to the rules above [CUDA_C_Programming_Guide:L2777-L2779].

### Memory Nodes
*   It is not possible to update a `cudaGraphExec_t` with a `cudaGraph_t` if the `cudaGraph_t` is currently instantiated as a different `cudaGraphExec_t` [CUDA_C_Programming_Guide:L2779-L2782].

There are no restrictions on updates to host nodes, event record nodes, or event wait nodes [CUDA_C_Programming_Guide:L2782-L2784].

## Typical Workflow

A typical workflow involves the following steps [CUDA_C_Programming_Guide:L2784-L2790]:
1.  Create the initial `cudaGraph_t` using either stream capture or the Graph API.
2.  Instantiate the graph into a `cudaGraphExec_t` and launch it.
3.  Create a new `cudaGraph_t` using the same method as the initial graph.
4.  Call `cudaGraphExecUpdate()` to update the instantiated graph.
5.  If the update is successful, launch the updated `cudaGraphExec_t`.
6.  If the update fails, destroy the original `cudaGraphExec_t` and instantiate a new one from the new `cudaGraph_t`.

Conditional handle flags and default values are updated as part of the graph update process [CUDA_C_Programming_Guide:L2790-L2792].

## Example

The following example demonstrates updating an instantiated graph using stream capture [CUDA_C_Programming_Guide:L2792-L2805]:

```c
cudaGraphExec_t graphExec = NULL;

for (int i = 0; i < 10; i++) {
    cudaGraph_t graph;
    cudaGraphExecUpdateResult updateResult;
    cudaGraphNode_t errorNode;

    // In this example we use stream capture to create the graph.
    // You can also use the Graph API to produce a graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);

    // Call a user-defined, stream based workload, for example
    do_cuda_work(stream);

    cudaStreamEndCapture(stream, &graph);

    // If we've already instantiated the graph, try to update it directly
    // and avoid the instantiation overhead
    if (graphExec != NULL) {
        // If the graph fails to update, errorNode will be set to the
        // node causing the failure and updateResult will be set to a
        // reason code.
        cudaGraphExecUpdate(graphExec, graph, &errorNode, &updateResult);
    }

    // Instantiate during the first iteration or whenever the update
    // fails for any reason
    if (graphExec == NULL || updateResult != cudaGraphExecUpdateSuccess) {

        // If a previous update failed, destroy the cudaGraphExec_t
        // before re-instantiating it
        if (graphExec != NULL) {
            cudaGraphExecDestroy(graphExec);
        }
        // Instantiate graphExec from graph. The error node and
        // error message parameters are unused here.
        cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
    }

    cudaGraphDestroy(graph);
    cudaGraphLaunch(graphExec, stream);
    cudaStreamSynchronize(stream);
}
```
