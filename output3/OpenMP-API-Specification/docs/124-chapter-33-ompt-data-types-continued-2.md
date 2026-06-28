} ompt\_record\_native\_t;

C / C++

## Semantics

The record\_native OMPT type indicates the integer codes that identify OMPT native trace record contents.

33.26 OMPT record\_ompt Type

<table><tr><td>Name: record_emptProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

<table><tr><td colspan="3">Fields</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>type</td><td>callbacks</td><td>C/C++-only, common-field, OMPT</td></tr><tr><td>time</td><td>device_time</td><td>C/C++-only, OMPT</td></tr><tr><td>thread_id</td><td>id</td><td>C/C++-only, OMPT</td></tr><tr><td>target_id</td><td>id</td><td>C/C++-only, OMPT</td></tr><tr><td>record</td><td>any_record_ompt</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

typedef struct ompt\_record\_ompt\_t { ompt\_callbacks\_t type; ompt\_device\_time\_t time; ompt\_id\_t thread\_id; ompt\_id\_t target\_id; ompt\_any\_record\_ompt\_t record; } ompt\_record\_ompt\_t;

C / C++

## C / C++

## Semantics

The record\_ompt OMPT type provides a complete trace record by specifying the common fields of the standard trace format along with a field that is an instance of the any\_record\_ompt OMPT type. The type field specifies the type of trace record that the structure provides. According to the type, event-specific information is stored in the matching record field.

## Restrictions

Restrictions to the record\_ompt OMPT type are as follows:

• If type is ompt\_callback\_thread\_end then the value of record is undefined.

## Cross References

• OMPT any\_record\_ompt Type, see Section 33.2

• OMPT callbacks Type, see Section 33.6

• OMPT device\_time Type, see Section 33.12

• OMPT id Type, see Section 33.18

## 33.27 OMPT scope\_endpoint Type

<table><tr><td>Name: scope_endpointProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_scope_begin</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_scope_end</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_scope_beginend</td><td>3</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

C / C++

typedef enum ompt\_scope\_endpoint\_t {

ompt\_scope\_begin = 1,

ompt\_scope\_end = 2,

ompt\_scope\_beginend = 3

} ompt\_scope\_endpoint\_t;

C / C++

## Summary

The scope\_endpoint OMPT type defines valid region endpoint values.

## 33.28 OMPT set\_result Type

<table><tr><td>Name: set_resultProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_set_error</td><td>0</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_set_never</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_set_impossible</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_set_sometimes</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_set_sometimes_paired</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_set_always</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum ompt_set_result_t {ompt_set_error = 0,ompt_set_never = 1,ompt_set_impossible = 2,ompt_set_sometimes = 3,ompt_set_sometimes_paired = 4,ompt_set_always = 5} ompt_set_result_t;</td></tr></table>

C / C++

## Summary

The set\_result OMPT type corresponds to values that the set\_callback,

possible outcomes. The ompt\_set\_error value indicates that the associated call failed.

Otherwise, the value indicates when an event may occur and, when appropriate, callback dispatch leads to the invocation of the callback. The ompt\_set\_never value indicates that the event will never occur or that the callback will never be invoked at runtime. The ompt\_set\_impossible value indicates that the event may occur but that tracing of it is not possible. The ompt\_set\_sometimes value indicates that the event may occur and, for an implementation defined subset of associated event occurrences, will be traced or the callback will be invoked at runtime. The ompt\_set\_sometimes\_paired value indicates the same result as ompt\_set\_sometimes and, in addition, that a callback with an endpoint value of ompt\_scope\_begin will be invoked if and only if the same callback with an endpoint value of ompt\_scope\_end will also be invoked sometime in the future. The ompt\_set\_always value indicates that, whenever an associated event occurs, it will be traced or the callback will be invoked.

## Cross References

• OMPT scope\_endpoint Type, see Section 33.27

• set\_callback Entry Point, see Section 36.4

• set\_trace\_native Entry Point, see Section 37.5

• set\_trace\_ompt Entry Point, see Section 37.4

## 33.29 OMPT severity Type

<table><tr><td>Name: severityProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_warning</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_fatal</td><td>2</td><td>C/C++-only, OMPT</td></tr></table>

