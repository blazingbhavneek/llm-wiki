## 41.7 Handle Comparing Routines

This section describes handle-comparing routines, which are routines that have the handle-comparing property and, thus, enable the comparison of two handles. The internal structure of handles is opaque to tools. While tools can easily compare pointers to handles, they cannot determine whether handles at two diferent addresses refer to the same underlying context and instead must use a handle-comparing routine.

On success, a handle-comparing routine returns, in the location to which its cmp\_value argument points, a signed integer value that indicates how the underlying contexts compare. A value less than, equal to, or greater than 0 indicates that the context to which <handle-type>\_handle\_1 corresponds is, respectively, less than, equal to, or greater than that to which <handle-type>\_handle\_2 corresponds. The <handle-type>\_handle\_1 and <handle-type>\_handle\_2 arguments are handles that correspond to the type of handle that the routine compares. In each handle-comparing routine, <handle-type> is replaced with the name of the type of handle that the routine compares. For all types of handles, the means by which two handles are ordered is implementation defined.

41.7.1 ompd\_parallel\_handle\_compare Routine

<table><tr><td colspan="2">Name: ompd_parallel_handle_compareCategory: function</td><td colspan="2">Properties: C-only, handle-comparing, OMPD</td></tr><tr><td colspan="4">Return Type and Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">rc</td><td>default</td></tr><tr><td>parallel_handle_1</td><td colspan="2">parallel_handle</td><td>opaque, pointer</td></tr><tr><td>parallel_handle_2</td><td colspan="2">parallel_handle</td><td>opaque, pointer</td></tr><tr><td>cmp_value</td><td colspan="2">integer</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_parallel\_handle\_compare(

ompd\_parallel\_handle\_t <sub>\*</sub>parallel\_handle\_1,

ompd\_parallel\_handle\_t \*parallel\_handle\_2, int \*cmp\_value);

C

## Semantics

The ompd\_parallel\_handle\_compare routine compares two parallel handles. The parallel\_handle\_1 and parallel\_handle\_2 arguments are parallel handles that correspond to parallel regions.

## Cross References

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

## 41.7.2 ompd\_task\_handle\_compare Routine

<table><tr><td>Name: ompd_task_handle_compareCategory: function</td><td>Properties: C-only, handle-comparing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle_1</td><td>task_handle</td><td>opaque, pointer</td></tr><tr><td>task_handle_2</td><td>task_handle</td><td>opaque, pointer</td></tr><tr><td>cmp_value</td><td>integer</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_task\_handle\_compare(

ompd\_task\_handle\_t <sub>\*</sub>task\_handle\_1,

ompd\_task\_handle\_t \*task\_handle\_2, int \*cmp\_value);

C

## Semantics

The ompd\_task\_handle\_compare routine compares two task handles. The task\_handle\_1 and task\_handle\_2 arguments are task handles that correspond to tasks.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

## 41.7.3 ompd\_thread\_handle\_compare Routine

<table><tr><td>Name: ompd_thread_handle_compareCategory: function</td><td>Properties: C-only, handle-comparing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle_1</td><td>thread_handle</td><td>opaque, pointer</td></tr><tr><td>thread_handle_2</td><td>thread_handle</td><td>opaque, pointer</td></tr><tr><td>cmp_value</td><td>integer</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_thread\_handle\_compare(

ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle\_1,

ompd\_thread\_handle\_t \*thread\_handle\_2, int \*cmp\_value);

C

## Semantics

The ompd\_thread\_handle\_compare routine compares two native thread handles. The thread\_handle\_1 and thread\_handle\_2 arguments are native thread handles that correspond to native threads.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

## 41.8 Handle Releasing Routines

This section describes handle-releasing routines, which are routines that have the handle-releasing property and, thus, release a handle owned by a tool. When a tool finishes with a handle that a handle argument identifies, it should release it with the corresponding handle-releasing routine so the OMPD library can release any resources that it has related to the corresponding context.

## Restrictions

Restrictions to handle-releasing routines are as follows:

• A context must not be used after its corresponding handle is released.

