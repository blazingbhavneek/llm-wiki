## Table of Contents

About the Authors....xix
Preface ....xxi
Foreword ....xxv
Acknowledgments ....xxix
Chapter 1: Introduction....1
Read the Book, Not the Spec ....2
SYCL 2020 and DPC++ ....3
Why Not CUDA? ....4
Why Standard C++ with SYCL? ....5
Getting a C++ Compiler with SYCL Support ....5
Hello, World! and a SYCL Program Dissection....6
Queues and Actions ....7
It Is All About Parallelism ....8
Throughput ....8
Latency ....9
Think Parallel....9
Amdahl and Gustafson ....10
Scaling....11
Heterogeneous Systems....11
Data-Parallel Programming ....13

Key Attributes of C++ with SYCL....14
Single-Source....14
Host....15
Devices....15
Kernel Code....16
Asynchronous Execution....18
Race Conditions When We Make a Mistake....19
Deadlock....22
C++ Lambda Expressions....23
Functional Portability and Performance Portability....26
Concurrency vs. Parallelism....28
Summary....30

Chapter 2: Where Code Executes....31
Single-Source....31
Host Code....33
Device Code....34
Choosing Devices....36
Method#1: Run on a Device of Any Type....37
Queues....37
Binding a Queue to a Device When Any Device Will Do....41
Method#2: Using a CPU Device for Development, Debugging, and Deployment....42
Method#3: Using a GPU (or Other Accelerators)....45
Accelerator Devices....46
Device Selectors....46
Method#4: Using Multiple Devices....50

Method#5: Custom (Very Specific) Device Selection....51
Selection Based on Device Aspects....51
Selection Through a Custom Selector....53
Creating Work on a Device....54
Introducing the Task Graph....54
Where Is the Device Code?....56
Actions....60
Host tasks....63
Summary....65
Chapter 3: Data Management....67
Introduction....68
The Data Management Problem....69
Device Local vs. Device Remote....69
Managing Multiple Memories....70
Explicit Data Movement....70
Implicit Data Movement....71
Selecting the Right Strategy....71
USM, Buffers, and Images....72
Unified Shared Memory....72
Accessing Memory Through Pointers....73
USM and Data Movement....74
Buffers....77
Creating Buffers....78
Accessing Buffers....78
Access Modes....80

Ordering the Uses of Data....80
In-order Queues....83
Out-of-Order Queues....84
Choosing a Data Management Strategy....92
Handler Class: Key Members....93
Summary....96
Chapter 4: Expressing Parallelism....97
Parallelism Within Kernels....98
Loops vs. Kernels....99
Multidimensional Kernels....101
Overview of Language Features....102
Separating Kernels from Host Code....102
Different Forms of Parallel Kernels....103
Basic Data-Parallel Kernels....105
Understanding Basic Data-Parallel Kernels....105
Writing Basic Data-Parallel Kernels....107
Details of Basic Data-Parallel Kernels....109
Explicit ND-Range Kernels....112
Understanding Explicit ND-Range Parallel Kernels....113
Writing Explicit ND-Range Data-Parallel Kernels....121
Details of Explicit ND-Range Data-Parallel Kernels....122
Mapping Computation to Work-Items....127
One-to-One Mapping....128
Many-to-One Mapping....128
Choosing a Kernel Form....130
Summary....132

Chapter 5: Error Handling....135
Safety First....135
Types of Errors....136
Let's Create Some Errors!....138
Synchronous Error....139
Asynchronous Error....139
Application Error Handling Strategy....140
Ignoring Error Handling....141
Synchronous Error Handling....143
Asynchronous Error Handling....144
The Asynchronous Handler....145
Invocation of the Handler....148
Errors on a Device....149
Summary....150
Chapter 6: Unified Shared Memory....153
Why Should We Use USM?....153
Allocation Types....154
Device Allocations....154
Host Allocations....155
Shared Allocations....155
Allocating Memory....156
What Do We Need to Know?....156
Multiple Styles....157
Deallocating Memory....164
Allocation Example....165

