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

## 36.5 get\_callback Entry Point

<table><tr><td>Name: get_callbackCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>event</td><td>callbacks</td><td>OMPT</td></tr><tr><td>callback</td><td>callback</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_callback\_t) (ompt\_callbacks\_t event, ompt\_callback\_t <sub>\*</sub>callback);

C / C++

## Semantics

The get\_callback entry point, which has the get\_callback OMPT type, enables a tool to retrieve a pointer to a registered callback (if any) that an OpenMP implementation invokes when a host event occurs. If the callback that is registered for the event that is specified by the event argument is not NULL, the pointer to the callback is assigned to the variable passed by reference in callback and get\_callback returns 1; otherwise, it returns 0. If get\_callback returns 0, the value of the variable passed by reference as callback is undefined.

## Restrictions

Restrictions on the get\_callback entry point are as follows:

• The callback argument must not be NULL and must point to valid storage.

## Cross References

• OMPT callback Type, see Section 33.5

• OMPT callbacks Type, see Section 33.6

• set\_callback Entry Point, see Section 36.4

Return Type

## 36.6 get\_thread\_data Entry Point

<table><tr><td>Name:get_thread_dataCategory:function</td><td>Properties:async-signal-safe, C/C++-only, OMPT</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>data</td><td>pointer</td></tr></table>

## Type Signature

C / C++

typedef ompt\_data\_t <sub>\*</sub>(<sub>\*</sub>ompt\_get\_thread\_data\_t) (void);

C / C++

## Semantics

Each thread can have an associated thread data object of data OMPT type. The get\_thread\_data entry point, which has the get\_thread\_data OMPT type, enables a tool to retrieve a pointer to the thread data object, if any, that is associated with the encountering thread. A tool may use a pointer to a thread’s data object that get\_thread\_data retrieves to inspect or to modify the value of the data object. When a thread is created, its data object is initialized with the value ompt\_data\_none.

## Cross References

• OMPT data Type, see Section 33.8

## 36.7 get\_num\_procs Entry Point

<table><tr><td>Name: get_num_procsCategory: function</td><td>Properties: all-device-threads-binding, async-signal-safe, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_num\_procs\_t) (void);

C / C++

## Semantics

The get\_num\_procs entry point, which has the get\_num\_procs OMPT type, enables a tool to retrieve the number of processors that are available on the host device at the time the entry point is called. This value may change between the time that it is determined and the time that it is read in the calling context due to system actions outside the control of the OpenMP implementation. The binding thread set of this entry point is all threads on the host device.

## 36.8 get\_num\_places Entry Point

Return Type and Arguments

<table><tr><td>Name: get_num_placesCategory: function</td><td>Properties: all-device-threads-binding, async-signal-safe, C/C++-only, OMPT</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_num\_places\_t) (void);

C / C++

## Semantics

The get\_num\_places entry point, which has the get\_num\_places OMPT type, enables a tool to retrieve the number of places in the place list. This value is equal to the number of places in the place-partition-var ICV in the execution environment of the initial task. The binding thread set of this entry point is all threads on the host device.

## Cross References

• OMP\_PLACES, see Section 4.1.6

• place-partition-var ICV, see Table 3.1

## 36.9 get\_place\_proc\_ids Entry Point

<table><tr><td>Name: get_place_proc_idsCategory: function</td><td>Properties: all-device-threads-binding, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>place_num</td><td>integer</td><td>default</td></tr><tr><td>ids_size</td><td>integer</td><td>default</td></tr><tr><td>ids</td><td>integer</td><td>pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_place\_proc\_ids\_t) (int place\_num, int ids\_size, int \*ids);

C / C++

## Semantics

The get\_place\_proc\_ids entry point, which has the get\_place\_proc\_ids OMPT type, enables a tool to retrieve the numerical identifiers of each processor that is associated with the place specified by the place\_num argument. The ids argument is an array in which the entry point can

return a vector of processor identifiers in the specified place; these identifiers are non-negative, and their meaning is implementation defined. The ids\_size argument indicates the size of the result array that is specified by ids. The binding thread set of this entry point is all threads on the device.

If the ids array of size ids\_size is large enough to contain all identifiers then they are returned in ids and their order in the array is implementation defined. Otherwise, if the ids array is too small, the values in ids when the entry point returns are undefined. The entry point always returns the number of numerical identifiers of the processors that are available to the execution environment in the specified place.

## 36.10 get\_place\_num Entry Point

<table><tr><td colspan="2">Name: get_place_numCategory: function</td><td colspan="2">Properties: async-signal-safe, C/C++-only, OMPT</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">integer</td><td>default</td></tr><tr><td colspan="4">Type SignatureC / C++typedef int (*ompt_get_place_num_t) (void);C / C++</td></tr></table>

