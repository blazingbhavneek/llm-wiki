## 39.7 OMPD frame\_info Type

<table><tr><td>Name: frame_infoProperties: C/C++-only, OMPD</td><td>Base Type: structure</td></tr></table>

## Fields

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>frame_address</td><td>address</td><td>C/C++-only, OMPD</td></tr><tr><td>frame_flag</td><td>word</td><td>C/C++-only, OMPD</td></tr></table>

## Type Definition

C / C++

typedef struct ompd\_frame\_info\_t { ompd\_address\_t frame\_address; ompd\_word\_t frame\_flag; } ompd\_frame\_info\_t;

C / C++

## Semantics

The frame\_info OMPD type is a structure type that OMPD uses to specify frame information. The frame\_address field of frame\_info identifies a frame. The frame\_flag field of frame\_info indicates what type of information is provided in frame\_address. The values and meaning are the same as are defined for the frame\_flag OMPT type.

## Cross References

• OMPD address Type, see Section 39.2

• OMPT frame\_flag Type, see Section 33.16

• OMPD word Type, see Section 39.17

## 39.8 OMPD icv\_id Type

<table><tr><td>Name: icv_idProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompd_icv_undefined</td><td>0</td><td>C/C++-only, OMPD</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompd\_icv\_id\_t;

C / C++

## Semantics

The icv\_id OMPD type identifies ICVs.

39.9 OMPD rc Type

<table><tr><td>Name: rcProperties: C/C++-only, OMPD</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompd_rc_ok</td><td>0</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_unavailable</td><td>1</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_stale_handle</td><td>2</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_bad_input</td><td>3</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_error</td><td>4</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_unsupported</td><td>5</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_needs_state_tracking</td><td>6</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_incompatible</td><td>7</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_device_read_error</td><td>8</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_device_write_error</td><td>9</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_nomem</td><td>10</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_incomplete</td><td>11</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_callback_error</td><td>12</td><td>C-only, OMPD</td></tr><tr><td>ompd_rc_incompatible_handle</td><td>13</td><td>C-only, OMPD</td></tr></table>

<table><tr><td colspan="2">typedef enum ompd_rc_t {</td></tr><tr><td>ompd_rc_ok</td><td>= 0,</td></tr><tr><td>ompd_rc_unavailable</td><td>= 1,</td></tr><tr><td>ompd_rc_stale_handle</td><td>= 2,</td></tr><tr><td>ompd_rc_bad_input</td><td>= 3,</td></tr><tr><td>ompd_rc_error</td><td>= 4,</td></tr><tr><td>ompd_rc_UNSUPPORTED</td><td>= 5,</td></tr><tr><td>ompd_rc_needs_state_tracking</td><td>= 6,</td></tr><tr><td>ompd_rc_incompatible</td><td>= 7,</td></tr><tr><td>ompd_rc_device_read_error</td><td>= 8,</td></tr><tr><td>ompd_rc_device_write_error</td><td>= 9,</td></tr><tr><td>ompd_rc_nomem</td><td>= 10,</td></tr><tr><td>ompd_rc_incomplete</td><td>= 11,</td></tr><tr><td>ompd_rc_callback_error</td><td>= 12,</td></tr><tr><td>ompd_rc_incompatible_handle</td><td>= 13</td></tr><tr><td colspan="2">} ompd_rc_t;</td></tr></table>

The rc OMPD type is the return code type of OMPD routines and OMPD callbacks. The values of the rc OMPD type and their semantics are defined as follows:

• ompd\_rc\_ok: The routine or callback procedure was successful;

• ompd\_rc\_unavailable: Information was not available for the specified context;

• ompd\_rc\_stale\_handle: The specified handle was not valid;

• ompd\_rc\_bad\_input: The arguments (other than handles) are invalid;

• ompd\_rc\_error: A fatal error occurred;

• ompd\_rc\_unsupported: The requested routine or callback is not supported for the specified arguments;

• ompd\_rc\_needs\_state\_tracking: The state tracking operation failed because state tracking was not enabled;

• ompd\_rc\_incompatible: The selected OMPD library was incompatible with the OpenMP program or was incapable of handling it;

• ompd\_rc\_device\_read\_error: A read operation failed on the device;

• ompd\_rc\_device\_write\_error: A write operation failed on the device;

• ompd\_rc\_nomem: A memory allocation failed;

• ompd\_rc\_incomplete: The information provided on return was incomplete, while the arguments were set to valid values;

