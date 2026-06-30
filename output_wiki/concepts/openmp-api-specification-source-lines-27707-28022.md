# OpenMP-API-Specification Source Lines 27707-28022

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L27707-L28022

Citation: [OpenMP-API-Specification:L27707-L28022]

````text
## Type Signature

mutex

## Semantics

A tool provides a lock\_destroy callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when it executes a lock-destroying routine.

## Cross References

• Lock Destroying Routines, see Section 28.2

• OMPT mutex Type, see Section 34.7.10

## 34.7.12 mutex\_acquired Callback

<table><tr><td>Name: mutex_acquiredCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-execution, OMPT</td></tr></table>

## Type Signature

mutex

## Semantics

A tool provides a mutex\_acquired callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when the structured block associated with a mutual-exclusion construct begins execution or when a region guarded by a lock-acquiring routine or lock-testing routine begins execution.

## Cross References

• Lock Acquiring Routines, see Section 28.3

• Lock Testing Routines, see Section 28.5

• OMPT mutex Type, see Section 34.7.10

## 34.7.13 mutex\_released Callback

<table><tr><td>Name: mutex_releasedCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-execution, OMPT</td></tr></table>

## Type Signature

mutex

## Semantics

A tool provides a mutex\_released callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when the structured block associated with a mutual-exclusion construct completes execution or, similarly, when a region that a lock-releasing routine guards completes execution.

## Cross References

• Lock Releasing Routines, see Section 28.4

• OMPT mutex Type, see Section 34.7.10

## 34.7.14 nest\_lock Callback

