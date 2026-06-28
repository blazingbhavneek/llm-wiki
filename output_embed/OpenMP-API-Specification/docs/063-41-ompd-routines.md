## 41 OMPD Routines

This chapter defines the OMPD routines, which are routines that have the OMPD property and, thus, are provided by the OMPD library to be used by third-party tools. Some OMPD routines require one or more specified threads to be stopped for the returned values to be meaningful. In this context, a stopped thread is a thread that is not modifying the observable OpenMP runtime state.

## 41.1 OMPD Library Initialization and Finalization

The OMPD library must be initialized exactly once after it is loaded, and finalized exactly once before it is unloaded. Per OpenMP process or core file initialization and finalization are also required. Once loaded, the tool can determine the version of the OMPD API that the library supports by calling ompd\_get\_api\_version. If the tool supports the version that ompd\_get\_api\_version returns, the tool starts the initialization by calling ompd\_initialize using the version of the OMPD API that the library supports. If the tool does not support the version that ompd\_get\_api\_version returns, it may attempt to call ompd\_initialize with a diferent version.

## Cross References

• ompd\_get\_api\_version Routine, see Section 41.1.2

• ompd\_initialize Routine, see Section 41.1.1

## 41.1.1 ompd\_initialize Routine

<table><tr><td>Name: ompd_initializeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>api_version</td><td>word</td><td>default</td></tr><tr><td>callbacks</td><td>callbacks</td><td>intent(in), pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_initialize(ompd\_word\_t api\_version, const ompd\_callbacks\_t <sub>\*</sub>callbacks);

## Semantics

A tool that uses OMPD calls ompd\_initialize to initialize each OMPD library that it loads. More than one library may be present in a third-party tool because the tool may control multiple devices, which may use diferent runtime systems that require diferent OMPD libraries. This initialization must be performed exactly once before the tool can begin to operate on an OpenMP process or core file.

The api\_version argument is the OMPD API version that the tool requests to use. The tool may call ompd\_get\_api\_version to obtain the latest OMPD API version that the OMPD library supports.

The tool provides the OMPD library with a set of callbacks in the callbacks input argument, which enables the OMPD library to allocate and to deallocate memory in the address space of the tool, to lookup the sizes of basic primitive types in the device, to lookup symbols in the device, and to read and to write memory in the device.

This routine returns ompd\_rc\_bad\_input if invalid callbacks are provided. In addition to the return codes permitted for all OMPD routines, this routine may return ompd\_rc\_unsupported if the requested API version cannot be provided.

## Cross References

• OMPD callbacks Type, see Section 39.4

• ompd\_get\_api\_version Routine, see Section 41.1.2

• OMPD rc Type, see Section 39.9

• OMPD word Type, see Section 39.17

## 41.1.2 ompd\_get\_api\_version Routine

<table><tr><td>Name: ompd_get_api_versionCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>api_version</td><td>word</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_api\_version(ompd\_word\_t <sub>\*</sub>api\_version);

C

## Semantics

The tool may call the ompd\_get\_api\_version routine to obtain the latest OMPD API version number of the OMPD library. The OMPD API version number is equal to the value of the \_OPENMP macro defined in the associated OpenMP implementation, if the C preprocessor is

supported. If the associated OpenMP implementation compiles Fortran codes without the use of a C preprocessor, the OMPD API version number is equal to the value of the openmp\_version predefined identifier. The latest version number is returned into the location to which the version argument points.

## Cross References

• ompd\_initialize Routine, see Section 41.1.1

• OMPD rc Type, see Section 39.9

• OMPD word Type, see Section 39.17

## 41.1.3 ompd\_get\_version\_string Routine

<table><tr><td>Name: ompd_get_version_stringCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>string</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_version\_string(const char <sub>\*\*</sub>string);

C

## Semantics

The ompd\_get\_version\_string routine returns a pointer to a descriptive version string of the OMPD library vendor, implementation, internal version, date, or any other information that may be useful to a tool user or vendor. An implementation should provide a diferent string for every change to its source code or build that could be visible to the OMPD user.

A pointer to a descriptive version string is placed into the location to which the string output argument points. The OMPD library owns the string that the OMPD library returns; the tool must not modify or release this string. The string remains valid for as long as the library is loaded. The ompd\_get\_version\_string routine may be called before ompd\_initialize. Accordingly, the OMPD library must not use heap or stack memory for the string.

The signatures of ompd\_get\_api\_version and ompd\_get\_version\_string are guaranteed not to change in future versions of OMPD. In contrast, the type definitions and prototypes in the rest of OMPD do not carry the same guarantee. Therefore a tool that uses OMPD should check the version of the loaded OMPD library before it calls any other OMPD routine.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• ompd\_get\_api\_version Routine, see Section 41.1.2

• OMPD rc Type, see Section 39.9

## 41.1.4 ompd\_finalize Routine

<table><tr><td colspan="2">Name: ompd_finalizeCategory: function</td><td colspan="2">Properties: C-only, OMPD</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">rc</td><td>default</td></tr><tr><td colspan="4">Prototypes</td></tr></table>

## Semantics

