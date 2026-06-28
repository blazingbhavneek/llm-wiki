
If the OMPT interface state is OMPT active, the OMPT-tool finalizer, which is a finalize callback and is specified by the finalize field in the start\_tool\_result OMPT type structure returned from the ompt\_start\_tool procedure, is called when the OpenMP implementation shuts down.

## Cross References

• finalize Callback, see Section 34.1.2

• ompt\_start\_tool Procedure, see Section 32.2.1

• OMPT start\_tool\_result Type, see Section 33.30

# 33 OMPT Data Types

This chapter specifies OMPT types that the omp-tools.h C/C++ header file defines.

C / C++

## 33.1 OMPT Predefined Identifiers

Predefined Identifiers

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_addr_none</td><td>~0</td><td>default</td></tr><tr><td>ompt_mutex_impl_none</td><td>0</td><td>default</td></tr></table>

In addition to the predefined identifiers of OMPT type that are defined with their corresponding OMPT type, the OpenMP API includes the predefined identifiers shown above. The ompt\_addr\_none void \* predefined identifier indicates that no address on the relevant device is available. The ompt\_mutex\_impl\_none predefined identifier indicates an invalid mutex implementation.

C / C++

## 33.2 OMPT any\_record\_ompt Type

<table><tr><td>Name: any_record_emptProperties: C/C++-only, OMPT</td><td>Base Type: union</td></tr></table>

Fields

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_begin</td><td>thread_begin</td><td>C/C++-only</td></tr><tr><td>parallel_begin</td><td>parallel_begin</td><td>C/C++-only</td></tr><tr><td>parallel_end</td><td>parallel_end</td><td>C/C++-only</td></tr><tr><td>work</td><td>work</td><td>C/C++-only</td></tr><tr><td>dispatch</td><td>dispatch</td><td>C/C++-only</td></tr><tr><td>task_create</td><td>task_create</td><td>C/C++-only</td></tr><tr><td>dependencies</td><td>dependencies</td><td>C/C++-only</td></tr><tr><td>task_dependence</td><td>task_dependence</td><td>C/C++-only</td></tr><tr><td>task_schedule</td><td>task_schedule</td><td>C/C++-only</td></tr><tr><td>implicit_task</td><td>implicit_task</td><td>C/C++-only</td></tr><tr><td>masked</td><td>masked</td><td>C/C++-only</td></tr><tr><td>sync_region</td><td>sync_region</td><td>C/C++-only</td></tr><tr><td>mutex_acquire</td><td>mutex_acquire</td><td>C/C++-only</td></tr><tr><td>mutex</td><td>mutex</td><td>C/C++-only</td></tr><tr><td>nest_lock</td><td>nest_lock</td><td>C/C++-only</td></tr><tr><td>flush</td><td>flush</td><td>C/C++-only</td></tr><tr><td>cancel</td><td>cancel</td><td>C/C++-only</td></tr><tr><td>target_emi</td><td>target_emi</td><td>C/C++-only</td></tr><tr><td>target_data_op_emi</td><td>target_data_op_emi</td><td>C/C++-only</td></tr><tr><td>target_map_emi</td><td>target_map_emi</td><td>C/C++-only</td></tr><tr><td>target_submit_emi</td><td>target_submit_emi</td><td>C/C++-only</td></tr><tr><td>control_tool</td><td>control_tool</td><td>C/C++-only</td></tr><tr><td>error</td><td>error</td><td>C/C++-only</td></tr></table>

C / C++ typedef union ompt\_any\_record\_ompt\_t { ompt\_record\_thread\_begin\_t thread\_begin; ompt\_record\_parallel\_begin\_t parallel\_begin; ompt\_record\_parallel\_end\_t parallel\_end; ompt\_record\_work\_t work; ompt\_record\_dispatch\_t dispatch; ompt\_record\_task\_create\_t task\_create; ompt\_record\_dependences\_t dependences; ompt\_record\_task\_dependence\_t task\_dependence; ompt\_record\_task\_schedule\_t task\_schedule; ompt\_record\_implicit\_task\_t implicit\_task; ompt\_record\_masked\_t masked; ompt\_record\_sync\_region\_t sync\_region; ompt\_record\_mutex\_acquire\_t mutex\_acquire; ompt\_record\_mutex\_t mutex;

ompt\_record\_nest\_lock\_t nest\_lock; ompt\_record\_flush\_t flush; ompt\_record\_cancel\_t cancel; ompt\_record\_target\_emi\_t target\_emi; ompt\_record\_target\_data\_op\_emi\_t target\_data\_op\_emi; ompt\_record\_target\_map\_emi\_t target\_map\_emi; ompt\_record\_target\_submit\_emi\_t target\_submit\_emi; ompt\_record\_control\_tool\_t control\_tool; ompt\_record\_error\_t error; } ompt\_any\_record\_ompt\_t;