<table><tr><td>Name: nest_lockCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>wait_id</td><td>wait_id</td><td>OMPT</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_nest\_lock\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_wait\_id\_t wait\_id, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_nest\_lock\_t { ompt\_scope\_endpoint\_t endpoint; ompt\_wait\_id\_t wait\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_nest\_lock\_t;

C / C++

## Semantics

A tool provides a nest\_lock callback, which has the nest\_lock OMPT type, that the OpenMP implementation dispatches when a thread that owns a nestable lock invokes a routine that alters the nesting count of the lock but does not relinquish its ownership.

Cross References

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT wait\_id Type, see Section 33.40

## 34.7.15 flush Callback

<table><tr><td>Name: flushCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_flush\_t) (ompt\_data\_t <sub>\*</sub>thread\_data, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_flush\_t {const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_flush\_t;

C / C++

## Semantics

A tool provides a flush callback, which has the flush OMPT type, that the OpenMP implementation dispatches when it encounters a flush construct. The binding of the thread\_data argument is the encountering thread.

Cross References

• OMPT data Type, see Section 33.8

• flush Construct, see Section 17.8.6

## 34.8 control\_tool Callback

<table><tr><td>Name: control_toolCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>command</td><td>c_uint64_t</td><td>default</td></tr><tr><td>modifier</td><td>c_uint64_t</td><td>default</td></tr><tr><td>arg</td><td>c_ptr</td><td>iso_c, value, untraced-argument</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_callback\_control\_tool\_t) (uint64\_t command, uint64\_t modifier, void <sub>\*</sub>arg, const void <sub>\*</sub>codeptr\_ra);

## Trace Record

typedef struct ompt\_record\_control\_tool\_t { uint64\_t command; uint64\_t modifier; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_control\_tool\_t;

C / C++

## C / C++

## Semantics

A tool provides a control\_tool callback, which has the control\_tool OMPT type, that the OpenMP implementation uses to dispatch tool-control events. This callback may return any non-negative value, which will be returned to the OpenMP program as the return value of the omp\_control\_tool call that triggered the callback.

The command argument passes a command from an OpenMP program to a tool. Standard values for command are defined by the control\_tool OpenMP type. The modifier argument passes a command modifier from an OpenMP program to a tool. The command and modifier arguments may have tool-defined values. Tools must ignore command values that they are not designed to handle. The arg argument is a void pointer that enables a tool and an OpenMP program to exchange arbitrary state. The arg argument may be NULL.

## Restrictions

Restrictions on control\_tool callbacks are as follows:

• Tool-defined values for command must be greater than or equal to 64 and less than or equal to 2147483647 (INT32\_MAX).

• Tool-defined values for modifier must be non-negative and less than or equal to 2147483647 (INT32\_MAX).

## Cross References

• OpenMP control\_tool Type, see Section 20.12.1

• omp\_control\_tool Routine, see Section 31.1

# 35 Device Callbacks and Tracing

This chapter describes device-tracing callbacks, which have the device-tracing property. An OMPT tool may register these callbacks to monitor and to trace events that involve device execution. The C/C++ header file (omp-tools.h) also provides the types that this chapter defines.

## 35.1 device\_initialize Callback

<table><tr><td>Name: device_initializeCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>type</td><td>char</td><td>intent(in), pointer</td></tr><tr><td>device</td><td>device</td><td>OMPT, opaque, pointer</td></tr><tr><td>lookup</td><td>function_lookup</td><td>OMPT</td></tr><tr><td>documentation</td><td>char</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_device\_initialize\_t) ( int device\_num, const char <sub>\*</sub>type, ompt\_device\_t <sub>\*</sub>device, ompt\_function\_lookup\_t lookup, const char <sub>\*</sub>documentation);

C / C++

## Semantics

A tool provides device\_initialize callbacks, which have the device\_initialize OMPT type, that the OpenMP implementation can use to initialize asynchronous collection of traces for devices. The OpenMP implementation dispatches this callback after OpenMP is initialized for the device but before execution of any construct is started on the device.

A device\_initialize callback must fulfill several duties. First, the type argument should be used to determine if any special knowledge about the hardware or software of a device is employed. Second, the lookup argument should be used to look up pointers to device-tracing entry points for the device. Finally, these entry points should be used to set up tracing for the device. Initialization of tracing for a target device is described in Section 32.2.5.

The device\_num argument indicates the device number of the device that is being initialized. The type argument is a C string that indicates the type of the device. A device type string is a semicolon-separated character string that includes, at a minimum, the vendor and model name of the device. These names may be followed by a semicolon-separated sequence of characteristics of the hardware or software of the device.

The device argument is a pointer to an OpenMP object that represents the target device instance. Device-tracing entry points use this pointer to identify the device that is being addressed. The lookup argument points to a function\_lookup entry point that a tool must use to obtain pointers to other device-tracing entry points. If a device does not support tracing then lookup is NULL. The documentation argument is a C string that describes how to use these entry points. This documentation string may be a pointer to external documentation, or it may be inline descriptions that include names and type signatures for any device-specific entry points that are available through the function\_lookup entry point along with descriptions of how to use them to control monitoring and analysis of device traces.

The type and documentation arguments are immutable strings that are defined for the lifetime of program execution.

## Cross References

• OMPT device Type, see Section 33.11

• function\_lookup Entry Point, see Section 36.1

## 35.2 device\_finalize Callback

<table><tr><td colspan="2">Name: device_finalizeCategory: subroutine</td><td colspan="2">Properties: C/C++-only, device-tracing, OMPT</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>device_num</td><td colspan="2">integer</td><td>default</td></tr><tr><td colspan="4">Type SignatureC / C++typedef void (*ompt_callback_device_finalize_t) (int device_num);C / C++</td></tr></table>

A tool provides device\_finalize callbacks, which have the device\_finalize OMPT type, that the OpenMP implementation can use to finalize asynchronous collection of traces for devices. The OpenMP implementation dispatches this callback immediately prior to finalizing the device that the device\_num argument identifies. Prior to dispatching a device\_finalize callback for a device on which tracing is active, the OpenMP implementation stops tracing on the device and synchronously flushes all trace records for the device that have not yet been reported. These trace records are flushed through one or more buffer\_complete callbacks as needed prior to the dispatch of the device\_finalize callback.

## Cross References

• buffer\_complete Callback, see Section 35.6

## 35.3 device\_load Callback

<table><tr><td>Name: device_loadCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>filename</td><td>char</td><td>intent(in), pointer</td></tr><tr><td>offset_in_file</td><td>c_int64_t</td><td>iso_c, value</td></tr><tr><td>vma_in_file</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>bytes</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>host_addr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>device_addr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>module_id</td><td>c_uint64_t</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_device\_load\_t) (int device\_num,const char \*filename, int64\_t ofset\_in\_file, void \*vma\_in\_file,size\_t bytes, void \*host\_addr, void \*device\_addr,uint64\_t module\_id);

C / C++

## Semantics

