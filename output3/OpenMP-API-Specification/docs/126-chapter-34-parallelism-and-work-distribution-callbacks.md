typedef struct ompt\_record\_error\_t {

ompt\_severity\_t severity;

const char <sub>\*</sub>message;

size\_t length;

const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_error\_t;

C / C++

## Semantics

A tool provides an error callback, which has the error OMPT type, that the OpenMP implementation dispatches when an error directive is encountered for which the action-time argument of the at clause is specified as execution. The severity argument passes the specified severity level. The message argument passes the C string from the message clause. The length argument provides the length of the C string.

Cross References

• error Directive, see Section 10.1

• OMPT severity Type, see Section 33.29

## 34.3 Parallelism Generation Callback Signatures

This section describes callbacks that are related to constructs for generating and controlling parallelism.

34.3.1 parallel\_begin Callback

<table><tr><td>Name: parallel_beginCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>encountering_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>encountering_task_frame</td><td>frame</td><td>intent(in), OMPT, pointer, untraced-argument</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>requested_parallelism</td><td>integer</td><td>unsigned</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_parallel\_begin\_t) ( ompt\_data\_t \*encountering\_task\_data, const ompt\_frame\_t \*encountering\_task\_frame, ompt\_data\_t \*parallel\_data, unsigned int requested\_parallelism, int flags, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_parallel\_begin\_t {

ompt\_id\_t encountering\_task\_id;

ompt\_id\_t parallel\_id;

unsigned int requested\_parallelism;

const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_parallel\_begin\_t;

C / C++

## Semantics

A tool provides a parallel\_begin callback, which has the parallel\_begin OMPT type, that the OpenMP implementation dispatches when a parallel or teams region starts. The requested\_parallelism argument indicates the number of threads or teams that the user requested. The flags argument indicates whether the code for the region is inlined into the application or invoked by the runtime and also whether the region is a parallel or teams region. Valid values for flags are a disjunction of elements in the parallel\_flag OMPT type.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT frame Type, see Section 33.15

• OMPT id Type, see Section 33.18

• parallel Construct, see Section 12.1

• OMPT parallel\_flag Type, see Section 33.22

• teams Construct, see Section 12.2

## 34.3.2 parallel\_end Callback

<table><tr><td>Name: parallel_endCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>encountering_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_parallel\_end\_t) ( ompt\_data\_t \*parallel\_data, ompt\_data\_t \*encountering\_task\_data, int flags, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_parallel\_end\_t {

ompt\_id\_t parallel\_id;

ompt\_id\_t encountering\_task\_id;

int flags;

const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_parallel\_end\_t;

C / C++

## Semantics

A tool provides a parallel\_end callback, which has the parallel\_end OMPT type, that the OpenMP implementation dispatches when a parallel or teams region ends. The flags

argument indicates whether the code for the region is inlined into the application or invoked by the runtime and also whether the region is a parallel or teams region. Valid values for flags are a disjunction of elements in the parallel\_flag OMPT type.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

• parallel Construct, see Section 12.1

• OMPT parallel\_flag Type, see Section 33.22

• teams Construct, see Section 12.2

## 34.3.3 masked Callback

<table><tr><td>Name: maskedCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_masked\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_data\_t <sub>\*</sub>parallel\_data, ompt\_data\_t <sub>\*</sub>task\_data, const void <sub>\*</sub>codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_masked\_t { ompt\_scope\_endpoint\_t endpoint; ompt\_id\_t parallel\_id; ompt\_id\_t task\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_masked\_t;

C / C++

## Semantics

26 A tool provides a masked callback, which has the masked OMPT type, that the OpenMP 27 implementation dispatches for masked regions.

## Cross References

• OMPT data Type, see Section 33.8

• masked Construct, see Section 12.5

• OMPT id Type, see Section 33.18

• OMPT scope\_endpoint Type, see Section 33.27

## 34.4 Work Distribution Callback Signatures

This section describes callbacks that are related to work-distribution constructs.

## 34.4.1 work Callback

<table><tr><td colspan="2">Name: workCategory: subroutine</td><td>Properties: C/C++-only, OMPT, overlapping-type-name</td></tr><tr><td colspan="3">Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>work_type</td><td>work</td><td>OMPT, overlapping-type-name</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>count</td><td>c_uint64_t</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr><tr><td colspan="3">Type SignatureC / C++typedef void (*empt_callback_work_t) (empt_work_t work_type,empt_scope_endpoint_t endpoint,empt_data_t *parallel_data,empt_data_t *task_data, uint64_t count, const void *codeptr_ra);C / C++Trace RecordC / C++typedef struct empt_record_work_t {empt_work_t work_type;empt_scope_endpoint_t endpoint;empt_id_t parallel_id;empt_id_t task_id;uint64_t count;const void *codeptr_ra;}empt_record_work_t;</td></tr></table>

## Semantics

A tool provides a work callback, which has the work OMPT type, that the OpenMP implementation dispatches for worksharing regions and taskloop regions. The work\_type argument indicates the kind of region. The count argument is a measure of the quantity of work involved in the construct. For a worksharing-loop construct or taskloop construct, count represents the number of collapsed iterations. For a sections construct, count represents the number of sections. For a workshare or workdistribute construct, count represents the units of work, as defined by the workshare or workdistribute construct. For a single or scope construct, count is always 1. When the endpoint argument signals the end of a region, a count value of 0 indicates that the actual count value is not available.

## Cross References

• OMPT data Type, see Section 33.8

• Work-Distribution Constructs, see Chapter 13

• OMPT id Type, see Section 33.18

• OMPT scope\_endpoint Type, see Section 33.27

• taskloop Construct, see Section 14.2

• OMPT work Type, see Section 33.41

## 34.4.2 dispatch Callback

<table><tr><td>Name: dispatchCategory: subroutine</td><td>Properties: C/C++-only, OMPT, overlapping-type-name</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td> $parallel\_data$ </td><td>data</td><td>OMPT, pointer</td></tr><tr><td> $task\_data$ </td><td>data</td><td>OMPT, pointer</td></tr><tr><td>kind</td><td>dispatch</td><td>OMPT, overlapping-type-name</td></tr><tr><td>instance</td><td>data</td><td>OMPT</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_dispatch\_t) ( ompt\_data\_t \*parallel\_data, ompt\_data\_t \*task\_data, ompt\_dispatch\_t kind, ompt\_data\_t instance);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_dispatch\_t { ompt\_id\_t parallel\_id; ompt\_id\_t task\_id; ompt\_dispatch\_t kind; ompt\_id\_t instance; } ompt\_record\_dispatch\_t;

## C / C++

## Semantics

A tool provides a dispatch callback, which has the dispatch OMPT type (which has an overlapping type name with the dispatch OMPT type that applies to the kind argument of the callback), that the OpenMP implementation dispatches when a thread begins to execute a section or a collapsed iteration. The kind argument indicates whether a collapsed iteration or a section is being dispatched. If the kind argument is ompt\_dispatch\_iteration, the value field of the instance argument contains the logical iteration number. If the kind argument is ompt\_dispatch\_section, the ptr field of the instance argument contains a code address that identifies the structured block. In cases where a routine implements the structured block associated with this callback, the ptr field of the instance argument contains the return address of the call to the routine. In cases where the implementation of the structured block is inlined, the ptr field of the instance argument contains the return address of the invocation of this callback. If the kind argument is ompt\_dispatch\_ws\_loop\_chunk, ompt\_dispatch\_taskloop\_chunk or ompt\_dispatch\_distribute\_chunk, the ptr field of the instance argument points to a structure of type dispatch\_chunk that contains the information for the chunk.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT dispatch Type, see Section 33.13

• OMPT dispatch\_chunk Type, see Section 33.14

• Worksharing-Loop Constructs, see Section 13.6

• OMPT id Type, see Section 33.18

• sections Construct, see Section 13.3

• taskloop Construct, see Section 14.2

# 34.5 Tasking Callback Signatures
