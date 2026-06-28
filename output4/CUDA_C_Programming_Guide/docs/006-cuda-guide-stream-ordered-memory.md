15 Stream Ordered Memory Allocator 375
15.1 Introduction 375
15.2 Query for Support 376
15.3 API Fundamentals (cudaMallocAsync and cudaFreeAsync) 376
15.4 Memory Pools and the cudaMemPool\_t 378
15.5 Default/Implicit Pools 378
15.6 Explicit Pools 378
15.7 Physical Page Caching Behavior 379
15.8 Resource Usage Statistics 380
15.9 Memory Reuse Policies 381

15.9.1 cudaMemPoolReuseFollowEventDependencies 381
15.9.2 cudaMemPoolReuseAllowOpportunistic 381
15.9.3 cudaMemPoolReuseAllowInternalDependencies 382
15.9.4 Disabling Reuse Policies 382
15.10 Device Accessibility for Multi-GPU Support 382
15.11 IPC Memory Pools 383
15.11.1 Creating and Sharing IPC Memory Pools 383
15.11.2 Set Access in the Importing Process 384
15.11.3 Creating and Sharing Allocations from an Exported Pool 384
15.11.4 IPC Export Pool Limitations 386
15.11.5 IPC Import Pool Limitations 386
15.12 Synchronization API Actions 386
15.13 Addendums 387
15.13.1 cudaMemcpyAsync Current Context/Device Sensitivity 387
15.13.2 cuPointerGetAttribute Query 387
15.13.3 cuGraphAddMemsocketNode 387
15.13.4 Pointer Attributes 387
15.13.5 CPU Virtual Memory 387
