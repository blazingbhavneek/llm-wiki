# Device Graph Update

Covers that device graphs can only be updated from the host and require re-upload to the device for changes to take effect. Launching from the device during an update causes undefined behavior.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2923-L2926

Citation: [CUDA_C_Programming_Guide:L2923-L2926]

````text
## 6.2.8.7.7.4 Device Graph Update

Device graphs can only be updated from the host, and must be re-uploaded to the device upon executable graph update in order for the changes to take efect. This can be achieved using the same methods outlined in the previous section. Unlike host graphs, launching a device graph from the device while an update is being applied will result in undefined behavior.
````