• ompd\_rc\_callback\_error: The callback interface or one of the required callback procedures provided by the third-party tool was invalid; and

• ompd\_rc\_incompatible\_handle: The specified handle was incompatible with the routine or callback.

## 39.10 OMPD seg Type

<table><tr><td>Name: segProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr></table>

## Predefined Identifiers

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompd_segment_none</td><td>0</td><td>C/C++-only, OMPD</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompd\_seg\_t;

C / C++

## Semantics

The seg OMPD type represents a segment value as an unsigned integer.

39.11 OMPD scope Type

<table><tr><td>Name: scopeProperties: C/C++-only, OMPD</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompd_scope_global</td><td>1</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_address_space</td><td>2</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_thread</td><td>3</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_parallel</td><td>4</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_implicit_task</td><td>5</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_task</td><td>6</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_teams</td><td>7</td><td>C-only, OMPD</td></tr><tr><td>ompd_scope_target</td><td>8</td><td>C-only, OMPD</td></tr></table>

<table><tr><td>Type Definition</td><td>C / C++</td></tr><tr><td>typedef enum ompd_scope_t {</td><td></td></tr><tr><td>ompd_scope_global = 1,</td><td></td></tr><tr><td>ompd_scope_address_space = 2,</td><td></td></tr><tr><td>ompd_scope_thread = 3,</td><td></td></tr><tr><td>ompd_scope_parallel = 4,</td><td></td></tr><tr><td>ompd_scope_implicit_task = 5,</td><td></td></tr><tr><td>ompd_scope_task = 6,</td><td></td></tr><tr><td>ompd_scope_teams = 7,</td><td></td></tr><tr><td>ompd_scope_target = 8</td><td></td></tr><tr><td>} ompd_scope_t;</td><td></td></tr></table>

## Semantics

The scope OMPD type is used for scope handles to identify OpenMP scopes, including those related to parallel regions and tasks. When used in an OMPD routine or OMPD callback procedure, the scope OMPD type and the OMPD handle must match according to Table 39.1.

## 39.12 OMPD size Type

<table><tr><td>Name: sizeProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr></table>

TABLE 39.1: Mapping of Scope Type and OMPD Handles

<table><tr><td>Scope types</td><td>Handles</td></tr><tr><td>ompd_scope_global</td><td>Address space handle for the host device</td></tr><tr><td>ompd_scope_address_space</td><td>Any address space handle</td></tr><tr><td>ompd_scope_thread</td><td>Any native thread handle</td></tr><tr><td>ompd_scope_parallel</td><td>Any parallel handle</td></tr><tr><td>ompd_scope_implicit_task</td><td>Task handle for an implicit task</td></tr><tr><td>ompd_scope_teams</td><td>Parallel handle for an implicit parallel region generated from a teams construct</td></tr><tr><td>ompd_scope_target</td><td>Parallel handle for an implicit parallel region generated from a target construct</td></tr><tr><td>ompd_scope_task</td><td>Any task handle</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompd\_size\_t;

C / C++

The size OMPD type specifies the number of bytes in opaque data objects that are passed across the OMPD API.

## 39.13 OMPD team\_generator Type

<table><tr><td>Name: team_generatorProperties: C/C++-only, OMPD</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompd_generator_program</td><td>0</td><td>C-only, OMPD</td></tr><tr><td>ompd_generator_parallel</td><td>1</td><td>C-only, OMPD</td></tr><tr><td>ompd_generator_teams</td><td>2</td><td>C-only, OMPD</td></tr><tr><td>ompd_generator_target</td><td>3</td><td>C-only, OMPD</td></tr></table>

C / C++

typedef enum ompd\_team\_generator\_t {

ompd\_generator\_program = 0,

ompd\_generator\_parallel = 1,

ompd\_generator\_teams = 2,

ompd\_generator\_target = 3

} ompd\_team\_generator\_t;

C / C++

<table><tr><td>Name: thread_contextProperties: C/C++-only, handle, OMPD</td><td>Base Type: thread_cont</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef struct _ompd_thread_cont ompd_thread_context_t;C / C++</td></tr></table>

## Semantics

The team\_generator OMPD type represents the value of the team-generator-var ICV. The ompd\_generator\_program value indicates that the team is the initial team created at the start of the OpenMP program. The ompd\_generator\_parallel, ompd\_generator\_teams, and ompd\_generator\_target values indicate that the team was created by an encountered parallel construct, teams construct, or target construct, respectively.

## 39.14 OMPD thread\_context Type

