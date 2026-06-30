# OpenMP-API-Specification Source Lines 29015-29449

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L29015-L29449

Citation: [OpenMP-API-Specification:L29015-L29449]

````text
## 37.8 pause\_trace Entry Point

<table><tr><td>Name: pause_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>begin_pause</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_pause\_trace\_t) (ompt\_device\_t <sub>\*</sub>device, int begin\_pause);

C / C++

## Semantics

The pause\_trace entry point, which has the pause\_trace OMPT type, enables a tool to pause or to resume tracing on a device. The begin\_pause argument indicates whether to pause or to resume tracing. To resume tracing, zero should be supplied for begin\_pause; to pause tracing, any other value should be supplied. An invocation of pause\_trace returns one if it succeeds and zero otherwise. Redundant pause or resume commands are idempotent and will return the same value as the prior command.

## Cross References

• OMPT device Type, see Section 33.11

## 37.9 flush\_trace Entry Point

<table><tr><td>Name: flush_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_flush\_trace\_t) (ompt\_device\_t <sub>\*</sub>device);

C / C++

## Semantics

The flush\_trace entry point, which has the flush\_trace OMPT type, enables a tool to cause the OpenMP implementation to issue a sequence of zero or more buffer\_complete callbacks to deliver all trace records that have been collected prior to the flush for the specified device. An invocation of flush\_trace returns one if the entry point succeeds and zero otherwise.

## Cross References

• OMPT device Type, see Section 33.11

## 37.10 stop\_trace Entry Point

Type Signature

<table><tr><td>Name: stop_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

<table><tr><td></td><td>C / C++</td></tr><tr><td colspan="2">typedef int (*ompt_stop_trace_t) (ompt_device_t *device);</td></tr><tr><td></td><td>C / C++</td></tr></table>

## Semantics

The stop\_trace entry point, which has the stop\_trace OMPT type, provides a superset of the functionality of the flush\_trace entry point. Specifically, the stop\_trace entry point stops tracing for the specified device in addition to flushing pending trace records. An invocation of stop\_trace returns one if the entry point succeeds and zero otherwise.

Cross References

• OMPT device Type, see Section 33.11

• flush\_trace Entry Point, see Section 37.9

## 37.11 advance\_buffer\_cursor Entry Point

<table><tr><td>Name: advance_buffer_cursorCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>size</td><td>size_t</td><td>default</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr><tr><td>next</td><td>buffer_cursor</td><td>OMPT, opaque, pointer</td></tr></table>

## Type Signature

typedef int (<sub>\*</sub>ompt\_advance\_buffer\_cursor\_t) ( ompt\_device\_t <sub>\*</sub>device, ompt\_buffer\_t <sub>\*</sub>bufer, size\_t size, ompt\_buffer\_cursor\_t current, ompt\_buffer\_cursor\_t <sub>\*</sub>next);

C / C++

## Semantics

The advance\_buffer\_cursor entry point, which has the advance\_buffer\_cursor OMPT type, enables a tool to advance the trace bufer pointer for the bufer that the bufer argument indicates to the next trace record. The size argument indicates the size of bufer in bytes. The current argument is an OpenMP object that indicates the current position, while the next argument returns an OpenMP object with the next value. An invocation of advance\_buffer\_cursor returns true if the advance is successful and the next position in the bufer is valid. Otherwise, it returns false.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT device Type, see Section 33.11

## 37.12 get\_record\_type Entry Point

<table><tr><td>Name: get_record_typeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT</td></tr></table>

## Type Signature

C / C++

typedef ompt\_record\_t (<sub>\*</sub>ompt\_get\_record\_type\_t) ( ompt\_buffer\_t <sub>\*</sub>bufer, ompt\_buffer\_cursor\_t current);

C / C++

## Semantics

