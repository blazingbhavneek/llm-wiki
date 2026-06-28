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
