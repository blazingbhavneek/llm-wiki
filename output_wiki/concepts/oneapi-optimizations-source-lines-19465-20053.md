# oneapi_optimizations Source Lines 19465-20053

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L19465-L20053

Citation: [oneapi_optimizations:L19465-L20053]

````text

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

Since the algorithms are implemented in hardware, the main concerns with media development are data locality, synchronization, and providing a pipeline of work to keep the hardware busy.

Data locality: keep frames on the GPU, avoiding copying to the CPU unnecessarily. Since the media engine is connected to the GPU memory hierarchy, data can be shared locally between slice and media engine components. From a GPGPU perspective these operations work on local GPU data. Frames can be shared between this hardware and execution units with low latency/zero copy. This is especially important for discrete GPUs, since moving raw frames across a PCI bus can be expensive.

Synchronization: Because the multiple hardware units can function independently, they can work asynchronously. For best performance, the application should force synchronization with CPU as infrequently as possible. Design algorithms so that the accelerator can proceed as far as it can without interrupt.

Keeping the hardware busy: If the instruction queue is not kept full, the engine clock will go down. It can take a few milliseconds to ramp up to full clock speed again.

## Media Pipeline Inter-operation and Memory Sharing

Media engine capabilities exposed in low-level OS-specific interfaces, such as:

• VA-API (Video Acceleration API) for Linux OS

• Microsoft DirectX® Video Acceleration for Windows OS

as well as various high-level media frameworks built on top of low-level interfaces, such as:

• Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL)

• FFmpeg and libav

• GStreamer

Each media framework defines own interfaces for device and context creation, memory allocation and task submission. Most frameworks also expose export/import interfaces to convert memory objects to/from other memory handles.

• High-level media frameworks (FFMpeg, GStreamer) support conversion to/from low-level media handles (VA-API and DirectX surfaces).

• Low-level media interfaces (VA-API, DirectX) support conversion to/ OS-specific general-purpose GPU memory handles such as DMA buffers on Linux and NT handles on Windows.

• Level-zero support conversion between DMA buffers / NT handles and USM device pointers.

Together these interfaces allow zero-copy memory sharing between media operations submitted via media frameworks and SYCL compute kernels submitted into SYCL queue, assuming the SYCL queue created on same GPU device as media framework and SYCL device uses Level-zero backend (not OpenCL backend).

Despite multiple stages of memory handles conversion (FFmpeg/GStreamer, VA-API/DirectX, DMA/NT, Level-Zero, SYCL), all converted memory handles refer to the same physical memory block. Thus writing data into one memory handle makes the data available in all other memory handles, assuming proper synchronization between write and read operations.

Below is reference to interfaces used for zero-copy buffer sharing between media frameworks and SYCL

1. (Linux) VA-API to DMA-BUF

2. (Windows) DirectX to NT-Handle

3. DMA-BUF or NT-Handle to Level-zero