When the encountering thread is bound to a place, the get\_place\_num entry point, which has the get\_place\_num OMPT type, enables a tool to retrieve the place number associated with the thread. The returned value is between zero and one less than the value returned by get\_num\_places, inclusive. When the encountering thread is not bound to a place, the entry point returns −1.

## 36.11 get\_partition\_place\_nums Entry Point

<table><tr><td>Name: get_partition_place_numsCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>place_nums_size</td><td>integer</td><td>default</td></tr><tr><td>place_nums</td><td>integer</td><td>pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_partition\_place\_nums\_t) ( int place\_nums\_size, int \*place\_nums);

C / C++

## Semantics

The get\_partition\_place\_nums entry point, which has the

get\_partition\_place\_nums OMPT type, enables a tool to retrieve a list of place numbers that correspond to the places in the place-partition-var ICV of the innermost implicit task. The place\_nums argument is an array in which the entry point can return a vector of place identifiers. The place\_nums\_size argument indicates the size of that array.

If the place\_nums array of size place\_nums\_size is large enough to contain all identifiers then they are returned in place\_nums and their order in the array is implementation defined. Otherwise, if the place\_nums array is too small, the values in place\_nums when the entry point returns are undefined. The entry point always returns the number of places in the place-partition-var ICV of the innermost implicit task.

## Cross References

• OMP\_PLACES, see Section 4.1.6

• place-partition-var ICV, see Table 3.1

## 36.12 get\_proc\_id Entry Point

<table><tr><td>Name: get_proc_idCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_proc\_id\_t) (void);

C / C++

The get\_proc\_id entry point, which has the get\_proc\_id OMPT type, enables a tool to retrieve the numerical identifier of the processor of the encountering thread. A defined numerical identifier is non-negative, and its meaning is implementation defined. A negative number indicates a failure to retrieve the numerical identifier.

## 36.13 get\_state Entry Point

<table><tr><td>Name: get_stateCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>wait_id</td><td>wait_id</td><td>OMPT, pointer</td></tr></table>

Type Signature

typedef int (<sub>\*</sub>ompt\_get\_state\_t) (ompt\_wait\_id\_t <sub>\*</sub>wait\_id);

C / C++

## Semantics

Each thread has an associated state and a wait identifier. If the thread state indicates that the thread is waiting for mutual exclusion then its wait identifier contains a handle that indicates the data object upon which the thread is waiting. The get\_state entry point, which has the get\_state OMPT type, enables a tool to retrieve the state and the wait identifier of the encountering thread. The returned value may be any one of the states predefined by the state OMPT type or a value that represents an implementation defined state. The tool may obtain a string representation for each state with the enumerate\_states entry point. If the returned state indicates that the thread is waiting for a lock, nestable lock, critical region, atomic region, or ordered region and the wait identifier passed as the wait\_id argument is not NULL then the value of the wait identifier is assigned to that argument, which is a pointer to a handle. If the returned state is not one of the specified wait states then the value of that handle is undefined after the call.

## Restrictions

Restrictions on the get\_state entry point are as follows:

• The wait\_id argument must be a reference to a variable of the wait\_id OMPT type or NULL.

## Cross References

• enumerate\_states Entry Point, see Section 36.2

• OMPT state Type, see Section 33.31

• OMPT wait\_id Type, see Section 33.40

## 36.14 get\_parallel\_info Entry Point

<table><tr><td>Name: get_parallel_infoCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>ancestor_level</td><td>integer</td><td>default</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer-to-pointer</td></tr><tr><td>team_size</td><td>integer</td><td>pointer</td></tr></table>

Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_parallel\_info\_t) (int ancestor\_level, ompt\_data\_t \*\*parallel\_data, int \*team\_size);

C / C++

## Semantics

During execution, an OpenMP program may employ nested parallel regions. The During execution, an OpenMP program may employ nested parallel regions. The get\_parallel\_info entry point, which has the get\_parallel\_info OMPT type, enables a tool to retrieve information about the current parallel region and any enclosing parallel regions for the current execution context.

The ancestor\_level argument specifies the parallel region of interest by its ancestor level. Ancestor level 0 refers to the innermost parallel region; information about enclosing parallel regions may be obtained using larger values for ancestor\_level. Information about a parallel region may not be available if the ancestor level is 0; otherwise it must be available if a parallel region exists at the specified ancestor level. The entry point returns 2 if a parallel region exists at the specified ancestor level and the information is available, 1 if a parallel region exists at the specified ancestor level but the information is currently unavailable, and 0 otherwise. The parallel\_data argument returns the parallel data if the argument is not NULL. The team\_size argument returns the team size if the argument is not NULL. If no parallel region exists at the specified ancestor level or the information is unavailable then the values of variables passed by reference to the entry point are undefined when get\_parallel\_info returns.

