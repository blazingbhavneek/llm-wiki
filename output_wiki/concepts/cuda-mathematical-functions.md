# CUDA Mathematical Functions

CUDA provides a comprehensive set of mathematical functions that can be executed on the GPU (device code). These include functions from the C/C++ standard library as well as specific intrinsic functions that are only supported in device code [CUDA_C_Programming_Guide:L16364-L16373].

## Accuracy and Precision

For applicable functions, CUDA provides accuracy information quantified using Units in the Last Place (ULP). For a formal definition of ULP, refer to Jean-Michel Muller’s paper "On the definition of ulp(x)" (RR-5504, LIP RR-2005-09, INRIA, LIP, 2005) [CUDA_C_Programming_Guide:L16364-L16373].

## Error Handling and Exceptions

Mathematical functions supported in device code have specific restrictions regarding error reporting:

*   **No `errno`**: These functions do not set the global `errno` variable [CUDA_C_Programming_Guide:L16364-L16373].
*   **No Floating-Point Exceptions**: They do not report floating-point exceptions to indicate errors [CUDA_C_Programming_Guide:L16364-L16373].

Consequently, if error diagnostic mechanisms are required, the user must implement additional screening for inputs and outputs of the functions [CUDA_C_Programming_Guide:L16364-L16373].

## Usage Constraints

*   **Pointer Validity**: The user is responsible for the validity of pointer arguments passed to these functions [CUDA_C_Programming_Guide:L16364-L16373].
*   **Uninitialized Parameters**: Users must not pass uninitialized parameters to mathematical functions, as this may result in undefined behavior [CUDA_C_Programming_Guide:L16364-L16373].
*   **Inlining**: Functions are inlined in the user program and are thus subject to compiler optimizations [CUDA_C_Programming_Guide:L16364-L16373].

## Legacy Notice

This content is based on the legacy "Chapter 17. Mathematical Functions" from the CUDA C Programming Guide. As of CUDA 13.0, this document has been replaced by the new CUDA Programming Guide and is no longer being updated [CUDA_C_Programming_Guide:L16364-L16373]. Users should refer to the current CUDA Programming Guide for up-to-date information [CUDA_C_Programming_Guide:L16364-L16373].