Type Definition

<table><tr><td>typedef enum ompt_severity_t {</td></tr><tr><td>ompt_warning = 1,</td></tr><tr><td>ompt_fatal = 2</td></tr><tr><td>} ompt_severity_t;</td></tr></table>

C / C++

## Semantics

The severity OMPT type defines severity values.

## 33.30 OMPT start\_tool\_result Type

<table><tr><td>Name: start_tool_resultProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

## Fields

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>initialize</td><td>initialize</td><td>C/C++-only, OMPT</td></tr><tr><td>finalize</td><td>finalize</td><td>C/C++-only, OMPT</td></tr><tr><td>tool_data</td><td>data</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

typedef struct ompt\_start\_tool\_result\_t { ompt\_initialize\_t initialize; ompt\_finalize\_t finalize; ompt\_data\_t tool\_data; } ompt\_start\_tool\_result\_t;

## C / C++

## Semantics

The ompt\_start\_tool procedure returns a pointer to a structure of the

start\_tool\_result OMPT type, which provides pointers to the tool’s initialize and finalize callbacks as well as a data object for use by the tool.

## Restrictions

Restrictions to the start\_tool\_result OMPT type are as follows:

• The initialize and finalize callback pointer values in a start\_tool\_result structure that ompt\_start\_tool returns must be non-null values.

## Cross References

• OMPT data Type, see Section 33.8

• finalize Callback, see Section 34.1.2

• initialize Callback, see Section 34.1.1

• ompt\_start\_tool Procedure, see Section 32.2.1

## 33.31 OMPT state Type

<table><tr><td>Name: stateProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_state_work_serial</td><td>0x000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_work_parallel</td><td>0x001</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_work_reduction</td><td>0x002</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_work_free_agent</td><td>0x003</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_work_induction</td><td>0x004</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_barrier_implicit_parallel</td><td>0x011</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_barrier_implicit_workshare</td><td>0x012</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_barrier_explicit</td><td>0x014</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_barrier_implementation</td><td>0x015</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_barrier_teams</td><td>0x016</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_taskwait</td><td>0x020</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_taskgroup</td><td>0x021</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_mutex</td><td>0x040</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_lock</td><td>0x041</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_critical</td><td>0x042</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_atomic</td><td>0x043</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_ordered</td><td>0x044</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_target</td><td>0x080</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_target_map</td><td>0x081</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_wait_target_update</td><td>0x082</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_idle</td><td>0x100</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_overhead</td><td>0x101</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_state_undefined</td><td>0x102</td><td>C/C++-only, OMPT</td></tr></table>

<table><tr><td colspan="2">typedef enum ompt_state_t {</td></tr><tr><td>ompt_state_work_serial</td><td>= 0x000,</td></tr><tr><td>ompt_state_work_parallel</td><td>= 0x001,</td></tr><tr><td>ompt_state_work_reduction</td><td>= 0x002,</td></tr><tr><td>ompt_state_work_free_agent</td><td>= 0x003,</td></tr><tr><td>ompt_state_work_induction</td><td>= 0x004,</td></tr><tr><td>ompt_state_wait_barrier_implicit_parallel</td><td>= 0x011,</td></tr><tr><td>ompt_state_wait_barrier_implicit_workshare</td><td>= 0x012,</td></tr><tr><td>ompt_state_wait_barrier_explicit</td><td>= 0x014,</td></tr><tr><td>ompt_state_wait_barrier_implementation</td><td>= 0x015,</td></tr><tr><td>ompt_state_wait_barrier_teams</td><td>= 0x016,</td></tr><tr><td>ompt_state_wait_taskwait</td><td>= 0x020,</td></tr><tr><td>ompt_state_wait_taskgroup</td><td>= 0x021,</td></tr><tr><td>ompt_state_wait_mutex</td><td>= 0x040,</td></tr><tr><td>ompt_state_wait_lock</td><td>= 0x041,</td></tr></table>

ompt\_state\_wait\_critical = 0x042, ompt\_state\_wait\_atomic 0x043, ompt\_state\_wait\_ordered 0x044, ompt\_state\_wait\_target 0x080, ompt\_state\_wait\_target\_map 0x081, ompt\_state\_wait\_target\_update 0x082, ompt\_state\_idle = 0x100, ompt\_state\_overhead = 0x101, ompt\_state\_undefined = 0x102 } ompt\_state\_t;