A tool provides a device\_load callback, which has the device\_load OMPT type, that the OpenMP implementation can use to indicate that it has just loaded code onto the specified device. The device\_num argument indicates the device number of the device that is being loaded. The filename argument indicates the name of a file in which the device code can be found. A NULL filename indicates that the code is not available in a file in the file system. The ofset\_in\_file argument indicates an ofset into filename at which the code can be found. A value of -1 indicates that no ofset is provided. The vma\_in\_file argument indicates a virtual address in filename at which the code can be found. If no virtual address in the file is available then ompt\_addr\_none is used. The bytes argument indicates the size of the device code object in bytes.

The host\_addr argument indicates the address at which a copy of the device code is available in host memory. The device\_addr argument indicates the address at which the device code has been loaded in device memory. Both host\_addr and device\_addr will be ompt\_addr\_none when no code address is available for the relevant device. The module\_id argument is an identifier that is associated with the device code object.

## 35.4 device\_unload Callback

Arguments

<table><tr><td>Name: device_unloadCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>module_id</td><td>c_uint64_t</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_device\_unload\_t) (int device\_num, uint64\_t module\_id);

C / C++

## Semantics

A tool provides a device\_unload callback, which has the device\_unload OMPT type, that the OpenMP implementation can use to indicate that it is about to unload code from the specified device. The device\_num argument indicates the device number of the device that is being unloaded. The module\_id argument is an identifier that is associated with the device code object.

## 35.5 buffer\_request Callback

<table><tr><td>Name: buffer_requestCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>pointer-to-pointer</td></tr><tr><td>bytes</td><td>size_t</td><td>pointer</td></tr></table>

Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_buffer\_request\_t) (int device\_num, ompt\_buffer\_t <sub>\*\*</sub>bufer, size\_t <sub>\*</sub>bytes);

C / C++

## Semantics

A tool provides a buffer\_request callback, which has the buffer\_request OMPT type, that the OpenMP implementation dispatches to request a bufer in which to store trace records for the device specified by the device argument. The callback sets the location to which the bufer argument points to point to the location of the provided bufer. On entry to the callback, the location to which the bytes argument points holds the minimum size of the bufer in bytes that the implementation requests; the implementation must ensure that this size does not exceed the

recommended bufer size returned by the get\_buffer\_limits entry point for that device. A bufer request callback may set the location to which bytes points to 0 if it does not provide a bufer. If a callback sets that location to a value less than the minimum requested bufer size, further recording of events for the device may be disabled until the next invocation of the start\_trace entry point. This action causes the implementation to drop any trace records for the device until recording is restarted.

## Cross References

• OMPT buffer Type, see Section 33.3

• get\_buffer\_limits Entry Point, see Section 37.6

## 35.6 buffer\_complete Callback

<table><tr><td>Name: buffer_completeCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>pointer</td></tr><tr><td>bytes</td><td>size_t</td><td>default</td></tr><tr><td>begin</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr><tr><td>buffer_owned</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_buffer\_complete\_t) (int device\_num, ompt\_buffer\_t <sub>\*</sub>bufer, size\_t bytes, ompt\_buffer\_cursor\_t begin, int bufer\_owned);

C / C++

## Semantics

A tool provides a buffer\_complete callback, which has the buffer\_complete OMPT type, that the OpenMP implementation dispatches to indicate that it will not record any more trace records in the bufer at the location to which the bufer argument points. The implementation guarantees that all trace records in the bufer, which was previously allocated by a buffer\_request callback, are valid. The device argument specifies the device for which the trace records were gathered. The bytes argument indicates the full size of the bufer. The begin argument is a OpenMP object that indicates the position of the beginning of the first trace record in the bufer. The bufer\_owned argument is 1 if the data to which bufer points can be deleted by the callback and 0 otherwise. If multiple devices accumulate events into a single bufer, this callback may be invoked with a pointer to one or more trace records in a shared bufer with bufer\_owned equal to zero.

Typically, a tool will iterate through the trace records in the bufer and process them. The OpenMP implementation makes these callbacks on a native thread that is not an OpenMP thread so these buffer\_complete callbacks are not required to be async signal safe.

## Restrictions

Restrictions on buffer\_complete callbacks are as follows:

• The callback must not delete the bufer if bufer\_owned is zero.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4
````
