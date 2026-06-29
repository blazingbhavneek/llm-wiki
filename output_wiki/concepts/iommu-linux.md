# IOMMU on Linux

On Linux only, CUDA and the display driver do not support IOMMU-enabled bare-metal PCIe peer-to-peer memory copy [CUDA_C_Programming_Guide:L3557-L3564]. As a consequence, users on Linux running on a native bare-metal system should disable the IOMMU [CUDA_C_Programming_Guide:L3557-L3564].

However, CUDA and the display driver do support IOMMU via VM pass-through [CUDA_C_Programming_Guide:L3557-L3564]. For virtual machines, the IOMMU should be enabled and the VFIO driver should be used as a PCIe pass-through [CUDA_C_Programming_Guide:L3557-L3564].

This limitation does not exist on Windows [CUDA_C_Programming_Guide:L3557-L3564].

See also: Allocating DMA Buffers on 64-bit Platforms.
