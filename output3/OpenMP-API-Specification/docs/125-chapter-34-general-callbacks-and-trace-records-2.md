## 34 General Callbacks and Trace Records

This chapter describes general OMPT callbacks that an OMPT tool may register and that are called during the runtime of an OpenMP program. The C/C++ header file (omp-tools.h) provides the types that this chapter defines. Tool implementations of callbacks are not required to be async signal safe.

Several OMPT callbacks include a codeptr\_ra argument that relates the implementation of an OpenMP region to its source code. If a routine implements the region associated with a callback then codeptr\_ra contains the return address of the call to that routine. If the implementation of the region is inlined then codeptr\_ra contains the return address of the callback invocation. If attribution to source code is impossible or inappropriate, codeptr\_ra may be NULL.

Several OMPT callbacks have a flags argument; the meaning and valid values for that argument is described with the callback. Some callbacks have an encountering\_task\_frame argument that points to the frame object that is associated with the encountering task. The behavior for accessing the frame object after the callback returns is unspecified. Some callbacks have a tool\_data argument that is a pointer to the tool\_data field in the start\_tool\_result structure that

ompt\_start\_tool returned. Some callbacks have a parallel\_data argument; the binding of these arguments is the parallel or teams region that is beginning or ending or the current parallel region for callbacks that are dispatched during the execution of one. Some callbacks have an encountering\_task\_data argument; the binding of these arguments is the encountering task. Some callbacks have an endpoint argument that indicates whether the callback signals that a region begins or ends. Some callbacks have a wait\_id argument, which indicates the object being awaited. Several OMPT callbacks have a task\_data argument; unless otherwise specified, the binding of these arguments is the encountering task of the event for which the implementation dispatches the callback. For some of those callbacks, OpenMP semantics imply that this task to which the task\_data argument binds is the implicit task that executes the structured block of the binding parallel region or teams region.

An implementation may also provide a trace of events per device. Along with the callbacks, this chapter also defines standard trace records. For these trace records, unless otherwise specified, tool data arguments are replaced by an ID, which must be initialized by the OpenMP implementation. Each of parallel\_id, task\_id, and thread\_id must be unique per target region. If the target\_emi callback is dispatched, the target\_id used in any trace records associated with the device region is given by the value field of the target\_data data object that is set in the callback.

## Restrictions

Restrictions to OpenMP tool callbacks are as follows:

• Tool callbacks may not use directives or call any routines.

• Tool callbacks must exit by either returning to the caller or aborting.

## 34.1 Initialization and Finalization Callbacks

This section describes callbacks that are called to initialize and to finalize tools and when native threads are initialized and finalized.

## 34.1.1 initialize Callback

<table><tr><td>Name: initializeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>lookup</td><td>function_lookup</td><td>OMPT</td></tr><tr><td>initial_device_num</td><td>integer</td><td>default</td></tr><tr><td>tool_data</td><td>data</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_initialize\_t) (ompt\_function\_lookup\_t lookup, int initial\_device\_num, ompt\_data\_t \*tool\_data);

C / C++

## Semantics

A tool provides an initialize callback, which has the initialize OMPT type, in the non-null pointer to a start\_tool\_result OMPT type structure that its implementation of ompt\_start\_tool returns. An OpenMP implementation must call this OMPT-tool initializer after fully initializing itself but before beginning execution of any construct or routine. An initialize callback returns a non-zero value if it succeeds; otherwise, the OMPT interface state changes to OMPT inactive as described in Section 32.2.3.

The lookup argument of an initialize callback is a pointer to a runtime entry point that a tool must use to obtain pointers to the other entry points in the OMPT interface. The initial\_device\_num argument provides the value that a call to omp\_get\_initial\_device would return.

C / C++

A callback of initialize OMPT type is a callback of type ompt\_initialize\_t.

C / C++

## Cross References

• OMPT data Type, see Section 33.8

• omp\_get\_initial\_device Routine, see Section 24.10

• ompt\_start\_tool Procedure, see Section 32.2.1

• OMPT start\_tool\_result Type, see Section 33.30

## 34.1.2 finalize Callback

<table><tr><td>Name: finalizeCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>tool_data</td><td>data</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_finalize\_t) (ompt\_data\_t <sub>\*</sub>tool\_data);

C / C++

## Semantics

A tool provides a finalize callback, which has the finalize OMPT type, in the non-null pointer to a start\_tool\_result OMPT type structure that its implementation of ompt\_start\_tool returns. An OpenMP implementation must call this OMPT-tool finalizer after the last OMPT event as the OpenMP implementation shuts down.

C / C++

A callback of finalize OMPT type is a callback of type ompt\_finalize\_t.

C / C++

## Cross References

• OMPT data Type, see Section 33.8

• ompt\_start\_tool Procedure, see Section 32.2.1

• OMPT start\_tool\_result Type, see Section 33.30

## 34.1.3 thread\_begin Callback

<table><tr><td>Name: thread_beginCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_type</td><td>thread</td><td>OMPT</td></tr><tr><td>thread_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_thread\_begin\_t) ( ompt\_thread\_t thread\_type, ompt\_data\_t <sub>\*</sub>thread\_data);

## Trace Record

C / C++

typedef struct ompt\_record\_thread\_begin\_t {

ompt\_thread\_t thread\_type;

} ompt\_record\_thread\_begin\_t;

C / C++

## Semantics

A tool provides a thread\_begin callback, which has the thread\_begin OMPT type, that the OpenMP implementation dispatches when native threads are created. The thread\_type argument indicates the type of the new thread: initial, worker, other, or unknown. The binding of the thread\_data argument is the new thread.

Cross References

• OMPT data Type, see Section 33.8

• OMPT thread Type, see Section 33.39

## 34.1.4 thread\_end Callback

<table><tr><td>Name: thread_endCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_data</td><td>data</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_thread\_end\_t) ( ompt\_data\_t <sub>\*</sub>thread\_data);

C / C++

## Semantics

A tool provides a thread\_end callback, which has the thread\_end OMPT type, that the OpenMP implementation dispatches when native threads are destroyed. The binding of the thread\_data argument is the thread that will be destroyed.

## Cross References

• OMPT data Type, see Section 33.8

## 34.2 error Callback

<table><tr><td>Name: errorCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>severity</td><td>severity</td><td>OMPT</td></tr><tr><td>message</td><td>char</td><td>intent(in), pointer</td></tr><tr><td>length</td><td>size_t</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_error\_t) (ompt\_severity\_t severity, const char <sub>\*</sub>message, size\_t length, const void <sub>\*</sub>codeptr\_ra);

C / C++

## Trace Record

C / C++