## 41.8.1 ompd\_rel\_address\_space\_handle Routine

<table><tr><td>Name: ompd_rel_address_space_handleCategory: function</td><td>Properties: C-only, handle-releasing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_rel\_address\_space\_handle( ompd\_address\_space\_handle\_t <sub>\*</sub>handle);

C

## Semantics

A tool calls ompd\_rel\_address\_space\_handle to release an address space handle.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD rc Type, see Section 39.9

## 41.8.2 ompd\_rel\_parallel\_handle Routine

<table><tr><td>Name: ompd_rel_parallel_handleCategory: function</td><td>Properties: C-only, handle-releasing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>parallel_handle</td><td>parallel_handle</td><td>opaque, pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_rel\_parallel\_handle(

ompd\_parallel\_handle\_t <sub>\*</sub>parallel\_handle);

C

## Semantics

A tool calls ompd\_rel\_parallel\_handle to release a parallel handle.

## Cross References

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

## 41.8.3 ompd\_rel\_task\_handle Routine

<table><tr><td>Name: ompd_rel_task_handleCategory: function</td><td>Properties: C-only, handle-releasing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>opaque, pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_rel\_task\_handle(ompd\_task\_handle\_t <sub>\*</sub>task\_handle);

C

## Semantics

A tool calls ompd\_rel\_task\_handle to release a task handle.

## Cross References

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

## 41.8.4 ompd\_rel\_thread\_handle Routine

<table><tr><td>Name: ompd_rel_thread_handleCategory: function</td><td>Properties: C-only, handle-releasing, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>opaque, pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_rel\_thread\_handle(

ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle);

C

## Semantics

A tool calls ompd\_rel\_thread\_handle to release a native thread handle.

Cross References

• OMPD rc Type, see Section 39.9

• OMPD thread\_handle Type, see Section 39.18.4

## 41.9 Querying Thread States

## 41.9.1 ompd\_enumerate\_states Routine

<table><tr><td>Name: ompd_enumerate_statesCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>address_space_handle</td><td>address_space_handle</td><td>opaque, pointer</td></tr><tr><td>current_state</td><td>word</td><td>default</td></tr><tr><td>next_state</td><td>word</td><td>pointer</td></tr><tr><td>next_state_name</td><td>const char</td><td>intent(out), pointer-to-pointer</td></tr><tr><td>more_endums</td><td>word</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_enumerate\_states( ompd\_address\_space\_handle\_t <sub>\*</sub>address\_space\_handle, ompd\_word\_t current\_state, ompd\_word\_t \*next\_state, const char \*\*next\_state\_name, ompd\_word\_t \*more\_enums);

## Semantics

An OpenMP implementation may support only a subset of the states that the state OMPT type defines. In addition, an OpenMP implementation may support implementation defined states. The ompd\_enumerate\_states routine enumerates the thread states that an OpenMP implementation supports.

When the current\_state argument is a thread state that an OpenMP implementation supports, the routine assigns the value and string name of the next thread state in the enumeration to the locations to which the next\_state and next\_state\_name arguments point. On return, the tool owns the next\_state\_name string. The OMPD library allocates storage for the string with the alloc\_memory callback that the tool provides. The tool is responsible for releasing the storage. On return, the location to which the more\_enums argument points has the value 1 whenever one or more states are left in the enumeration. On return, the location to which the more\_enums argument points has the value 0 when current\_state is the last state in the enumeration.

The address\_space\_handle argument identifies the address space. The current\_state argument must be a thread state that the OpenMP implementation supports. To begin enumerating the supported states, a tool should pass ompt\_state\_undefined as the value of current\_state. Subsequent calls to ompd\_enumerate\_states by the tool should pass the value that the routine returned in the next\_state argument. This routine returns ompd\_rc\_bad\_input if an unknown value is provided in current\_state.

## Cross References

• OMPD address\_space\_handle Type, see Section 39.18.1

• OMPD rc Type, see Section 39.9

• OMPT state Type, see Section 33.31

• OMPD word Type, see Section 39.17
