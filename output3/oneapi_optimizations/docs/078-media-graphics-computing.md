## Media Graphics Computing on GPU

We have focused on GPGPU optimization techniques and tools so far. When it comes to media graphics computing, a new set of optimization techniques and tools are also needed for maximizing utilization efficiency of the hardware, especially the dedicated units, for example, the media engines.

• Optimizing Media Pipelines

• Performance Analysis with Intel<sup>®</sup> Graphics Performance Analyzers

## Optimizing Media Pipelines

Media operations are ideal candidates for hardware acceleration because they are relatively large algorithms with well-defined inputs and outputs. Video processing hardware capabilities can be accessed via industrystandard frameworks, Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL), or low-level/operating system specific approaches like Video Acceleration API (VA-API) for Linux or Microsoft\* DirectX\* for Windows. Which path to choose depends on many factors. However, the basic principles like parallelization by multiple streams and maximizing data locality apply for all options.

The main differences between video processing and GPGPU work apply to all accelerator API options. Many typical GPGPU optimizations focus on optimizing how large grids of work are partitioned across multiple processing units. Hardware-accelerated media operations are implemented in silicon. They work in units of frames and usually work is partitioned by streams of frames.

Media optimization steps don’t match the GPGPU workflow described in other sections. However, they can be easily added before or after GPGPU work. Media steps will supply inputs to or take outputs from GPGPU steps. For example:

![](images/6b76cab6c597c0a67fca93fafa11263a98ebb0727f79d476b2ab34e2eb3f2484.jpg)

• Media Engine Hardware

• Media API Options for Hardware Acceleration

• Media Pipeline Parallelism

• Media Pipeline Inter-operation and Memory Sharing

• SYCL-Blur Example

Video streaming is prevalent in our world today. We stream meetings at work. We watch movies at home. We expect good quality. Taking advantage of this new media engine hardware gives you the option to stream faster, stream at higher quality and/or stream at lower power. This hardware solution is an important consideration for End-to-End performance in pipelines working with video data.

## Media Engine Hardware

As described in Intel<sup>®</sup> X<sup>e</sup> Architecture section, Xe- Intel® Data Center GPU Flex Series and some other Intel<sup>®</sup> GPUs contain media engine which provide fully-accelerated video decode, encode and processing capabilities. This is sometimes called Intel<sup>®</sup> Quick Sync Video. The media engine runs completely independent of compute engines (vector and matrix engines).

![](images/c99b74538d2f14a57f2754caf4f7cfe67eea8ebe288f98908d4a7be0bd45435f.jpg)

Several components can be used by applications:

• MFX/Multi-format codec: hardware decode and encode. Some configurations include two forms of encode. 1) motion estimation + bit packing and 2) full fixed function/low power

• SFC/scaler and format conversion: resize (primarily intended for downscaling), conversion between color formats such as NV12 and BGRA

• Video Quality Engine: multiple frame processing operations, such as denoise and deinterlace.

This hardware has its own instruction queue and clock, so fully fixed function work can be very low power if configured to use low power pathways. This can also leave the slice capabilities on the GPU free for other work.

## Supported codecs

New codec capabilities are added with each new GPU hardware generation.

<table><tr><td></td><td></td><td>AVC</td><td>MPEG 2</td><td>JPEG</td><td>VP8</td><td>HEVC 8-bit</td><td>HEVC 8-bit 422</td><td>HEVC 8-bit 444</td><td>HEVC 10-bit</td><td>HEVC 10-bit 422</td></tr><tr><td>CPU</td><td></td><td>D/E*</td><td>D</td><td>D/E</td><td></td><td>D/E</td><td></td><td></td><td>D/E</td><td></td></tr><tr><td rowspan="6">Media SDK GPU</td><td> $5^{th}$  Generation Intel® Core (BDW)</td><td>D/Es</td><td>D/Es</td><td>D</td><td>D</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td> $6^{th}$  Generation Intel® Core (SKL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td></td><td></td></tr><tr><td>Intel Atom® Processor E3900 series (APL)</td><td>D/E/Es</td><td>D</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td>D</td><td></td></tr><tr><td> $7^{th}$  Generation Intel® Core (KBLx)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/Es</td><td></td><td></td><td>D/Es</td><td></td></tr><tr><td> $10^{th}$  Generation Intel® Core (ICL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/E/Es</td><td>D/Es</td></tr><tr><td>Intel Atom® Processor X Series (EHL)</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D/E</td><td>D</td></tr><tr><td rowspan="2">oneVPL GPU</td><td>Intel® Iris® Xe (TGL/RKL/ADL), Intel® Iris® Xe MAX (DGI)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D (TGL only)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/E/Es</td><td>D/Es</td></tr><tr><td>Intel® ARC</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D/E</td><td></td></tr></table>

Note: in this table two kinds of encode are represented.  
E=Hardware Encode via low power VDEnc  
Es=Hardware Encode via (PAK) + Shader (media kernel +VME)  
Intel<sup>®</sup> Arc A-series and Intel<sup>®</sup> Server GPU (previously known as Arctic Sound-M) add AV1 encode. This cutting edge successor to VP9 adds additional encode control for stack, segmentation, film grain filtering, and other new features. These increase encode quality at a given bitrate or allow a decrease in bitrate to provide increased quality.

![](images/273d1d75f5d8dfdf0c5111099ced4f5645b70db9e50fe69402dac7972aebe352.jpg)

## Media API Options for Hardware Acceleration

There are multiple ways to accelerate video processing on Intel<sup>®</sup> architecture (CPUs, GPUs). To choose the option that benefits you most, ensure your goals align with the tools you choose.

## Industry Standard Frameworks: FFmpeg, GStreamer,

OpenCV, etc.

Used for

• Full media solution w/ network protocols, container support, audio support, etc.

• Easily move across accelerators and HW vendors

## Intel® oneAPI Video Processing Library (oneVPL)

Used for

• Project focused on video elementary stream processing only

· OS agnostic