Data Management....165
Initialization....165
Data Movement....166
Queries....174
One More Thing....177
Summary....178
Chapter 7: Buffers....179
Buffers....180
Buffer Creation....181
What Can We Do with a Buffer?....188
Accessors....189
Accessor Creation....192
What Can We Do with an Accessor?....198
Summary....199
Chapter 8: Scheduling Kernels and Data Movement....201
What Is Graph Scheduling?....202
How Graphs Work in SYCL....202
Command Group Actions....203
How Command Groups Declare Dependences....203
Examples....204
When Are the Parts of a Command Group Executed?....213
Data Movement....213
Explicit Data Movement....213
Implicit Data Movement....214
Synchronizing with the Host....216
Summary....218

Chapter 9: Communication and Synchronization....221
Work-Groups and Work-Items....221
Building Blocks for Efficient Communication....223
Synchronization via Barriers....223
Work-Group Local Memory....225
Using Work-Group Barriers and Local Memory....227
Work-Group Barriers and Local Memory in ND-Range Kernels....231
Sub-Groups....235
Synchronization via Sub-Group Barriers....236
Exchanging Data Within a Sub-Group....237
A Full Sub-Group ND-Range Kernel Example....239
Group Functions and Group Algorithms....241
Broadcast....241
Votes....242
Shuffles....243
Summary....246
Chapter 10: Defining Kernels....249
Why Three Ways to Represent a Kernel?....249
Kernels as Lambda Expressions....251
Elements of a Kernel Lambda Expression....251
Identifying Kernel Lambda Expressions....254
Kernels as Named Function Objects....255
Elements of a Kernel Named Function Object....256
Kernels in Kernel Bundles....259
Interoperability with Other APIs....264
Summary....264

Chapter 11: Vectors and Math Arrays....267
The Ambiguity of Vector Types....268
Our Mental Model for SYCL Vector Types....269
Math Array (marray)....271
Vector (vec)....273
Loads and Stores....274
Interoperability with Backend-Native Vector Types....276
Swizzle Operations....276
How Vector Types Execute....280
Vectors as Convenience Types....280
Vectors as SIMD Types....284
Summary....286
Chapter 12: Device Information and Kernel Specialization....289
Is There a GPU Present?....290
Refining Kernel Code to Be More Prescriptive....291
How to Enumerate Devices and Capabilities....293
Aspects....296
Custom Device Selector....298
Being Curious: get\_info<>....300
Being More Curious: Detailed Enumeration Code....301
Very Curious: get\_info plus has()....303
Device Information Descriptors....303
Device-Specific Kernel Information Descriptors....303
The Specifics: Those of “Correctness”....304
Device Queries....305
Kernel Queries....306

The Specifics: Those of "Tuning/Optimization"....307
Device Queries....307
Kernel Queries....308
Runtime vs. Compile-Time Properties....308
Kernel Specialization....309
Summary....312
Chapter 13: Practical Tips....313
Getting the Code Samples and a Compiler....313
Online Resources....313
Platform Model....314
Multiarchitecture Binaries....315
Compilation Model....316
Contexts: Important Things to Know....319
Adding SYCL to Existing C++ Programs....321
Considerations When Using Multiple Compilers....322
Debugging....323
Debugging Deadlock and Other Synchronization Issues....325
Debugging Kernel Code....326
Debugging Runtime Failures....327
Queue Profiling and Resulting Timing Capabilities....330
Tracing and Profiling Tools Interfaces....334
Initializing Data and Accessing Kernel Outputs....335
Multiple Translation Units....344
Performance Implication of Multiple Translation Units....345
When Anonymous Lambdas Need Names....345
Summary....346

Chapter 14: Common Parallel Patterns....349
Understanding the Patterns....350
Map....351
Stencil ....352
Reduction ....354
Scan....356
Pack and Unpack....358
Using Built-In Functions and Libraries....360
The SYCL Reduction Library ....360
Group Algorithms....366
Direct Programming....370
Map....370
Stencil ....371
Reduction ....373
Scan....374
Pack and Unpack....377
Summary....380
For More Information....381
Chapter 15: Programming for GPUs....383
Performance Caveats....383
How GPUs Work....384
GPU Building Blocks....384
Simpler Processors (but More of Them)....386
Simplified Control Logic (SIMD Instructions)....391
Switching Work to Hide Latency....398
Offloading Kernels to GPUs....400
SYCL Runtime Library....400
GPU Software Drivers....401

