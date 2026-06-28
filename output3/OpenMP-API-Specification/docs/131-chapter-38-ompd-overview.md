
## OMPD

## 38 OMPD Overview

This chapter provides an overview of OMPD, which is an interface for third-party tools, such as a debugger. Third-party tools exist in separate processes from the OpenMP program. To provide OMPD support, an OpenMP implementation must provide an OMPD library that the third-party tool can load. An OpenMP implementation does not need to maintain any extra information to support OMPD inquiries from third-party tools unless it is explicitly instructed to do so.

OMPD allows third-party tools to inspect the OpenMP state of a live OpenMP program or core file in an implementation-agnostic manner. Thus, a third-party tool that uses OMPD should work with any compliant implementation. An OpenMP implementation provides a library for OMPD that a third-party tool can dynamically load. The third-party tool can use the interface exported by the OMPD library to inspect the OpenMP state of an OpenMP program. In order to satisfy requests from the third-party tool, the OMPD library may need to read data from the OpenMP program, or to find the addresses of symbols in it. The OMPD library provides this functionality through a callback interface that the third-party tool must instantiate for the OMPD library.

To use OMPD, the third-party tool loads the OMPD library, which exports the OMPD API and which the third-party tool uses to determine OpenMP information about the OpenMP program. The OMPD library must look up symbols and read data out of the program. It does not perform these operations directly but instead directs the third-party tool to perform them by using the callback interface that the third-party tool exports.

The OMPD design insulates third-party tools from the internal structure of the OpenMP runtime, while the OMPD library is insulated from the details of how to access the OpenMP program. This decoupled design allows for flexibility in how the OpenMP program and third-party tool are deployed, so that, for example, the third-party tool and the OpenMP program are not required to execute on the same machine.

Generally, the third-party tool does not interact directly with the OpenMP runtime but instead interacts with the runtime through the OMPD library. However, a few cases require the third-party tool to access the OpenMP runtime directly. These cases fall into two broad categories. The first is during initialization where the third-party tool must look up symbols and read variables in the OpenMP runtime in order to identify the OMPD library that it should use, which is discussed in Section 38.3.2 and Section 38.3.3. The second category relates to arranging for the third-party tool to be notified when certain events occur during the execution of the OpenMP program. For this purpose, the OpenMP implementation must define certain symbols in the runtime code, as is discussed in Chapter 42. Each of these symbols corresponds to an event type. The OpenMP runtime must ensure that control passes through the appropriate named location when events occur. If the third-party tool requires notification of an event, it can plant a breakpoint at the matching

location. The location can, but may not, be a function. It can, for example, simply be a label. However, the names of the locations must have external C linkage.

## 38.1 OMPD Interfaces Definitions

C / C++

A compliant implementation must supply a set of definitions for the OMPD third-party tool callback signatures, third-party tool interface routines and the special data types of their parameters and return values. These definitions, which are listed throughout the OMPD chapters, and their associated declarations shall be provided in a header file named omp-tools.h. In addition, the set of definitions may specify other implementation defined values. The ompd\_dll\_locations variable and all OMPD third-party tool interface routines are external symbols with C linkage.

C / C++

## 38.2 Thread and Signal Safety

The OMPD library does not need to be reentrant. The third-party tool must ensure that only one native thread enters the OMPD library at a time. The OMPD library must not install signal handlers or otherwise interfere with the signal configuration of the third-party tool.

## 38.3 Activating a Third-Party Tool

The third-party tool and the OpenMP program exist as separate processes. Thus, OMPD requires coordination between the OpenMP runtime and the third-party tool.

## 38.3.1 Enabling Runtime Support for OMPD

In order to support third-party tools, the OpenMP runtime may need to collect and to store information that it may not otherwise maintain. The OpenMP runtime collects whatever information is necessary to support OMPD if the debug-var ICV is set to enabled.

Cross References

• debug-var ICV, see Table 3.1

## 38.3.2 ompd\_dll\_locations

Format

extern const char <sub>\*\*</sub>ompd\_dll\_locations;

C

## Semantics

An OpenMP runtime may have more than one OMPD library. The third-party tool must be able to locate the right library to use for the program that it is examining. The ompd\_dll\_locations global variable points to the locations of OMPD libraries that are compatible with the OpenMP implementation. The OpenMP runtime system must provide this public variable, which is an argv-style vector of pathname string pointers that provide the names of the compatible OMPD libraries. This variable must have C linkage. The third-party tool uses the name of the variable verbatim and, in particular, does not apply any name mangling before performing the look up.

The architecture on which the third-party tool and, thus, the OMPD library execute does not have to match the architecture on which the OpenMP program that is being examined executes. The third-party tool must interpret the contents of ompd\_dll\_locations to find a suitable OMPD library that matches its own architectural characteristics. On platforms that support diferent architectures (for example, 32-bit vs 64-bit), OpenMP implementations should provide an OMPD library for each supported architecture that can handle OpenMP programs that run on any supported architecture. Thus, for example, a 32-bit debugger that uses OMPD should be able to debug a 64-bit OpenMP program by loading a 32-bit OMPD implementation that can manage a 64-bit OpenMP runtime.

The ompd\_dll\_locations variable points to a NULL-terminated vector of zero or more null-terminated pathname strings that do not have any filename conventions. This vector must be fully initialized before ompd\_dll\_locations is set to a non-null value. Thus, if a third-party tool stops execution of the OpenMP program at any point at which ompd\_dll\_locations is a non-null value, the vector of strings to which it points shall be valid and complete.

## 38.3.3 ompd\_dll\_locations\_valid Breakpoint

## Format

void ompd\_dll\_locations\_valid(void);

## Semantics

Since ompd\_dll\_locations may not be a static variable, it may require runtime initialization. The OpenMP runtime notifies third-party tools that ompd\_dll\_locations is valid by having execution pass through a location that the symbol ompd\_dll\_locations\_valid identifies. If ompd\_dll\_locations is NULL, a third-party tool can place a breakpoint at ompd\_dll\_locations\_valid to be notified that ompd\_dll\_locations is initialized. In practice, the symbol ompd\_dll\_locations\_valid may not be a function; instead, it may be a labeled machine instruction through which execution passes once the vector is valid.

# 39 OMPD Data Types