The memory pointer created by Level-zero from DMA-BUF or NT-Handle (#3 above) is USM device pointer only accessible by SYCL kernels running on same GPU device as used for media memory allocation and media operations. This USM pointer is not accessible from host and not accessible from SYCL kernels running on CPU or other XPU devices.

Example in next section demonstrates zero-copy buffer sharing between VA-API and SYCL using interfaces 1 and 3 from list above and synthetic video data (moving rectangle). For more advanced examples with FFmpeg/GStreamer video decode/encode on GPU media engine and SYCL kernels on GPU compute engines please refer to Intel® DL Streamer memory interoperability API (preview) and Intel® DL Streamer samples

## VA-API and SYCL Memory Sharing Example

## The example

1. allocates shared VA-API surfaces and USM device pointers for NUM\_FRAMES frames

2. submits VA-API calls to draw moving rectangle on frames

3. submits SYCL kernels to draw sub-rectangle inside rectangle created by VA-API on step 2

4. synchronize all frames and write RGB data into file

Output frames generated by this example look like the picture below.

![](images/1de22f19a947ac676aced2acfc5c09a91ba833049151a13291c6806245ca542a.jpg)

The example supports Linux OS and requires installation of the following additional packages besides oneAPI packages (installation example via apt package manager on Ubuntu OS).

```shell
sudo apt install intel-level-zero-gpu level-zero-dev
sudo apt install intel-media-va-driver-non-free libva-dev libva-drm2
```

and requires linkage with Level-zero and VA-API libraries

```batch
icpx -fsycl memory-sharing-with-media.cpp -lze_loader -lva -lva-drm
```

```batch
ffmpeg -f rawvideo -pix_fmt bgra -s 320x240 -i output.bgra output.mp4 and then played by any media player, for example
```

Example execution generates file output.bgra which could be directly played by some media players (ex, ffplay) or transcoded to compressed video format, for example using the following ffmpeg command:

```c
and then played by any media player, for example
ffplay output.mp4
// SYCL
#include <sycl/sycl.hpp>
// SYCL oneAPI extension
#include <sycl/ext/oneapi/backend/level_zero.hpp>
// Level-zero
#include <level_zero/ze_api.h>
// VA-API
#include <va/va_drm.h>
#include <va/va_drmcommon.h>
#include <cstdio>
#include <fcntl.h>
#include <unistd.h>
#include <vector>
#define OUTPUT_FILE "output.bgra"
#define VAAPI_DEVICE "/dev/dri/renderD128"
#define FRAME_WIDTH 320
#define FRAME_HEIGHT 240
#define RECT_WIDTH 160
#define RECT_HEIGHT 160
#define RECT_Y (FRAME_HEIGHT - RECT_HEIGHT) / 2
#define NUM_FRAMES (FRAME_WIDTH - RECT_WIDTH)
#define VA_FORMAT VA_FOURCC_BGRA
#define RED 0xffff0000
#define GREEN 0xff00ff00
#define BLUE 0xff0000ff
#define CHECK_STS(_FUNC)
{
    auto _sts = _FUNC;
    if (_sts != 0) {
        printf("Error %d calling " #_FUNC, (int)_sts);
        return -1;
    }
}
VASurfaceID alloc_va_surface(VADisplay va_display, int width, int height) {
    VASurfaceID va_surface;
    VASurfaceAttrib surface_attrib {};
    surface_attrib.type = VASurfaceAttribPixelFormat;
    surface_attrib.flags = VA_SURFACE_ATTRIB_SETTABLE;
    surface_attrib.value.type = VAGenericValueTypeInteger;
```

```cpp
surface_attrib.value.value.i = VA_FORMAT;
vaCreateSurfaces(va_display, VA_RT_FORMAT_RGB32, width, height, &va_surface,
                    1, &surface_attrib, 1);
return va_surface;
}

int main() {
  // Create SYCL queue on GPU device and Level-zero backend, and query
  // Level-zero context and device
  sycl::queue sycl_queue{sycl::ext::oneapi::filter_selector(
    "level_zero")}; // { sycl::gpu_selector() }
  auto ze_context = sycl::get_native<sycl::backend::ext_oneapi_level_zero>(
    sycl_queue.get_context());
  auto ze_device = sycl::get_native<sycl::backend::ext_oneapi_level_zero>(
    sycl_queue.get_device());

  // Create VA-API context (VADisplay)
  VADisplay va_display = vaGetDisplayDRM(open(VAAPI_DEVICE, O_RDWR));
  if (!va_display) {
    printf("Error creating VADisplay on device %s\n", VAAPI_DEVICE);
    return -1;
  }
  int major = 0, minor = 0;
  CHECK_STS(vaInitialize(va_display, &major, &minor));

  // Create VA-API surfaces
  VASurfaceID surfaces[NUM_FRAMES];
  for (int i = 0; i < NUM_FRAMES; i++) {
    surfaces[i] = alloc_va_surface(va_display, FRAME_WIDTH, FRAME_HEIGHT);
  }

  // Convert each VA-API surface into USM device pointer (zero-copy buffer
  // sharing between VA-API and Level-zero)
  void *device_ptr[NUM_FRAMES];
  size_t stride;
  for (int i = 0; i < NUM_FRAMES; i++) {
    // Export DMA-FD from VASurface
    VADRMPRIMESurfaceDescriptor prime_desc {};
    CHECK_STS(vaExportSurfaceHandle(va_display, surfaces[i],
                             VA_SURFACE_ATTRIB_MEM_TYPE_DRM_PRIME_2,
                             VA_EXPORT_SURFACE_READ_WRITE, &prime_desc));
    auto dma_fd = prime_desc.objects->fd;
    auto dma_size = prime_desc.objects->size;
    stride = prime_desc.layers[0].pitch[0] / sizeof(uint32_t);

    // Import DMA-FD into Level-zero device pointer
    ze_external_memory_import_fd_t import_fd = {
      ZE_STRUCTURE_TYPE_EXTERNAL_MEMORY_IMPORT_FD,
      nullptr, // pNext
      ZE_EXTERNAL_MEMORY_TYPE_FLAG_DMA_BUF, dma_fd};
    ze_device_mem_alloc_desc_t alloc_desc = {};
    alloc_desc.style = ZE_STRUCTURE_TYPE_DEVICE_MEM_ALLOC_DESC;
    alloc_desc.pNext = &import_fd;
    CHECK_STS(zeMemAllocDevice(ze_context, &alloc_desc, dma_size, 1, ze_device,
                           &device_ptr[i]));
    // Close DMA-FD
    close(dma_fd);
```

```cpp
}

// Create VA-API surface with size 1x1 and write GREEN pixel
VASurfaceID surface1x1 = alloc_va_surface(va_display, 1, 1);
VAImage va_image;
void *data = nullptr;
CHECK_STS(vaDeriveImage(va_display, surface1x1, &va_image));
CHECK_STS(vaMapBuffer(va_display, va_image.buf, &data));
*(uint32_t *)data = GREEN;
CHECK_STS(vaUnmapBuffer(va_display, va_image.buf));
CHECK_STS(vaDestroyImage(va_display, va_image.image_id));

// VA-API call to fill background with BLUE color and upscale 1x1 surface into
// moving GREEN rectangle
VAConfigID va_config_id;
VAContextID va_context_id;
CHECK_STS(vaCreateConfig(va_display, VAProfileNone, VAEntrypointVideoProc,
                                nullptr, 0, &va_config_id));
CHECK_STS(vaCreateContext(va_display, va_config_id, 0, 0, VA_PROGRESSIVE,
                                nullptr, 0, &va_context_id));
for (int i = 0; i < NUM_FRAMES; i++) {
    VAProcPipelineParameterBuffer param {};
    param.output_background_color = BLUE;
    param.surface = surface1x1;
    VARectangle output_region = {int16_t(i), RECT_Y, RECT_WIDTH, RECT_HEIGHT};
    param.output_region = &output_region;
    VABufferID param_buf;
    CHECK_STS(vaCreateBuffer(va_display, va_context_id,
                             VAProcPipelineParameterBufferType, sizeof(param),
                             1, &param, &param_buf));
    CHECK_STS(vaBeginPicture(va_display, va_context_id, surfaces[i]));
    CHECK_STS(vaRenderPicture(va_display, va_context_id, &param_buf, 1));
    CHECK_STS(vaEndPicture(va_display, va_context_id));
    CHECK_STS(vaDestroyBuffer(va_display, param_buf));
}

#if 0
    // Synchronization is optional on Linux OS as i915 KMD driver synchronizes
    // write/read commands submitted from Intel media and compute drivers
    for (int i = 0; i < NUM_FRAMES; i++) {
        CHECK_STS(vaSyncSurface(va_display, surfaces[i]));
    }
#endif

// Submit SYCL kernels to write RED sub-rectangle inside GREEN rectangle
std::vector<sycl::event> sycl_events(NUM_FRAMES);
for (int i = 0; i < NUM_FRAMES; i++) {
    uint32_t *ptr = (uint32_t *)device_ptr[i] +
                    (RECT_Y + RECT_HEIGHT / 4) * stride + (i + RECT_WIDTH / 4);
    sycl_events[i] = sycl_queue.parallel_for(
        sycl::range<2>(RECT_HEIGHT / 2, RECT_WIDTH / 2), [=](sycl::id<2> idx) {
            auto y = idx.get(0);
            auto x = idx.get(1);
            ptr[y * stride + x] = RED;
        });
}

// Synchronize all SYCL kernels
```

```c
sycl::event::wait(sycl_events);

// Map VA-API surface to system memory and write to file
FILE *file = fopen(OUTPUT_FILE, "wb");
if (!file) {
    printf("Error creating file %s\n", OUTPUT_FILE);
    return -1;
}
for (int i = 0; i < NUM_FRAMES; i++) {
    CHECK_STS(vaDeriveImage(va_display, surfaces[i], &va_image));
    CHECK_STS(vaMapBuffer(va_display, va_image.buf, &data));
    fwrite(data, 1, FRAME_HEIGHT * FRAME_WIDTH * 4, file);
    CHECK_STS(vaUnmapBuffer(va_display, va_image.buf));
    CHECK_STS(vaDestroyImage(va_display, va_image.image_id));
}
fclose(file);
printf("Created file %s\n", OUTPUT_FILE);

// Free device pointers and VA-API surfaces
for (int i = 0; i < NUM_FRAMES; i++)
    zeMemFree(ze_context, device_ptr[i]);
vaDestroySurfaces(va_display, surfaces, NUM_FRAMES);

return 0;
```

## SYCL-Blur Example

For a working Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL) example which ties several of these concepts together (currently only for a single stream), see sycl-blur. This sample shows memory interoperation between video APIs and Intel VPL as the frame is input, manipulated and output using the following steps.

