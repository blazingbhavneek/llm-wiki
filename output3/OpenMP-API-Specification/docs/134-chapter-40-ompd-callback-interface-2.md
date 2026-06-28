## 40 OMPD Callback Interface

For the OMPD library to provide information about the internal state of the OpenMP runtime system in an OpenMP process or core file, it must be able to extract information from the OpenMP process that the third-party tool is examining. The process on which the tool is operating may be either a live process or a core file, and a thread may be either a live thread in a live process or a thread in a core file. To enable the OMPD library to extract state information from a process or core file, the tool must supply the OMPD library with callbacks to inquire about the size of primitive types in the device of the process, to look up the addresses of symbols, and to read and to write memory in the device. The OMPD library uses these callbacks to implement its interface operations. The OMPD library only invokes the OMPD callbacks in response to calls to the OMPD library. The names of the OMPD callbacks correspond to the names of the fields of the callbacks OMPD type.

## Restrictions

The following restrictions apply to all OMPD callbacks:

• Unless explicitly specified otherwise, all OMPD callbacks must return ompd\_rc\_ok or ompd\_rc\_stale\_handle.

## 40.1 Memory Management of OMPD Library

A tool provides alloc\_memory and free\_memory callbacks to obtain and to release heap memory. This mechanism ensures that the OMPD library does not interfere with any custom memory management scheme that the tool may use.

If the OMPD library is implemented in C++ then memory management operators, like new and delete and their variants, must all be overloaded and implemented in terms of the callbacks that the third-party tool provides. The OMPD library must be implemented such that any of its definitions of new and delete do not interfere with any that the tool defines. In some cases, the OMPD library must allocate memory to return results to the tool. The tool then owns this memory and has the responsibility to release it. Thus, the OMPD library and the tool must use the same memory manager.

The OMPD library creates OMPD handles, which are opaque to tools and may have a complex internal structure. A tool cannot determine if the handle pointers that OMPD returns correspond to discrete heap allocations. Thus, the tool must not simply deallocate a handle by passing an address that it receives from the OMPD library to its own memory manager. Instead, OMPD includes routines that the tool must use when it no longer needs a handle.

A tool creates tool contexts and passes them to the OMPD library. The OMPD library does not release tool contexts; instead the tool releases them after it releases any handles that may reference the tool contexts.

## Cross References

• alloc\_memory Callback, see Section 40.1.1

• free\_memory Callback, see Section 40.1.2

## 40.1.1 alloc\_memory Callback

<table><tr><td>Name: alloc_memoryCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>nbytes</td><td>size</td><td>default</td></tr><tr><td>ptr</td><td>void</td><td>pointer-to-pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_memory\_alloc\_fn\_t) ( ompd\_size\_t nbytes, void <sub>\*\*</sub>ptr);

## Semantics

A tool provides an alloc\_memory callback, which has the memory\_alloc OMPD type, that the OMPD library may call to allocate memory. The nbytes argument is the size in bytes of the block of memory to allocate. The address of the newly allocated block of memory is returned in the location to which the ptr argument points. The newly allocated block is suitably aligned for any type of variable but is not guaranteed to be set to zero.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

## 40.1.2 free\_memory Callback

<table><tr><td>Name: free_memoryCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>ptr</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

C

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_memory\_free\_fn\_t) (void <sub>\*</sub>ptr);

C

## Semantics

A tool provides a free\_memory callback, which has the memory\_free OMPD type, that the OMPD library may call to deallocate memory that was obtained from a prior call to the alloc\_memory callback. The ptr argument is the address of the block to be deallocated.

## Cross References

• alloc\_memory Callback, see Section 40.1.1

• OMPD rc Type, see Section 39.9

## 40.2 Accessing Program or Runtime Memory

The OMPD library cannot directly read from or write to memory of the OpenMP program. Instead the OMPD library must use callbacks into the third-party tool that perform the operation.

## 40.2.1 symbol\_addr\_lookup Callback

<table><tr><td>Name: symbol_addr_lookupCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>pointer</td></tr><tr><td>thread_context</td><td>thread_context</td><td>pointer</td></tr><tr><td>symbol_name</td><td>char</td><td>intent(in), pointer</td></tr><tr><td>symbol_addr</td><td>address</td><td>pointer</td></tr><tr><td>file_name</td><td>char</td><td>intent(in), pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_symbol\_addr\_fn\_t) ( ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context, ompd\_thread\_context\_t <sub>\*</sub>thread\_context, const char <sub>\*</sub>symbol\_name, ompd\_address\_t <sub>\*</sub>symbol\_addr, const char <sub>\*</sub>file\_name);