Trace records for a device may be in one of two forms: native trace format, which may be device-specific, or standard trace format, in which each trace record corresponds to an OpenMP event and most fields in the trace record structure are the arguments that would be passed to the callback for the event. For the bufer specified by the bufer argument, the get\_record\_type entry point, which has the get\_record\_type OMPT type, enables a tool to inspect the type of a trace record at the position that the current argument specifies and to determine whether the trace record is an OMPT trace record, a native trace record, or is an invalid record, which is returned if the cursor is out of bounds.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT record Type, see Section 33.23

## 37.13 get\_record\_ompt Entry Point

<table><tr><td>Name: get_record_emptCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record_ompt</td><td>pointer</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr></table>

## Type Signature

C / C++

typedef ompt\_record\_ompt\_t <sub>\*</sub>(<sub>\*</sub>ompt\_get\_record\_ompt\_t) ( ompt\_buffer\_t <sub>\*</sub>bufer, ompt\_buffer\_cursor\_t current);

C / C++

## Semantics

The get\_record\_ompt entry point, which has the get\_record\_ompt OMPT type, enables a tool to obtain a pointer to an OMPT trace record from a trace bufer associated with a device. The pointer may point to storage in the bufer indicated by the bufer argument or it may point to a trace record in thread-local storage in which the information extracted from a trace record was

assembled. The information available for an event depends upon its type. The current argument is an OpenMP object that indicates the position from which to extract the trace record. The return value of the record\_ompt OMPT type includes a field of the any\_record\_ompt OMPT type, which is a union that can represent information for any OMPT trace record type. Another call to the entry point may overwrite the contents of the fields in a trace record returned by a prior invocation.

## Cross References

• OMPT any\_record\_ompt Type, see Section 33.2

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT device Type, see Section 33.11

• OMPT record\_ompt Type, see Section 33.26

## 37.14 get\_record\_native Entry Point

<table><tr><td colspan="2">Name: get_record_nativeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="3">Return Type and Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr><tr><td>host_op_id</td><td>id</td><td>OMPT, pointer</td></tr><tr><td colspan="3">Type SignatureC / C++typedef void *(*ompt_get_record_native_t) (empt_buffer_t *buffer, ompt_buffer_cursor_t current,empt_id_t *host_op_id);</td></tr></table>

C / C++

## Semantics

The get\_record\_native entry point, which has the get\_record\_native OMPT type, enables a tool to obtain a pointer to a native trace record from a trace bufer associated with a device. The pointer may point to storage in the bufer indicated by the bufer argument or it may point to a trace record in thread-local storage in which the information extracted from a trace record was assembled. The information available for a native event depends upon its type. The current argument is an OpenMP object that indicates the position from which to extract the trace record. If the entry point returns a non-null pointer result, it will also set the object to which the host\_op\_id argument points to a host-side identifier for the operation that is associated with the trace record on the target device and was created when the operation was initiated by the host device. Another cal to the entry point may overwrite the contents of the fields in a trace record returned by a prior invocation.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT id Type, see Section 33.18

## 37.15 get\_record\_abstract Entry Point

<table><tr><td>Name: get_record_abstractCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record_abstract</td><td>pointer</td></tr><tr><td>native_record</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

C / C++

(<sub>\*</sub>ompt\_get\_record\_abstract\_t) (void <sub>\*</sub>native\_record);

C / C++

## Semantics

An OpenMP implementation may execute on a device that logs trace records in a native trace format that a tool cannot interpret directly. The get\_record\_abstract entry point, which has the get\_record\_abstract OMPT type, enables a tool to translate a native trace record to which the native\_record argument points into a standard form.

## Cross References

• OMPT record\_abstract Type, see Section 33.24

Part V

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

This chapter defines OMPD types, which support interactions with the OMPD library and provide information about the device architecture.

## 39.1 OMPD addr Type

<table><tr><td>Name: addrProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompd\_addr\_t;

C / C++

## Semantics

The addr OMPD type represents an address in an OpenMP process as an unsigned integer.

## 39.2 OMPD address Type

<table><tr><td>Name: addressProperties: C/C++-only, OMPD</td><td>Base Type: structure</td></tr></table>