C / C++

## Additional information

The union also includes target, taget\_data\_op, target\_kernel, and target\_map fields with corresponding trace record OMPT types. These fields have been deprecated.

## Semantics

The any\_record\_ompt OMPT type is a union of all standard trace format event-specific trace record OMPT types that is the type of the record field of the record\_ompt OMPT type.

## Cross References

• OMPT record\_ompt Type, see Section 33.26

## 33.3 OMPT buffer Type

<table><tr><td>Name: bufferProperties: C/C++-only, OMPT, opaque</td><td>Base Type: void</td></tr></table>

typedef void ompt\_buffer\_t;

C / C++

C / C++

## Semantics

The buffer OMPT type represents a handle for a device bufer.

## 33.4 OMPT buffer\_cursor Type

<table><tr><td>Name: buffer_cursorProperties: C/C++-only, OMPT, opaque</td><td>Base Type: c_uint64_t</td></tr></table>

Type Definition

C / C++

typedef uint64\_t ompt\_buffer\_cursor\_t;

C / C++

3 Summary

The buffer\_cursor OMPT type represents a handle for a position in a device bufer.

## 33.5 OMPT callback Type

<table><tr><td>Name: callbackCategory: subroutine pointer</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_t) (void);

C / C++

## Semantics

Pointers to OMPT callbacks with diferent type signatures are passed to the set\_callback entry point and returned by the get\_callback entry point. For convenience, these entry points require all type signatures to be cast to the callback OMPT type.

## 33.6 OMPT callbacks Type

<table><tr><td>Name: callbacksProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_callback_thread_begin</td><td>1</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_thread_end</td><td>2</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_parallel_begin</td><td>3</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_parallel_end</td><td>4</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_task_create</td><td>5</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_task_schedule</td><td>6</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_implicit_task</td><td>7</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_control_tool</td><td>11</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_device_initialize</td><td>12</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_device_finalize</td><td>13</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_device_load</td><td>14</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_device_unload</td><td>15</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_sync_region_wait</td><td>16</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_mutex_released</td><td>17</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_dependencies</td><td>18</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_task_dependence</td><td>19</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_work</td><td>20</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_masked</td><td>21</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_sync_region</td><td>23</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_lock_init</td><td>24</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_lock_destroy</td><td>25</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_mutex_acquire</td><td>26</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_mutex_acquired</td><td>27</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_nest_lock</td><td>28</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_flush</td><td>29</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_cancel</td><td>30</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_reduction</td><td>31</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_dispatch</td><td>32</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_target_emi</td><td>33</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_target_data_op_emi</td><td>34</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_target_submit_emi</td><td>35</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_target_map_emi</td><td>36</td><td>C-only, OMPT</td></tr><tr><td>ompt_callback_error</td><td>37</td><td>C-only, OMPT</td></tr></table>

```c
ompt_callback_task_create          = 5,
    ompt_callback_task_schedule         = 6,
    ompt_callback_implicit_task       = 7,
    ompt_callback_control_tool        = 11,
    ompt_callback_device_initialize      = 12,
    ompt_callback_device_finalize       = 13,
    ompt_callback_device_load          = 14,
    ompt_callback_device_unload       = 15,
    ompt_callback_sync_region_wait      = 16,
    ompt_callback_mutex_released     = 17,
    ompt_callback_dependencies           = 18,
    ompt_callback_task_dependence      = 19,
    ompt_callback_work                = 20,
    ompt_callback_masked             = 21,
    ompt_callback_sync_region        = 23,
    ompt_callback_lock_init            = 24,
    ompt_callback_lock_destroy       = 25,
    ompt_callback_mutex_acquire       = 26,
    ompt_callback_mutex_acquired      = 27,
    ompt_callback_nest_lock              = 28,
    ompt_callback_flush               = 29,
    ompt_callback_cancel              = 30,
    ompt_callback_reduction          = 31,
    ompt_callback_dispatch            = 32,
    ompt_callback_target_emi          = 33,
    ompt_callback_target_data_op_emi   = 34,
    ompt_callback_target_submit_emi   = 35,
    ompt_callback_target_map_emi       = 36,
    ompt_callback_error              = 37
} ompt_callbacks_t;
```

