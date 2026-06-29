# Device Graph Upload

In order to launch a graph on the device, it must first be uploaded to the device to populate the necessary device resources [CUDA_C_Programming_Guide:L2888-L2922]. This process can be achieved in one of two ways: explicit upload or implicit upload [CUDA_C_Programming_Guide:L2888-L2922].

## Explicit Upload

The graph can be uploaded explicitly using one of the following methods:

1.  **Via `cudaGraphUpload()`**: The graph can be uploaded after instantiation using the `cudaGraphUpload()` function [CUDA_C_Programming_Guide:L2888-L2922]. An example of this approach is:
    ```c
    // Explicit upload after instantiation
    cudaGraphInstantiate(&deviceGraphExec1, deviceGraph1,
    →cudaGraphInstantiateFlagDeviceLaunch);
    cudaGraphUpload(deviceGraphExec1, stream);
    ```

2.  **Via `cudaGraphInstantiateWithParams()`**: The upload can be requested as part of the instantiation process by setting the `cudaGraphInstantiateFlagUpload` flag and specifying the `uploadStream` in the `cudaGraphInstantiateParams` structure [CUDA_C_Programming_Guide:L2888-L2922]. An example of this approach is:
    ```c
    // Explicit upload as part of instantiation
    cudaGraphInstantiateParams instantiateParams = {0};
    instantiateParams.flags = cudaGraphInstantiateFlagDeviceLaunch |
    cudaGraphInstantiateFlagUpload;
    instantiateParams.uploadStream = stream;
    cudaGraphInstantiateWithParams(&deviceGraphExec2, deviceGraph2, &instantiateParams);
    ```

## Implicit Upload

Alternatively, the graph can be launched from the host, which will perform the upload step implicitly as part of the launch [CUDA_C_Programming_Guide:L2888-L2922]. An example of this approach is:

```c
// Implicit upload via host launch
cudaGraphInstantiate(&deviceGraphExec3, deviceGraph3,
cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphLaunch(deviceGraphExec3, stream);
```

## Summary of Methods

| Method | Function(s) | Description |
| :--- | :--- | :--- |
| Explicit | `cudaGraphUpload()` | Uploads the graph after instantiation. |
| Explicit | `cudaGraphInstantiateWithParams()` | Uploads the graph during instantiation. |
| Implicit | `cudaGraphLaunch()` | Uploads the graph during the initial host launch. |

All three methods achieve the same goal of populating device resources, but they differ in when and how the upload is triggered [CUDA_C_Programming_Guide:L2888-L2922].
