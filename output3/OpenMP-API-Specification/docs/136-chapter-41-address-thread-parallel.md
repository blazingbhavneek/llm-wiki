## 41.3 Address Space Information

## 41.3.1 ompd\_get\_omp\_version Routine

<table><tr><td>Name: ompd_get_omp_versionCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>omp_version</td><td>word</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_omp\_version(

ompd\_address\_space\_handle\_t <sub>\*</sub>address\_space, ompd\_word\_t <sub>\*</sub>omp\_version);

C

## Semantics

The tool may call the ompd\_get\_omp\_version routine to obtain the version of the OpenMP API that is associated with the address space address\_space. The address\_space argument is an opaque handle that the tool provides to reference the address space of the process or device. Upon return, the omp\_version argument contains the version of the OpenMP runtime in the \_OPENMP version macro format.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD rc Type, see Section 39.9

• OMPD word Type, see Section 39.17

## 41.3.2 ompd\_get\_omp\_version\_string Routine

<table><tr><td colspan="2">Name: ompd_get_omp_version_stringCategory: function</td><td colspan="2">Properties: C-only, OMPD</td></tr><tr><td colspan="2">Name: ompd_get_thread_in_parallelCategory: function</td><td colspan="2">Properties: C-only, OMPD</td></tr><tr><td colspan="4">Return Type and Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">rc</td><td>default</td></tr><tr><td>parallel_handle</td><td colspan="2">parallel_handle</td><td>opaque, pointer</td></tr><tr><td>thread_num</td><td colspan="2">integer</td><td>default</td></tr><tr><td>thread_handle</td><td colspan="2">thread_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>string</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_omp\_version\_string(

ompd\_address\_space\_handle\_t <sub>\*</sub>address\_space, const char <sub>\*\*</sub>string);

C

## Semantics

The ompd\_get\_omp\_version\_string routine returns a descriptive string for the OpenMP API version that is associated with an address space. The address\_space argument is an opaque handle that the tool provides to reference the address space of a process or device. A pointer to a descriptive version string is placed into the location to which the string output argument points. After returning from the routine, the tool owns the string. The OMPD library must use the memory allocation callback that the tool provides to allocate the string storage. The tool is responsible for releasing the memory.

## Cross References

• OMPD Handle Types, see Section 39.18

• OMPD rc Type, see Section 39.9

## 41.4 Thread Handle Routines

## 41.4.1 ompd\_get\_thread\_in\_parallel Routine

## Prototypes

C

ompd\_rc\_t ompd\_get\_thread\_in\_parallel( ompd\_parallel\_handle\_t <sub>\*</sub>parallel\_handle, int thread\_num, ompd\_thread\_handle\_t <sub>\*\*</sub>thread\_handle);

C

## Semantics

The ompd\_get\_thread\_in\_parallel routine enables a tool to obtain handles for OpenMP threads that are associated with a parallel region. A successful invocation of

ompd\_get\_thread\_in\_parallel returns a pointer to a native thread handle in the location to which thread\_handle points. This routine yields meaningful results only if all OpenMP threads in the team that is executing the parallel region are stopped.

The parallel\_handle argument is an opaque handle for a parallel region and selects the parallel region on which to operate. The thread\_num argument represents the thread number and selects the thread, the handle for which is to be returned. On return, the thread\_handle argument is a handle for the selected thread.

This routine returns ompd\_rc\_bad\_input if the thread\_num argument is greater than or equal to the team-size-var ICV or negative, in which case the value returned in thread\_handle is invalid.

## Cross References

• ompd\_get\_icv\_from\_scope Routine, see Section 41.11.2

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

## 41.4.2 ompd\_get\_thread\_handle Routine

<table><tr><td>Name: ompd_get_thread_handleCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>address_space_handle</td><td>pointer</td></tr><tr><td>kind</td><td>thread_id</td><td>default</td></tr><tr><td>sizeof_thread_id</td><td>size</td><td>default</td></tr><tr><td>thread_id</td><td>void</td><td>intent(in), pointer</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_thread\_handle( ompd\_address\_space\_handle\_t <sub>\*</sub>handle, ompd\_thread\_id\_t kind, ompd\_size\_t sizeof\_thread\_id, const void \*thread\_id, ompd\_thread\_handle\_t <sub>\*\*</sub>thread\_handle);

C

## Semantics

The ompd\_get\_thread\_handle routine maps a native thread to a native thread handle.

Further, the routine determines if the native thread identifier to which thread\_id points represents an OpenMP thread. If so, the routine returns ompd\_rc\_ok and the location to which thread\_handle points is set to the native thread handle for the native thread to which the OpenMP thread is mapped.

The handle argument is a handle that the tool provides to reference an address space. The kind, sizeof\_thread\_id, and thread\_id arguments represent a native thread identifier. On return, the thread\_handle argument provides a handle to the native thread within the provided address space.

The native thread identifier to which thread\_id points must be valid for the duration of the call to the routine. If the OMPD library must retain the native thread identifier, it must copy it.

This routine returns ompd\_rc\_bad\_input if a diferent value in sizeof\_thread\_id is expected for a thread kind of kind. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unsupported if the kind of thread is not supported and it returns ompd\_rc\_unavailable if the native thread is not an OpenMP thread.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_handle Type, see Section 39.18.4

• OMPD thread\_id Type, see Section 39.15

## 41.4.3 ompd\_get\_thread\_id Routine

