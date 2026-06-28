## 6.2.8.7.6 Using Graph APIs

cudaGraph\_t objects are not thread-safe. It is the responsibility of the user to ensure that multiple threads do not concurrently access the same cudaGraph\_t.

A cudaGraphExec\_t cannot run concurrently with itself. A launch of a cudaGraphExec\_t will be ordered after previous launches of the same executable graph.

Graph execution is done in streams for ordering with other asynchronous work. However, the stream is for ordering only; it does not constrain the internal parallelism of the graph, nor does it afect where graph nodes execute.

See Graph API.

## 6.2.8.7.7 Device Graph Launch

There are many workflows which need to make data-dependent decisions during runtime and execute diferent operations depending on those decisions. Rather than ofloading this decision-making process to the host, which may require a round-trip from the device, users may prefer to perform it on the device. To that end, CUDA provides a mechanism to launch graphs from the device.

Device graph launch provides a convenient way to perform dynamic control flow from the device, be it something as simple as a loop or as complex as a device-side work scheduler. This functionality is only available on systems which support unified addressing.

Graphs which can be launched from the device will henceforth be referred to as device graphs, and graphs which cannot be launched from the device will be referred to as host graphs.

Device graphs can be launched from both the host and device, whereas host graphs can only be launched from the host. Unlike host launches, launching a device graph from the device while a previous launch of the graph is running will result in an error, returning cudaErrorInvalidValue; therefore, a device graph cannot be launched twice from the device at the same time. Launching a device graph from the host and device simultaneously will result in undefined behavior.

## 6.2.8.7.7.1 Device Graph Creation

In order for a graph to be launched from the device, it must be instantiated explicitly for device launch. This is achieved by passing the cudaGraphInstantiateFlagDeviceLaunch flag to the cudaGraphInstantiate() call. As is the case for host graphs, device graph structure is fixed at time of instantiation and cannot be updated without re-instantiation, and instantiation can only be performed on the host. In order for a graph to be able to be instantiated for device launch, it must adhere to various requirements.

## 6.2.8.7.7.2 Device Graph Requirements

## General requirements:

▶ The graph’s nodes must all reside on a single device.

▶ The graph can only contain kernel nodes, memcpy nodes, memset nodes, and child graph nodes. Kernel nodes:

Use of CUDA Dynamic Parallelism by kernels in the graph is not permitted.

▶ Cooperative launches are permitted so long as MPS is not in use.

## Memcpy nodes:

▶ Only copies involving device memory and/or pinned device-mapped host memory are permitted.

▶ Copies involving CUDA arrays are not permitted.

▶ Both operands must be accessible from the current device at time of instantiation. Note that the copy operation will be performed from the device on which the graph resides, even if it is targeting memory on another device.

## 6.2.8.7.7.3 Device Graph Upload

In order to launch a graph on the device, it must first be uploaded to the device to populate the necessary device resources. This can be achieved in one of two ways.

Firstly, the graph can be uploaded explicitly, either via cudaGraphUpload() or by requesting an upload as part of instantiation via cudaGraphInstantiateWithParams().

Alternatively, the graph can first be launched from the host, which will perform this upload step implicitly as part of the launch.

Examples of all three methods can be seen below:

```txt
// Explicit upload after instantiation
cudaGraphInstantiate(&deviceGraphExec1, deviceGraph1,
→cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphUpload(deviceGraphExec1, stream);

// Explicit upload as part of instantiation
cudaGraphInstantiateParams instantiateParams = {0};
```

(continues on next page)

```txt
(continued from previous page)
instantiateParams.flags = cudaGraphInstantiateFlagDeviceLaunch |
cudaGraphInstantiateFlagUpload;
instantiateParams.uploadStream = stream;
cudaGraphInstantiateWithParams(&deviceGraphExec2, deviceGraph2, &instantiateParams);

// Implicit upload via host launch
cudaGraphInstantiate(&deviceGraphExec3, deviceGraph3,
cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphLaunch(deviceGraphExec3, stream);
```

## 6.2.8.7.7.4 Device Graph Update
