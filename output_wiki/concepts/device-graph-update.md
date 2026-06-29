# Device Graph Update

Device graphs can only be updated from the host. To apply changes, the executable graph must be re-uploaded to the device. This process utilizes the same methods outlined for previous graph updates.

Unlike host graphs, launching a device graph from the device while an update is being applied will result in undefined behavior [CUDA_C_Programming_Guide:L2923-L2926].
