
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

## 35.7 target\_data\_op\_emi Callback

<table><tr><td>Name: target_data_op_emiCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT, untraced-argument</td></tr><tr><td>target_task_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>target_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>host_op_id</td><td>id</td><td>OMPT, pointer</td></tr><tr><td>optype</td><td>target_data_op</td><td>OMPT</td></tr><tr><td>dev1_addr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>dev1_device_num</td><td>integer</td><td>default</td></tr><tr><td>dev2_addr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>dev2_device_num</td><td>integer</td><td>default</td></tr><tr><td>bytes</td><td>size_t</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

## C / C++

typedef void (<sub>\*</sub>ompt\_callback\_target\_data\_op\_emi\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_data\_t <sub>\*</sub>target\_task\_data, ompt\_data\_t \*target\_data, ompt\_id\_t \*host\_op\_id, ompt\_target\_data\_op\_t optype, void <sub>\*</sub>dev1\_addr, int dev1\_device\_num, void \*dev2\_addr, int dev2\_device\_num, size\_t bytes, const void <sub>\*</sub>codeptr\_ra);

## Trace Record

typedef struct ompt\_record\_target\_data\_op\_emi\_t { ompt\_id\_t host\_op\_id; ompt\_target\_data\_op\_t optype; void <sub>\*</sub>dev1\_addr; int dev1\_device\_num; void <sub>\*</sub>dev2\_addr; int dev2\_device\_num; size\_t bytes; ompt\_device\_time\_t end\_time; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_target\_data\_op\_emi\_t;

## C / C++

## Additional information

The target\_data\_op callback may also be used. This callback has identical arguments to the target\_data\_op\_emi callback except that the endpoint and target\_task\_data arguments are omitted and the target\_data argument is replaced by the target\_id argument, which has the id OMPT type, and the host\_op\_id argument is not a pointer and is provided by the implementation. If this callback is registered, it is dispatched for the target\_data\_op\_end,

target-data-allocation-end, target-data-free-begin, target-data-associate, target-global-data-op, and target-data-disassociate events. This callback has been deprecated. In addition to the standard trace record OMPT type name, the target\_data\_op name may be used to specify a trace record OMPT type with identical fields. This OMPT type name has been deprecated.

## Semantics

A tool provides a target\_data\_op\_emi callback, which has the target\_data\_op\_emi OMPT type, that the OpenMP implementation dispatches when a device memory is allocated or freed, as well as when data is copied to or from a device.

Note – An OpenMP implementation may aggregate variables and data operations upon them. For instance, an implementation may synthesize a composite to represent multiple scalar variables and then allocate, free, or copy this composite as a whole rather than performing data operations on each one individually. Thus, the implementation may not dispatch callbacks for separate data operations on each variable.

The binding of the target\_task\_data argument is the target task region. The binding of the target\_data argument is the device region. The host\_op\_id argument points to a tool-controlled integer value that identifies a data operation for a target device. The optype argument indicates the kind of data operation.

TABLE 35.1: Association of dev1 and dev2 arguments for target data operations

<table><tr><td>Data op</td><td>dev1</td><td>dev2</td></tr><tr><td>allocate</td><td>host/none</td><td>device</td></tr><tr><td>transfer</td><td>from device</td><td>to device</td></tr><tr><td>delete</td><td>host/none</td><td>device</td></tr><tr><td>associate</td><td>host</td><td>device</td></tr><tr><td>disassociate</td><td>host</td><td>device</td></tr><tr><td>memset</td><td>none</td><td>device</td></tr></table>

The dev1\_addr argument indicates the data address on the device given by Table 35.1 or NULL if the table indicates none for device memory routines that solely operate on device memory. For rectangular-memory-copying routines this argument points to a structure of subvolume OMPT type that describes a rectangular subvolume of a multi-dimensional array src, in the device data environment of device dev1\_device\_num. The address src of the array is referenced as base in the subvolume OMPT type. The dev1\_device\_num argument indicates the device number on the device given by Table 35.1. The dev2\_addr argument indicates the data address on the device given by Table 35.1. For rectangular-memory-copying routines this argument points to a structure of subvolume OMPT type that describes a rectangular subvolume of a multi-dimensional array dst, in the device data environment of device dev2\_device\_num. The address dst of the array is referenced as base in the subvolume OMPT type. The dev2\_device\_num argument indicates the device number on the device given by Table 35.1. Whether in some operations dev1\_addr or dev2\_addr may point to an intermediate bufer is implementation defined. The bytes argument indicates the size of the data in bytes.

If set\_trace\_ompt has configured the implementation to trace data operations to device memory then the implementation will log a target\_data\_op\_emi trace record in a trace. The fields in the record are as follows:

• The host\_op\_id field contains an identifier of a data operation for a target device; if the corresponding target\_data\_op\_emi callback was dispatched, this identifier is the tool-controlled integer value to which the host\_op\_id argument of the callback points so that a tool may correlate the trace record with the callback, and otherwise the host\_op\_id field contains an implementation-controlled identifier;

• The optype, dev1\_addr, dev1\_device\_num, dev2\_addr, dev2\_device\_num, bytes, and codeptr\_ra fields contain the same values as the callback;

• The time when the data operation began execution for the device is recorded in the time field of an enclosing trace record of record\_ompt OMPT type; and

• The time when the data operation completed execution for the device is recorded in the end\_time field.

## Restrictions

Restrictions to target\_data\_op\_emi callbacks are as follows:

• The deprecated target\_data\_op callback must not be registered if a target\_data\_op\_emi callbacks is registered.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT device\_time Type, see Section 33.12

• OMPT id Type, see Section 33.18

• map Clause, see Section 7.9.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT target\_data\_op Type, see Section 33.35

## 35.8 target\_emi Callback

<table><tr><td>Name: target_emiCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>target</td><td>OMPT</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>target_task_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>target_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_target\_emi\_t) (ompt\_target\_t kind, ompt\_scope\_endpoint\_t endpoint, int device\_num, ompt\_data\_t \*task\_data, ompt\_data\_t \*target\_task\_data, ompt\_data\_t \*target\_data, const void \*codeptr\_ra);

