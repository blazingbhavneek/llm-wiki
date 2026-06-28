
Runtime Library Routines

# 20 Runtime Library Definitions

This chapter defines the naming convention for the OpenMP API routines. It also defines several OpenMP types. The names of OpenMP API routines have an omp\_ prefix. Names that begin with the ompx\_ prefix are reserved for routines that are implementation defined extensions.

For each base language, a compliant implementation must supply a set of definitions for the OpenMP API routines and the OpenMP types that are used for their arguments and return values. The C/C++ header file (omp.h) and the Fortran module file (omp\_lib) or the deprecated Fortran include file (omp\_lib.h) provide these definitions and must contain a declaration for each routine and predefined identifier as well as a definition of each OpenMP type. In addition, each set of definitions may specify other implementation defined values.

C / C++

The routines are external functions with “C” linkage. C/C++ prototypes for the routines shall be provided in the omp.h header file.

C / C++

Fortran

The Fortran OpenMP API routines are external procedures. The return values of these routines are of default kind, unless otherwise specified. Interface declarations for the Fortran routines shall be provided in the form of a Fortran module named omp\_lib or the deprecated Fortran include file named omp\_lib.h. Whether the omp\_lib.h file provides derived-type definitions or those routines that require an explicit interface is implementation defined. Whether the include file or the module file (or both) is provided is also implementation defined. Whether any of the routines that take an argument are extended with a generic interface so arguments of diferent KIND type can be accommodated is implementation defined.

Fortran

## Restrictions

The following restrictions apply to all routines and OpenMP types:

C++

• Enumeration OpenMP types provided in the omp.h header file shall not be scoped enumeration types unless explicitly allowed.

C++

Predefined Identifiers

Fortran

• Routines may not be called from PURE or ELEMENTAL procedures.

• Routines may not be called in DO CONCURRENT constructs.

Fortran

## 20.1 Predefined Identifiers

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_curr_progress_width</td><td>see below</td><td>default</td></tr><tr><td>omp_fill</td><td>see below</td><td>default</td></tr><tr><td>omp_initial_device</td><td>-1</td><td>constant</td></tr><tr><td>omp_invalid_device</td><td>&lt; -1</td><td>constant</td></tr><tr><td>omp_num_args</td><td>see below</td><td>default</td></tr><tr><td>omp_unassigned_thread</td><td>&lt; -1</td><td>constant</td></tr><tr><td>openmp_version</td><td>see below</td><td>constant, Fortran-only</td></tr></table>

In addition to the predefined identifiers of OpenMP types that are defined with their corresponding OpenMP type, the OpenMP API includes the predefined identifiers shown above. The predefined identifiers omp\_invalid\_device and omp\_unassigned\_thread have implementation defined values less than -1. The predefined identifier omp\_num\_args can only be used in parameter list items and is a context-specific value that evaluates to the number of parameters of the associated declaration plus any variadic arguments that were passed, if any, at a given procedure call site. The predefined identifier omp\_curr\_progress\_width is a context-specific value that represents the maximum size, in terms of hardware threads, of a progress unit that is available to threads that are executing tasks in the current contention group.

The predefined identifier omp\_fill is a context-specific value that can only be used as a list item of the counts clause. It represents the number of logical iterations of a logical iteration space that remain after removing those specified by the other list items.

Fortran

The predefined identifiers are represented as default integer named constants. The predefined identifier openmp\_version has a value yyyymm where yyyy and mm are the year and month designations of the version of the OpenMP API that the implementation supports. This value matches that of the C preprocessor macro \_OPENMP, when a macro preprocessor is supported (see Section 5.3).

Fortran

## 20.2 Routine Bindings

Unless otherwise specified, the binding task set of any routine region is its encountering task and the binding thread set of any routine region is the encountering thread. That is, the default binding properties for routines are the encountering-task binding property and the encountering-thread binding property. However, the binding task set for all lock routine regions is all tasks in the contention group so all of those routines have the all-contention-group-tasks binding property. Further, the binding region of any routine that has a binding region for any type of region that is relevant to that routine region is the innermost enclosing region of that type. The binding thread set of several routines is all threads or all threads on the current device. Those routine have the all-threads binding property or the all-device-threads binding property.

## 20.3 Routine Argument Properties

