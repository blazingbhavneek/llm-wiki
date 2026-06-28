## 5.6. Compute Capability

The compute capability of a device is represented by a version number, also sometimes called its “SM version”. This version number identifies the features supported by the GPU hardware and is used by applications at runtime to determine which hardware features and/or instructions are available on the present GPU.

The compute capability comprises a major revision number X and a minor revision number Y and is denoted by X.Y.

The major revision number indicates the core GPU architecture of a device. Devices with the same major revision number share the same fundamental architecture. The table below lists the major revision numbers corresponding to each NVIDIA GPU architecture.

Table 2: GPU Architecture and Major Revision Numbers

<table><tr><td>Major Revision Number</td><td>NVIDIA GPU Architecture</td></tr><tr><td>9</td><td>NVIDIA Hopper GPU Architecture</td></tr><tr><td>8</td><td>NVIDIA Ampere GPU Architecture</td></tr><tr><td>7</td><td>NVIDIA Volta GPU Architecture</td></tr><tr><td>6</td><td>NVIDIA Pascal GPU Architecture</td></tr><tr><td>5</td><td>NVIDIA Maxwell GPU Architecture</td></tr><tr><td>3</td><td>NVIDIA Kepler GPU Architecture</td></tr></table>

The minor revision number corresponds to an incremental improvement to the core architecture, pos-

sibly including new features.

Table 3: Incremental Updates in GPU Architectures

<table><tr><td>Compute Capability</td><td>NVIDIA GPU Architecture</td><td>Based On</td></tr><tr><td>7.5</td><td>NVIDIA Turing GPU Architecture</td><td>NVIDIA Volta GPU Architecture</td></tr></table>

CUDA-Enabled GPUs lists of all CUDA-enabled devices along with their compute capability. Compute Capabilities gives the technical specifications of each compute capability.

Note: The compute capability version of a particular GPU should not be confused with the CUDA version (for example, CUDA 7.5, CUDA 8, CUDA 9), which is the version of the CUDA software platform. The CUDA platform is used by application developers to create applications that run on many generations of GPU architectures, including future GPU architectures yet to be invented. While new versions of the CUDA platform often add native support for a new GPU architecture by supporting the compute capability version of that architecture, new versions of the CUDA platform typically also include software features that are independent of hardware generation.

The Tesla and Fermi architectures are no longer supported starting with CUDA 7.0 and CUDA 9.0, respectively.

# Chapter 6. Programming Interface
