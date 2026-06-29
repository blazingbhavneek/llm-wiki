# Device Launch Streams and Modes

Unlike host launch, device graphs cannot be launched into regular CUDA streams. Instead, they must be launched into distinct named streams, each of which denotes a specific launch mode [CUDA_C_Programming_Guide:L2933-L2940].

The available device-only graph launch streams are:

* **cudaStreamGraphFireAndForget**: Used for fire and forget launch [CUDA_C_Programming_Guide:L2933-L2940].
* **cudaStreamGraphTailLaunch**: Used for tail launch [CUDA_C_Programming_Guide:L2933-L2940].
* **cudaStreamGraphFireAndForgetAsSibling**: Used for sibling launch [CUDA_C_Programming_Guide:L2933-L2940].
