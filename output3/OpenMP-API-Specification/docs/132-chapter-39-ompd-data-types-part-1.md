
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
