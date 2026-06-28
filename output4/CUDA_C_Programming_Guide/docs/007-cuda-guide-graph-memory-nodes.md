16 Graph Memory Nodes 389
16.1 Introduction 389
16.2 Support and Compatibility 389
16.3 API Fundamentals 390
16.3.1 Graph Node APIs 391
16.3.2 Stream Capture 392
16.3.3 Accessing and Freeing Graph Memory Outside of the Allocating Graph 393
16.3.4 cudaGraphInstantiateFlagAutoFreeOnLaunch 395
16.4 Optimized Memory Reuse 396
16.4.1 Address Reuse within a Graph 397
16.4.2 Physical Memory Management and Sharing 397
16.5 Performance Considerations 400
16.5.1 First Launch / cudaGraphUpload 400
16.6 Physical Memory Footprint 400
16.7 Peer Access 401
16.7.1 Peer Access with Graph Node APIs 401
16.7.2 Peer Access with Stream Capture 402
16.8 Memory Nodes in Child Graphs 402
