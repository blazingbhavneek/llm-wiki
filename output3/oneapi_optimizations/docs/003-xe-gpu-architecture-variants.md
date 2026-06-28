![](images/7dae06dc26eeccefa65026106c5cba1b1e166bcdaa98d3d468ae4474e8d6cfba.jpg)

## X<sup>e</sup>-Core

Unlike the X<sup>e</sup>-LP and prior generations of Intel GPUs that used the Execution Unit (EU) as a compute unit, ${ \tt X } ^ { \tt e _ { - } }$ HPG and $\mathsf { X } ^ { \mathsf { e } . }$ -HPC use the $\mathsf { X } ^ { \mathsf { e } _ { \mathsf { - } } }$ core. This is similar to an ${ \tt X } ^ { \tt e \mathrm { \mathrm { - } \mathrm { 1 } \mathrm { P } } }$ dual subslice.

An $\mathsf { X } ^ { \mathsf { e } _ { \mathsf { - } } }$ core contains vector and matrix ALUs, which are referred to as vector and matrix engines.

An X<sup>e</sup>-core of the ${ \tt X } ^ { \tt e _ { - \displaystyle H P C } }$ GPU contains 8 vector and 8 matrix engines, alongside a large 512KB L1 cache/ SLM. It powers the Intel<sup>®</sup> Data Center GPU Max Series. Each vector engine is 512 bit wide supporting 16 FP32 SIMD operations with fused FMAs. With 8 vector engines, the X<sup>e</sup>-core delivers 512 FP16, 256 FP32 and

128 FP64 operations/cycle. Each matrix engine is 4096 bit wide. With 8 matrix engines, the X<sup>e</sup>-core delivers 8192 int8 and 4096 FP16/BF16 operations/cycle. The X<sup>e</sup>-core provides 1024B/cycle load/store bandwidth to the memory system.

## Xe-core

![](images/3d329c67ee987b25e1b5f03f3b7f60fe83c1091605c20d26321581a97afaaf35.jpg)

## X<sup>e</sup>-Slice

An X<sup>e</sup>-slice contains 16 X<sup>e</sup>-core for a total of 8MB L1 cache, 16 ray tracing units and 1 hardware context.

## Xe-slice

![](images/552e908f361ffcb35ddabe7e8940a559bfbcc89aa8524e82b958228c1456e784.jpg)

## X<sup>e</sup>-Stack

An X<sup>e</sup>-stack contains up to 4 X<sup>e</sup>-slice: 64 X<sup>e</sup>-cores, 64 ray tracing units, 4 hardware contexts, 4 HBM2e controllers, 1 media engine, and 8 X<sup>e</sup>-Links of high speed coherent fabric. It also contains a shared L2 cache.

## Xe-stack

![](images/70919005ac7d6234ee06eda8d1e718c9d87bc849cb47e3ae66f05a4a93f59626.jpg)

## X<sup>e</sup>-HPC 2-Stack Data Center GPU Max

An X<sup>e</sup>-HPC 2-stack Data Center GPU Max, previously code named Ponte Vecchio or PVC, consists of up to 2 stacks:: 8 slices, 128 X<sup>e</sup>-cores, 128 ray tracing units, 8 hardware contexts, 8 HBM2e controllers, and 16 X<sup>e</sup>- Links.

Xe-HPC 2-Stack  
![](images/54e60d1c84d4e4f68c4ffc5444987a6b376b494154c4dcedaac25b8ec4175064.jpg)

## X<sup>e</sup>-HPG GPU

X<sup>e</sup>-HPG is the enthusiast or high performance gaming variant of the X<sup>e</sup> architecture. The microarchitecture is focused on graphics performance and supports hardware-accelerated ray tracing.

An X<sup>e</sup>-core of the X<sup>e</sup>-HPG GPU contains 16 vector and 16 matrix engines. It powers the Intel<sup>®</sup> Arc GPUs. Each vector engine is 256 bit wide, supporting 8 FP32 SIMD operations with fused FMAs. With 16 vector engines, the X<sup>e</sup>-core delivers 256 FP32 operations/cycle. Each matrix engine is 1024 bit wide. With 16 matrix engines, the X<sup>e</sup>-core delivers 4096 int8 and 2048 FP16/BF16 operations/cycle. The X<sup>e</sup>-core provides 512B/cycle load/ store bandwidth to the memory system.

An X<sup>e</sup>-HPG GPU consists of 8 X<sup>e</sup>-HPG-slice, which contains up to 4 X<sup>e</sup>-HPG-cores for a total of 4096 FP32 ALU units/shader cores.

## X<sup>e</sup>- Intel<sup>®</sup> Data Center GPU Flex Series

Intel<sup>®</sup> Data Center GPU Flex Series come in two configurations. The 150W option has 32 X<sup>e</sup>-cores on a PCIe Gen4 card. The 75W option has two GPUs for 16 X<sup>e</sup>-cores (8 X<sup>e</sup>-cores per GPU). Both configurations come with 4 X<sup>e</sup> media engines, the industry’s first AV1 hardware encoder and accelerator for data center, GDDR6 memory, ray tracing units, and built-in XMX AI acceleration.