Similarly to directive and clause arguments, routine arguments have properties that often specify constraints on their values. For all routines, if an argument is specified that does not conform to the constraints implied by its properties then the behavior is implementation defined. Routine properties include the properties that apply to the arguments of directives and clauses with the same meanings. The default property for all routine arguments is the required property. Routine arguments that have the optional property may be omitted in base languages for which a default value is defined. In addition, routine argument properties include ones that correspond to aspects of their base language prototypes, as shown in Table 20.1.

TABLE 20.1: Routine Argument Properties

<table><tr><td>Property</td><td>Property Description</td></tr><tr><td>C/C++ pointer propertyintent(in) property</td><td>A pointer type in C/C++, an array in FortranAn intent (in) argument in Fortran and, if type corresponds to a pointer type but not pointer to char, a const argument in C/C++</td></tr><tr><td>intent(out) property</td><td>An intent (out) argument in Fortran</td></tr><tr><td>ISO C propertypointer property</td><td>Binds to an ISO C type in FortranA pointer type in C/C++ and an assumed-size array in Fortran</td></tr><tr><td>pointer-to-pointer propertyprocedure property</td><td>A pointer-to-pointer type in C/C++A function pointer type in C/C++ and a procedure type in Fortran</td></tr><tr><td>value property</td><td>A value argument in Fortran</td></tr></table>

# 20.4 General OpenMP Types

This section describes general OpenMP types.

## 20.4.1 OpenMP intptr Type

<table><tr><td>Name: intptrProperties: omp</td><td>Base Type: c_intptr_t</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef intptr_t omp_intptr_t;C / C++Fortraninteger (kind=omp_c_intptr_t_kind)Fortran</td></tr></table>

The intptr OpenMP type is a signed integer type that is capable of holding a pointer on any device, and is equivalent to intptr\_t on platforms that provide it.

20.4.2 OpenMP uintptr Type

<table><tr><td>Name: uintptrProperties: C/C++-only, omp</td><td>Base Type: c_uintptr_t</td></tr></table>

Type Definition

C / C++

typedef uintptr\_t omp\_uintptr\_t;

C / C++

The uintptr OpenMP type is an unsigned integer type that is capable of holding a pointer on any device, and is equivalent to uintptr\_t on platforms that provide it.

## 20.5 OpenMP Parallel Region Support Types

This section describes OpenMP types that support parallel regions.

20.5.1 OpenMP sched Type

<table><tr><td>Name: schedProperties: omp</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_sched_static</td><td>0x1</td><td>omp</td></tr><tr><td>omp_sched_dynamic</td><td>0x2</td><td>omp</td></tr><tr><td>omp_sched_guided</td><td>0x3</td><td>omp</td></tr><tr><td>omp_sched_auto</td><td>0x4</td><td>omp</td></tr><tr><td>omp_sched_monotonic</td><td>0x80000000u</td><td>omp</td></tr></table>

## Type Definition

```txt
typedef enum omp_sched_t {
    omp_sched_static      = 0x1,
    omp_sched_dynamic     = 0x2,
    omp_sched_guided       = 0x3,
    omp_sched_auto         = 0x4,
    omp_sched_monotonic  = 0x80000000u
} omp_sched_t;
```

## C / C++

C / C++

Fortran

```fortran
integer (kind=omp_sched_kind), &
  parameter :: omp_sched_static = &
    int(Z'1', kind=omp_sched_kind)
integer (kind=omp_sched_kind), &
  parameter :: omp_sched_dynamic = &
    int(Z'2', kind=omp_sched_kind)
integer (kind=omp_sched_kind), &
  parameter :: omp_sched_guided = &
    int(Z'3', kind=omp_sched_kind)
integer (kind=omp_sched_kind), &
  parameter :: omp_sched_auto = int(Z'4', kind=omp_sched_kind)
integer (kind=omp_sched_kind), &
  parameter :: omp_sched_monotonic = &
    int(Z'80000000', kind=omp_sched_kind)
```

## Fortran

The sched type is used in routines that modify or retrieve the value of the run-sched-var ICV. Each of omp\_sched\_static, omp\_sched\_dynamic, omp\_sched\_guided, and omp\_sched\_auto can be combined with omp\_sched\_monotonic by using the + or | operator in C/C++ or the + operator in Fortran. If the schedule type is combined with the omp\_sched\_monotonic, the value corresponds to a schedule that is modified with the monotonic ordering-modifier. Otherwise, the value corresponds to a schedule that is modified with the nonmonotonic ordering-modifier.

