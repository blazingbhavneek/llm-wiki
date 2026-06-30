# OpenMP-API-Specification Source Lines 28023-28412

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L28023-L28412

Citation: [OpenMP-API-Specification:L28023-L28412]

````text
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

# 36 General Entry Points

OMPT supports two principal sets of runtime entry points for tools. For both sets, entry points should not be global symbols since tools cannot rely on the visibility of such symbols. This chapter defines the first set, which enables a tool to register callbacks for events and to inspect the state of threads while executing in a callback or a signal handler. The omp-tools.h C/C++ header file provides the definitions of the types that are specified throughout this chapter.

OMPT also supports entry points for two classes of lookup entry points. The first class of lookup entry points contains a single member that is provided through the initialize callback: a function\_lookup entry point that returns pointers to the set of entry points that are defined in this chapter. The second class of lookup entry points includes a unique lookup entry point for each kind of device that can return pointers to entry points in a device’s OMPT tracing interface.

The binding thread set for each OMPT entry point is the encountering thread unless otherwise specified. The binding task set is the task executing on the encountering thread.

Several entry points are async-signal-safe entry points, which means they each have the async-signal-safe property, which implies that they are async signal safe.

## Restrictions

Restrictions on OMPT runtime entry points are as follows:

• Entry points must not be called from a signal handler on a native thread before a native-thread-begin or after a native-thread-end event.

• Device entry points must not be called after a device-finalize event for that device.

## 36.1 function\_lookup Entry Point

<table><tr><td>Name: function_lookupCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>interface_fn</td><td>default</td></tr><tr><td>interface_function_name</td><td>char</td><td>intent(in), pointer</td></tr></table>

Type Signature

C / C++

typedef ompt\_interface\_fn\_t (<sub>\*</sub>ompt\_function\_lookup\_t) ( const char \*interface\_function\_name);

C / C++

## Semantics

The function\_lookup entry point, which has the function\_lookup OMPT type, enables tools to look up pointers to OMPT entry points by name. When an OpenMP implementation invokes the initialize callback to configure the OMPT callback interface, it provides an entry point that provides pointers to other entry points that implement routines that are part of the OMPT callback interface. Alternatively, when it invokes a device\_initialize callback to configure the OMPT tracing interface for a device, it provides an entry point that provides pointers to entry points that implement tracing control routines appropriate for that device.

For these entry points, the interface\_function\_name argument is a C string that represents the name of the entry point to look up. If the name is unknown to the implementation, the entry point returns NULL. In a compliant implementation, the entry point that is provided by the initialize callback returns a valid function pointer for any entry point name listed in Table 32.1. Similarly, in a compliant implementation, the entry point that is provided by the device\_initialize callback returns non-NULL function pointers for any entry point name listed in Table 32.3, except for set\_trace\_ompt and get\_record\_ompt, as described in Section 32.2.5.

## Cross References

• device\_initialize Callback, see Section 35.1

• Binding Entry Points, see Section 32.2.3.1

• Tracing Activity on Target Devices, see Section 32.2.5

• initialize Callback, see Section 34.1.1

• OMPT interface\_fn Type, see Section 33.19

## 36.2 enumerate\_states Entry Point

<table><tr><td>Name: enumerate_statesCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>current_state</td><td>integer</td><td>default</td></tr><tr><td>next_state</td><td>integer</td><td>pointer</td></tr><tr><td>next_state_name</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr></table>

Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_enumerate\_states\_t) (int current\_state, int \*next\_state, const char \*\*next\_state\_name);

C / C++

## Semantics

An OpenMP implementation may support only a subset of the thread states that the state OMPT type defines. An OpenMP implementation may also support implementation defined states. The enumerate\_states entry point, which has the enumerate\_states OMPT type, is the entry point that enables a tool to enumerate the supported thread states.

When a supported thread state is passed as current\_state, the entry point assigns the next thread state in the enumeration to the variable passed by reference in next\_state and assigns the name associated with that state to the character pointer passed by reference in next\_state\_name; the returned string is immutable and defined for the lifetime of program execution. Whenever one or more states are left in the enumeration, the enumerate\_states entry point returns 1. When the last state in the enumeration is passed as current\_state, enumerate\_states returns 0, which indicates that the enumeration is complete.

To begin enumerating the supported states, a tool should pass ompt\_state\_undefined as current\_state. Subsequent invocations of enumerate\_states should pass the value assigned to the variable that was passed by reference in next\_state to the previous call. The ompt\_state\_undefined value is returned to indicate an invalid thread state.

## Cross References

• OMPT state Type, see Section 33.31

## 36.3 enumerate\_mutex\_impls Entry Point

Type Signature

<table><tr><td>Name: enumerate_mutex_implsCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>current_impl</td><td>integer</td><td>default</td></tr><tr><td>next_impl</td><td>integer</td><td>pointer</td></tr><tr><td>next_impl_name</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr></table>

<table><tr><td>C/C++</td></tr><tr><td>typedef int (*ompt_enumerate_mutex_impl_t) (int current_impl, int *next_impl, const char **next_impl_name);</td></tr></table>

C / C++

## Semantics

Mutual exclusion for locks, critical regions, and atomic regions may be implemented in several ways. The enumerate\_mutex\_impls entry point, which has the enumerate\_mutex\_impls OMPT type, enables a tool to enumerate the supported mutual exclusion implementations.

When a supported mutex implementation is passed as current\_impl, the entry point assigns the next mutex implementation in the enumeration to the variable passed by reference in next\_impl and assigns the name associated with that mutex implementation to the character pointer passed by reference in next\_impl\_name; the returned string is immutable and defined for the lifetime of program execution. Whenever one or more mutex implementations are left in the enumeration, the enumerate\_mutex\_impls entry point returns 1. When the last mutex implementation in the enumeration is passed as current\_impl, the entry point returns 0, which indicates that the enumeration is complete.

To begin enumerating the supported mutex implementations, a tool should pass ompt\_mutex\_impl\_none as current\_impl. Subsequent invocations of enumerate\_mutex\_impls should pass the value assigned to the variable that was passed by reference in next\_impl to the previous call. The value ompt\_mutex\_impl\_none is returned to indicate an invalid mutex implementation.

## 36.4 set\_callback Entry Point

<table><tr><td>Name: set_callbackCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>set_result</td><td>default</td></tr><tr><td>event</td><td>callbacks</td><td>OMPT</td></tr><tr><td>callback</td><td>callback</td><td>OMPT</td></tr></table>

## Type Signature

C / C++

typedef ompt\_set\_result\_t (<sub>\*</sub>ompt\_set\_callback\_t) ( ompt\_callbacks\_t event, ompt\_callback\_t callback);

C / C++

## Semantics

OpenMP implementations can use callbacks to indicate the occurrence of events during the execution of an OpenMP program. The set\_callback entry point, which has the set\_callback OMPT type, enables a tool to register the callback indicated by the callback argument for the event indicated by the event argument on the current device. The return value of set\_callback indicates the outcome of registering the callback and may be any value in the set\_result OMPT type except ompt\_set\_impossible. If callback is NULL then callbacks associated with event are disabled. If callbacks are successfully disabled then ompt\_set\_always is returned.

## Restrictions

Restrictions on the set\_callback entry point are as follows:

• The type signature for callback must match the type signature appropriate for the event.

## Cross References

• OMPT callback Type, see Section 33.5

• OMPT callbacks Type, see Section 33.6

• Monitoring Activity on the Host with OMPT, see Section 32.2.4

• OMPT set\_result Type, see Section 33.28
````
