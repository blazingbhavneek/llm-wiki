# CUDA Dynamic Parallelism (CDP1) Implicit (NULL) Stream

In the context of CUDA Dynamic Parallelism version 1 (CDP1), the behavior of the implicit NULL stream differs from its usage on the host. Specifically, the device runtime's NULL stream does not insert implicit dependencies on pending work in other streams [CUDA_C_Programming_Guide:L14547-L14549].

Additionally, this implicit NULL stream is shared between all threads within a block [CUDA_C_Programming_Guide:L14547-L14549].

For the corresponding behavior in CDP2, see the section on The Implicit (NULL) Stream in the CDP2 version of the documentation [CUDA_C_Programming_Guide:L14547-L14549].