• Set up SYCL

• Set up an Intel VPL session

• Initialize Intel VPL VPP

• Loop through frames

• Read the frame from a file

• Run VPP resize/colorspace conversion on the GPU

• Get access to the GPU surface, convert to USM

• Run SYCL kernel (blur) on the GPU

• Output the frame to a file

Find this sample here:

https://github.com/oneapi-src/oneAPI-samples/tree/master/Publications/GPU-Opt-Guide/memory-sharingwith-media

In this example, you can see that the interaction between Intel VPL and SYCL is at a frame level. Intel VPL provides a frame then the SYCL kernel processes it. For the OS environment where zero-copy capabilities are enabled in L0 (Linux), the libva frame data is made available to SYCL as USM. Instead of copying the libva raw frame to a new USM surface, it is possible for the app to work with the frame on the GPU as a libva surface then start working with the same memory as if it were USM.

To keep this example simple there are many design simplifications which currently limit its ability to fully showcase the benefits of zero copy.

• Raw frames are read from disk and written to disk - this sets the overall frame rate

• VPP data is read in as system memory and converted to video memory

• The pipeline is synchronized at each frame

However, zero copy is the core concept which can be built into a high performance application.

## Performance Analysis with Intel® Graphics Performance Analyzers

## Introduction

Intel<sup>®</sup> Graphics Performance Analyzers (Intel<sup>®</sup> GPA)

