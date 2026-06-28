![](images/a23e9ab4278380e5210fa318a790495e17e2bf20da37894bd51a1d6f2ee3ad0e.jpg)

CUDA C++ Programming Guide

Release 13.3

NVIDIA Corporation

May 21, 2026

## Contents

1 Overview
2 What Is the CUDA C Programming Guide?
3 Introduction
3.1 The Benefits of Using GPUs ..... 5
3.2 CUDA®: A General-Purpose Parallel Computing Platform and Programming Model ..... 6
3.3 A Scalable Programming Model ..... 6
4 Changelog
5 Programming Model
5.1 Kernels ..... 11
5.2 Thread Hierarchy ..... 12
5.2.1 Thread Block Clusters ..... 14
5.2.2 Blocks as Clusters ..... 16
5.3 Memory Hierarchy ..... 16
5.4 Heterogeneous Programming ..... 18
5.5 Asynchronous SIMT Programming Model ..... 18
5.5.1 Asynchronous Operations ..... 18
5.6 Compute Capability ..... 20
6 Programming Interface
6.1 Compilation with NVCC ..... 23
6.1.1 Compilation Workflow ..... 24
6.1.1.1 Offline Compilation ..... 24
6.1.1.2 Just-in-Time Compilation ..... 24
6.1.2 Binary Compatibility ..... 25
6.1.3 PTX Compatibility ..... 25
6.1.4 Application Compatibility ..... 25
6.1.5 C++ Compatibility ..... 27
6.1.6 64-Bit Compatibility ..... 27
6.2 CUDA Runtime ..... 27
6.2.1 Initialization ..... 28
6.2.2 Device Memory ..... 28
6.2.3 Device Memory L2 Access Management ..... 32
6.2.3.1 L2 Cache Set-Aside for Persisting Accesses ..... 32
6.2.3.2 L2 Policy for Persisting Accesses ..... 32
6.2.3.3 L2 Access Properties ..... 34
6.2.3.4 L2 Persistence Example ..... 34
6.2.3.5 Reset L2 Access to Normal ..... 35
6.2.3.6 Manage Utilization of L2 set-aside cache ..... 35
6.2.3.7 Query L2 cache Properties ..... 36
6.2.3.8 Control L2 Cache Set-Aside Size for Persisting Memory Access ..... 36

6.2.4 Shared Memory 36
6.2.5 Distributed Shared Memory 41
6.2.6 Page-Locked Host Memory 44
6.2.6.1 Portable Memory 45
6.2.6.2 Write-Combining Memory 45
6.2.6.3 Mapped Memory 45
6.2.7 Memory Synchronization Domains 46
6.2.7.1 Memory Fence Interference 46
6.2.7.2 Isolating Traffic with Domains 47
6.2.7.3 Using Domains in CUDA 47
6.2.8 Asynchronous Concurrent Execution 48
6.2.8.1 Concurrent Execution between Host and Device 49
6.2.8.2 Concurrent Kernel Execution 49
6.2.8.3 Overlap of Data Transfer and Kernel Execution 50
6.2.8.4 Concurrent Data Transfers 50
6.2.8.5 Streams 50
6.2.8.6 Programmatic Dependent Launch and Synchronization 54
6.2.8.7 CUDA Graphs 57
6.2.8.8 Events 84
6.2.8.9 Synchronous Calls 85
6.2.9 Multi-Device System 85
6.2.9.1 Device Enumeration 85
6.2.9.2 Device Selection 85
6.2.9.3 Stream and Event Behavior 86
6.2.9.4 Peer-to-Peer Memory Access 86
6.2.9.5 Peer-to-Peer Memory Copy 87
6.2.10 Unified Virtual Address Space 88
6.2.11 Interprocess Communication 88
6.2.12 Error Checking 89
6.2.13 Call Stack 89
6.2.14 Texture and Surface Memory 90
6.2.14.1 Texture Memory 90
6.2.14.2 Surface Memory 95
6.2.14.3 CUDA Arrays 98
6.2.14.4 Read/Write Coherency 98
6.2.15 Graphics Interoperability 98
6.2.15.1 OpenGL Interoperability 99
6.2.15.2 Direct3D Interoperability 101
6.2.15.3 SLI Interoperability 107
6.2.16 External Resource Interoperability 108
6.2.16.1 Vulkan Interoperability 109
6.2.16.2 OpenGL Interoperability 116
6.2.16.3 Direct3D 12 Interoperability 117
6.2.16.4 Direct3D 11 Interoperability 123
6.2.16.5 NVIDIA Software Communication Interface Interoperability (NVSCI) 132
6.3 Versioning and Compatibility 137
6.4 Compute Modes 138
6.5 Mode Switches 139
6.6 Tesla Compute Cluster Mode for Windows 139