<table><tr><td colspan="3">Fields</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>segment</td><td>seg</td><td>C/C++-only, OMPD</td></tr><tr><td>address</td><td>addr</td><td>C/C++-only, OMPD</td></tr></table>

## Type Definition

C / C++

typedef struct ompd\_address\_t {

ompd\_seg\_t segment;

ompd\_addr\_t address;

} ompd\_address\_t;

C / C++

## Semantics

The address type is a structure that OMPD uses to specify addresses, which may or may not be segmented. For non-segmented architectures, ompd\_segment\_none is used in the segment field of the address OMPD type.

## Cross References

• OMPD addr Type, see Section 39.1

• OMPD seg Type, see Section 39.10

## 39.3 OMPD address\_space\_context Type

<table><tr><td>Name: address_space_contextProperties: C/C++-only, handle, OMPD</td><td>Base Type: aspace_cont</td></tr></table>

## Type Definition

C / C++

typedef struct \_ompd\_aspace\_cont ompd\_address\_space\_context\_t;

C / C++

## Semantics

A third-party tool uses the address\_space\_context OMPD type, which represents handles that are opaque to the OMPD library and that define an address space context uniquely, to identify the address space of the OpenMP process that it is monitoring.

## 39.4 OMPD callbacks Type

<table><tr><td>Name: callbacksProperties: C/C++-only, OMPD</td><td>Base Type: structure</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>alloc_memory</td><td>memory_alloc</td><td>C-only, OMPD</td></tr><tr><td>free_memory</td><td>memory_free</td><td>C-only, OMPD</td></tr><tr><td>print_string</td><td>print_string</td><td>C-only, OMPD</td></tr><tr><td>sizeof_type</td><td>sizeof</td><td>C-only, OMPD</td></tr><tr><td>symbol_addr_lookup</td><td>symbol_addr</td><td>C-only, OMPD</td></tr><tr><td>read_memory</td><td>memory_read</td><td>C-only, OMPD</td></tr><tr><td>write_memory</td><td>memory_write</td><td>C-only, OMPD</td></tr><tr><td>read_string</td><td>memory_read</td><td>C-only, OMPD</td></tr><tr><td>device_to_host</td><td>device_host</td><td>C-only, OMPD</td></tr><tr><td>host_to_device</td><td>device_host</td><td>C-only, OMPD</td></tr><tr><td>get_thread_context_for_thread_id</td><td>get_thread_context_for_thread_id</td><td>C-only, OMPD</td></tr></table>

## Type Definition

C / C++

typedef struct ompd\_callbacks\_t { ompd\_callback\_memory\_alloc\_fn\_t alloc\_memory; ompd\_callback\_memory\_free\_fn\_t free\_memory; ompd\_callback\_print\_string\_fn\_t print\_string; ompd\_callback\_sizeof\_fn\_t sizeof\_type; ompd\_callback\_symbol\_addr\_fn\_t symbol\_addr\_lookup; ompd\_callback\_memory\_read\_fn\_t read\_memory; ompd\_callback\_memory\_write\_fn\_t write\_memory; ompd\_callback\_memory\_read\_fn\_t read\_string; ompd\_callback\_device\_host\_fn\_t device\_to\_host; ompd\_callback\_device\_host\_fn\_t host\_to\_device; ompd\_callback\_get\_thread\_context\_for\_thread\_id\_fn\_t get\_thread\_context\_for\_thread\_id;

} ompd\_callbacks\_t;

C / C++

## Semantics

All OMPD library interactions with the OpenMP program must be through a set of callbacks that the third-party tool provides. These callbacks must also be used for allocating or releasing resources, such as memory, that the OMPD library needs. The set of callbacks that the OMPD library must use is collected in an instance of the callbacks OMPD type that is passed to the OMPD library as an argument to ompd\_initialize. Each field points to a procedure that the OMPD library must use to interact with the OpenMP program or for memory operations.

The alloc\_memory and free\_memory fields are pointers to alloc\_memory and free\_memory callbacks, which the OMPD library uses to allocate and to release dynamic memory. The print\_string field points to a print\_string callback that prints a string.