## Trace Record

C / C++

typedef struct ompt\_record\_target\_emi\_t { ompt\_target\_t kind; ompt\_scope\_endpoint\_t endpoint; int device\_num; ompt\_id\_t task\_id; ompt\_id\_t target\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_target\_emi\_t;

## C / C++

## Additional information

The target callback may also be used. This callback has identical arguments to the target\_emi callback except that the target\_task\_data argument is omitted and the target\_data argument is replaced by the target\_id argument, which has the id OMPT type. If this callback is registered, it is dispatched for the target-begin, target-end, target-enter-data-begin,

target-enter-data-end, target-exit-data-begin, target-exit-data-end, target-update-begin, and target-update-end events. This callback has been deprecated. In addition to the standard trace record OMPT type name, the target name may be used to specify a trace record OMPT type with identical fields. This OMPT type name has been deprecated.

## Semantics

A tool provides a target\_emi callback, which has the target\_emi OMPT type, that the OpenMP implementation dispatches when a thread begins to execute a device construct. The kind argument indicates the kind of device region. The device\_num argument specifies the device number of the target device associated with the region. The binding of the task\_data argument is the encountering task. The binding of the target\_task\_data argument is the target task. If a device region does not have a target task or if the target task is a merged task, this argument is NULL. The binding of the target\_data argument is the device region.

## Restrictions

Restrictions to target\_emi callbacks are as follows:

• The deprecated target callback must not be registered if a target\_emi callback is registered.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8

• OMPT target Type, see Section 33.34

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

## 35.9 target\_map\_emi Callback

<table><tr><td>Name: target_map_emiCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>target_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>nitems</td><td>integer</td><td>unsigned</td></tr><tr><td>host_addr</td><td>void</td><td>pointer-to-pointer</td></tr><tr><td>device_addr</td><td>void</td><td>pointer-to-pointer</td></tr><tr><td>bytes</td><td>size_t</td><td>pointer</td></tr><tr><td>mapping_flags</td><td>integer</td><td>unsigned, pointer</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_target\_map\_emi\_t) ( ompt\_data\_t \*target\_data, unsigned int nitems, void \*\*host\_addr, void \*\*device\_addr, size\_t \*bytes, unsigned int \*mapping\_flags, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_target\_map\_emi\_t { ompt\_id\_t target\_id; unsigned int nitems; void <sub>\*\*</sub>host\_addr; void <sub>\*\*</sub>device\_addr; size\_t <sub>\*</sub>bytes; unsigned int <sub>\*</sub>mapping\_flags; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_target\_map\_emi\_t;

C / C++

## Additional information

The target\_map callback may also be used. This callback has identical arguments to the target\_map\_emi callback except that the target\_data argument is replaced by the target\_id argument, which has the id OMPT type. If this callback is registered, it is dispatched for any target-map events. This callback has been deprecated. In addition to the standard trace record OMPT type name, the target\_map name may be used to specify a trace record OMPT type with identical fields. This OMPT type name has been deprecated.

## Semantics

A tool provides a target\_map\_emi callback, which has the target\_map\_emi OMPT type, that the OpenMP implementation dispatches to indicate data mapping relationships. The implementation may report mappings associated with multiple map clauses that appear on the same construct with a single callback to report the efect of all mappings or multiple callbacks with each reporting a subset of the mappings. Further, the implementation may omit mappings that it determines are unnecessary. If the implementation issues multiple target\_map\_emi callbacks, these callbacks may be interleaved with target\_data\_op\_emi callbacks that report data operations associated with the mappings.

The binding of the target\_data argument is the device region. The nitems argument indicates the number of data mappings that the callback reports. The host\_addr argument indicates an array of host addresses. The device\_addr argument indicates an array of device addresses. The bytes argument indicates an array of sizes of data. The mapping\_flags argument indicates the kind of mapping operations, which may result from explicit map clauses or the implicit data-mapping rules (see Section 7.9). Flags for the mapping operations include one or more values specified by the target\_map\_flag type.

## Restrictions

Restrictions to target\_map\_emi callbacks are as follows:

• The deprecated target\_map callback must not be registered if a target\_map\_emi callback is registered.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

• map Clause, see Section 7.9.6

• target\_data\_op\_emi Callback, see Section 35.7

• OMPT target\_map\_flag Type, see Section 33.36

## 35.10 target\_submit\_emi Callback

<table><tr><td>Name: target_submit_emiCategory: subroutine</td><td>Properties: C/C++-only, device-tracing, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT, untraced-argument</td></tr><tr><td>target_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>host_op_id</td><td>id</td><td>OMPT, pointer</td></tr><tr><td>requested_num_teams</td><td>integer</td><td>unsigned</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_target\_submit\_emi\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_data\_t <sub>\*</sub>target\_data, ompt\_id\_t \*host\_op\_id, unsigned int requested\_num\_teams);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_target\_submit\_emi\_t {

ompt\_id\_t host\_op\_id;

unsigned int requested\_num\_teams;

unsigned int granted\_num\_teams;

ompt\_device\_time\_t end\_time;

} ompt\_record\_target\_submit\_emi\_t;

C / C++

## Additional information

The target\_submit callback may also be used. This callback has identical arguments to the target\_submit\_emi callback except that the endpoint argument is omitted and the target\_data argument is replaced by the target\_id argument, which has the id OMPT type, and the host\_op\_id argument is not a pointer and is provided by the implementation. If this callback is registered, it is dispatched for any target-submit-begin events. This callback has been deprecated. In addition to the standard trace record OMPT type name, the target\_kernel name may be used to specify a trace record OMPT type with identical fields. This OMPT type name has been deprecated.

## Semantics

A tool provides a target\_submit\_emi callback, which has the target\_submit\_emi OMPT type, that the OpenMP implementation dispatches before and after a target task initiates creation of an initial task on a device. The binding of the target\_data argument is the device region. The host\_op\_id argument points to a tool-controlled integer value that identifies an initial task on a target device. The requested\_num\_teams argument is the number of teams that the device construct requested to execute the region. The actual number of teams that execute the region may be smaller and generally will not be known until the region begins to execute on the device.

If set\_trace\_ompt has configured the implementation to trace device region execution for a device then the implementation will log a target\_submit\_emi trace record. The fields in the record are as follows:

• The host\_op\_id field contains an identifier that identifies the initial task on the device; if the corresponding target\_submit\_emi callback was dispatched, this identifier is the tool-controlled integer value to which the host\_op\_id argument of the callback points so that a tool may correlate the trace record with the callback, and otherwise the host\_op\_id field contains an implementation-controlled identifier;

• The requested\_num\_teams field contains the number of teams that the device construct requested to execute the device region;

• The granted\_num\_teams field contains the number of teams that the device actually used to execute the device region;

• The time when the initial task began execution on the device is recorded in the time field of an enclosing trace record of record\_ompt OMPT type; and

• The time when the initial task completed execution on the device is recorded in the end\_time field.

## Restrictions

Restrictions to target\_submit\_emi callbacks are as follows:

• The deprecated target\_submit callback must not be registered if a target\_submit\_emi callback is registered.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT device\_time Type, see Section 33.12

• OMPT id Type, see Section 33.18

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8