## C / C++

## Semantics

The state OMPT type defines thread states that indicate the current activity of a thread. If the OMPT interface is in the active state then an OpenMP implementation must maintain thread state information for each thread. The thread state maintained is an approximation of the instantaneous state of a thread. A thread state must be one of the values of the state OMPT type or an implementation defined state value of 0x200 (512) or higher that extends the OMPT type.

A tool can query the OpenMP thread state at any time. If a tool queries the thread state of a native thread that is not associated with OpenMP then the implementation reports the state as ompt\_state\_undefined.

The ompt\_state\_work\_serial value indicates that the thread is executing code outside all parallel regions. The ompt\_state\_work\_parallel value indicates that the thread is executing code within the scope of a parallel region. The ompt\_state\_work\_reduction value indicates that the thread is combining partial reduction results from threads in its team. An OpenMP implementation may never report a thread in this state; a thread that is combining partial reduction results may have its state reported as ompt\_state\_work\_parallel or ompt\_state\_overhead. The ompt\_state\_work\_free\_agent value indicates that the thread is executing code within the scope of a task while not being assigned to the current team of that task. The ompt\_state\_wait\_barrier\_implicit\_parallel value indicates that the thread is waiting at the implicit barrier at the end of a parallel region. The ompt\_state\_wait\_barrier\_implicit\_workshare value indicates that the thread is waiting at an implicit barrier at the end of a worksharing construct. The ompt\_state\_wait\_barrier\_explicit value indicates that the thread is waiting in an explicit barrier region. The ompt\_state\_wait\_barrier\_implementation value indicates that the thread is waiting in a barrier that the OpenMP specification does not require but the implementation introduces. The ompt\_state\_wait\_barrier\_teams value indicates that the thread is waiting at a barrier at the end of a teams region. The value ompt\_state\_wait\_taskwait indicates that the thread is waiting at a taskwait construct. The ompt\_state\_wait\_taskgroup value indicates that the thread is waiting at the end of a taskgroup construct. The ompt\_state\_wait\_mutex value indicates that the thread is waiting for a mutex of an unspecified type. The ompt\_state\_wait\_lock value indicates that the thread is waiting for a lock or nestable lock. The ompt\_state\_wait\_critical value indicates that the thread is waiting to enter a critical region. The ompt\_state\_wait\_atomic value indicates that the thread is waiting to enter an atomic region. The ompt\_state\_wait\_ordered value indicates that the thread is waiting to enter an ordered region. The ompt\_state\_wait\_target value indicates that the thread is waiting for a target region to complete. The ompt\_state\_wait\_target\_map value indicates that the thread is waiting for a mapping operation to complete. An implementation may report ompt\_state\_wait\_target for target\_data constructs. The ompt\_state\_wait\_target\_update value indicates that the thread is waiting for a target\_update operation to complete. An implementation may report ompt\_state\_wait\_target for target\_update constructs. The ompt\_state\_idle value indicates that the native thread is an idle thread, that is, it is an unassigned thread that is not a free-agent thread. The ompt\_state\_overhead value indicates that the thread is in the overhead state at any point while executing within the OpenMP runtime, except while waiting at a synchronization point. The ompt\_state\_undefined value indicates that the native thread is not created by the OpenMP implementation.

## 33.32 OMPT subvolume Type

<table><tr><td colspan="2">Name: subvolumeProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: structure</td></tr><tr><td colspan="4">Fields</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>base</td><td colspan="2">c_ptr</td><td>C/C++-only, intent(in), value</td></tr><tr><td>size</td><td colspan="2">c_uint64_t</td><td>value</td></tr><tr><td>num_dims</td><td colspan="2">c_uint64_t</td><td>value, positive</td></tr><tr><td>volume</td><td colspan="2">c_uint64_t</td><td>C/C++-only, intent(in), pointer</td></tr><tr><td>offsets</td><td colspan="2">c_uint64_t</td><td>C/C++-only, intent(in), pointer</td></tr><tr><td>dimensions</td><td colspan="2">c_uint64_t</td><td>C/C++-only, intent(in), pointer</td></tr></table>

