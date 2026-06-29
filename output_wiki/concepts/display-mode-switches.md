# Display Mode Switches and CUDA

GPUs that have a display output dedicate a portion of DRAM memory to the **primary surface**, which is used to refresh the display device viewed by the user [CUDA_C_Programming_Guide:L6111-L6115].

## Mechanism of Memory Impact

When a user initiates a mode switch by changing the display resolution or bit depth (e.g., via the NVIDIA Control Panel or Windows Display control panel), the amount of memory required for the primary surface changes [CUDA_C_Programming_Guide:L6111-L6115]. For instance, increasing the resolution from 1280x1024x32-bit to 1600x1200x32-bit increases the dedicated memory from 5.24 MB to 7.68 MB [CUDA_C_Programming_Guide:L6111-L6115]. Additionally, full-screen graphics applications with anti-aliasing enabled may require significantly more display memory for the primary surface [CUDA_C_Programming_Guide:L6111-L6115].

On Windows, mode switches can also be triggered by events such as:
* Launching a full-screen DirectX application.
* Pressing Alt+Tab to switch away from a full-screen DirectX application.
* Pressing Ctrl+Alt+Del to lock the computer [CUDA_C_Programming_Guide:L6111-L6115].

## Impact on CUDA Applications

If a mode switch increases the memory demand for the primary surface, the system may need to cannibalize memory allocations that were previously dedicated to CUDA applications [CUDA_C_Programming_Guide:L6111-L6115]. Consequently, any subsequent call to the CUDA runtime will fail and return an **invalid context error** [CUDA_C_Programming_Guide:L6111-L6115].

## Aliases

* Primary Surface