<table><tr><td>Name: ompd_get_thread_idCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>pointer</td></tr><tr><td>kind</td><td>thread_id</td><td>default</td></tr><tr><td>sizeof_thread_id</td><td>size</td><td>default</td></tr><tr><td>thread_id</td><td>void</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_thread\_id(ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle, ompd\_thread\_id\_t kind, ompd\_size\_t sizeof\_thread\_id, void \*thread\_id);

C

## Semantics

The ompd\_get\_thread\_id routine maps a native thread handle to a native thread identifier. This routine yields meaningful results only if the referenced OpenMP thread is stopped. The thread\_handle argument is a native thread handle. The kind argument represents the native thread identifier. The sizeof\_thread\_id argument represents the size of the native thread identifier. On return, the thread\_id argument is a bufer that represents a native thread identifier.

This routine returns ompd\_rc\_bad\_input if a diferent value in sizeof\_thread\_id is expected for a native thread kind of kind. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unsupported if the kind of native thread is not supported.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_handle Type, see Section 39.18.4

• OMPD thread\_id Type, see Section 39.15

## 41.4.4 ompd\_get\_device\_from\_thread Routine

<table><tr><td>Name: ompd_get_device_from_threadCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>pointer</td></tr><tr><td>device</td><td>address_space_handle</td><td>pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_device\_from\_thread( ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle, ompd\_address\_space\_handle\_t <sub>\*\*</sub>device);

C

## Semantics

The ompd\_get\_device\_from\_thread routine obtains a pointer to the address space handle for a device on which an OpenMP thread is executing. The returned pointer will be the same as the address space handle pointer that was previously returned by a call to

ompd\_process\_initialize (for a host device) or a call to ompd\_device\_initialize (for a non-host device). This routine yields meaningful results only if the referenced OpenMP thread is stopped.

The thread\_handle argument is a pointer to a native thread handle that represents a native thread to which an OpenMP thread is mapped. On return, the device argument is the address of a pointer to an address space handle.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

## 41.5 Parallel Region Handle Routines

## 41.5.1 ompd\_get\_curr\_parallel\_handle Routine

<table><tr><td colspan="2">Name: ompd_get_curr_parallel_handleCategory: function</td><td colspan="2">Properties: C-only, OMPD</td></tr><tr><td colspan="4">Return Type and Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">rc</td><td>default</td></tr><tr><td>thread_handle</td><td colspan="2">thread_handle</td><td>opaque, pointer</td></tr><tr><td>parallel_handle</td><td colspan="2">parallel_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_curr\_parallel\_handle( ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle, ompd\_parallel\_handle\_t <sub>\*\*</sub>parallel\_handle);

C

## Semantics

The ompd\_get\_curr\_parallel\_handle routine enables a tool to obtain a pointer to the parallel handle for the innermost parallel region that is associated with an OpenMP thread. This routine yields meaningful results only if the referenced OpenMP thread is stopped. The parallel handle is owned by the tool and it must be released by calling ompd\_rel\_parallel\_handle.

The thread\_handle argument is an opaque handle for a thread and selects the thread on which to operate. On return, the parallel\_handle argument is set to a handle for the parallel region that the associated thread is currently executing, if any.

In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unavailable if the thread is not currently part of a team.

## Cross References

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

## 41.5.2 ompd\_get\_enclosing\_parallel\_handle Routine

<table><tr><td>Name: ompd_get_enclosing_parallel_handle Category: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>parallel_handle</td><td>parallel_handle</td><td>opaque, pointer</td></tr><tr><td>enclosing_parallel_handle</td><td>parallel_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_enclosing\_parallel\_handle( ompd\_parallel\_handle\_t <sub>\*</sub>parallel\_handle, ompd\_parallel\_handle\_t \*\*enclosing\_parallel\_handle);

C

## Semantics

The ompd\_get\_enclosing\_parallel\_handle routine enables a tool to obtain a pointer to the parallel handle for the parallel region that encloses the parallel region that parallel\_handle specifies. This routine yields meaningful results only if at least one thread in the team that is executing the parallel region is stopped. A pointer to the parallel handle for the enclosing region is returned in the location to which enclosing\_parallel\_handle points. After a call to this routine, the tool owns the handle; the tool must release the handle with ompd\_rel\_parallel\_handle when it is no longer required. The parallel\_handle argument is an opaque handle for a parallel region that selects the parallel region on which to operate.

In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unavailable if no enclosing parallel region exists.

## Cross References

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

## 41.5.3 ompd\_get\_task\_parallel\_handle Routine

<table><tr><td>Name: ompd_get_task_parallel_handleCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>pointer</td></tr><tr><td>task_parallel_handle</td><td>parallel_handle</td><td>pointer-to-pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_task\_parallel\_handle(

ompd\_task\_handle\_t <sub>\*</sub>task\_handle,

ompd\_parallel\_handle\_t <sub>\*\*</sub>task\_parallel\_handle);

## Semantics

The ompd\_get\_task\_parallel\_handle routine enables a tool to obtain a pointer to the parallel handle for the parallel region that encloses the task region that task\_handle specifies. This routine yields meaningful results only if at least one thread in the team that is executing the parallel region is stopped. A pointer to the parallel handle is returned in the location to which task\_parallel\_handle points. The tool owns that parallel handle, which it must release with ompd\_rel\_parallel\_handle.

## Cross References

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3