Intel<sup>®</sup> Data Center GPU Flex Series are derivatives of the X<sup>e</sup>-HPG GPUs. An Intel<sup>®</sup> Data Center GPU Flex 170 consists of 8 X<sup>e</sup>-HPG-slices for a total of 32 X<sup>e</sup>-cores with 4096 FP32 ALU units/shader cores.

Targeting data center cloud gaming, media streaming and video analytics applications, Intel<sup>®</sup> Data Center GPU Flex Series provide hardware accelerated AV1 encoder, delivering a 30% bit-rate improvement without compromising on quality. It supports 8 simultaneous 4K streams or more than 30 1080p streams per card. AI models can be applied to the decoded streams utilizing Intel<sup>®</sup> Data Center GPU Flex Series’ X<sup>e</sup>-cores.

Media streaming and delivery software stacks lean on Intel<sup>®</sup> Video Processing Library (Intel VPL) to decode and encode acceleration for all the major codecs including AV1. Media distributors can choose from the two leading media frameworks FFMPEG or GStreamer, both enabled for acceleration with Intel VPL on Intel CPUs and GPUs.

In parallel to Intel VPL accelerating decoding and encoding of media streams, Intel<sup>®</sup> oneAPI Deep Neural Network Library (oneDNN) delivers AI optimized kernels enabled to accelerate inference modes in TensorFlow or PyTorch frameworks, or with the OpenVINO model optimizer and inference engine to further accelerate inference and speed customer deployment of their workloads.

## Terminology and Configuration Summary

The following table maps legacy GPU terminologies (used in Generation 9 through Generation 12 Intel<sup>®</sup> Core<sup>TM</sup> architectures) to their new names in the Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> GPU (Generation 12.7 and newer) architecture paradigm.

Architecture Terminology Changes

<table><tr><td>Old Term</td><td>New Intel Term</td><td>Generic Term</td><td>New Abbreviation</td></tr><tr><td>Execution Unit (EU)</td><td>XeVector Engine</td><td>Vector Engine</td><td>XVE</td></tr><tr><td>Systolic/&quot;DPAS part of EU&quot;</td><td>XeMatrix eXtension</td><td>Matrix Engine</td><td>XMX</td></tr><tr><td>Subslice (SS) or Dual Subslice (DSS)</td><td>Xe-core</td><td>NA</td><td>XC</td></tr><tr><td>Slice</td><td>Render Slice / Compute Slice</td><td>Slice</td><td>SLC</td></tr><tr><td>Tile</td><td>Stack</td><td>Stack</td><td>STK</td></tr></table>

The following table lists the hardware characteristics across the X<sup>e</sup> family GPUs.

X<sup>e</sup> Configurations

<table><tr><td>Architecture</td><td>Xe-LP (TGL)</td><td>Xe-HPG (Arc A770)</td><td>Xe-HPG (Data Center GPU Flex 170)</td><td>Xe-HPC (Data Center GPU Max 1550)</td></tr><tr><td>Slice count</td><td>1</td><td>8</td><td>8</td><td>4 x 2</td></tr><tr><td>XC (DSS/SS) count</td><td>6</td><td>32</td><td>32</td><td>64 x 2</td></tr><tr><td>XVE (EU) / XC</td><td>16</td><td>16</td><td>16</td><td>8</td></tr><tr><td>XVE count</td><td>96</td><td>512</td><td>512</td><td>512 x 2</td></tr><tr><td>Threads / XVE</td><td>7</td><td>8</td><td>8</td><td>8</td></tr><tr><td>Thread count</td><td>672</td><td>4096</td><td>4096</td><td>4096 x 2</td></tr><tr><td>FLOPs / clk - single precision, MAD</td><td>1536</td><td>8192</td><td>8192</td><td>16384 x 2</td></tr><tr><td>FLOPs / clk - double precision, MAD</td><td>NA</td><td>NA</td><td>NA</td><td>16384 x 2</td></tr><tr><td>FLOPs / clk - FP16 DP4AS</td><td>NA</td><td>65536</td><td>65536</td><td>262144 x 2</td></tr><tr><td>GTI bandwidth bytes / unslice-clk</td><td>r:128, w:128</td><td>r:512, w:512</td><td>r:512, w:512</td><td>r:1024, w:1024</td></tr><tr><td>LL cache size</td><td>3.84MB</td><td>16MB</td><td>16MB</td><td>up to 408MB</td></tr><tr><td>SLM size</td><td>6 × 128KB × 2</td><td>32 × 128KB × 2</td><td>32 × 128KB × 2</td><td>64 × 128KB × 2</td></tr><tr><td>FMAD, SP (ops / XVE / clk)</td><td>8</td><td>8</td><td>8</td><td>16</td></tr><tr><td>SQRT, SP (ops / XVE / clk)</td><td>2</td><td>2</td><td>2</td><td>4</td></tr></table>
