# OpenMP-API-Specification Source Lines 31070-31497

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L31070-L31497

Citation: [OpenMP-API-Specification:L31070-L31497]

````text
## 41.10 Display Control Variables

## 41.10.1 ompd\_get\_display\_control\_vars Routine

<table><tr><td>Name: ompd_get_display_control_varsCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>control_vars</td><td>const char * const *</td><td>intent(out), pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_display\_control\_vars( ompd\_address\_space\_handle\_t <sub>\*</sub>address\_space\_handle, const char <sub>\*</sub> const <sub>\*</sub> <sub>\*</sub>control\_vars);

## Semantics

The ompd\_get\_display\_control\_vars routine returns a list of OpenMP control variables as a NULL-terminated vector of null-terminated strings of name/value pairs. These control variables have user-controllable settings and are important to the operation or performance of an OpenMP runtime system. The control variables that this interface exposes include all OpenMP environment variables, settings that may come from vendor or platform-specific environment variables, and other settings that afect the operation or functioning of an OpenMP runtime. The format of the strings is NAME ’=’ VALUE. NAME corresponds to the control variable name, optionally prepended with a bracketed DEVICE. VALUE corresponds to the value of the control variable.

On return, the tool owns the vector and the strings. The OMPD library must satisfy the termination constraints; it may use static or dynamic memory for the vector and/or the strings and is unconstrained in how it arranges them in memory. If it uses dynamic memory then the OMPD library must use the alloc\_memory callback that the tool provides. The tool must use the ompd\_rel\_display\_control\_vars routine to release the vector and the strings.

The address\_space\_handle argument identifies the address space. On return, the control\_vars argument points to the vector of display control variables.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• ompd\_initialize Routine, see Section 41.1.1

• ompd\_rel\_display\_control\_vars Routine, see Section 41.10.2

• OMPD rc Type, see Section 39.9

## 41.10.2 ompd\_rel\_display\_control\_vars Routine

<table><tr><td>Name: ompd_rel_display_control_varsCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>control_vars</td><td>const char * const *</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_rel\_display\_control\_vars( const char <sub>\*</sub> const <sub>\*</sub> <sub>\*</sub>control\_vars);

C

## Semantics

After a tool calls ompd\_get\_display\_control\_vars, it owns the vector and strings that it acquires. The tool must call ompd\_rel\_display\_control\_vars to release them. The control\_vars argument is the vector of display control variables to be released.

Cross References

• ompd\_get\_display\_control\_vars Routine, see Section 41.10.1

• OMPD rc Type, see Section 39.9

## 41.11 Accessing Scope-Specific Information

## 41.11.1 ompd\_enumerate\_icvs Routine

<table><tr><td>Name: ompd_enumerate_icvsCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>current</td><td>icv_id</td><td>default</td></tr><tr><td>next_id</td><td>icv_id</td><td>pointer</td></tr><tr><td>next_icv_name</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr><tr><td>next_scope</td><td>scope</td><td>pointer</td></tr><tr><td>more</td><td>integer</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_enumerate\_icvs( ompd\_address\_space\_handle\_t <sub>\*</sub>handle, ompd\_icv\_id\_t current, ompd\_icv\_id\_t <sub>\*</sub>next\_id, const char <sub>\*\*</sub>next\_icv\_name, ompd\_scope\_t <sub>\*</sub>next\_scope, int <sub>\*</sub>more);

C

## Semantics

The ompd\_enumerate\_icvs routine enables a tool to enumerate the ICVs that an OpenMP implementation supports and their related scopes. An OpenMP implementation must support all ICVs listed in Section 3.1. An OpenMP implementation may support additional implementation defined ICVs. An implementation may store ICVs in a diferent scope than Section 3.1 indicates.

When the current argument is set to the identifier of a supported ICV, ompd\_enumerate\_icvs assigns the value, string name, and scope of the next ICV in the enumeration to the locations to which the next\_id, next\_icv\_name, and next\_scope arguments point. On return, the tool owns the next\_icv\_name string. The OMPD library uses the alloc\_memory callback that the tool provides to allocate the string storage; the tool is responsible for releasing the memory.

