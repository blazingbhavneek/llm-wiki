# CUDA Implicit (NULL) Stream

The CUDA device runtime offers a single implicit, unnamed stream that is shared between all threads within a thread block [CUDA_C_Programming_Guide:L13868-L13871].

While the unnamed (NULL) stream in host programs typically has additional barrier synchronization semantics with other streams, the behavior differs in the device runtime context [CUDA_C_Programming_Guide:L13868-L13871]. Because all named streams must be created with the `cudaStreamNonBlocking` flag, work launched into the implicit NULL stream will not insert an implicit dependency on pending work in any other streams [CUDA_C_Programming_Guide:L13868-L13871]. This applies to other streams as well as NULL streams associated with other thread blocks [CUDA_C_Programming_Guide:L13868-L13871].