Hardware Implementation 141
7.1 SIMT Architecture 141
7.2 Hardware Multithreading 143

8 Performance Guidelines 145
8.1 Overall Performance Optimization Strategies 145
8.2 Maximize Utilization 145
8.2.1 Application Level 146
8.2.2 Device Level 146
8.2.3 Multiprocessor Level 146
8.2.3.1 Occupancy Calculator 148
8.3 Maximize Memory Throughput 150
8.3.1 Data Transfer between Host and Device 151
8.3.2 Device Memory Accesses 152
8.4 Maximize Instruction Throughput 155
8.5 Minimize Memory Thrashing 155

9 CUDA-Enabled GPUs 157

10 C++ Language Extensions 159
10.1 Function Execution Space Specifiers 159
10.1.1 \_\_global\_\_ 159
10.1.2 \_\_device\_\_ 160
10.1.3 \_\_host\_\_ 160
10.1.4 Undefined behavior 160
10.1.5 \_\_noinline\_\_ and \_\_forceinline\_\_ 161
10.1.6 \_\_inline\_hint\_\_ 161
10.2 Variable Memory Space Specifiers 161
10.2.1 \_\_device\_\_ 161
10.2.2 \_\_constant\_\_ 162
10.2.3 \_\_shared\_\_ 162
10.2.4 \_\_grid\_constant\_\_ 163
10.2.5 \_\_managed\_\_ 164
10.2.6 \_\_restrict\_\_ 164
10.3 Built-in Vector Types 165
10.3.1 char, short, int, long, longlong, float, double 165
10.3.2 dim3 167
10.4 Built-in Variables 167
10.4.1 gridDim 167
10.4.2 blockIdx 167
10.4.3 blockDim 167
10.4.4 threadIdx 168
10.4.5 warpSize 168
10.5 Memory Fence Functions 168
10.6 Synchronization Functions 171
10.7 Mathematical Functions 172
10.8 Texture Functions 172
10.8.1 Texture Object API 172
10.8.1.1 texIDfetch() 172
10.8.1.2 texID() 172
10.8.1.3 texIDLod() 173
10.8.1.4 texIDGrad() 173
10.8.1.5 tex2D() 173
10.8.1.6 tex2D() for sparse CUDA arrays 173
10.8.1.7 tex2Dgather() 173
10.8.1.8 tex2Dgather() for sparse CUDA arrays 174
10.8.1.9 tex2DGrad() 174
10.8.1.10 tex2DGrad() for sparse CUDA arrays 174

10.8.1.11 tex2DLod() 174
10.8.1.12 tex2DLod() for sparse CUDA arrays 174
10.8.1.13 tex3D() 175
10.8.1.14 tex3D() for sparse CUDA arrays 175
10.8.1.15 tex3DLod() 175
10.8.1.16 tex3DLod() for sparse CUDA arrays 175
10.8.1.17 tex3DGrad() 175
10.8.1.18 tex3DGrad() for sparse CUDA arrays 176
10.8.1.19 tex1DLayered() 176
10.8.1.20 tex1DLayeredLod() 176
10.8.1.21 tex1DLayeredGrad() 176
10.8.1.22 tex2DLayered() 176
10.8.1.23 tex2DLayered() for Sparse CUDA Arrays 177
10.8.1.24 tex2DLayeredLod() 177
10.8.1.25 tex2DLayeredLod() for sparse CUDA arrays 177
10.8.1.26 tex2DLayeredGrad() 177
10.8.1.27 tex2DLayeredGrad() for sparse CUDA arrays 177
10.8.1.28 texCubemap() 178
10.8.1.29 texCubemapGrad() 178
10.8.1.30 texCubemapLod() 178
10.8.1.31 texCubemapLayered() 178
10.8.1.32 texCubemapLayeredGrad() 178
10.8.1.33 texCubemapLayeredLod() 179
10.9 Surface Functions 179
10.9.1 Surface Object API 179
10.9.1.1 surf1Dread() 179
10.9.1.2 surf1Dwrite 179
10.9.1.3 surf2Dread() 180
10.9.1.4 surf2Dwrite() 180
10.9.1.5 surf3Dread() 180
10.9.1.6 surf3Dwrite() 180
10.9.1.7 surf1DLayeredread() 181
10.9.1.8 surf1DLayeredwrite() 181
10.9.1.9 surf2DLayeredread() 181
10.9.1.10 surf2DLayeredwrite() 182
10.9.1.11 surfCubemapread() 182
10.9.1.12 surfCubemapwrite() 182
10.9.1.13 surfCubemapLayeredread() 182
10.9.1.14 surfCubemapLayeredwrite() 183
Read-Only Data Cache Load Function 183
Load Functions Using Cache Hints 183
Store Functions Using Cache Hints 184
Time Function 184
Atomic Functions 184
Arithmetic Functions 187
atomicAdd() 187
atomicSub() 188
atomicExch() 188
atomicMin() 188
atomicMax() 189
atomicInc() 189
atomicDec() 189
atomicCAS() 189
\_nv\_atomic\_exchange() 190

