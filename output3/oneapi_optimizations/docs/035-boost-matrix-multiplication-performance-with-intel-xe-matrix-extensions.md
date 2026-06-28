## Boost Matrix Multiplication Performance with Intel® Xe Matrix Extensions

The increasing popularity of Artificial Intelligence (AI) in today’s world demands the introduction of low precision data types and hardware support for these data types to boost application performance. Low precision models are faster in computation and have smaller memory footprints. For the same reason low precision data types are getting highly used for both training and inference in AI / machine learning (ML) even though float32 is the default data type. To optimize and support these low precision data types, special hardware features and instructions are required. Intel provides those in the form of Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions (Intel<sup>®</sup> XMX) in its GPUs. Some of the most used 16-bit formats and 8-bit formats are float16 (fp16), bfloat16 (bf16), 16-bit integer (int16), 8-bit integer (int8) etc. The figure below visualizes the differences between some of these formats.

![](images/63da75d6ddb0956738a45f602cb731d72843b26f5a1a18269fa2cd88d9d29e89.jpg)  
In the above figure, s is the signed bit(the first digit of the binary presentation, 0 implies positive number and 1 implies negative number) and exp is the exponent.

## Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions

Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions (Intel<sup>®</sup> XMX) specializes in executing Dot Product Accumulate Systolic (DPAS) instructions on 2D systolic arrays. A systolic array in parallel computer architecture is a homogeneous network of tightly coupled data processing units. Each unit computes a partial result as a function of data received from its upstream neighbors, stores the result within itself and passes it downstream. Intel<sup>®</sup> XMX supports numerous data types, depending on hardware generation, such as int8, fp16, bf16, and tf32. To understand Intel<sup>®</sup> XMX inside Intel<sup>®</sup> Data Center GPU Max Series, please refer to Intel<sup>®</sup> Intel<sup>®</sup> Iris<sup>®</sup> X<sup>e</sup> GPU Architecture section.

## Programming Intel<sup>®</sup> XMX

Users can interact with XMX at many different levels: from deep learning frameworks, dedicated libraries, custom SYCL kernels, down to low-level intrinsics. Programming and running applications using Intel XMX requires Intel<sup>®</sup> oneAPI Base Toolkit.

Using Intel<sup>®</sup> oneAPI Deep Neural Network Library (oneDNN)

To take the maximum advantage of the hardware, oneDNN has enabled Intel<sup>®</sup> XMX support on Intel GPUs (Intel<sup>®</sup> X<sup>e</sup> 4th Generation Scalable processors and later) by default. To uses the data types supported by XMX and oneDNN, the applications needs to be built with GPU support enabled.

The Matrix Multiplication Performance bundled with oneDNN is a good example to learn how to use oneDNN to program Intel XMX.

## Using Intel<sup>®</sup> oneAPI Math Kernel Library (oneMKL)

Like oneDNN, oneMKL also enables Intel<sup>®</sup> XMX by default if we use the supported data types and the code is compiled using the Intel<sup>®</sup> oneAPI DPC++ Compiler.

oneMKL supports several algorithms for accelerating single-precision gemm and gemm\_batch using XMX. The bf16x2 and bf16x3 are 2 such algorithms using bf16 to approximate single-precision gemm.

Internally single-precision input data is converted into bf16 and multiplied with the systolic array. The three variants – bf16, bf16x2, and bf16x3 – allow you to make a tradeoff between accuracy and performance, with bf16 being the fastest and bf16x3 the most accurate (similar to the accuracy of standard single-precision gemm). The example Matrix Multiplication shows how to use these algorithms and the table below compares the performance difference.

<table><tr><td>Precision</td><td>Data type/ Algorithm</td><td>Peak (TF)</td><td>Performance relative totheoretical peak ofsingle precision(%)</td></tr><tr><td>Single</td><td>fp32</td><td>26</td><td>98</td></tr><tr><td>Single</td><td>bf16</td><td>151</td><td>577</td></tr><tr><td>Single</td><td>bf16x2</td><td>74</td><td>280</td></tr><tr><td>Single</td><td>bf16x3</td><td>42</td><td>161</td></tr></table>

![](images/bf7a9cb8dd402e5c289b65e5e65d4eb404bc7c9dbe92556e21e824ca827edbd9.jpg)  
The test is performed on a Intel<sup>®</sup> Xeon<sup>®</sup> 8480+ with512 GB DDR5-4800 + Intel<sup>®</sup> Data Center GPU Max 1550 running Ubuntu 22.04.

This table shows the Performance of bf16, bf16x2 and bf16x3 far outweigh the theoretical peak of single precision. If the accuracy tradeoff is acceptable, bf16, followed by bf16x2 and then bf16x3, is highly recommended.
