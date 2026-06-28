## 41.9.2 ompd\_get\_state Routine

<table><tr><td>Name: ompd_get_stateCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>opaque, pointer</td></tr><tr><td>state</td><td>word</td><td>pointer</td></tr><tr><td>wait_id</td><td>wait_id</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_state(ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle, ompd\_word\_t <sub>\*</sub>state, ompd\_wait\_id\_t <sub>\*</sub>wait\_id);

## Semantics

The ompd\_get\_state routine returns the state of an OpenMP thread. This routine yields meaningful results only if the referenced thread is stopped. The thread\_handle argument identifies the thread. The state argument represents the state of that thread as represented by a value that ompd\_enumerate\_states returns. On return, if the wait\_id argument is a non-null value then it points to a handle that corresponds to the wait\_id wait identifier of the thread. If the thread state is not one of the specified wait states, the value to which wait\_id points is undefined.

## Cross References

• ompd\_enumerate\_states Routine, see Section 41.9.1

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

• OMPD wait\_id Type, see Section 39.16

• OMPD word Type, see Section 39.17

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