10.14.1.10 \_\_nv\_atomic\_exchange\_n() . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
10.14.1.11 \_\_nv\_atomic\_compare\_exchange() . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
10.14.1.12 \_\_nv\_atomic\_compare\_exchange\_n() . . . . . . . . . . . . . . . . . . . . 191
10.14.1.13 \_\_nv\_atomic\_fetch\_add() and \_\_nv\_atomic\_add() . . . . . . . . . . . . 192
10.14.1.14 \_\_nv\_atomic\_fetch\_sub() and \_\_nv\_atomic\_sub() . 192
10.14.1.15 \_\_nv\_atomic\_fetch\_min() and \_\_nv\_atomic\_min() 193
10.14.1.16 \_\_nv\_atomic\_fetch\_max() and \_\_nv\_atomic\_max() 193
10.14.2 Bitwise Functions .... 193
10.14.2.1 atomicAnd() .. 193
10.14.2.2 atomicOr() .. 194
10.14.2.3 atomicXor() .. 194
10.14.2.4 \_\_nv\_atomic\_fetch\_or() and \_\_nv\_atomic\_or() 194
10.14.2.5 \_\_nv\_atomic\_fetch\_xor() and \_\_nv\_atomic\_xor() 195
10.14.2.6 \_\_nv\_atomic\_fetch\_and() and \_\_nv\_atomic\_and() 195
10.14.3 Other atomic functions .... 195
10.14.3.1 \_\_nv\_atomic\_load() .. 195
10.14.3.2 \_\_nv\_atomic\_load\_n() .. 196
10.14.3.3 \_\_nv\_atomic\_store() .. 196
10.14.3.4 \_\_nv\_atomic\_store\_n() .. 197
10.14.3.5 \_\_nv\_atomic\_thread\_fence() .. 197
10.15 Address Space Predicate Functions .... 197
10.15.1 \_\_isGlobal() .. 197
10.15.2 \_\_isShared() .. 198
10.15.3 \_\_isConstant() .. 198
10.15.4 \_\_isGridConstant() .. 198
10.15.5 \_\_isLocal() .. 198
10.16 Address Space Conversion Functions .... 198
10.16.1 \_\_cvta\_generic\_to\_global() .. 199
10.16.2 \_\_cvta\_generic\_to\_shared() .. 199
10.16.3 \_\_cvta\_generic\_to\_constant() .. 200
10.16.4 \_\_cvta\_generic\_to\_local() .. 200
10.16.5 \_\_cvta\_global\_to\_generic() .. 200
10.16.6 \_\_cvta\_shared\_to\_generic() .. 200
10.16.7 \_\_cvta\_constant\_to\_generic() .. 200
10.16.8 \_\_cvta\_local\_to\_generic() .. 201
10.17 Alloca Function .... 201
10.17.1 Synopsis .. 201
10.17.2 Description .. 201
10.17.3 Example .. 201
10.18 Compiler Optimization Hint Functions .... 202
10.18.1 \_\_builtin\_assume\_aligned() .. 202
10.18.2 \_\_builtin\_assume() .. 202
10.18.3 \_\_assume() .. 203
10.18.4 \_\_builtin\_expect() .. 203
10.18.5 \_\_builtin\_unreachable() .. 203
10.18.6 Restrictions .. 204
10.19 Warp Vote Functions .... 204
10.20 Warp Match Functions .... 205
10.20.1 Synopsis .. 205
10.20.2 Description .. 205
10.21 Warp Reduce Functions .... 206
10.21.1 Synopsis .. 206
10.21.2 Description .. 206
10.22 Warp Shuffle Functions .... 207