On return, the location to which the more argument points has the value of 1 whenever one or more ICVs are left in the enumeration. On return, that location has the value 0 when current is the last ICV in the enumeration. The address\_space\_handle argument identifies the address space. The current argument must be an ICV that the OpenMP implementation supports. To begin enumerating the ICVs, a tool should pass ompd\_icv\_undefined as the value of current.

Subsequent calls to ompd\_enumerate\_icvs should pass the value returned by the routine in the next\_id output argument. On return, the next\_id argument points to an integer with the value of the ID of the next ICV in the enumeration. On return, the next\_icv\_name argument points to a character string with the name of the next ICV. On return, the value to which the next\_scope argument points identifies the scope of the next ICV. On return, the more\_enums argument points to an integer with the value of 1 when more ICVs are left to enumerate and the value of 0 when no more ICVs are left. This routine returns ompd\_rc\_bad\_input if an unknown value is provided in current.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD icv\_id Type, see Section 39.8

• OMPD rc Type, see Section 39.9

• OMPD scope Type, see Section 39.11

## 41.11.2 ompd\_get\_icv\_from\_scope Routine

<table><tr><td>Name: ompd_get_icv_from_scopeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>void</td><td>opaque, pointer</td></tr><tr><td>scope</td><td>scope</td><td>default</td></tr><tr><td>icv_id</td><td>icv_id</td><td>default</td></tr><tr><td>icv_value</td><td>word</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_icv\_from\_scope(void <sub>\*</sub>handle,

ompd\_scope\_t scope, ompd\_icv\_id\_t icv\_id, ompd\_word\_t <sub>\*</sub>icv\_value);

C

## Summary

The ompd\_get\_icv\_from\_scope routine returns the value of an ICV. The handle argument provides an OpenMP scope handle. The scope argument specifies the kind of scope provided in handle. The icv\_id argument specifies the ID of the requested ICV. On return, the icv\_value argument points to a location with the value of the requested ICV.

This routine returns ompd\_rc\_bad\_input if an unknown value is provided in icv\_id. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_incomplete if only the first item of the ICV is returned in the integer (e.g., if nthreads-var has more than one list item). Further, it returns ompd\_rc\_incompatible if the ICV cannot be represented as an integer or if the scope of the handle matches neither the scope as defined in Section 39.8 nor the scope for icv\_id as identified by ompd\_enumerate\_icvs.

## Cross References

• OMPD Handle Types, see Section 39.18

• OMPD icv\_id Type, see Section 39.8

• ompd\_enumerate\_icvs Routine, see Section 41.11.1

• OMPD rc Type, see Section 39.9

• OMPD scope Type, see Section 39.11

• OMPD word Type, see Section 39.17

## 41.11.3 ompd\_get\_icv\_string\_from\_scope Routine

<table><tr><td>Name: ompd_get_icv_string_from_scopeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>void</td><td>opaque, pointer</td></tr><tr><td>scope</td><td>scope</td><td>default</td></tr><tr><td>icv_id</td><td>icv_id</td><td>default</td></tr><tr><td>icv_string</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_icv\_string\_from\_scope(void <sub>\*</sub>handle,

ompd\_scope\_t scope, ompd\_icv\_id\_t icv\_id,

const char \*\*icv\_string);

C

## Semantics

The ompd\_get\_icv\_string\_from\_scope routine returns the value of an ICV. The handle argument provides an OpenMP scope handle. The scope argument specifies the kind of scope provided in handle. The icv\_id argument specifies the ID of the requested ICV. On return, the icv\_string argument points to a string representation of the requested ICV; on return, the tool owns the string. The OMPD library allocates the string storage with the alloc\_memory callback that the tool provides. The tool is responsible for releasing the memory.

This routine returns ompd\_rc\_bad\_input if an unknown value is provided in icv\_id. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_incompatible if the scope of the handle does not match the scope as defined in Section 39.8 or if it does not match the scope for icv\_id as identified by ompd\_enumerate\_icvs.

## Cross References

• OMPD Handle Types, see Section 39.18

• OMPD icv\_id Type, see Section 39.8

• ompd\_enumerate\_icvs Routine, see Section 41.11.1

