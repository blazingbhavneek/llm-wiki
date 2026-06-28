
## Low-level Hardware or OS-specific Solutions: VA-API/DXVA

Used for

• Most control/direct integration with OS-specific graphics stack

• Project is already based on VA-API/DXVA

As shown above there are higher-level tools and lower-level tools. Do you need the extremely low-level control you can get with operating system specific tools like libva\* or DirectX\*? And do you have the extra time it takes to develop these low-level applications? Or is it more important to be able to easily port your code from Linux\* to Windows\* and save time by coding with higher level tools?

More details to help match the approach option to requirements are in the table below.

<table><tr><td></td><td>Intel® Video Processing Library</td><td>Media Frameworks (FFmpeg &amp; GStreamer)</td><td>Low-level/OS-specific solutions (Libva &amp; DXVA)</td></tr><tr><td>Functionality</td><td>Elementary video stream processing with a limited set of frame processing operations</td><td>Full stack (network protocols, container support, audio support)</td><td>Working directly with the OS graphics stack</td></tr><tr><td>Level of control over hardware capabilities</td><td>Medium</td><td>Low</td><td>High</td></tr><tr><td>Portability</td><td>High</td><td>High</td><td>Low</td></tr></table>

## Media Pipeline Parallelism

For GPGPU, parallelism focuses on concerns like how the ND range is partitioned and related edge conditions. Multiple accelerators can work on this partitioned space, executing the same algorithm over the entire grid (SIMD). This is not the case for encode/decode.

Instead of analyzing the internal implementation details of an encoder or decoder to find opportunities for parallelism as it processes each frame, in most cases the entire operation would be treated as a black box. Decode implementations for a codec are intended to be interchangeable, like substituting one box for another. Encode replacement is more complex, since effects of a broader range of parameters must be considered. However, the strategy is usually the same - swap the entire optimization to one best suited to the hardware instead of attempting to optimize hotspots/inner loops.

In theory, operations could parallelize by slice within frames:

![](images/76c951aacb2577ec256dcb6a8412b8985cf46b0014af4a4ca14f729c45362423.jpg)

This is usually not practical. Since motion search cannot “see” across slice boundaries, overall compression quality is affected as the number of slices increase. Additional header bytes are required for slices as well.

Single streams can be processed asynchronously, but this is also not scalable. Dependencies between frames prevent parallelism. Turning off these dependencies reduces quality at a given bitrate. Increasing the number of frames in flight also increases latency.

<table><tr><td>Frame0</td><td>Frame1</td><td>Frame2</td><td>...</td><td>FrameN</td></tr></table>

For single stream optimization, Intel<sup>®</sup> Deep Link Hyper Encode may simplify development. Intel<sup>®</sup> Deep Link Hyper Encode can provide a performance boost when one or more discrete GPUs are available on a system where integrated/processor graphics is also available by automatically coordinating work between integrated and discrete GPUs. Single stream performance can be improved by utilizing the capabilities of dGPU and iGPU together.

![](images/b0dcc49336697a6957504542563edbc2e21b88c5ecf97e77a3e08303fc2df192.jpg)

Power Share 回《回

Hyper code

Hmprut回+

The best way to scale efficiently while preserving quality and reducing latency is to process multiple streams simultaneously. (Note: for non-realtime processing even a single stream can be processed in parallel as segments since frames will not have dependencies across segment/GOP boundaries.)

Stream0

Stream1

Stream2

![](images/2d832944bb481a709a0cc22db17127dd0fb9c108e32da7e45282659071198bd9.jpg)

StreamN

This approach provides ideal “embarrassing” parallelism which scales across accelerators. There are no dependencies across streams, so each accelerator can process as quickly as possible without coordination. For the Hyper Encode case, it is usually faster to schedule separate streams on iGPU and dGPU.

From a oneAPI perspective, these properties greatly simplify interoperability with SYCL. Media operations generally will not run “inside” kernels, which means there are fewer concerns at the API or development level. Media operations will either provide data for a kernel (act as a source), or they will work as a sink on data provided by a kernel. The main concern for performance is that the handoff between media operation and kernel implies synchronization and reduces opportunities to process asynchronously within a single stream. Processing multiple streams concurrently is the best workaround for this limitation.

## Optimizing Media Operations
