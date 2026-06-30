# Device Launch Modes

Covers the three distinct named streams for device graph launch modes: Fire and Forget, Tail Launch, and Fire and Forget As Sibling. Device graphs cannot be launched into regular CUDA streams.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2933-L2940

Citation: [CUDA_C_Programming_Guide:L2933-L2940]

````text
## 6.2.8.7.7.6 Device Launch Modes

Unlike host launch, device graphs cannot be launched into regular CUDA streams, and can only be launched into distinct named streams, which each denote a specific launch mode:

Table 5: Device-only Graph Launch Streams

<table><tr><td>Stream</td><td>Launch Mode</td></tr><tr><td>cudaStreamGraphFireAndForget</td><td>Fire and forget launch</td></tr><tr><td>cudaStreamGraphTailLaunch</td><td>Tail launch</td></tr><tr><td>cudaStreamGraphFireAndForgetAsSibling</td><td>Sibling launch</td></tr></table>
````
