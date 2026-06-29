# Data Migration and Coherency (Pre-6.x)

GPU architectures with a compute capability lower than 6.0 do not support fine-grained movement of managed data to the GPU on-demand [CUDA_C_Programming_Guide:L21829-L21832]. Consequently, whenever a GPU kernel is launched, all managed memory generally must be transferred to GPU memory to avoid faulting on memory access [CUDA_C_Programming_Guide:L21829-L21832].

This behavior contrasts with compute capability 6.x and later, which introduced a new GPU page faulting mechanism [CUDA_C_Programming_Guide:L21829-L21832]. This mechanism provides more seamless Unified Memory functionality by allowing the CUDA system software to avoid synchronizing all managed memory allocations to the GPU before each kernel launch [CUDA_C_Programming_Guide:L21829-L21832]. Instead, if a kernel accesses a page not resident in GPU memory, it triggers a fault, allowing the page to be automatically migrated on-demand or mapped into the GPU address space for access over PCIe or NVLink interconnects [CUDA_C_Programming_Guide:L21829-L21832].

Unified Memory is system-wide, meaning GPUs and CPUs can fault on and migrate memory pages from CPU memory or from the memory of other GPUs in the system [CUDA_C_Programming_Guide:L21829-L21832].