```c
typedef struct ompt_subvolume_t {
    const void *base;
    uint64_t size;
    uint64_t num_dims;
    const uint64_t *volume;
    const uint64_t *offsets;
```

C / C++

The subvolume OMPT type represents a rectangular subvolume used in a rectangular-memory-copying routine.

## Cross References

• Memory Copying Routines, see Section 25.7

## 33.33 OMPT sync\_region Type

<table><tr><td>Name: sync_regionProperties: C/C++-only, OMPT, overlapping-type-name</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_sync_region_barrier_explicit</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_barrier_implementation</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_taskwait</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_taskgroup</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_reduction</td><td>7</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_barrier_implicit_workshare</td><td>8</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_barrier_implicit_parallel</td><td>9</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_sync_region_barrier_teams</td><td>10</td><td>C/C++-only, OMPT</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum ompt_sync_region_t {ompt_sync_region_barrier_explicit = 3,ompt_sync_region_barrier_implementation = 4,ompt_sync_region_taskwait = 5,ompt_sync_region_taskgroup = 6,ompt_sync_region_reduction = 7,ompt_sync_region_barrier_implicit_workshare = 8,ompt_sync_region_barrier_implicit_parallel = 9,ompt_sync_region_barrier_teams = 10} ompt_sync_region_t;</td></tr></table>

The sync\_region OMPT type defines the valid synchronization region values.

33.34 OMPT target Type

<table><tr><td>Name: targetProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_target</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_enter_data</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_exit_data</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_update</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_nowait</td><td>9</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_enter_data_nowait</td><td>10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_exit_data_nowait</td><td>11</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_update_nowait</td><td>12</td><td>C/C++-only, OMPT</td></tr></table>

<table><tr><td colspan="2">typedef enum ompt_target_t {</td></tr><tr><td>ompt_target</td><td>= 1,</td></tr><tr><td>ompt_target_enter_data</td><td>= 2,</td></tr><tr><td>ompt_target_exit_data</td><td>= 3,</td></tr><tr><td>ompt_target_update</td><td>= 4,</td></tr><tr><td>ompt_target_nowait</td><td>= 9,</td></tr><tr><td>ompt_target_enter_data_nowait</td><td>= 10,</td></tr><tr><td>ompt_target_exit_data_nowait</td><td>= 11,</td></tr><tr><td>ompt_target_update_nowait</td><td>= 12</td></tr><tr><td colspan="2">} ompt_target_t;</td></tr></table>

## Semantics

The target OMPT type defines valid values to identify device constructs.

## 33.35 OMPT target\_data\_op Type

<table><tr><td>Name: target_data_opProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_target_data_alloc</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_delete</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_associate</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_disassociate</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_transfer</td><td>7</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_memset</td><td>8</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_transfer_rect</td><td>9</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_alloc_async</td><td>17</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_delete_async</td><td>20</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_transfer_async</td><td>23</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_memset_async</td><td>24</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_data_transfer_rect_async</td><td>25</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

## C / C++

typedef enum ompt\_target\_data\_op\_t { ompt\_target\_data\_alloc = 1, ompt\_target\_data\_delete = 4, ompt\_target\_data\_associate = 5, ompt\_target\_data\_disassociate = 6, ompt\_target\_data\_transfer = 7, ompt\_target\_data\_memset = 8, ompt\_target\_data\_transfer\_rect = 9, ompt\_target\_data\_alloc\_async = 17, ompt\_target\_data\_delete\_async = 20, ompt\_target\_data\_transfer\_async = 23, ompt\_target\_data\_memset\_async = 24, ompt\_target\_data\_transfer\_rect\_async = 25 } ompt\_target\_data\_op\_t;

## C / C++

## Additional information

The following instances and associated values of the target\_data\_op OMPT type are also defined: ompt\_target\_data\_transfer\_to\_device, with value 2;

ompt\_target\_data\_transfer\_from\_device, with value 3;

ompt\_target\_data\_transfer\_to\_device\_async, with value 18; and

ompt\_target\_data\_transfer\_from\_device, with value 19. These instances have been deprecated.

## Semantics