## Additional information

The following instances and associated values of the callbacks OMPT type are also defined: ompt\_callback\_target, with value 8; ompt\_callback\_target\_data\_op, with value 9; ompt\_callback\_target\_submit, with value 10; and ompt\_callback\_target\_map, with value 22. These instances have been deprecated.

## Semantics

The callbacks OMPT type provides codes that identify OMPT callbacks when registering or querying them.

33.7 OMPT cancel\_flag Type

<table><tr><td>Name: cancel_flagProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_cancel_parallel</td><td>0x01</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_sections</td><td>0x02</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_loop</td><td>0x04</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_taskgroup</td><td>0x08</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_activated</td><td>0x10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_detected</td><td>0x20</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_cancel_discarded_task</td><td>0x40</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

<table><tr><td colspan="2">typedef enum empt_cancel_flag_t {</td></tr><tr><td>empt_cancel_parallel</td><td>= 0x01,</td></tr><tr><td>empt_cancel_sections</td><td>= 0x02,</td></tr><tr><td>empt_cancel_loop</td><td>= 0x04,</td></tr><tr><td>empt_cancel_taskgroup</td><td>= 0x08,</td></tr><tr><td>empt_cancel_activated</td><td>= 0x10,</td></tr><tr><td>empt_cancel_detected</td><td>= 0x20,</td></tr><tr><td>empt_cancel_discarded_task</td><td>= 0x40</td></tr><tr><td colspan="2">} empt_cancel_flag_t;</td></tr></table>

## Semantics

The cancel\_flag OMPT type defines cancel flag values.

## 33.8 OMPT data Type

<table><tr><td>Name: dataProperties: C/C++-only, OMPT</td><td>Base Type: union</td></tr></table>

<table><tr><td colspan="3">Fields</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>value</td><td>c_uint64_t</td><td>default</td></tr><tr><td>ptr</td><td>void</td><td>C/C++-only, pointer</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_data_none</td><td>0</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

C / C++

} ompt\_data\_t;

C / C++

## Semantics

The data OMPT type represents data that is reserved for tool use. When an OpenMP implementation creates a thread or an instance of a parallel region, teams region, task region, or device region, it initializes the associated data object with the value ompt\_data\_none.

## 33.9 OMPT dependence Type

<table><tr><td>Name: dependenceProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>variable</td><td>data</td><td>C/C++-only</td></tr><tr><td>dependence_type</td><td>dependence_type</td><td>C/C++-only</td></tr></table>

## Type Definition

C / C++

typedef struct ompt\_dependence\_t {

ompt\_data\_t variable;

ompt\_dependence\_type\_t dependence\_type;

} ompt\_dependence\_t;

C / C++

## Semantics

The dependence OMPT type represents a dependence in a structure that holds information about a depend or doacross clause. For task dependences, the ptr field of its variable field points to the storage location of the dependence. For doacross dependences, the value field of the variable field contains the value of a vector element that describes the dependence. The dependence\_type field indicates the type of the dependence. For task dependences with the reserved locator omp\_all\_memory, the value of the variable field is undefined and the dependence\_type field contains a value that has the \_all\_memory sufix.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT dependence\_type Type, see Section 33.10

