# Device Graph Upload

Covers methods to upload device graphs to the GPU to populate device resources: explicit upload via `cudaGraphUpload()`, upload during instantiation via `cudaGraphInstantiateWithParams()`, or implicit upload via an initial host launch.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2888-L2922

Citation: [CUDA_C_Programming_Guide:L2888-L2922]

````text
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
````