## Semantics

A tool provides a symbol\_addr\_lookup callback, which has the symbol\_addr OMPD type, that the OMPD library may call to look up the address of the symbol provided in the symbol\_name argument within the address space specified by the address\_space\_context argument. This argument provides the tool’s representation of the address space of the process, core file, or device.

The thread\_context argument is NULL for global memory accesses. If thread\_context is not NULL, thread\_context gives the native thread context for the symbol lookup for the purpose of calculating thread local storage addresses. In this case, the native thread to which thread\_context refers must be associated with either the OpenMP process or the device that corresponds to the address\_space\_context argument.

The tool uses the symbol\_name argument that the OMPD library supplies verbatim. In particular, no name mangling, demangling or other transformations are performed before the lookup. The symbol\_name parameter must correspond to a statically allocated symbol within the specified address space. The symbol can correspond to any type of object, such as a variable, thread local storage variable, procedure, or untyped label. The symbol can have local, global, or weak binding. The callback returns the address of the symbol in the location to which symbol\_addr points.

The file\_name argument is an optional input argument that indicates the name of the shared library in which the symbol is defined, and it is intended to help the third-party tool disambiguate symbols that are defined multiple times across the executable or shared library files. The shared library name may not be an exact match for the name seen by the third-party tool. If file\_name is NULL then the third-party tool first tries to find the symbol in the executable file, and, if the symbol is not found, the third-party tool tries to find the symbol in the shared libraries in the order in which the shared libraries are loaded into the address space. If file\_name is a non-null value then the third-party tool first tries to find the symbol in the libraries that match the name in the file\_name argument, and, if the symbol is not found, the third-party tool then uses the same lookup order as when file\_name is NULL.

In addition to the general return codes for OMPD callbacks, symbol\_addr\_lookup callbacks may also return the following return codes:

• ompd\_rc\_error if the symbol that the symbol\_name argument specifies is not found; or

• ompd\_rc\_bad\_input if no symbol name is provided.

## Restrictions

Restrictions on symbol\_addr\_lookup callbacks are as follows:

• The address\_space\_context argument must be a non-null value.

• The callback does not support finding either symbols that are dynamically allocated on the call stack or statically allocated symbols that are defined within the scope of a procedure.

## Cross References

• OMPD address Type, see Section 39.2

• OMPD address\_space\_context Type, see Section 39.3

• OMPD rc Type, see Section 39.9

• OMPD thread\_context Type, see Section 39.14

## 40.2.2 OMPD memory\_read Type

<table><tr><td>Name: memory_readCategory: function pointer</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>pointer</td></tr><tr><td>thread_context</td><td>thread_context</td><td>pointer</td></tr><tr><td>addr</td><td>address</td><td>intent(in), pointer</td></tr><tr><td>nbytes</td><td>size</td><td>default</td></tr><tr><td>buffer</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_memory\_read\_fn\_t) (

ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context,

ompd\_thread\_context\_t <sub>\*</sub>thread\_context,

const ompd\_address\_t <sub>\*</sub>addr, ompd\_size\_t nbytes, void <sub>\*</sub>bufer);

C

Callbacks that have the memory\_read OMPD type are memory-reading callbacks, which each have the memory-reading property. A tool provides these callbacks to read memory from an OpenMP program. The thread\_context argument of this type should be NULL for global memory accesses. If it is a non-null value, the thread\_context argument identifies the native thread context for the memory access for the purpose of accessing thread local storage. The data are returned through the bufer argument, which is allocated and owned by the OMPD library. The contents of the bufer are unstructured, raw bytes. The OMPD library must use the device\_to\_host callback to perform any transformations such as byte-swapping that may be necessary.

In addition to the general return codes for OMPD callbacks, memory-reading callbacks may also return the following return code:

• ompd\_rc\_error if unallocated memory is reached while reading nbytes.

## Cross References

• OMPD address Type, see Section 39.2

• OMPD address\_space\_context Type, see Section 39.3

• device\_to\_host Callback, see Section 40.4.2

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_context Type, see Section 39.14

## 40.2.2.1 read\_memory Callback