The architecture on which the OMPD library and third-party tool execute may be diferent from the architecture on which the OpenMP program that is being examined executes. The sizeof\_type field points to a sizeof\_type callback that allows the OMPD library to determine the sizes of the basic integer and pointer types that the OpenMP program uses. Because of the potential diferences in the targeted architectures, the conventions for representing data in the OMPD library and the OpenMP program may be diferent. The device\_to\_host field points to a device\_to\_host callback that translates data from the conventions that the OpenMP program uses to those that the third-party tool and OMPD library use. The reverse operation is performed by the host\_to\_device callback to which the host\_to\_device field points.

The symbol\_addr\_lookup field points to a symbol\_addr\_lookup callback, which the OMPD library can use to find the address of a global or thread local storage symbol. The read\_memory, read\_string and write\_memory fields are pointers to read\_memory, read\_string and write\_memory callbacks for reading from and writing to global memory or thread local storage in the OpenMP program.

The get\_thread\_context\_for\_thread\_id field is a pointer to a

get\_thread\_context\_for\_thread\_id callback that the OMPD library can use to obtain a native thread context that corresponds to a native thread identifier.

## Cross References

• alloc\_memory Callback, see Section 40.1.1

• device\_to\_host Callback, see Section 40.4.2

• free\_memory Callback, see Section 40.1.2

• get\_thread\_context\_for\_thread\_id Callback, see Section 40.3.1

• host\_to\_device Callback, see Section 40.4.3

• ompd\_initialize Routine, see Section 41.1.1

• print\_string Callback, see Section 40.5

• read\_memory Callback, see Section 40.2.2.1

• read\_string Callback, see Section 40.2.2.2

• sizeof\_type Callback, see Section 40.3.2

• symbol\_addr\_lookup Callback, see Section 40.2.1

• write\_memory Callback, see Section 40.2.3

## 39.5 OMPD device Type

<table><tr><td>Name: deviceProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompd\_device\_t;

C / C++

## Semantics

The device OMPD type provides information about OpenMP devices. OpenMP runtimes may utilize diferent underlying devices, each represented by a device identifier. The device identifiers can vary in size and format and, thus, are not explicitly represented in OMPD. Instead, a device identifier is passed across the interface via its device kind, its size in bytes and a pointer to where it is stored. The OMPD library and the third-party tool use the device kind to interpret the format of the device identifier that is referenced by the pointer argument. Each diferent device identifier kind is represented by a unique unsigned 64-bit integer value. Recommended values of device kinds are defined in the ompd-types.h header file, which is contained in the Supplementary Source Code package available via https://www.openmp.org/specifications/.

```c
typedef struct ompd_device_type_sizes_t {
    uint8_t sizeof_char;
    uint8_t sizeof_short;
    uint8_t sizeof_int;
    uint8_t sizeof_long;
    uint8_t sizeof_long_long;
    uint8_t sizeof_pointer;
} ompd_device_type_sizes_t;
```

## 39.6 OMPD device\_type\_sizes Type

<table><tr><td>Name: device_type_sizesProperties: C/C++-only, OMPD</td><td>Base Type: structure</td></tr></table>

## Fields

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>sizeof_char</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr><tr><td>sizeof_short</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr><tr><td>sizeof_int</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr><tr><td>sizeof_long</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr><tr><td>sizeof_long_long</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr><tr><td>sizeof_pointer</td><td>c_uint8_t</td><td>C/C++-only, OMPD</td></tr></table>

## Type Definition

## Semantics

The device\_type\_sizes OMPD type is used in OMPD callbacks through which the OMPD library can interrogate a third-party tool about the size of primitive types for the target architecture of the OpenMP runtime, as returned by the sizeof operator. The fields of device\_type\_sizes give the sizes of the eponymous basic types used by the OpenMP runtime. As the third-party tool and the OMPD library, by definition, execute on the same architecture, the size of the fields can be given as uint8\_t.

## Cross References

• sizeof\_type Callback, see Section 40.3.2
````