Intel<sup>®</sup> GPA is a performance analysis tool suite for analysis of applications run on single and multi-CPU platforms as well as single and multi-GPU platforms. It offers detailed analysis of data both visually and via scripting.

Intel<sup>®</sup> GPA consists of 4 GUI tools and a command line tool.

## • GUI Tools

• Graphics Monitor - hub of Intel<sup>®</sup> GPA tools for selecting options and starting trace and frame captures.

• System Analyzer - live analysis of CPU and GPU activity.

• Graphics Trace Analyzer - deep analysis of CPU/GPU interactions during a capture of a few seconds of data.

• Graphics Frame Analyzer - deep analysis of GPU activity in one or more frames.

• Command Line Interface Tool

• Intel<sup>®</sup> GPA Framework - scriptable command line interface allowing the capture and analysis of extensive data from one or more frames.

This chapter focuses on the functionality of Graphics Frame Analyzer for the deep view it provides into GPU behavior.

(Note: Intel<sup>®</sup> GPA Framework can be used to capture the same data as it is the backend of Graphics Frame Analyzer. In addition Intel<sup>®</sup> GPA Framework can be used to automate profiling work.)

## Graphics Frame Analyzer Features

Some of the useful features of Graphics Frame Analyzer are:

• Immediately see which frame of a set of frames takes longest.