<table><tr><td>Name: read_memoryCategory: function</td><td>Properties: C-only, common-type-callback, memory-reading, OMPD</td></tr></table>

## Type Signature

memory\_read

## Semantics

A tool provides a read\_memory callback, which is a memory-reading callback, that the OMPD library may call to copy a block of data from addr within the address space given by address\_space\_context to the tool bufer.

## Cross References

• OMPD address Type, see Section 39.2

• OMPD address\_space\_context Type, see Section 39.3

• OMPD memory\_read Type, see Section 40.2.2

## 40.2.2.2 read\_string Callback

<table><tr><td>Name: read_stringCategory: function</td><td>Properties: C-only, common-type-callback, memory-reading, OMPD</td></tr></table>

## Type Signature

memory\_read

## Semantics

A tool provides a read\_string callback, which is a memory-reading callback, that the OMPD library may call to copy a string to which addr points, including the terminating null byte (’\0’), to the tool bufer. At most nbytes bytes are copied. If a null byte is not among the first nbytes bytes, the string placed in bufer is not null-terminated.

In addition to the general return codes for memory-reading callbacks, read\_string callbacks may also return the following return code:

• ompd\_rc\_incomplete if no terminating null byte is found while reading nbytes using the read\_string callback.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

## 40.2.3 write\_memory Callback

<table><tr><td>Name: write_memoryCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>pointer</td></tr><tr><td>thread_context</td><td>thread_context</td><td>pointer</td></tr><tr><td>addr</td><td>address</td><td>intent(in), pointer</td></tr><tr><td>nbytes</td><td>size</td><td>default</td></tr><tr><td>buffer</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_memory\_write\_fn\_t) ( ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context, ompd\_thread\_context\_t <sub>\*</sub>thread\_context, const ompd\_address\_t <sub>\*</sub>addr, ompd\_size\_t nbytes, void <sub>\*</sub>bufer);

C

## Semantics

A tool provides a write\_memory callback, which has the memory\_write OMPD type, that the OMPD library may call to have the tool write a block of data to a location within an address space from a provided bufer. The address to which the data are to be written in the OpenMP program that address\_space\_context specifies is given by addr. The nbytes argument is the number of bytes to be transferred. The thread\_context argument for global memory accesses should be NULL. If it is a non-null value, then thread\_context identifies the native thread context for the memory access for the purpose of accessing thread local storage.

The data to be written are passed through bufer, which is allocated and owned by the OMPD library. The contents of the bufer are unstructured, raw bytes. The OMPD library must use the host\_to\_device callback to perform any transformations such as byte-swapping that may be necessary to render the data into a form that is compatible with the OpenMP runtime.

In addition to the general return codes for OMPD callbacks, write\_memory callbacks may also return the following return codes:

• ompd\_rc\_error if unallocated memory is reached while writing nbytes.

## Cross References

• OMPD address Type, see Section 39.2

• OMPD address\_space\_context Type, see Section 39.3

• host\_to\_device Callback, see Section 40.4.3

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_context Type, see Section 39.14

## 40.3 Context Management and Navigation

## Summary

A tool provides callbacks to manage and to navigate tool context relationships.

## 40.3.1 get\_thread\_context\_for\_thread\_id Callback

<table><tr><td>Name:get_thread_context_for_thread_idCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>opaque, pointer</td></tr><tr><td>kind</td><td>thread_id</td><td>default</td></tr><tr><td>sizeof_thread_id</td><td>size</td><td>default</td></tr><tr><td>thread_id</td><td>void</td><td>intent(in), pointer</td></tr><tr><td>thread_context</td><td>thread_context</td><td>pointer-to-pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_get\_thread\_context\_for\_thread\_id\_fn\_t) ( ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context, ompd\_thread\_id\_t kind, ompd\_size\_t sizeof\_thread\_id, const void <sub>\*</sub>thread\_id, ompd\_thread\_context\_t <sub>\*\*</sub>thread\_context);

## Semantics

A tool provides a get\_thread\_context\_for\_thread\_id callback, which has the get\_thread\_context\_for\_thread\_id OMPD type, that the OMPD library may call to map a native thread identifier to a third-party tool native thread context. The native thread identifier is within the address space that address\_space\_context identifies. The OMPD library can use the native thread context, for example, to access thread local storage.

