
## 6.2.8.7.5 Updating Instantiated Graphs

Work submission using graphs is separated into three distinct stages: definition, instantiation, and execution. In situations where the workflow is not changing, the overhead of definition and instantiation can be amortized over many executions, and graphs provide a clear advantage over streams.

A graph is a snapshot of a workflow, including kernels, parameters, and dependencies, in order to replay it as rapidly and eficiently as possible. In situations where the workflow changes the graph becomes out of date and must be modified. Major changes to graph structure such as topology or types of nodes will require re-instantiation of the source graph because various topology-related optimization techniques must be re-applied.

The cost of repeated instantiation can reduce the overall performance benefit from graph execution, but it is common for only node parameters, such as kernel parameters and cudaMemcpy addresses, to change while graph topology remains the same. For this case, CUDA provides a lightweight mechanism known as “Graph Update,” which allows certain node parameters to be modified in-place without having to rebuild the entire graph. This is much more eficient than re-instantiation.

Updates will take efect the next time the graph is launched, so they will not impact previous graph launches, even if they are running at the time of the update. A graph may be updated and relaunched repeatedly, so multiple updates/launches can be queued on a stream.

CUDA provides two mechanisms for updating instantiated graph parameters, whole graph update and individual node update. Whole graph update allows the user to supply a topologically identical cudaGraph\_t object whose nodes contain updated parameters. Individual node update allows the user to explicitly update the parameters of individual nodes. Using an updated cudaGraph\_t is more convenient when a large number of nodes are being updated, or when the graph topology is unknown to the caller (i.e., The graph resulted from stream capture of a library call). Using individual node update is preferred when the number of changes is small and the user has the handles to the nodes requiring updates. Individual node update skips the topology checks and comparisons for unchanged nodes, so it can be more eficient in many cases.

CUDA also provides a mechanism for enabling and disabling individual nodes without afecting their current parameters.

The following sections explain each approach in more detail.

## 6.2.8.7.5.1 Graph Update Limitations

Kernel nodes:

▶ The owning context of the function cannot change.

▶ A node whose function originally did not use CUDA dynamic parallelism cannot be updated to a function which uses CUDA dynamic parallelism.

cudaMemset and cudaMemcpy nodes:

▶ The CUDA device(s) to which the operand(s) was allocated/mapped cannot change.

▶ The source/destination memory must be allocated from the same context as the original source/destination memory.

▶ Only 1D cudaMemset/cudaMemcpy nodes can be changed.

Additional memcpy node restrictions:

Changing either the source or destination memory type (i.e., cudaPitchedPtr, cudaArray\_t, etc.), or the type of transfer (i.e., cudaMemcpyKind) is not supported.

External semaphore wait nodes and record nodes:

▶ Changing the number of semaphores is not supported.

## Conditional nodes:

▶ The order of handle creation and assignment must match between the graphs.

▶ Changing node parameters is not supported (i.e. number of graphs in the conditional, node context, etc).

▶ Changing parameters of nodes within the conditional body graph is subject to the rules above.

## Memory nodes:

▶ It is not possible to update a cudaGraphExec\_t with a cudaGraph\_t if the cudaGraph\_t is currently instantiated as a diferent cudaGraphExec\_t.

There are no restrictions on updates to host nodes, event record nodes, or event wait nodes.