10.22.1 Synopsis . 207
10.22.2 Description . 207
10.22.3 Examples . 208
10.22.3.1 Broadcast of a single value across a warp . 208
10.22.3.2 Inclusive plus-scan across sub-partitions of 8 threads . 209
10.22.3.3 Reduction across a warp . 209
10.23 Nanosleep Function . 210
10.23.1 Synopsis . 210
10.23.2 Description . 210
10.23.3 Example . 210
10.24 Warp Matrix Functions . 210
10.24.1 Description . 211
10.24.2 Alternate Floating Point . 213
10.24.3 Double Precision . 213
10.24.4 Sub-byte Operations . 213
10.24.5 Restrictions . 215
10.24.6 Element Types and Matrix Sizes . 215
10.24.7 Example . 217
10.25 DPX . 217
10.25.1 Examples . 218
10.26 Asynchronous Barrier . 219
10.26.1 Simple Synchronization Pattern . 219
10.26.2 Temporal Splitting and Five Stages of Synchronization . 219
10.26.3 Bootstrap Initialization, Expected Arrival Count, and Participation . 220
10.26.4 A Barrier's Phase: Arrival, Countdown, Completion, and Reset . 221
10.26.5 Spatial Partitioning (also known as Warp Specialization) . 222
10.26.6 Early Exit (Dropping out of Participation) . 224
10.26.7 Completion Function . 224
10.26.8 Memory Barrier Primitives Interface . 226
10.26.8.1 Data Types . 226
10.26.8.2 Memory Barrier Primitives API . 226
10.27 Asynchronous Data Copies . 227
10.27.1 memcpy\_async API . 227
10.27.2 Copy and Compute Pattern - Staging Data Through Shared Memory . 227
10.27.3 Without memcpy\_async . 228
10.27.4 With memcpy\_async . 229
10.27.5 Asynchronous Data Copies using cuda::barrier . 230
10.27.6 Performance Guidance for memcpy\_async . 231
10.27.6.1 Alignment . 231
10.27.6.2 Trivially copyable . 231
10.27.6.3 Warp Entanglement - Commit . 231
10.27.6.4 Warp Entanglement - Wait . 232
10.27.6.5 Warp Entanglement - Arrive-On . 232
10.27.6.6 Keep Commit and Arrive-On Operations Converged . 233
10.28 Asynchronous Data Copies using cuda::pipeline . 233
10.28.1 Single-Stage Asynchronous Data Copies using cuda::pipeline . 233
10.28.2 Multi-Stage Asynchronous Data Copies using cuda::pipeline . 235
10.28.3 Pipeline Interface . 240
10.28.4 Pipeline Primitives Interface . 240
10.28.4.1 memcpy\_async Primitive . 241
10.28.4.2 Commit Primitive . 241
10.28.4.3 Wait Primitive . 241
10.28.4.4 Arrive On Barrier Primitive . 242
10.29 Asynchronous Data Copies using the Tensor Memory Accelerator (TMA) . 242

10.29.1 Using TMA to transfer one-dimensional arrays ..... 243
10.29.2 Using TMA to transfer multi-dimensional arrays ..... 246
10.29.2.1 Multi-dimensional TMA PTX wrappers ..... 250
10.29.3 TMA Swizzle ..... 252
10.29.3.1 Example 'Matrix Transpose' ..... 252
10.29.3.2 The Swizzle Modes ..... 256
10.30 Encoding a Tensor Map on Device ..... 258
10.30.1 Device-side Encoding and Modification of a Tensor Map ..... 259
10.30.2 Usage of a Modified Tensor Map ..... 261
10.30.3 Creating a Template Tensor Map Value Using the Driver API ..... 262
10.31 Profiler Counter Function ..... 263
10.32 Assertion ..... 263
10.33 Trap function ..... 264
10.34 Breakpoint Function ..... 265
10.35 Formatted Output ..... 265
10.35.1 Format Specifiers ..... 265
10.35.2 Limitations ..... 266
10.35.3 Associated Host-Side API ..... 267
10.35.4 Examples ..... 267
10.36 Dynamic Global Memory Allocation and Operations ..... 268
10.36.1 Heap Memory Allocation ..... 269
10.36.2 Interoperability with Host Memory API ..... 269
10.36.3 Examples ..... 269
10.36.3.1 Per Thread Allocation ..... 269
10.36.3.2 Per Thread Block Allocation ..... 270
10.36.3.3 Allocation Persisting Between Kernel Launches ..... 271
10.37 Execution Configuration ..... 272
10.38 Launch Bounds ..... 274
10.39 Maximum Number of Registers per Thread ..... 276
10.40 #pragma unroll ..... 276
10.41 SIMD Video Instructions ..... 277
10.42 Diagnostic Pragmas ..... 278
10.43 Custom ABI Pragmas ..... 279
10.44 CUDA C++ Memory Model ..... 280
10.45 CUDA C++ Execution Model ..... 280