## Semantics

A third-party tool uses the thread\_context OMPD type, which represents handles that are opaque to the OMPD library and that uniquely identify a native thread of the OpenMP process that it is monitoring.

## 39.15 OMPD thread\_id Type

<table><tr><td>Name: thread_idProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr><tr><td colspan="2">Type DefinitionC / C+mtypedef uint64_t ompd_thread_id_t;C / C++</td></tr></table>

The thread\_id OMPD type provides information about native threads. OpenMP runtimes may use diferent native thread implementations. Native thread identifiers for these implementations can vary in size and format and, thus, are not explicitly represented in OMPD. Instead, a native thread identifier is passed across the interface via the thread\_id OMPD type, its size in bytes and a

pointer to where it is stored. The OMPD library and the third-party tool use the thread\_id OMPD type to interpret the format of the native thread identifier that is referenced by the pointer argument. Each diferent native thread identifier kind is represented by a unique unsigned 64-bit integer value. Recommended values of the thread\_id OMPD type and formats for some corresponding native thread identifiers are defined in the ompd-types.h header file, which is contained in the Supplementary Source Code package available via https://www.openmp.org/specifications/.

## 39.16 OMPD wait\_id Type

<table><tr><td>Name: wait_idProperties: C/C++-only, OMPD</td><td>Base Type: c_uint64_t</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef uint64_t ompd_wait_id_t;C / C++</td></tr></table>

## Semantics

A variable of wait\_id OMPD type identifies the object on which a thread waits. The values and meaning of wait\_id are the same as those defined for the wait\_id OMPT type.

## Cross References

• OMPT wait\_id Type, see Section 33.40

## 39.17 OMPD word Type

<table><tr><td>Name: wordProperties: C/C++-only, OMPD</td><td>Base Type: c_int64_t</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef int64_t ompd_word_t;C / C++</td></tr></table>

## Semantics

The word OMPD type represents a data word from the OpenMP runtime as a signed integer.

## 39.18 OMPD Handle Types

The OMPD library defines handles, which have OMPD types that are handle types (i.e., they have the handle property). These handles are used to refer to address spaces, threads, parallel regions and tasks and are managed by the OpenMP runtime. The internal structures that these handles represent are opaque to the third-party tool. Defining externally visible type names in this way introduces type safety to the interface and helps to catch instances where incorrect handles are passed by a third-party tool to the OMPD library. The structures do not need to be defined; instead, the OMPD library must cast incoming (pointers to) handles to the appropriate internal, private types.

Each OMPD routine or OMPD callback procedure that applies to a particular address space, thread, parallel region or task must explicitly specify a corresponding handle. A handle remains constant and valid while the associated entity is managed by the OpenMP runtime or until it is released with the corresponding OMPD routine for releasing handles of that type. If a third-party tool receives notification of the end of the lifetime of a managed entity (see Chapter 42) or it releases the handle, the handle may no longer be referenced.

39.18.1 OMPD address\_space\_handle Type

<table><tr><td>Name: address_space_handleProperties: C/C++-only, handle, OMPD</td><td>Base Type: aspace_handle</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef struct _ompd_aspace_handle ompd_address_space_handle_t;C / C++</td></tr></table>

## Semantics

The address\_space\_handle OMPD type is used for handles that represent address spaces.

## 39.18.2 OMPD parallel\_handle Type

<table><tr><td>Name: parallel_handleProperties: C/C++-only, handle, OMPD</td><td>Base Type: parallel_handle</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef struct _ompd_parallel_handle ompd_parallel_handle_t;C / C++</td></tr></table>

## Semantics

The parallel\_handle OMPD type is used for parallel handles that represent parallel regions.

## 39.18.3 OMPD task\_handle Type

<table><tr><td>Name: task_handleProperties: C/C++-only, handle, OMPD</td><td>Base Type: task_handle</td></tr></table>

## Type Definition

C / C++

typedef struct \_ompd\_task\_handle ompd\_task\_handle\_t;

C / C++

## Semantics

The task\_handle OMPD type is used for handles that represent tasks.

## 39.18.4 OMPD thread\_handle Type

<table><tr><td>Name: thread_handleProperties: C/C++-only, handle, OMPD</td><td>Base Type: thread_handle</td></tr></table>

## Type Definition

C / C++

typedef struct \_ompd\_thread\_handle ompd\_thread\_handle\_t;

C / C++

## Semantics

The thread\_handle OMPD type is used for handles that represent threads.
