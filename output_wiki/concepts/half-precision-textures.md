# 16-Bit Floating-Point Textures

The 16-bit floating-point or half format supported by CUDA arrays is identical to the IEEE 754-2008 binary2 format [CUDA_C_Programming_Guide:L3811-L3813].

## Data Types and Conversion

CUDA C++ does not provide a native matching data type for the 16-bit half format. Instead, it provides intrinsic functions to convert between the 32-bit floating-point format and the 16-bit half format, represented as an `unsigned short` [CUDA_C_Programming_Guide:L3813-L3816].

The available device code intrinsics are:
*   `__float2half_rn(float)`: Converts a 32-bit float to a 16-bit half.
*   `__half2float(unsigned short)`: Converts a 16-bit half to a 32-bit float [CUDA_C_Programming_Guide:L3813-L3816].

These conversion functions are only supported in device code. For host code, equivalent functions can be found in external libraries such as the OpenEXR library [CUDA_C_Programming_Guide:L3816-L3818].

## Texture Fetching Behavior

When 16-bit floating-point components are fetched from textures, they are promoted to 32-bit floats before any filtering operations are performed [CUDA_C_Programming_Guide:L3818-L3819].

## Channel Description

To create a channel description for the 16-bit floating-point format, developers must call one of the `cudaCreateChannelDescHalf*()` functions [CUDA_C_Programming_Guide:L3819-L3820].