<table><tr><td colspan="2">typedef enum ompt_dependence_type_t {</td></tr><tr><td>ompt_dependence_type_in</td><td>= 1,</td></tr><tr><td>ompt_dependence_type_out</td><td>= 2,</td></tr><tr><td>ompt_dependence_type_inout</td><td>= 3,</td></tr><tr><td>ompt_dependence_type_mutexinoutset</td><td>= 4,</td></tr><tr><td>ompt_dependence_type_source</td><td>= 5,</td></tr><tr><td>ompt_dependence_type_sink</td><td>= 6,</td></tr><tr><td>ompt_dependence_type_inoutset</td><td>= 7,</td></tr><tr><td>ompt_dependence_type_out_all_memory</td><td>= 34,</td></tr><tr><td>ompt_dependence_type_inout_all_memory</td><td>= 35</td></tr><tr><td colspan="2">} ompt_dependence_type_t;</td></tr></table>

## 33.10 OMPT dependence\_type Type

<table><tr><td>Name: dependence_typeProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_dependence_type_in</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_out</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_inout</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_mutexinoutset</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_source</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_sink</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_inoutset</td><td>7</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_out_all_memory</td><td>34</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dependence_type_inout_all_memory</td><td>35</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

## C / C++

## C / C++

## Semantics

The dependence\_type OMPT type defines task dependence type values. The ompt\_dependence\_type\_in, ompt\_dependence\_type\_out, ompt\_dependence\_type\_inout, ompt\_dependence\_type\_mutexinoutset, ompt\_dependence\_type\_inoutset, ompt\_dependence\_type\_out\_all\_memory, and ompt\_dependence\_type\_inout\_all\_memory values represent the task dependence type present in a depend clause while the ompt\_dependence\_type\_source and ompt\_dependence\_type\_sink values represent the dependence-type present in a doacross clause. The ompt\_dependence\_type\_out\_all\_memory and ompt\_dependence\_type\_inout\_all\_memory represent task dependences for which the omp\_all\_memory reserved locator is specified.

## 33.11 OMPT device Type

<table><tr><td>Name: deviceProperties: C/C++-only, OMPT, opaque</td><td>Base Type: void</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef void ompt_device_t;C / C++</td></tr></table>

## Semantics

The device OMPT type represents a device.

## 33.12 OMPT device\_time Type

<table><tr><td>Name: device_timeProperties: C/C++-only, OMPT, opaque</td><td>Base Type: c_uint64_t</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_time_none</td><td>0</td><td>C/C++-only, OMPT</td></tr></table>

C / C++

typedef uint64\_t ompt\_device\_time\_t;

C / C++

## Semantics

The device\_time OMPT type represents raw device time values; ompt\_time\_none represents an unknown or unspecified time.

## 33.13 OMPT dispatch Type

<table><tr><td>Name: dispatchProperties: C/C++-only, OMPT, overlapping-type-name</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_dispatch_iteration</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dispatch_section</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dispatch_ws_loop_chunk</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dispatch_taskloop_chunk</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_dispatch_distribute_chunk</td><td>5</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

<table><tr><td colspan="2">typedef enum empt_dispatch_t {</td></tr><tr><td>empt_dispatch_iteration</td><td>= 1,</td></tr><tr><td>empt_dispatch_section</td><td>= 2,</td></tr><tr><td>empt_dispatch_ws_loop_chunk</td><td>= 3,</td></tr><tr><td>empt_dispatch_taskloop_chunk</td><td>= 4,</td></tr><tr><td>empt_dispatch_distribute_chunk</td><td>= 5</td></tr><tr><td colspan="2">} empt_dispatch_t;</td></tr></table>

## Semantics

The dispatch OMPT type defines the valid dispatch values.

## 33.14 OMPT dispatch\_chunk Type

<table><tr><td>Name: dispatch_chunkProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>start</td><td>c_uint64_t</td><td>default</td></tr><tr><td>iterations</td><td>c_uint64_t</td><td>default</td></tr></table>

## Type Definition