GPU Hardware....402
Beware the Cost of Offloading!....403
GPU Kernel Best Practices....405
Accessing Global Memory....405
Accessing Work-Group Local Memory....409
Avoiding Local Memory Entirely with Sub-Groups....412
Optimizing Computation Using Small Data Types....412
Optimizing Math Functions....413
Specialized Functions and Extensions....414
Summary....414
For More Information....415
Chapter 16: Programming for CPUs....417
Performance Caveats....418
The Basics of Multicore CPUs....419
The Basics of SIMD Hardware....422
Exploiting Thread-Level Parallelism....428
Thread Affinity Insight....431
Be Mindful of First Touch to Memory....435
SIMD Vectorization on CPU....436
Ensure SIMD Execution Legality....437
SIMD Masking and Cost....440
Avoid Array of Struct for SIMD Efficiency....442
Data Type Impact on SIMD Efficiency....444
SIMD Execution Using single\_task....446
Summary....448

Chapter 17: Programming for FPGAs....451
Performance Caveats....452
How to Think About FPGAs....452
Pipeline Parallelism....456
Kernels Consume Chip “Area”....459
When to Use an FPGA....460
Lots and Lots of Work....460
Custom Operations or Operation Widths....461
Scalar Data Flow....462
Low Latency and Rich Connectivity....463
Customized Memory Systems....464
Running on an FPGA....465
Compile Times....467
The FPGA Emulator....469
FPGA Hardware Compilation Occurs “Ahead-of-Time”....470
Writing Kernels for FPGAs....471
Exposing Parallelism....472
Keeping the Pipeline Busy Using ND-Ranges....475
Pipelines Do Not Mind Data Dependences!....478
Spatial Pipeline Implementation of a Loop....481
Loop Initiation Interval....483
Pipes....489
Custom Memory Systems....495
Some Closing Topics....498
FPGA Building Blocks....498
Clock Frequency....500
Summary....501

Chapter 18: Libraries....503
Built-In Functions....504
Use the sycl:: Prefix with Built-In Functions....506
The C++ Standard Library....507
oneAPI DPC++ Library (oneDPL)....510
SYCL Execution Policy....511
Using oneDPL with Buffers....513
Using oneDPL with USM....517
Error Handling with SYCL Execution Policies....519
Summary....520
Chapter 19: Memory Model and Atomics....523
What's in a Memory Model?....525
Data Races and Synchronization....526
Barriers and Fences....529
Atomic Operations....531
Memory Ordering....532
The Memory Model....534
The memory\_order Enumeration Class....536
The memory\_scope Enumeration Class....538
Querying Device Capabilities....540
Barriers and Fences....542
Atomic Operations in SYCL....543
Using Atomics with Buffers....548
Using Atomics with Unified Shared Memory....550
Using Atomics in Real Life....550
Computing a Histogram....551
Implementing Device-Wide Synchronization....553

Summary....556
For More Information....557

Chapter 20: Backend Interoperability....559
What Is Backend Interoperability?....559
When Is Backend Interoperability Useful?....561
Adding SYCL to an Existing Codebase....562
Using Existing Libraries with SYCL....564
Using Backend Interoperability for Kernels....569
Interoperability with API-Defined Kernel Objects....569
Interoperability with Non-SYCL Source Languages....571
Backend Interoperability Hints and Tips....574
Choosing a Device for a Specific Backend....574
Be Careful About Contexts!....576
Access Low-Level API-Specific Features....576
Support for Other Backends....577
Summary....577

Chapter 21: Migrating CUDA Code....579
Design Differences Between CUDA and SYCL....579
Multiple Targets vs. Single Device Targets....579
Aligning to C++ vs. Extending C++....581
Terminology Differences Between CUDA and SYCL....582
Similarities and Differences....583
Execution Model....584
Memory Model....589
Other Differences....592

Features in CUDA That Aren't In SYCL... Yet!....595
Global Variables....595
Cooperative Groups....596
Matrix Multiplication Hardware....597
Porting Tools and Techniques....598
Migrating Code with dpct and SYCLomatic....598
Summary....603
For More Information....604
Epilogue: Future Direction of SYCL....605
Index....615