When the tool is finished with the OMPD library, it should call ompd\_finalize before it unloads the library. The call to the ompd\_finalize routine must be the last OMPD call that the tool makes before it unloads the library. This routine allows the OMPD library to free any resources that it may be holding. The OMPD library may implement a finalizer section, which executes as the library is unloaded and therefore after the call to ompd\_finalize. During finalization, the OMPD library may use the callbacks that the tool provided earlier during the call to ompd\_initialize. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unsupported if the OMPD library is not initialized.

## Cross References

• OMPD rc Type, see Section 39.9

## 41.2 Process Initialization and Finalization

## 41.2.1 ompd\_process\_initialize Routine

<table><tr><td>Name: ompd_process_initializeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>context</td><td>address_space_context</td><td>opaque, pointer</td></tr><tr><td>host_handle</td><td>address_space_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_process\_initialize( ompd\_address\_space\_context\_t <sub>\*</sub>context, ompd\_address\_space\_handle\_t <sub>\*\*</sub>host\_handle);

C

## Semantics

A tool calls ompd\_process\_initialize to obtain an address space handle for the host device when it initializes a session on an OpenMP process or core file. On return from ompd\_process\_initialize, the tool owns the address space handle, which it must release with ompd\_rel\_address\_space\_handle. The initialization function must be called before any OMPD operations are performed on the OpenMP process or core file. This routine allows the OMPD library to confirm that it can handle the OpenMP process or core file that context identifies.

The context argument is an opaque handle that the tool provides to address an address space from the host device. On return, the host\_handle argument provides an opaque handle to the tool for this address space, which the tool must release when it is no longer needed.

In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_incompatible if the OMPD library is incompatible with the runtime library loaded in the process.

## Cross References

• OMPD address\_space\_context Type, see Section 39.3

• OMPD address\_space\_handle Type, see Section 39.18.1

• ompd\_rel\_address\_space\_handle Routine, see Section 41.8.1

• OMPD rc Type, see Section 39.9

## 41.2.2 ompd\_device\_initialize Routine

<table><tr><td>Name: ompd_device_initializeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>host_handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>device_context</td><td>address_space_context</td><td>opaque, pointer</td></tr><tr><td>kind</td><td>device</td><td>default</td></tr><tr><td>sizeof_id</td><td>size</td><td>pointer</td></tr><tr><td>id</td><td>void</td><td>pointer</td></tr><tr><td>device_handle</td><td>address_space_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_device\_initialize(

ompd\_address\_space\_handle\_t <sub>\*</sub>host\_handle,

ompd\_address\_space\_context\_t <sub>\*</sub>device\_context,

ompd\_device\_t kind, ompd\_size\_t <sub>\*</sub>sizeof\_id, void <sub>\*</sub>id,

ompd\_address\_space\_handle\_t <sub>\*\*</sub>device\_handle);

C

## Semantics

A tool calls ompd\_device\_initialize to obtain an address space handle for a non-host device that has at least one active target region. On return from

ompd\_device\_initialize, the tool owns the address space handle. The host\_handle argument is an opaque handle that the tool provides to reference the host device address space associated with an OpenMP process or core file. The device\_context argument is an opaque handle that the tool provides to reference a non-host device address space. The kind, sizeof\_id, and id arguments represent a device identifier. On return the device\_handle argument provides an opaque handle to the tool for this address space.

In addition to the return codes permitted for all OMPD routines, this routine may return ompd\_rc\_unsupported if the OMPD library has no support for the specific device.

## Cross References

• OMPD address\_space\_context Type, see Section 39.3

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD device Type, see Section 39.5

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

## 41.2.3 ompd\_get\_device\_thread\_id\_kinds Routine

<table><tr><td>Name: ompd_get_device_thread_id_kinds Category: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>device_handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>kinds</td><td>thread_id</td><td>pointer-to-pointer</td></tr><tr><td>thread_id_sizes</td><td>size</td><td>pointer-to-pointer</td></tr><tr><td>count</td><td>integer</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_device\_thread\_id\_kinds( ompd\_address\_space\_handle\_t <sub>\*</sub>device\_handle, ompd\_thread\_id\_t <sub>\*\*</sub>kinds, ompd\_size\_t <sub>\*\*</sub>thread\_id\_sizes, int \*count);

C

## Semantics

The ompd\_get\_device\_thread\_id\_kinds routine returns an array of supported native thread identifier kinds and a corresponding array of their respective sizes for a given device. The OMPD library allocates storage for the arrays with the memory allocation callback that the tool provides. Each supported native thread identifier kind is guaranteed to be recognizable by the OMPD library and may be mapped to and from any OpenMP thread that executes on the device. The third-party tool owns the storage for the array of kinds and the array of sizes that is returned via the kinds and thread\_id\_sizes arguments, and it is responsible for freeing that storage.

The device\_handle argument is a pointer to an opaque address space handle that represents a host device (returned by ompd\_process\_initialize) or a non-host device (returned by ompd\_device\_initialize). On return, the kinds argument is the address of a pointer to an array of native thread identifier kinds, the thread\_id\_sizes argument is the address of a pointer to an array of the corresponding native thread identifier sizes used by the OMPD library, and the count argument is the address of a variable that indicates the sizes of the returned arrays.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• ompd\_device\_initialize Routine, see Section 41.2.2

• ompd\_process\_initialize Routine, see Section 41.2.1

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_id Type, see Section 39.15

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