typedef struct ompt\_dispatch\_chunk\_t {

## Semantics

The dispatch\_chunk OMPT type represents chunk information for a dispatched chunk. The start field specifies the first logical iteration of the chunk and the iterations field specifies the number of logical iterations in the chunk. Whether the chunk of a taskloop region is contiguous is implementation defined.

## 33.15 OMPT frame Type

<table><tr><td>Name: frameProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>exit_frame</td><td>data</td><td>C/C++-only, OMPT</td></tr><tr><td>enter_frame</td><td>data</td><td>C/C++-only, OMPT</td></tr><tr><td>exit_frame_flags</td><td>integer</td><td>default</td></tr><tr><td>enter_frame_flags</td><td>integer</td><td>default</td></tr></table>

```txt
typedef struct ompt_frame_t {
    ompt_data_t exit_frame;
    ompt_data_t enter_frame;
    int exit_frame_flags;
    int enter_frame_flags;
} ompt_frame_t;
```

## Semantics

The frame OMPT type describes procedure frame information for a task. Each frame object is associated with the task to which the procedure frames belong. Every task that is not a merged task with one or more frames on the stack of a native thread, whether an initial task, an implicit task, an explicit task, or a target task, has an associated frame object.

The exit\_frame field contains information to identify the first procedure frame executing the task region. The exit\_frame for the frame object associated with the initial task that is not nested inside any OpenMP construct is ompt\_data\_none. The enter\_frame field contains information to identify the latest still active procedure frame executing the task region before entering the OpenMP runtime implementation or before executing a diferent task. If a task with frames on the stack is not executing implementation code in the OpenMP runtime, the value of enter\_frame for its associated frame object is ompt\_data\_none.

For the frame indicated by exit\_frame (enter\_frame), the exit\_frame\_flags (enter\_frame\_flags) field indicates that the provided frame information points to a runtime or an OpenMP program frame address. The same fields also specify the kind of information that is provided to identify the frame, These fields are a disjunction of values in the frame\_flag OMPT type.

The lifetime of a frame object begins when a task is created and ends when the task is destroyed. Tools should not assume that a frame structure remains at a constant location in memory throughout the lifetime of the task. A pointer to a frame object is passed to some callbacks; a pointer to the frame object of a task can also be retrieved by a tool at any time, including in a signal handler, by invoking the get\_task\_info entry point. A pointer to a frame object that a tool retrieved is valid as long as the tool does not pass back control to the OpenMP implementation.

Note – A monitoring tool that uses asynchronous sampling can observe values of exit\_frame and enter\_frame at inconvenient times. Tools must be prepared to handle frame objects observed just prior to when their field values will be set or cleared.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT frame\_flag Type, see Section 33.16

• get\_task\_info Entry Point, see Section 36.15

## 33.16 OMPT frame\_flag Type

<table><tr><td>Name: frame_flagProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_frame_runtime</td><td>0x00</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_frame_application</td><td>0x01</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_frame_cfa</td><td>0x10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_frame_framepointer</td><td>0x20</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_frame_stackaddress</td><td>0x30</td><td>C/C++-only, OMPT</td></tr></table>

<table><tr><td colspan="2">typedef enum ompt_frame_flag_t {</td></tr><tr><td>ompt_frame_runtime</td><td>= 0x00,</td></tr><tr><td>ompt_frame_application</td><td>= 0x01,</td></tr><tr><td>ompt_frame_cfa</td><td>= 0x10,</td></tr><tr><td>ompt_frame_framepointer</td><td>= 0x20,</td></tr></table>

<table><tr><td>ompt_frame_stackaddress = 0x30} ompt_frame_flag_t;</td></tr></table>

Type Definition

## Semantics

The frame\_flag OMPT type defines frame information flags. The ompt\_frame\_runtime value indicates that a frame address is a procedure frame in the OpenMP runtime implementation. The ompt\_frame\_application value indicates that a frame address is a procedure frame in the OpenMP program. Higher order bits indicate the specific information for a particular frame pointer. The ompt\_frame\_cfa value indicates that a frame address specifies a canonical frame address. The ompt\_frame\_framepointer value indicates that a frame address provides the value of the frame pointer register. The ompt\_frame\_stackaddress value indicates that a frame address specifies a pointer address that is contained in the current stack frame.

## 33.17 OMPT hwid Type

<table><tr><td>Name: hwidProperties: C/C++-only, OMPT</td><td>Base Type: c_uint64_t</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_hwid_none</td><td>0</td><td>C/C++-only, OMPT</td></tr></table>

C / C++

typedef uint64\_t ompt\_hwid\_t;

C / C++

## Semantics

The hwid OMPT type is a handle for a hardware identifier for a target device; ompt\_hwid\_none represents an unknown or unspecified hardware identifier. If no specific value for the hwid field is associated with an instance of the record\_abstract OMPT type then the value of hwid is ompt\_hwid\_none.

## Cross References

• OMPT record\_abstract Type, see Section 33.24

## 33.18 OMPT id Type

<table><tr><td>Name: idProperties: C/C++-only, OMPT</td><td>Base Type: c_uint64_t</td></tr></table>

<table><tr><td colspan="3">Predefined Identifiers</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_id_none</td><td>0</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

C / C++

typedef uint64\_t ompt\_id\_t;

C / C++

## Semantics

The id OMPT type is used to provide various identifiers to tools; ompt\_id\_none is used when the specific ID is unknown or unavailable. When tracing asynchronous activity on devices, identifiers enable tools to correlate device regions and operations that the host device initiates with associated activities on a target device. In addition, OMPT provides identifiers to refer to parallel regions and tasks that execute on a device.

## Restrictions

Restrictions to the id OMPT type are as follows:

• Identifiers created on each device must be unique from the time an OpenMP implementation is initialized until it is shut down. Identifiers for each device region and target data operation instance that the host device initiates must be unique over time on the host device. Identifiers for instances of parallel regions and task regions that execute on a device must be unique over time within that device.

## 33.19 OMPT interface\_fn Type

<table><tr><td>Name: interface_fnCategory: subroutine pointer</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="2">Type SignatureC / C++typedef void (*ompt_interface_fn_t) (void);C / C++</td></tr></table>

## Semantics

The interface\_fn OMPT type serves as a generic function pointer that the function\_lookup entry point returns to provide access to a tool to entry points by name.

## 33.20 OMPT mutex Type

<table><tr><td>Name: mutexProperties: C/C++-only, OMPT, overlapping-type-name</td><td>Base Type: enumeration</td></tr><tr><td>Type Definition</td><td>C / C++</td></tr><tr><td>typedef enum ompt_mutex_t {</td><td></td></tr><tr><td>ompt_mutex_lock</td><td>= 1,</td></tr><tr><td>ompt_mutex_test_lock</td><td>= 2,</td></tr><tr><td>ompt_mutex_nest_lock</td><td>= 3,</td></tr><tr><td>ompt_mutex_test_nest_lock</td><td>= 4,</td></tr><tr><td>ompt_mutex_critical</td><td>= 5,</td></tr><tr><td>ompt_mutex_atomic</td><td>= 6,</td></tr><tr><td>ompt_mutex_ordered</td><td>= 7</td></tr><tr><td>} ompt_mutex_t;</td><td></td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_mutex_lock</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_test_lock</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_nest_lock</td><td>3</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_test_nest_lock</td><td>4</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_critical</td><td>5</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_atomic</td><td>6</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_mutex_ordered</td><td>7</td><td>C/C++-only, OMPT</td></tr></table>

## Semantics

The mutex OMPT type defines the valid mutex values.

## 33.21 OMPT native\_mon\_flag Type

<table><tr><td>Name: native_mon_flagProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_native_data_motion_explicit</td><td>0x01</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_data_motion_implicit</td><td>0x02</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_kernel_invocation</td><td>0x04</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_kernel_execution</td><td>0x08</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_driver</td><td>0x10</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_runtime</td><td>0x20</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_overhead</td><td>0x40</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_native_idleness</td><td>0x80</td><td>C/C++-only, OMPT</td></tr></table>

```c
typedef enum ompt_native_mon_flag_t {
    ompt_native_data_motion_explicit = 0x01,
    ompt_native_data_motion_implicit = 0x02,
    ompt_native_kernel_invocation = 0x04,
    ompt_native_kernel_execution = 0x08,
    ompt_native_driver = 0x10,
    ompt_native_runtime = 0x20,
    ompt_native_overhead = 0x40,
    ompt_native_idleness = 0x80
} ompt_native_mon_flag_t;
```

<table><tr><td>Name: parallel_flagProperties: C/C++-only, OMPT</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_parallel_invoker_program</td><td>0x00000001</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_parallel_invoker_runtime</td><td>0x00000002</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_parallel_league</td><td>0x40000000</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_parallel_team</td><td>0x80000000</td><td>C/C++-only, OMPT</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum ompt_parallel_flag_t {ompt_parallel_invoker_program = 0x00000001,ompt_parallel_invoker_runtime = 0x00000002,ompt_parallel_league = 0x40000000,ompt_parallel_team = 0x80000000} ompt_parallel_flag_t;</td></tr></table>

## Semantics

The native\_mon\_flag OMPT type defines the valid native monitoring flag values.

## 33.22 OMPT parallel\_flag Type

## Semantics

The parallel\_flag OMPT type defines valid invoker values, which indicate how the code that implements the associated structured block of the region is invoked or encountered. The ompt\_parallel\_invoker\_program value indicates that the encountering thread for a parallel or teams region executes code to implement its associated structured block as if directly invoked or encountered in application code. The

ompt\_parallel\_invoker\_runtime value indicates that the encountering thread for a parallel or teams region invokes the code that implements its associated structured block from the runtime. The ompt\_parallel\_league value indicates that the callback is invoked due to the creation of a league of teams by a teams construct. The ompt\_parallel\_team value indicates that the callback is invoked due to the creation of a team of threads by a parallel construct.

## 33.23 OMPT record Type

<table><tr><td>Name: recordProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_record_empt</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_record_native</td><td>2</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_record_invalid</td><td>3</td><td>C/C++-only, OMPT</td></tr></table>

<table><tr><td>typedef enum empt_record_t {</td><td>C / C++</td></tr><tr><td>empt_record_empt = 1,</td><td></td></tr><tr><td>empt_record_native = 2,</td><td></td></tr><tr><td>empt_record_invalid = 3</td><td></td></tr><tr><td>} empt_record_t;</td><td></td></tr></table>

## Semantics

The record OMPT type indicates the integer codes that identify OMPT trace record formats.

## 33.24 OMPT record\_abstract Type

<table><tr><td>Name: record_abstractProperties: C/C++-only, OMPT</td><td>Base Type: structure</td></tr></table>

## Fields

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>rclass</td><td>record_native</td><td>C/C++-only, OMPT</td></tr><tr><td>type</td><td>char</td><td>common-field, intent(in), pointer</td></tr><tr><td>start_time</td><td>device_time</td><td>C/C++-only, OMPT</td></tr><tr><td>end_time</td><td>device_time</td><td>C/C++-only, OMPT</td></tr><tr><td>hwid</td><td>hwid</td><td>C/C++-only, OMPT</td></tr></table>

## Type Definition

typedef struct ompt\_record\_abstract\_t { ompt\_record\_native\_t rclass; const char <sub>\*</sub>type; ompt\_device\_time\_t start\_time; ompt\_device\_time\_t end\_time; ompt\_hwid\_t hwid; } ompt\_record\_abstract\_t;

## C / C++

## Semantics

The record\_abstract OMPT type is an abstract trace record format that summarizes native trace records. It contains information that a tool can use to process a native trace record that it may not fully understand. The rclass field indicates that the trace record is informational or that it represents an event; this information can help a tool determine how to present the trace record. The type field points to a statically-allocated, immutable character string that provides a meaningful name that a tool can use to describe the event. The start\_time and end\_time fields are used to place an event in time. The times are relative to the device clock. If an event does not have an associated start\_time (end\_time), the value of the start\_time (end\_time) field is ompt\_time\_none. The hardware identifier field, hwid, indicates the location on the device where the event occurred. A hwid may represent a hardware abstraction such as a core or a hardware thread identifier. The meaning of a hwid value for a device is implementation defined. If no hardware abstraction is associated with the trace record then the value of hwid is ompt\_hwid\_none.

## Cross References

• OMPT device\_time Type, see Section 33.12

• OMPT hwid Type, see Section 33.17

• OMPT record\_native Type, see Section 33.25

33.25 OMPT record\_native Type

<table><tr><td>Name: record_nativeProperties: C/C++-only, OMPT</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>ompt_record_native_info</td><td>1</td><td>C/C++-only, OMPT</td></tr><tr><td>ompt_record_native_event</td><td>2</td><td>C/C++-only, OMPT</td></tr></table>

Type Definition

C / C++

typedef enum ompt\_record\_native\_t {

ompt\_record\_native\_info = 1,