The address\_space\_context argument is an opaque handle that the tool provides to reference an address space. The kind, sizeof\_thread\_id, and thread\_id arguments represent a native thread identifier. On return, the thread\_context argument provides a handle that maps a native thread identifier to a tool native thread context.

In addition to the general return codes for OMPD callbacks,

get\_thread\_context\_for\_thread\_id callbacks may also return the following return codes:

• ompd\_rc\_bad\_input if a diferent value in sizeof\_thread\_id is expected for the native thread identifier kind given by kind; or

• ompd\_rc\_unsupported if the native thread identifier kind is not supported.

## Restrictions

Restrictions on get\_thread\_context\_for\_thread\_id callbacks are as follows:

• The provided thread\_context must be valid until the OMPD library returns from the tool procedure.

## Cross References

• OMPD address\_space\_context Type, see Section 39.3

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

• OMPD thread\_context Type, see Section 39.14

• OMPD thread\_id Type, see Section 39.15

## 40.3.2 sizeof\_type Callback

<table><tr><td>Name: sizeof_typeCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>pointer</td></tr><tr><td>sizes</td><td>device_type_sizes</td><td>pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_sizeof\_fn\_t) ( ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context, ompd\_device\_type\_sizes\_t <sub>\*</sub>sizes);

C

## Semantics

A tool provides a sizeof\_type callback, which has the sizeof OMPD type, that the OMPD library may call to query the sizes of the basic primitive types for the address space that the address\_space\_context argument specifies in the location to which sizes points.

## Cross References

• OMPD address\_space\_context Type, see Section 39.3

• OMPD device\_type\_sizes Type, see Section 39.6

• OMPD rc Type, see Section 39.9

## 40.4 Device Translating Callbacks

## Summary

A tool provides device-translating callbacks, which have the device-translating property, to perform any necessary translations between devices on which the tool and OMPD library run and on which the OpenMP program runs.

## 40.4.1 OMPD device\_host Type

<table><tr><td>Name: device_hostCategory: function pointer</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_context</td><td>address_space_context</td><td>pointer</td></tr><tr><td>input</td><td>void</td><td>intent(in), pointer</td></tr><tr><td>unit_size</td><td>size</td><td>default</td></tr><tr><td>count</td><td>size</td><td>default</td></tr><tr><td>output</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

typedef ompd\_rc\_t (<sub>\*</sub>ompd\_callback\_device\_host\_fn\_t) ( ompd\_address\_space\_context\_t <sub>\*</sub>address\_space\_context, const void <sub>\*</sub>input, ompd\_size\_t unit\_size, ompd\_size\_t count, void \*output);

## Semantics

The architecture on which the third-party tool and the OMPD library execute may be diferent from the architecture on which the OpenMP program that is being examined executes. Thus, the conventions for representing data may difer. The callback interface includes operations to convert between the conventions, such as the byte order (endianness), that the tool and OMPD library use and the ones that the OpenMP program uses. The device\_host OMPD type is the type signature of the device\_to\_host and host\_to\_device callbacks that the tool provides to convert data between formats.

The address\_space\_context argument specifies the address space that is associated with the data. The input argument is the source bufer and the output argument is the destination bufer. The unit\_size argument is the size of each of the elements to be converted. The count argument is the number of elements to be transformed.

The OMPD library allocates and owns the input and output bufers. It must ensure that the bufers have the correct size and are eventually deallocated when they are no longer needed.

## Cross References

• OMPD address\_space\_context Type, see Section 39.3

• device\_to\_host Callback, see Section 40.4.2

• host\_to\_device Callback, see Section 40.4.3

• OMPD rc Type, see Section 39.9

• OMPD size Type, see Section 39.12

## 40.4.2 device\_to\_host Callback

<table><tr><td>Name: device_to_hostCategory: function</td><td>Properties: C-only, common-type-callback, device-translating, OMPD</td></tr></table>

## Semantics

The device\_to\_host is the device-translating callback that translates data that is read from the OpenMP program.

## Cross References

• OMPD device\_host Type, see Section 40.4.1

## 40.4.3 host\_to\_device Callback

<table><tr><td>Name: host_to_deviceCategory: function</td><td>Properties: C-only, common-type-callback, device-translating, OMPD</td></tr></table>

## Type Signature

device\_host

## Semantics

The host\_to\_device is the device-translating callback that translates data that is to be written to the OpenMP program.

## Cross References

• OMPD device\_host Type, see Section 40.4.1

## 40.5 print\_string Callback
