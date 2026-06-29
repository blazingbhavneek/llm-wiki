# CUDA OpenGL Interoperability

Traditional OpenGL-CUDA interoperability works by CUDA directly consuming handles created in OpenGL [CUDA_C_Programming_Guide:L4957-L4960]. However, since OpenGL can also consume memory and synchronization objects created in Vulkan, there exists an alternative approach to performing OpenGL-CUDA interoperability [CUDA_C_Programming_Guide:L4960-L4963].

In this alternative approach, memory and synchronization objects exported by Vulkan can be imported into both OpenGL and CUDA, allowing them to coordinate memory accesses between the two APIs [CUDA_C_Programming_Guide:L4963-L4967]. For details on importing memory and synchronization objects exported by Vulkan, refer to the following OpenGL extensions:

* `GL_EXT_memory_object`
* `GL_EXT_memory_object_fd`
* `GL_EXT_memory_object_win32`
* `GL_EXT_semaphore`
* `GL_EXT_semaphore_fd`
* `GL_EXT_semaphore_win32`

[CUDA_C_Programming_Guide:L4967-L4970]