A tool may use the pointer to the data object of a parallel region that it obtains from this entry point to inspect or to modify the value of the data object. When a parallel region is created, its data object will be initialized with the value ompt\_data\_none. Between a parallel-begin event and an implicit-task-begin event, a call to get\_parallel\_info with an ancestor\_level value of 0 may return information about the outer team or the new team. If a thread is in the ompt\_state\_wait\_barrier\_implicit\_parallel state then a call to

get\_parallel\_info may return a pointer to a copy of the specified parallel region’s parallel\_data rather than a pointer to the data word for the region itself. This convention enables the primary thread for a parallel region to free storage for the region immediately after the region ends, yet avoid having some other thread in the team that is executing the region potentially reference the parallel\_data object for the region after it has been freed.

If get\_parallel\_info returns two then the entry point has the following efects:

• If a non-null value was passed for parallel\_data, the value returned in parallel\_data is a pointer to a data word that is associated with the parallel region at the specified level; and

• If a non-null value was passed for team\_size, the value returned in the integer to which team\_size points is the number of threads in the team that is associated with the parallel region.

## Restrictions

Restrictions on the get\_parallel\_info entry point are as follows:

• While the ancestor\_level argument is passed by value, all other arguments must be valid pointers to variables of the specified types or NULL.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT state Type, see Section 33.31

## 36.15 get\_task\_info Entry Point

<table><tr><td>Name: get_task_infoCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>ancestor_level</td><td>integer</td><td>default</td></tr><tr><td>flags</td><td>integer</td><td>pointer</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer-to-pointer</td></tr><tr><td>task_frame</td><td>frame</td><td>OMPT, pointer-to-pointer</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer-to-pointer</td></tr><tr><td>thread_num</td><td>integer</td><td>pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_task\_info\_t) (int ancestor\_level, int \*flags, ompt\_data\_t \*\*task\_data, ompt\_frame\_t \*\*task\_frame, ompt\_data\_t \*\*parallel\_data, int \*thread\_num);

## Semantics

During execution, a thread may be executing a task. Additionally, the stack of the thread may contain procedure frames that are associated with suspended tasks or routines. The get\_task\_info entry point, which has the get\_task\_info OMPT type, enables a tool to retrieve information about any task on the stack of the encountering thread.

The ancestor\_level argument specifies the task region of interest by its ancestor level. Ancestor level 0 refers to the encountering task; information about other tasks with associated frames present on the stack in the current execution context may be queried at higher ancestor levels. Information about a task region may not be available if the ancestor level is 0; otherwise it must be available if a task region exists at the specified ancestor level. The entry point returns 2 if a task region exists at the specified ancestor level and the information is available, 1 if a task region exists at the specified ancestor level but the information is currently unavailable, and 0 otherwise.

If a task exists at the specified ancestor level and the information is available then information is returned in the variables passed by reference to the entry point. The flags argument returns the task type if the argument is not NULL. The task\_data argument returns the task data if the argument is not NULL. The task\_frame argument returns the task frame pointer if the argument is not NULL. The parallel\_data argument returns the parallel data if the argument is not NULL. The thread\_num argument returns the thread number if the argument is not NULL. If no task region exists at the specified ancestor level or the information is unavailable then the values of variables passed by reference to the entry point are undefined when get\_task\_info returns.

A tool may use a pointer to a data object for a task or parallel region that it obtains from get\_task\_info to inspect or to modify the value of the data object. When either a parallel region or a task region is created, its data object will be initialized with the value ompt\_data\_none.

If get\_task\_info returns 2 then the entry point has the following efects:

• If a non-null value was passed for flags then the value returned in the integer to which flags points represents the type of the task at the specified level; possible task types include initial task, implicit task, explicit task, and target task;

• If a non-null value was passed for task\_data then the value that is returned in the object to which it points is a pointer to a data word that is associated with the task at the specified level;

• If a non-null value was passed for task\_frame then the value that is returned in the object to which task\_frame points is a pointer to the frame OMPT type structure that is associated with the task at the specified level;

• If a non-null value was passed for parallel\_data then the value that is returned in the object to which parallel\_data points is a pointer to a data word that is associated with the parallel region that contains the task at the specified level or, if the task at the specified level is an initial task, NULL; and

• If a non-null value was passed for thread\_num, then the value that is returned in the object to which thread\_num points indicates the number of the thread in the parallel region that is executing the task at the specified level.

## Restrictions

Restrictions on the get\_task\_info entry point are as follows:

• While the ancestor\_level argument is passed by value, all other arguments must be valid pointers to variables of the specified types or NULL.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT frame Type, see Section 33.15

• OMPT task\_flag Type, see Section 33.37

