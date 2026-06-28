22 CUDA Environment Variables 521

23 Error Log Management 531
23.1 Background 531
23.2 Activation 531
23.3 Output 531
23.4 API Description 532
23.5 Limitations and Known Issues 533

24 Unified Memory Programming 535
24.1 Unified Memory Introduction 535
24.1.1 System Requirements for Unified Memory 536
24.1.2 Programming Model 538
24.1.2.1 Allocation APIs for System-Allocated Memory 540
24.1.2.2 Allocation API for CUDA Managed Memory: cudaMallocManaged() 541
24.1.2.3 Global-Scope Managed Variables Using \_\_managed\_\_ 542
24.1.2.4 Difference between Unified Memory and Mapped Memory 543
24.1.2.5 Pointer Attributes 543
24.1.2.6 Runtime detection of Unified Memory Support Level 544
24.1.2.7 GPU Memory Oversubscription 545
24.1.2.8 Performance Hints 545
24.2 Unified memory on devices with full CUDA Unified Memory support 550
24.2.1 System-Allocated Memory: in-depth examples 550
24.2.1.1 File-backed Unified Memory 552
24.2.1.2 Inter-Process Communication (IPC) with Unified Memory 553
24.2.2 Performance Tuning 553
24.2.2.1 Memory Paging and Page Sizes 554
24.2.2.2 Direct Unified Memory Access from host 556

24.2.2.3 Host Native Atomics 558  
24.2.2.4 Atomic accesses & synchronization primitives 558  
24.2.2.5 Memcpy()/Memset() Behavior With Unified Memory 559  
24.3 Unified memory on devices without full CUDA Unified Memory support 559  
24.3.1 Unified memory on devices with only CUDA Managed Memory support 559  
24.3.2 Unified memory on Windows or devices with compute capability 5.x 560  
24.3.2.1 Data Migration and Coherency 560  
24.3.2.2 GPU Memory Oversubscription 560  
24.3.2.3 Multi-GPU 560  
24.3.2.4 Coherency and Concurrency 561  
25 Lazy Loading 569  
25.1 What is Lazy Loading? 569  
25.2 Lazy Loading version support 570  
25.2.1 Driver 570  
25.2.2 Toolkit 570  
25.2.3 Compiler 570  
25.3 Triggering loading of kernels in lazy mode 570  
25.3.1 CUDA Driver API 571  
25.3.2 CUDA Runtime API 571  
25.4 Querying whether Lazy Loading is Turned On 571  
25.5 Possible Issues when Adopting Lazy Loading 572  
25.5.1 Concurrent Execution 572  
25.5.2 Allocators 572  
25.5.3 Autotuning 573  
26 Extended GPU Memory 575  
26.1 Preliminaries 575  
26.1.1 EGM Platforms: System topology 576  
26.1.2 Socket Identifiers: What are they? How to access them? 576  
26.1.3 Allocators and EGM support 576  
26.1.4 Memory management extensions to current APIs 576  
26.2 Using the EGM Interface 577  
26.2.1 Single-Node, Single-GPU 577  
26.2.2 Single-Node, Multi-GPU 577  
26.2.2.1 Using VMM APIs 578  
26.2.2.2 Using CUDA Memory Pool 578  
26.2.3 Multi-Node, Single-GPU 579  
27 Notices 581  
27.1 Notice 581  
27.2 OpenCL 582  
27.3 Trademarks 582