Cross References

• run-sched-var ICV, see Table 3.1

## 20.6 OpenMP Tasking Support Types

This section describes OpenMP types that support tasking mechanisms.

## 20.6.1 OpenMP event\_handle Type

<table><tr><td>Name: event_handleProperties: named-handle, omp, opaque</td><td>Base Type:implementation-defined-int</td></tr></table>

Type Definition

C / C++

typedef <implementation-defined-integral> omp\_event\_handle\_t;

C / C++

Fortran

integer (kind=omp\_event\_handle\_kind)

Fortran

The event\_handle OpenMP type is an opaque type that represents events related to detachable tasks.

## 20.7 OpenMP Interoperability Support Types

This section describes OpenMP types that support interoperability mechanisms.

## 20.7.1 OpenMP interop Type

<table><tr><td>Name: interopProperties: named-handle, omp, opaque</td><td>Base Type:implementation-defined-int</td></tr></table>

<table><tr><td colspan="3">Predefined Identifiers</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_interop_none</td><td>0</td><td>default</td></tr></table>

Type Definition

C / C++

typedef <implementation-defined-integral> omp\_interop\_t;

C / C++

Fortran

integer (kind=omp\_interop\_kind)

Fortran

The interop OpenMP type is an opaque type that represents OpenMP interoperability objects, which thus have the opaque property. Interoperability objects may be initialized, destroyed or otherwise used by an interop construct and may be initialized to omp\_interop\_none.

Cross References

• interop Construct, see Section 16.1

## 20.7.2 OpenMP interop\_fr Type

<table><tr><td>Name: interop_frProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_ifr_last</td><td>N</td><td>omp</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum omp_interop_fr_t {omp_ifr_last = N} omp_interop_fr_t;C / C++Fortraninteger (kind=omp_interop_fr_kind), &amp; parameter :: omp_ifr_last = NFortran</td></tr></table>

The interop\_fr OpenMP type represents supported foreign runtime environments. Each value of the interop\_fr OpenMP type that an implementation provides will be available as omp\_ifr\_name, where name is the name of the foreign runtime environment. Available names include those that are listed in the OpenMP Additional Definitions document; implementation defined names may also be supported. The value of omp\_ifr\_last is defined as one greater than the value of the highest value of the supported foreign runtime environments that are listed in the aforementioned document or are implementation defined.

## Cross References

• OpenMP Contexts, see Section 9.1

• omp\_get\_num\_devices Routine, see Section 24.3

20.7.3 OpenMP interop\_property Type

<table><tr><td>Name: interop_propertyProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_ipr_fr_id</td><td>-1</td><td>omp</td></tr><tr><td>omp_ipr_fr_name</td><td>-2</td><td>omp</td></tr><tr><td>omp_ipr_vendor</td><td>-3</td><td>omp</td></tr><tr><td>omp_ipr_vendor_name</td><td>-4</td><td>omp</td></tr><tr><td>omp_ipr_device_num</td><td>-5</td><td>omp</td></tr><tr><td>omp_ipr_platform</td><td>-6</td><td>omp</td></tr><tr><td>omp_ipr_device</td><td>-7</td><td>omp</td></tr><tr><td>omp_ipr_device_context</td><td>-8</td><td>omp</td></tr><tr><td>omp_ipr_targetsync</td><td>-9</td><td>omp</td></tr><tr><td>omp_ipr_first</td><td>-9</td><td>omp</td></tr></table>

```txt
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_fr_id = -1
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_fr_name = -2
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_vendor = -3
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_vendor_name = -4
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_device_num = -5
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_platform = -6
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_device = -7
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_device_context = -8
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_targetsync = -9
integer (kind=omp_interop_property_kind), &
  parameter :: omp_ipr_first = -9
```

## Fortran

