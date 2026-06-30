# CUDA Mode Switches

Explains how display mode switches (resolution/bit depth changes, fullscreen app launches, task switches) alter the memory required for the GPU's primary surface. Notes that if mode switches increase primary surface memory, CUDA may cannibalize allocations, causing subsequent CUDA runtime calls to fail with an invalid context error.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6111-L6117

Citation: [CUDA_C_Programming_Guide:L6111-L6117]

````text
## 6.5. Mode Switches

GPUs that have a display output dedicate some DRAM memory to the so-called primary surface, which is used to refresh the display device whose output is viewed by the user. When users initiate a mode switch of the display by changing the resolution or bit depth of the display (using NVIDIA control panel or the Display control panel on Windows), the amount of memory needed for the primary surface changes. For example, if the user changes the display resolution from 1280x1024x32-bit to 1600x1200x32-bit, the system must dedicate 7.68 MB to the primary surface rather than 5.24 MB. (Full-screen graphics applications running with anti-aliasing enabled may require much more display memory for the primary surface.) On Windows, other events that may initiate display mode switches include launching a full-screen DirectX application, hitting Alt+Tab to task switch away from a fullscreen DirectX application, or hitting Ctrl+Alt+Del to lock the computer.

If a mode switch increases the amount of memory needed for the primary surface, the system may have to cannibalize memory allocations dedicated to CUDA applications. Therefore, a mode switch results in any call to the CUDA runtime to fail and return an invalid context error.

## 6.6. Tesla Compute Cluster Mode for Windows
````