• Use Advanced Profiling Mode to automatically calculate your application’s hottest bottlenecks based both on pipeline state and GPU metrics so that optimizing for one frame may optimize multiple parts of your application.

• Geometry - wire frame and solid:

• in seconds you can see if you have drawn outside of your screen view.

• View the geometry at any angle, dynamically.

## • Textures

• Visualize textures draw call by draw call.

• See if a draw call with a long duration is drawing an insignificant part of the frame.

## • Shaders

• See which shader code lines take the most time.

• See how many times each DXR (DirectX Raytracing) shader is called, as well as shader Vector Engine occupancy.

• Render State Experiments - at the push of a button simplify textures or pixels or disable events to help locate the causes of bottlenecks, immediately seeing the changes in the metrics and other data.

## Supported APIs

• Direct3D 11

• Direct3D 12 (including DirectX 12 Ultimate)

• Vulkan

## Execution Unit Stall, Active and Throughput

Graphics Frame Analyzer is a powerful tool that can be used by novice and expert alike to take a quick look at frame duration, API calls, resource data and event data. Understanding more about the meaning of each data element levels you up making it easier to root cause performance issues.

## Execution Stall, Execution Active, Execution Throughput

Knowing how to interpret the interrelationships of these 3 data elements can take you much further in your ability to understand the interworking of your applications with respect to the GPU(s).

## EU, XVE (X<sup>e</sup> Vector Engine), and XMX

As discussed in the \* Intel<sup>®</sup> X<sup>e</sup> GPU Architecture \* section of this document, in X<sup>e</sup>-LP and prior generations of Intel<sup>®</sup> GPUs the EU - execution unit - is the compute unit of the GPU. In X<sup>e</sup>-HPG and X<sup>e</sup>-HPC we introduced the X<sup>e</sup>-core as the compute unit. For these latter platforms each X<sup>e</sup>-core consists of ALUs (arithmetic logic units) - 8 vector engines (XVE) and 8 matrix extensions (XMX).

In Graphics Frame Analyzer, if you are running on X<sup>e</sup>-LP or earlier architecture, you will see EU Active, EU Stall and EU Throughput data labels. On newer architecture you will see XVE Active, XVE Stall and XVE Throughput data labels. Here we use X<sup>e</sup>-LP as our reference architecture, thus we will refer to the EU. But understand that whether it is the EU or the XVE, the Stall/Active/Throughput relationships affect performance in the same ways.

## Understanding these 3 data elements

First, let’s see what it looks like to drill down from the entire X<sup>e</sup>-LP unit with its 96 EUs into a single EU. The General Register File (GRF) on each EU of this particular GPU holds 7 threads. Figure 1 shows the zoom in from the entire GPU to a single EU.

Zooming in on a single EU  
![](images/1bcbb0cafd19d5ba7d10a35627ba631339c0054719250b6138f2b9a87493ecb7.jpg)

Let’s take a closer look at the details of the EU. In Figure 2, of the elements shown, we will focus primarily on the 7 thread slots of the GRF, addressing the importance of the thread interactions with the SEND unit and the 2 ALUs.

View of the GRF, the ALUs and the Thread Control, Branch and SEND units.

![](images/345cc1b4d590b6b2d66e58632a743b50835b1a34138fafd657eb6b20b2f4322e.jpg)

Now let’s look at a threading scenario. Figure 3 shows the contents of the GRF. We see that the GRF of this EU is loaded with only one thread in this instant. We see that single thread executing for some quantity of time. This means that one or both of the ALUs are invoked to execute instructions. At some point that thread needs to either read or write data, which activates the SEND unit. While the thread waits for the read/write to complete, the EU is stalled - it has a thread loaded but nothing to compute during that time.