## 36.16 get\_task\_memory Entry Point

<table><tr><td>Name:get_task_memoryCategory:function</td><td>Properties:async-signal-safe, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>addr</td><td>void</td><td>pointer-to-pointer</td></tr><tr><td>size</td><td>size_t</td><td>pointer</td></tr><tr><td>block</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_task\_memory\_t) (void <sub>\*\*</sub>addr, size\_t <sub>\*</sub>size, int block);

C / C++

## Semantics

During execution, a thread may be executing a task. The OpenMP implementation must preserve the data environment from the generation of the task for its execution. The get\_task\_memory entry point, which has the get\_task\_memory OMPT type, enables a tool to retrieve information about memory ranges that store the data environment for the encountering task. Multiple memory ranges may be used to store these data. The addr argument is a pointer to a void pointer return value to provide the start address of a memory range. The size argument is a pointer to a size type return value to provide the size of the memory range. The block argument, which is an integer value to specify the memory block of interest, supports iteration over the memory ranges. The get\_task\_memory entry point returns one if more memory ranges are available, and zero otherwise. If no memory is used for a task, size is set to zero. In this case, the value to which addr points is undefined.

## 36.17 get\_target\_info Entry Point

<table><tr><td>Name:get_target_infoCategory:function</td><td>Properties:async-signal-safe, C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device_num</td><td>c_uint64_t</td><td>pointer</td></tr><tr><td>target_id</td><td>id</td><td>OMPT, pointer</td></tr><tr><td>host_op_id</td><td>id</td><td>OMPT, pointer-to-pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_get\_target\_info\_t) (uint64\_t <sub>\*</sub>device\_num, ompt\_id\_t \*target\_id, ompt\_id\_t \*\*host\_op\_id);

C / C++

## Semantics

The get\_target\_info entry point, which has the get\_target\_info OMPT type, enables a tool to retrieve identifiers that specify the current target region and target operation ID of the encountering thread, if any. This entry point returns one if the encountering thread is in a target region and zero otherwise. If the entry point returns zero then the values of the variables passed by reference as its arguments are undefined. If the encountering thread is in a target region then get\_target\_info returns information about the current device, active target region, and active host operation, if any. In this case, the device\_num argument returns the device number of the target region and the target\_id argument returns the target region identifier. If the encountering thread is in the process of initiating an operation on a target device (for example, copying data to or from a device) then host\_op\_id returns the identifier for the operation; otherwise, host\_op\_id returns ompt\_id\_none.

## Restrictions

Restrictions on the get\_target\_info entry point are as follows:

• All arguments must be valid pointers to variables of the specified types.

## Cross References

• OMPT id Type, see Section 33.18

## 36.18 get\_num\_devices Entry Point

<table><tr><td>Name: get_num_devicesCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

C / C++

typedef int (<sub>\*</sub>ompt\_get\_num\_devices\_t) (void);

C / C++

## Semantics

The get\_num\_devices entry point, which has the get\_num\_devices OMPT type, is the entry point that enables a tool to retrieve the number of devices available to an OpenMP program.

## 36.19 get\_unique\_id Entry Point

<table><tr><td>Name: get_unique_idCategory: function</td><td>Properties: async-signal-safe, C/C++-only, OMPT</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_uint64_t</td><td>default</td></tr></table>

C / C++

typedef uint64\_t (<sub>\*</sub>ompt\_get\_unique\_id\_t) (void);

C / C++

## Semantics

The get\_unique\_id entry point, which has the get\_unique\_id OMPT type, enables a tool to retrieve a number that is unique for the duration of an OpenMP program. Successive invocations may not result in consecutive or even increasing numbers.

## 36.20 finalize\_tool Entry Point

<table><tr><td>Name: finalize_toolCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="2">Type SignatureC / C++typedef void (*ompt_finalize_tool_t) (void);C / C++</td></tr></table>

## Semantics

A tool may detect that the execution of an OpenMP program is ending before the OpenMP implementation does. To facilitate clean termination of the tool, the tool may invoke the finalize\_tool entry point, which has the finalize\_tool OMPT type. Upon completion of finalize\_tool, no OMPT callbacks are dispatched. The entry point detaches the tool from the runtime, unregisters all callbacks and invalidates all OMPT entry points passed to the tool by function\_lookup. Upon completion of finalize\_tool, no further callbacks will be issued on any thread. Before the callbacks are unregistered, the OpenMP runtime will dispatch all callbacks as if the program were exiting.

## Restrictions

Restrictions on the finalize\_tool entry point are as follows:

• The entry point must not be called from inside an explicit region.

• As finalize\_tool should only be called when a tool detects that the execution of an OpenMP program is ending, a thread encountering an explicit region after the entry point has completed results in unspecified behavior.