The interop\_property OpenMP type is used in interoperability routines to represent interoperability properties. OpenMP reserves all negative values for interoperability properties, as listed in Table 20.2; implementation defined interoperability properties may use non-negative values. The special interoperability property, omp\_ipr\_first, will always have the lowest interop\_property value, which may change in future versions of this specification. Valid values and types for the properties that Table 20.2 lists are specified in the OpenMP Additional Definitions document or are implementation defined unless otherwise specified. The Contexts column of Table 20.2 lists the OpenMP context that is relevant to the value.

## Cross References

• OpenMP Contexts, see Section 9.1

• omp\_get\_num\_devices Routine, see Section 24.3

## 20.7.4 OpenMP interop\_rc Type

<table><tr><td>Name: interop_rcProperties: omp</td><td>Base Type: enumeration</td></tr></table>

```txt
typedef enum omp_interop_rc_t {
    omp_irc_no_value      = 1,
    omp_irc_success       = 0,
    omp_irc_empty        = -1,
    omp_irc_out_of_range  = -2,
    omp_irc_type_int     = -3,
```

TABLE 20.2: Required Values of the interop\_property OpenMP Type

<table><tr><td>Enum Name</td><td>Contexts</td><td>Name</td><td>Property</td></tr><tr><td>omp_ipr_fr_id</td><td>all</td><td>fr_id</td><td>An intptr_t value that represents the foreign runtime environment ID of context</td></tr><tr><td>omp_ipr_fr_name</td><td>all</td><td>fr_name</td><td>C string value that represents the name of the foreign runtime environment of context</td></tr><tr><td>omp_ipr_vendor</td><td>all</td><td>vendor</td><td>An intptr_t that represents the vendor of context</td></tr><tr><td>omp_ipr_vendor_name</td><td>all</td><td>vendor_name</td><td>C string value that represents the vendor of context</td></tr><tr><td>omp_ipr_device_num</td><td>all</td><td>device_num</td><td>The OpenMP device number for the device in the range 0 to omp_get_num_devices inclusive</td></tr><tr><td>omp_ipr_platform</td><td>target</td><td>platform</td><td>A foreign platform handle usually spanning multiple devices</td></tr><tr><td>omp_ipr_device</td><td>target</td><td>device</td><td>A foreign device handle</td></tr><tr><td>omp_ipr_device_context</td><td>target</td><td>device_context</td><td>A handle to an instance of a foreign device context</td></tr><tr><td>omp_ipr_targetsync</td><td>targetsync</td><td>targetsync</td><td>A handle to a synchronization object of a foreign execution context</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_irc_no_value</td><td>1</td><td>omp</td></tr><tr><td>omp_irc_success</td><td>0</td><td>omp</td></tr><tr><td>omp_irc_empty</td><td>-1</td><td>omp</td></tr><tr><td>omp_irc_out_of_range</td><td>-2</td><td>omp</td></tr><tr><td>omp_irc_type_int</td><td>-3</td><td>omp</td></tr><tr><td>omp_irc_type_ptr</td><td>-4</td><td>omp</td></tr><tr><td>omp_irc_type_str</td><td>-5</td><td>omp</td></tr><tr><td>omp_irc_other</td><td>-6</td><td>omp</td></tr></table>

TABLE 20.3: Required Values for the interop\_rc OpenMP Type  
```txt
Enum Name
omp_irc_no_value
omp_irc_success
omp_irc_empty
omp_irc_out_of_range
omp_irc_type_int
omp_irc_type_ptr
omp_irc_type_str
omp_irc_other

Description
Valid but no meaningful value available
Successful, value is usable
The provided interoperability object is equal to
omp_interop_none
Property ID is out of range, see Table 20.2
Property type is int; use omp_get_interop_int
Property type is pointer; use omp_get_interop_ptr
Property type is string; use omp_get_interop_str
Other error; use omp_get_interop_rc_desc

omp_irc_type_ptr = -4,
omp_irc_type_str = -5,
omp_irc_other = -6
} omp_interop_rc_t;

C / C++
Fortran
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_no_value = 1
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_success = 0
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_empty = -1
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_out_of_range = -2
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_type_int = -3
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_type_ptr = -4
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_type_str = -5
integer (kind=omp_interop_rc_kind), &
parameter :: omp_irc_other = -6

Fortran
The interop_rc OpenMP type is used in several interoperability routines to specify their results. Table 20.3 describes the values that this type must include.
```

## Cross References

• OpenMP interop Type, see Section 20.7.1