• OMPD rc Type, see Section 39.9

• OMPD scope Type, see Section 39.11

41.11.4 ompd\_get\_tool\_data Routine

<table><tr><td>Name: ompd_get_tool_dataCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>void</td><td>opaque, pointer</td></tr><tr><td>scope</td><td>scope</td><td>default</td></tr><tr><td>value</td><td>word</td><td>pointer</td></tr><tr><td>ptr</td><td>address</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_tool\_data(void <sub>\*</sub>handle, ompd\_scope\_t scope, ompd\_word\_t <sub>\*</sub>value, ompd\_address\_t <sub>\*</sub>ptr);

## Semantics

The ompd\_get\_tool\_data routine provides access to the OMPT tool data stored for each scope. The handle argument provides an OpenMP scope handle. The scope argument specifies the kind of scope provided in handle. On return, the value argument points to the value field of the data OMPT type stored for the selected scope. On return, the ptr argument points to the ptr field of the data OMPT type stored for the selected scope. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unsupported if the runtime library does not support OMPT.

## Cross References

• OMPD address Type, see Section 39.2

• OMPT data Type, see Section 33.8

• OMPD Handle Types, see Section 39.18

• OMPD rc Type, see Section 39.9

• OMPD scope Type, see Section 39.11

• OMPD word Type, see Section 39.17

# 42 OMPD Breakpoint Symbol Names

The OpenMP implementation must define several symbols through which execution must pass when particular events occur and data collection for OMPD is enabled. A third-party tool can enable notification of an event by setting a breakpoint at the address of the symbol.

OMPD symbols have external C linkage and do not require demangling or other transformations to look up their names to obtain the address in the OpenMP program. While each OMPD symbol conceptually has a function type signature, it may not be a function. It may be a labeled location.

## 42.1 ompd\_bp\_thread\_begin Breakpoint

## Format

C

void ompd\_bp\_thread\_begin(void);

C

## Semantics

When starting a native thread that will be used as an OpenMP thread, the implementation must execute ompd\_bp\_thread\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_thread\_begin at every native-thread-begin and initial-thread-begin event. This execution occurs before the thread starts the execution of any OpenMP region.

## 42.2 ompd\_bp\_thread\_end Breakpoint

## Format

C

void ompd\_bp\_thread\_end(void);

C

## Semantics

When terminating an OpenMP thread or a native thread that has been used as an OpenMP thread, the implementation must execute ompd\_bp\_thread\_end. Thus, the OpenMP implementation must execute ompd\_bp\_thread\_end at every native-thread-end and initial-thread-end event. This execution occurs after the thread completes the execution of all OpenMP regions. After executing ompd\_bp\_thread\_end, any thread\_handle that was acquired for this thread is invalid and should be released by calling ompd\_rel\_thread\_handle.

## Cross References

• ompd\_rel\_thread\_handle Routine, see Section 41.8.4

## 42.3 ompd\_bp\_device\_begin Breakpoint

## Format

void ompd\_bp\_device\_begin(void);

## Semantics

When initializing a device for execution of target regions, the implementation must execute ompd\_bp\_device\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_device\_begin at every device-initialize event. This execution occurs before the work associated with any OpenMP region executes on the device.

## Cross References

• Device Initialization, see Section 15.4

• target Construct, see Section 15.8

## 42.4 ompd\_bp\_device\_end Breakpoint

## Format

void ompd\_bp\_device\_end(void);

## Semantics

When terminating use of a device, the implementation must execute ompd\_bp\_device\_end. Thus, the OpenMP implementation must execute ompd\_bp\_device\_end at every device-finalize event. This execution occurs after the device executes all OpenMP regions. After execution of ompd\_bp\_device\_end, any address\_space\_handle that was acquired for this device is invalid and should be released by calling ompd\_rel\_address\_space\_handle.

Cross References

• Device Initialization, see Section 15.4

• ompd\_rel\_address\_space\_handle Routine, see Section 41.8.1

## 42.5 ompd\_bp\_parallel\_begin Breakpoint

Format

void ompd\_bp\_parallel\_begin(void);

C

## Semantics

