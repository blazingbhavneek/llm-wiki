# Tensor Memory Accelerator (TMA)

The Tensor Memory Accelerator (TMA) is a hardware feature introduced in Compute Capability 9.0 to provide an efficient data transfer mechanism from global memory to shared memory for multi-dimensional arrays [CUDA_C_Programming_Guide:L10218-L10223]. It offloads address calculations and repetitive loading/storing operations, which are often error-prone and repetitive when moving large amounts of data [CUDA_C_Programming_Guide:L10218-L10223].

## Overview

Many applications require the movement of large amounts of data from and to global memory. Often, the data is laid out in global memory as a multi-dimensional array with non-sequential data access patterns. To reduce global memory usage, sub-tiles of such arrays are copied to shared memory before use in computations [CUDA_C_Programming_Guide:L10218-L10223]. The loading and storing involves address-calculations that can be error-prone and repetitive. To offload these computations, Compute Capability 9.0 introduces the Tensor Memory Accelerator (TMA) [CUDA_C_Programming_Guide:L10218-L10223]. The primary goal of TMA is to provide an efficient data transfer mechanism from global memory to shared memory for multi-dimensional arrays [CUDA_C_Programming_Guide:L10218-L10223].

## Naming and Terminology

"Tensor memory accelerator" (TMA) is a broad term used to refer to the features described in the CUDA C Programming Guide [CUDA_C_Programming_Guide:L10218-L10223]. For the purpose of forward-compatibility and to reduce discrepancies with the PTX ISA, the text refers to TMA operations as either **bulk-asynchronous copies** or **bulk tensor asynchronous copies**, depending on the specific type of copy used [CUDA_C_Programming_Guide:L10218-L10223]. The term "bulk" is used to contrast these operations with the asynchronous memory operations described in previous sections [CUDA_C_Programming_Guide:L10218-L10223].

## Key Capabilities

*   **Offloading Address Calculations:** TMA handles the complex address calculations required for non-sequential access patterns in multi-dimensional arrays [CUDA_C_Programming_Guide:L10218-L10223].
*   **Efficient Data Transfer:** It provides an efficient mechanism for transferring data from global memory to shared memory [CUDA_C_Programming_Guide:L10218-L10223].
*   **Support for Multi-dimensional Arrays:** TMA is specifically designed to handle sub-tiles of multi-dimensional arrays efficiently [CUDA_C_Programming_Guide:L10218-L10223].
*   **Bulk Operations:** TMA supports bulk-asynchronous copies and bulk tensor asynchronous copies, distinguishing them from standard asynchronous memory operations [CUDA_C_Programming_Guide:L10218-L10223].

## Prerequisites

*   **Compute Capability 9.0:** TMA is a hardware feature introduced in Compute Capability 9.0 [CUDA_C_Programming_Guide:L10218-L10223].

## Caveats

*   **PTX ISA Alignment:** The terminology used in documentation (bulk-asynchronous copies vs. bulk tensor asynchronous copies) is chosen to align with the PTX ISA and ensure forward-compatibility [CUDA_C_Programming_Guide:L10218-L10223].
*   **Non-Sequential Access:** TMA is particularly beneficial for data layouts with non-sequential access patterns, where traditional address calculations are error-prone [CUDA_C_Programming_Guide:L10218-L10223].

## See Also

*   CUDA C Programming Guide: Asynchronous Data Copies using the Tensor Memory Accelerator (TMA)
*   PTX ISA
*   Compute Capability 9.0