The GRF contains a single thread.  
![](images/24605f67c866a476d5ebad761acaedb98f3c314b92b6fe2344527e9cf7e85a65.jpg)  
Augmenting this scenario, in Figure 4 there is a second thread in the EU. If there is a second thread loaded into the GRF of this EU, then, at the time when the first thread invokes the SEND unit, instead of stalling execution, the EU begins executing the instructions of the second thread. When that second thread invokes a

command requiring the SEND unit, the EU becomes stalled until the first thread is able to continue. Had there been a third thread in this EU or if the first SEND returned sooner, all latency may have been hidden, resulting in thread latency, but no stall during this time for this EU.

The ALUs do nothing (no execution of instructions) while the EU waits for data to be read or written.

<table><tr><td></td><td></td><td>AVC</td><td>MPEG 2</td><td>JPEG</td><td>VP8</td><td>HEVC 8-bit</td><td>HEVC 8-bit 422</td><td>HEVC 8-bit 444</td><td>H10</td></tr><tr><td>CPU</td><td></td><td>D/E*</td><td>D</td><td>D/E</td><td></td><td>D/E</td><td></td><td></td><td>D</td></tr><tr><td rowspan="6">Media SDK GPU</td><td> $5^{th}$ Generation Intel®Core (BDW)</td><td>D/Es</td><td>D/Es</td><td>D</td><td>D</td><td></td><td></td><td></td><td></td></tr><tr><td> $6^{th}$ Generation Intel®Core (SKL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td></td></tr><tr><td>Intel Atom®Processor E3900 series (APL)</td><td>D/E/Es</td><td>D</td><td>D/E</td><td>D</td><td>D/Es</td><td></td><td></td><td>D</td></tr><tr><td> $7^{th}$ Generation Intel®Core (KBLx)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/Es</td><td></td><td></td><td>D</td></tr><tr><td> $10^{th}$ Generation Intel®Core (ICL)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D/Es</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D</td></tr><tr><td>Intel Atom®Processor X Series (EHL)</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td><td>D/E</td><td>D</td></tr><tr><td rowspan="2">oneVPL GPU</td><td>Intel®Iris®Xe (TGL/RKL/ADL),Intel®Iris®Xe MAX (DG1)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D(TGL only)</td><td>D/E/Es</td><td>D/Es</td><td>D/E</td><td>D</td></tr><tr><td>Intel®ARC</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D</td><td>D/E</td><td>D/E</td><td>D/E</td><td>D</td></tr></table>

## Terminology

For the following definitions the resulting data calculated

• is the average across all EUs;

• consists of both the full frame data and the data for the selected portion of the frame. The selection may be a single call or a set of calls, or even a set of frames.

## Idle

EU Idle is the percentage of time when no thread is loaded.

## Active

EU Active is the percentage of time when ALU0 or ALU1 were executing some instruction. It should be as high as possible; a low value is caused either by a lot of stalls or EUs being idle.

## Stall

EU Stall is the percentage of time, when one or more threads are loaded but none of them are able to execute because they are waiting for a read or write.

## Thread Occupancy

EU Thread Occupancy is the percentage of occupied GRF slots (threads loaded). This generally should be as high as possible. If the EU Thread Occupancy value is low, this indicates either a bottleneck in preceding HW blocks, such as vertex fetch or thread dispatch, or, for compute shaders it indicates a suboptimal SIMD-width or Shared Local Memory usage.

If only a single thread is executing on each of the 96 EUs, then 1 of 7 slots/EU is occupied, resulting in thread occupancy of 1/7 (14%).

If 2 EUs have no threads loaded (they are idle) but the other 94 EUs have 6 threads loaded, we have occupancy = (0 + 0 + 6\*94)/672 = 84%.

The Thread Occupancy values you will see in Graphics Frame Analyzer indicate the average occupancy across all EUs over the time selected. Though other hardware may have a different number of EUs or XVEs, the calculations are over all execution units. For example, below, on the left, you see a frame where over the entire frame duration of 6ms, though thread occupancy fluctuated during that 6ms, the average over that time for all 96 EUs is 77%. We can also look at thread occupancy over a part of the frame duration. Below, on the right, we select the 3 most time-consuming draw calls and see that during the 1.9ms that it took to execute these bits of the application, thread occupancy is 85.3%.

![](images/1578ba27c44f06bbaf4104c6f70eed2a15ade8e1ed0d973447d148f4b415a6db.jpg)

## Graphics Frame Analyzer

View this data in Intel<sup>®</sup> GPA’s Graphics Frame Analyzer. For usage, see our 8 short videos and/or their corresponding articles. Video Series: An In-Depth Look at Graphics Frame Analyzer (intel.com)

In Graphics Frame Analyzer after opening a frame, you will see a view such as that in Figure 5. If you look at the data just after opening the frame, you will see data percentage values for the entire frame. That means the percentages averaged over all 96 EUs over the frame time for data such as Active, Stall and Throughput.

Data values averaged across all EUs over the entire frame time.

![](images/5546b1eab6746fc13569a05c808bc4da1246d5fa5d09e610405fb88e88cf5517.jpg)

You can then select a single draw call or a set of calls to see that same data recalculated for the part of the frame you have selected.

After making a selection, in this case calls 91, 94 and 95, the data will be recalculated to represent the data for only those calls.

<table><tr><td>Frame0</td><td>Frame1</td><td>Frame2</td><td>...</td><td>FrameN</td></tr></table>

Additionally, if you captured a stream, it will open in multi-frame view. From there you can select a single frame or multiple frames. If you select multiple frames the data calculated will be the aggregate of the date from all selected frames.

While it is important to understand how the GPU works and what the metrics mean for efficient profiling, you don’t need to analyze each draw call in your frame manually in order to understand the problem type. To help with this sort of analysis, Intel<sup>®</sup> GPA provides automatic hotspot analysis - Advanced Profiling Mode.

## Hotspot Analysis

Now that we have some understanding of the EU architecture, let’s look at how that knowledge manifests in the profiler.

When you enable Advanced Profiling Mode Graphics, Graphics Frame Analyzer delineates bottlenecks by bottleneck type and pipeline state. This categorization provides the additional benefit of a fix for one issue often fixing not only the local issue, but rather an entire category of issues.

In Graphics Frame Analyzer enable Hotspot Analysis by clicking on the button on the top left of the tool - shown in Fig 7. The Bar Chart across the top then shows the bottlenecks, and the API Log in the left pane changes to show the bottleneck types. When you click on a bottleneck the metrics viewer will show more details about the bottleneck, with metrics descriptions and suggestions to alleviate the bottleneck.

![](images/b744a4faa41aafbbd3df48f955d753d65c8a54e091f0d45e92b0bf1c668cdf28.jpg)  
Hotspot: L2 Cache

Characterization of an L2 Cache Hotspot

When the application has high thread occupancy, close to 90%, that is good. But if the high thread occupancy is coupled with stall, greater than 5-10%, you may have an L2 Cache bottleneck.

With a frame open in Graphics Frame Analyzer, look at the Metrics Viewer Panel on the right, enlarged in Fig. x. Occupancy is more than 90%, but there is still a stall in the EU, which means that EU threads are waiting for some data from memory.

![](images/66a235ea802329a20d239ad29f625e11078f69b84737725142072b4c643ee879.jpg)

## Shader Profiler

For further analysis use the Shader Profiler to see per-instruction execution latencies. As you already know latency is not always equal to stall. However, an instruction with higher latency has a higher probability to cause a stall. And, therefore, when dealing with an EU Stall bottleneck, Shader Profiler gives a good approximation of what instructions most likely caused the stall.

## Enable Shader Profiler

Access the shader profiler by doing the following. Click on any shader in the Resource List, in this case SH:17, to display the shader code in the Resource Panel. Then click the flame button at the top of the Resource Pane to see the shader code with the lines taking the most time annotated with the timings, toggle between execution count and duration (percentage of frame time consumed).

## Map Shader Code to Assembly Code

For a potential L2 Cache bottleneck, you will also want to see the assembly code, where you will find the

![](images/c88a4b73463729382bfeb3c8e02bb2f8c5c350b90dfff5973f730bd9437a4071.jpg)

send commands from the Send Unit. Click the button in the Resource Panel above the shader code to see the mapping from the shader code to the assembly code.

![](images/e0eb7f5d310bdb7b2080aafec1ad1315143cb903819e6322c33ff7dbe6daece9.jpg)

Identify the Root Cause of the L2 Bottleneck

To find the root cause of an L2 Cache bottleneck, scroll through the assembly code, looking for the send instructions with the longest duration. Then identify which shader source portions caused them.

In the case of the application being profiled in Fig x, above, the CalcUnshadowedAmountPCF2x2 function which samples from ShadowMap and reads the constant buffer is cause of this bottleneck.

Hotspot: Shader Execution

Characterization of a Shader Execution Bottleneck

A Shader Execution bottleneck is characterized by very high thread occupancy and very low stall time. These are good. However, if the application reduced execution time, it is necessary to optimize the shader code itself.

![](images/297c92798906f49d0a8da4e6b19e597fa410ad220d990a04f752a1aa6cc792e8.jpg)  
Identify the Root Cause of the Shader Execution Bottleneck

For a shader execution bottleneck, it is necessary to analyze the hotspots in shader source code caused by arithmetic operations. Find these by toggling to Duration Mode in the shader profiler, then scroll through the code to find the lines of shader code that take exceedingly long. CalcLightingColor does calculations involving both simple and transcendental operations. Fig x shows that this function in this single shader consumes about 20% of the total frame time. In order to resolve this bottleneck this algorithm must be optimized.

![](images/cf140ef28ef06a9fcf775ba4984844cda832cb002c59a2b601f72b2c1dbfce0c.jpg)  
Hotspot: Thread Dispatch

## Characterization of a Thread Dispatch Bottleneck

In this final example of hotspot analysis there is a sequence of draw calls which have a Thread Dispatch bottleneck. In this particular case we have a rather high stall rate (20%) and low thread occupancy (66%). As stated earlier, low occupancy may be caused by an insufficient number of threads loaded on the EU. Thus, instead of directly fixing stall time in shader code, it is necessary, instead, to increase the overall EU Occupancy.

![](images/8acfc86398396bcbe2e73548000c7fc18eb53ed80607f83e394e034b0e651ad2.jpg)  
Identify the Root Cause of the Thread Dispatch Bottleneck

Which is better, SIMD8 or SIMD16?

Open Shader Profiler, but in Execution Count mode rather than Duration mode which shows how many times each instruction was executed. In Fig x notice that the pixel shader has been compiled into both SIMD8 and SIMD16. Shader Profiler shows that each instruction in the SIMD8 version was executed 24,000 times, while instructions in SIMD16 were executed 16,000 times - a 1.5 times difference!

It is preferable to have more SIMD16 threads, as they perform twice as many operations per single dispatch, compared to SIMD8 threads. Why so many SIMD8 dispatches? And why should there be 2 SIMD versions for the Pixel Shader?

![](images/6d473f011e596b9553f4ac050cde10d9f7630326d2910df7ee2b3e7b16d3ab34.jpg)

## Examine the Geometry

The geometry for these draw calls is rather fine-grained. The observed anomaly is a result of how the GPU handles pixel shading. The shader compiler produced two SIMD versions, SIMD8 and SIMD16. This is required so that the pixel shader dispatcher can choose which one to execute based on the rasterization result. It is important to know that hardware does not shade pixels one at a time. Instead shading happens in groups. A single pixel shader hardware thread shades 16 pixels at a time for SIMD16. With SIMD16, if a primitive is rasterized into very few or just a single pixel, then the GPU will still shade 16 pixels and will discard all those which were unnecessary. Therefore, in order to discard less, the pixel shader dispatcher schedules SIMD8 for very small primitives. This is the case here. A large number of highly-detailed geometry (many small primitives) produced a huge number of SIMD8 invocations. As you may guess, in order to fix such a performance problem you need to use geometry LODs in your game

![](images/44587ed500fac5f3f1f27054dd2c9dede0e77844a90fabf1262d53c0f603b627.jpg)
````