Before starting execution of a parallel region, the implementation must execute ompd\_bp\_parallel\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_parallel\_begin at every parallel-begin event. When the implementation reaches ompd\_bp\_parallel\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the parallel region that is beginning and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the parallel construct.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• parallel Construct, see Section 12.1

## 42.6 ompd\_bp\_parallel\_end Breakpoint

## Format ormat

C void ompd\_bp\_parallel\_end(void); C

## Semantics

After finishing execution of a parallel region, the implementation must execute ompd\_bp\_parallel\_end. Thus, the OpenMP implementation must execute ompd\_bp\_parallel\_end at every parallel-end event. When the implementation reaches ompd\_bp\_parallel\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the parallel region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the parallel construct. After execution of ompd\_bp\_parallel\_end, any parallel\_handle that was acquired for the parallel region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• parallel Construct, see Section 12.1

## 42.7 ompd\_bp\_teams\_begin Breakpoint

## Format

void ompd\_bp\_teams\_begin(void);

C

## Semantics

Before starting execution of a teams region, the implementation must execute ompd\_bp\_teams\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_teams\_begin at every teams-begin event. When the implementation reaches ompd\_bp\_teams\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the teams region that is beginning and the binding task set for

ompd\_get\_curr\_task\_handle is the encountering task for the teams construct.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• teams Construct, see Section 12.2

## 42.8 ompd\_bp\_teams\_end Breakpoint

## Format

void ompd\_bp\_teams\_end(void);

## Semantics

After finishing execution of a teams region, the implementation must execute ompd\_bp\_teams\_end. Thus, the OpenMP implementation must execute ompd\_bp\_teams\_end at every teams-end event. When the implementation reaches ompd\_bp\_teams\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the teams region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the teams construct. After execution of ompd\_bp\_teams\_end, any parallel\_handle that was acquired for the teams region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• teams Construct, see Section 12.2

## 42.9 ompd\_bp\_task\_begin Breakpoint

## Format

C

void ompd\_bp\_task\_begin(void);

C

## Semantics

Before starting execution of a task region, the implementation must execute ompd\_bp\_task\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_task\_begin immediately before starting execution of a structured block that is associated with a non-merged task. When the implementation reaches ompd\_bp\_task\_begin, the binding task set for ompd\_get\_curr\_task\_handle is the task that is scheduled to execute.

## Cross References

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

## 42.10 ompd\_bp\_task\_end Breakpoint

## Format

C

void ompd\_bp\_task\_end(void);

C

## Semantics

After finishing execution of a task region, the implementation must execute ompd\_bp\_task\_end. Thus, the OpenMP implementation must execute ompd\_bp\_task\_end immediately after completion of a structured block that is associated with a non-merged task. When the implementation reaches ompd\_bp\_task\_end, the binding task set for ompd\_get\_curr\_task\_handle is the task that finished execution. After execution of ompd\_bp\_task\_end, any task\_handle that was acquired for the task region is invalid and should be released by calling ompd\_rel\_task\_handle.

## Cross References

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_task\_handle Routine, see Section 41.8.3

## 42.11 ompd\_bp\_target\_begin Breakpoint

Format

C

void ompd\_bp\_target\_begin(void);

C

## Semantics

Before starting execution of a target region, the implementation must execute ompd\_bp\_target\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_target\_begin at every initial-task-begin event that results from the execution of an initial task enclosing a target region. When the implementation reaches ompd\_bp\_target\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the target region that is beginning and the binding task set for ompd\_get\_curr\_task\_handle is the initial task on the device.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• target Construct, see Section 15.8

## 42.12 ompd\_bp\_target\_end Breakpoint

## Format

void ompd\_bp\_target\_end(void);

## Semantics

After finishing execution of a target region, the implementation must execute ompd\_bp\_target\_end. Thus, the OpenMP implementation must execute ompd\_bp\_target\_end at every initial-task-end event that results from the execution of an initial task enclosing a target region. When the implementation reaches ompd\_bp\_target\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the target region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the initial task on the device. After execution of ompd\_bp\_target\_end, any parallel\_handle that was acquired for the target region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• target Construct, see Section 15.8
````