The target\_data\_op OMPT type indicates the kind of target data operation for target\_data\_op\_emi callbacks, which can be allocate (ompt\_target\_data\_alloc and ompt\_target\_data\_alloc\_async); delete (ompt\_target\_data\_delete and

```txt
typedef enum empt_target_map_flag_t {
    empt_target_map_flag_to          = 0x01,
    empt_target_map_flag_from       = 0x02,
    empt_target_map_flag_alloc     = 0x04,
    empt_target_map_flag_release   = 0x08,
    empt_target_map_flag_delete   = 0x10,
    empt_target_map_flag_implicit = 0x20,
    empt_target_map_flag_always   = 0x40,
    empt_target_map_flag_present   = 0x80,
    empt_target_map_flag_close      = 0x100,
    empt_target_map_flag_shared   = 0x200
} empt_target_map_flag_t;
```

```txt
ompt_target_data_delete_async); associate (ompt_target_data_associate);
disassociate (ompt_target_data_disassociate); transfer
(ompt_target_data_transfer, ompt_target_data_transfer_async,
ompt_target_data_transfer_rect, and
ompt_target_data_transfer_rect_async); or memset
(ompt_target_data_memset and ompt_target_data_memset_async), where the
values that end with _async correspond to asynchronous data operations.
```

## 33.36 OMPT target\_map\_flag Type

<table><tr><td>Name: target_map_flagProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_target_map_flag_to</td><td>0x01</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_from</td><td>0x02</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_alloc</td><td>0x04</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_release</td><td>0x08</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_delete</td><td>0x10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_implicit</td><td>0x20</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_always</td><td>0x40</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_present</td><td>0x80</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_close</td><td>0x100</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_target_map_flag_shared</td><td>0x200</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

## Semantics

The target\_map\_flag OMPT type defines the valid map flag values. The ompt\_target\_map\_flag\_to, ompt\_target\_map\_flag\_from,

ompt\_target\_map\_flag\_alloc, and ompt\_target\_map\_flag\_release values are set when the mapping operations have the corresponding map-type. If the map-type for the mapping operations is tofrom, both the ompt\_target\_map\_flag\_to and ompt\_target\_map\_flag\_from values are set. The ompt\_target\_map\_flag\_implicit value is set if the mapping operations correspond to implicitly determined data-mapping attributes. The ompt\_target\_map\_flag\_delete, ompt\_target\_map\_flag\_always, ompt\_target\_map\_flag\_present, and ompt\_target\_map\_flag\_close, values are set if the mapping operations are specified with the corresponding map-type-modifier modifiers. The ompt\_target\_map\_flag\_shared value is set if the original storage and corresponding storage are shared for the mapping operation.

## 33.37 OMPT task\_flag Type

<table><tr><td>Name: task_flagProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_task_initial</td><td>0x00000001</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_implicit</td><td>0x00000002</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_explicit</td><td>0x00000004</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_target</td><td>0x00000008</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_taskwait</td><td>0x00000010</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_importing</td><td>0x02000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_exporting</td><td>0x04000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_undeferred</td><td>0x08000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_untied</td><td>0x10000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_final</td><td>0x20000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_mergeable</td><td>0x40000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_merged</td><td>0x80000000</td><td>C/C++-only, OMPT</td></tr><tr><td>Name: task_statusProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_task_complete</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_yield</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_cancel</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_detach</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_early_fulfill</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_late_fulfill</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_task_switch</td><td>7</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_taskwait_complete</td><td>8</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

<table><tr><td colspan="2">typedef enum empt_task_flag_t {</td></tr><tr><td>empt_task_initial</td><td>= 0x00000001,</td></tr><tr><td>empt_task_implicit</td><td>= 0x00000002,</td></tr><tr><td>empt_task_explicit</td><td>= 0x00000004,</td></tr><tr><td>empt_task_target</td><td>= 0x00000008,</td></tr><tr><td>empt_task_taskwait</td><td>= 0x00000010,</td></tr><tr><td>empt_task_importing</td><td>= 0x02000000,</td></tr><tr><td>empt_task_exporting</td><td>= 0x04000000,</td></tr><tr><td>empt_task_undeferred</td><td>= 0x08000000,</td></tr><tr><td>empt_task_untied</td><td>= 0x10000000,</td></tr><tr><td>empt_task_final</td><td>= 0x20000000,</td></tr><tr><td>empt_task_mergeable</td><td>= 0x40000000,</td></tr><tr><td>empt_task_merged</td><td>= 0x80000000</td></tr><tr><td colspan="2">} empt_task_flag_t;</td></tr></table>

## Semantics

The task\_flag OMPT type defines valid task values. The least significant byte provides information about the general classification of the task. The other bits represent its properties.

## 33.38 OMPT task\_status Type

## Semantics

The task\_status OMPT type indicates the reason that a task was switched when it reached a task scheduling point. The ompt\_task\_complete value indicates that the task that encountered the task scheduling point completed execution of its associated structured block and any associated allow-completion event was fulfilled. The ompt\_task\_yield value indicates that the task encountered a taskyield construct. The ompt\_task\_cancel value indicates that the task was canceled when it encountered an active cancellation point. The ompt\_task\_detach value indicates that a task for which the detach clause was specified completed execution of the associated structured block and is waiting for an allow-completion event to be fulfilled. The ompt\_task\_early\_fulfill value indicates that the allow-completion event of the task was fulfilled before the task completed execution of the associated structured block. The ompt\_task\_late\_fulfill value indicates that the allow-completion event of the task was fulfilled after the task completed execution of the associated structured block. The ompt\_taskwait\_complete value indicates completion of the dependent task that results from a taskwait construct with one or more depend clauses. The ompt\_task\_switch value is used for all other cases that a task was switched.

## 33.39 OMPT thread Type

<table><tr><td>Name: threadProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_thread_initial</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_thread_worker</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_thread_other</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_thread_unknown</td><td>4</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

C / C++

ompt\_thread\_initial = 1,

ompt\_thread\_worker = 2,

ompt\_thread\_other = 3,

ompt\_thread\_unknown = 4

} ompt\_thread\_t;

