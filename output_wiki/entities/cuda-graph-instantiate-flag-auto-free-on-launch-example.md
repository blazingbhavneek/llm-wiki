# cudaGraphInstantiateFlagAutoFreeOnLaunch Example

This example demonstrates a single-producer, multiple-consumer algorithm using CUDA Graphs. It illustrates how to create producer and consumer graphs, launch them in a loop, and manage memory lifetimes using the `cudaGraphInstantiateFlagAutoFreeOnLaunch` flag.

## Producer Graph Creation

The producer graph captures memory allocation and kernel execution. The `cudaGraphInstantiateFlagAutoFreeOnLaunch` flag is used during instantiation to ensure that memory allocated within the graph (via `cudaMallocAsync`) is automatically freed upon launch.

```cpp
// Create producer graph which allocates memory and populates it with data
cudaStreamBeginCapture(cudaStreamPerThread, cudaStreamCaptureModeGlobal);
cudaMallocAsync(&data1, blocks * threads, cudaStreamPerThread);
cudaMallocAsync(&data2, blocks * threads, cudaStreamPerThread);
produce<<<blocks, threads, 0, cudaStreamPerThread>>>(data1, data2);
...
cudaStreamEndCapture(cudaStreamPerThread, &graph);
cudaGraphInstantiateWithFlags(&producer,
                             graph,
                             cudaGraphInstantiateFlagAutoFreeOnLaunch);
cudaGraphDestroy(graph);
```

## Consumer Graph Creation

Two consumer graphs are created. The first captures an asynchronous library call and is instantiated with regular flags (0). The second captures a kernel launch and is also instantiated with regular flags. Note that these consumers rely on memory (`data1`, `data2`) that was allocated by the producer graph.

```cpp
// Create first consumer graph by capturing an asynchronous library call
cudaStreamBeginCapture(cudaStreamPerThread, cudaStreamCaptureModeGlobal);
consumerFromLibrary(data1, cudaStreamPerThread);
cudaStreamEndCapture(cudaStreamPerThread, &graph);
cudaGraphInstantiateWithFlags(&consumer1, graph, 0); //regular instantiation
cudaGraphDestroy(graph);

// Create second consumer graph
cudaStreamBeginCapture(cudaStreamPerThread, cudaStreamCaptureModeGlobal);
consume2<<<blocks, threads, 0, cudaStreamPerThread>>>(data2);
...
cudaStreamEndCapture(cudaStreamPerThread, &graph);
cudaGraphInstantiateWithFlags(&consumer2, graph, 0);
cudaGraphDestroy(graph);
```

## Launch Loop and Cleanup

The graphs are launched in a loop. The producer graph is launched first, followed by the first consumer. The second consumer is launched conditionally based on `determineAction`. After the loop, explicit asynchronous frees are called for the data pointers, and the graph executions are destroyed.

```cpp
// Launch in a loop
bool launchConsumer2 = false;
do {
    cudaGraphLaunch(producer, myStream);
    cudaGraphLaunch(consumer1, myStream);
    if (launchConsumer2) {
        cudaGraphLaunch(consumer2, myStream);
    }
} while (determineAction(&launchConsumer2));

cudaFreeAsync(data1, myStream);
cudaFreeAsync(data2, myStream);

cudaGraphExecDestroy(producer);
cudaGraphExecDestroy(consumer1);
cudaGraphExecDestroy(consumer2);
```

## References

- CUDA C Programming Guide: [CUDA_C_Programming_Guide:L16140-L16189] [CUDA_C_Programming_Guide:L16140-L16189]