C / C++

## Semantics

The thread OMPT type defines the valid thread type values. Any initial thread has thread type ompt\_thread\_initial. All threads that are thread-pool-worker threads have thread type ompt\_thread\_worker. A native thread that an OpenMP implementation uses but that does not execute user code has thread type ompt\_thread\_other. Any native thread that is created outside an OpenMP implementation and that is not an initial thread has thread type ompt\_thread\_unknown.

## 33.40 OMPT wait\_id Type

<table><tr><td>Name: wait_idProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: c_uint64_t</td></tr><tr><td colspan="3">Predefined Identifiers</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_wait_id_none</td><td>0</td><td>C/C++-only, OMPT</td></tr><tr><td colspan="3">Type DefinitionC / C+mtypedef uint64_t ompt_wait_id_t;C / C++</td></tr></table>

## Semantics

The wait\_id OMPT type describes wait identifiers for a thread; each thread maintains one of these wait identifiers. When a task that a thread executes is waiting for mutual exclusion, the wait identifier of the thread indicates the reason that the thread is waiting. A wait identifier may represent the name argument of a critical section, or a lock, or a variable accessed in an atomic region, or a synchronization object that is internal to an OpenMP implementation. When a thread is not in a wait state then the value of the wait identifier of the thread is undefined.

33.41 OMPT work Type

<table><tr><td>Name: workProperties: C/C++-only, OMPT, overlapping-type-name</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_work_loop</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_sections</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_single_executor</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_single_other</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_workshare</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_distribute</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_taskloop</td><td>7</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_scope</td><td>8</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_workdistribute</td><td>9</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_loop_static</td><td>10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_loop_dynamic</td><td>11</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_loop_guided</td><td>12</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_work_loop_other</td><td>13</td><td>C/C++-only, OMPT</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum ompt_work_t {ompt_work_loop = 1,ompt_work_sections = 2,ompt_work_single_executor = 3,ompt_work_single_other = 4,ompt_work_workshare = 5,ompt_work_distribute = 6,ompt_work_taskloop = 7,ompt_work_scope = 8,ompt_work_workdistribute = 9,ompt_work_loop_static = 10,ompt_work_loop_dynamic = 11,ompt_work_loop_guided = 12,ompt_work_loop_other = 13} ompt_work_t;</td></tr></table>

The work OMPT type defines the valid work values.
