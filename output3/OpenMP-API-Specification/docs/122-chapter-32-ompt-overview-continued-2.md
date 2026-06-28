Part IV

## OMPT

# 32 OMPT Overview

This chapter provides an overview of OMPT, which is an interface for first-party tools. First-party tools are linked or loaded directly into the OpenMP program. OMPT defines mechanisms to initialize a tool, to examine thread state associated with a thread, to interpret the call stack of a thread, to receive notification about events, to trace activity on target devices, to assess implementation-dependent details of an OpenMP implementation (such as supported states and mutual exclusion implementations), and to control a tool from an OpenMP program.

## 32.1 OMPT Interfaces Definitions

C / C++

A compliant implementation must supply a set of definitions for the OMPT runtime entry points, OMPT callback signatures, and the OMPT types. These definitions, which are listed throughout this and the immediately following chapters, and their associated declarations shall be provided in a header file named omp-tools.h. In addition, the set of definitions may specify other implementation defined values.

The ompt\_start\_tool procedure is an external function with C linkage.

C / C++

## 32.2 Activating a First-Party Tool

To activate a tool, an OpenMP implementation first determines whether the tool should be initialized. If so, the OpenMP implementation invokes the OMPT-tool initializer of the tool, which enables the tool to prepare to monitor execution on the host device. The tool may then also arrange to monitor computation that executes on target devices. This section explains how the tool and an OpenMP implementation interact to accomplish these activities.

## 32.2.1 ompt\_start\_tool Procedure

<table><tr><td>Name:empt_start_toolCategory:function</td><td>Properties:C-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>start_tool_result</td><td>pointer, OMPT</td></tr><tr><td>omp_version</td><td>integer</td><td>unsigned</td></tr><tr><td>runtime_version</td><td>char</td><td>intent(in), pointer</td></tr></table>

## Prototypes

ompt\_start\_tool\_result\_t <sub>\*</sub>ompt\_start\_tool( unsigned int omp\_version, const char \*runtime\_version);

C

## Semantics

For a tool to use the OMPT interface that an OpenMP implementation provides, the tool must define a globally-visible implementation of the ompt\_start\_tool procedure. The tool indicates that it will use the OMPT interface that an OpenMP implementation provides by returning a non-null pointer to a start\_tool\_result OMPT type structure from the

ompt\_start\_tool implementation that it provides. The start\_tool\_result structure contains pointers to initialize and finalize callbacks as well as a tool data word that an OpenMP implementation must pass by reference to these callbacks. A tool may return NULL from ompt\_start\_tool to indicate that it will not use the OMPT interface in a particular execution.

A tool may use the omp\_version argument to determine if it is compatible with the OMPT interface that the OpenMP implementation provides. The omp\_version argument is the value of the

\_OPENMP version macro associated with the OpenMP implementation. This value identifies the version that an implementation supports, which specifies the version of the OMPT interface that it supports. The runtime\_version argument is a version string that unambiguously identifies the OpenMP implementation.

If a tool returns a non-null pointer to a start\_tool\_result OMPT type structure, an OpenMP implementation will call the OMPT-tool initializer specified by the initialize field in this structure before beginning execution of any construct or completing execution of any routine; the OpenMP implementation will call the OMPT-tool finalizer specified by the finalize field in this structure when the OpenMP implementation shuts down.

## Restrictions

Restrictions to ompt\_start\_tool procedures are as follows:

• The runtime\_version argument must be an immutable string that is defined for the lifetime of a program execution.

## Cross References

• finalize Callback, see Section 34.1.2

• initialize Callback, see Section 34.1.1

• OMPT start\_tool\_result Type, see Section 33.30

## 32.2.2 Determining Whether to Initialize a First-Party Tool

![](images/cb114be944521e5a45d8edc4d21de270f5093fcb81ca93e63583ce5d6afc10b0.jpg)  
FIGURE 32.1: First-Party Tool Activation Flow Chart

An OpenMP implementation examines the tool-var ICV as one of its first initialization steps. If the value of tool-var is disabled, the initialization continues without a check for the presence of a tool and the functionality of the OMPT interface will be unavailable as the OpenMP program executes. In this case, the OMPT interface state remains OMPT inactive.

Otherwise, the OMPT interface state changes to OMPT pending and the OpenMP implementation activates any first-party tool that it finds. A tool can provide a definition of ompt\_start\_tool to an OpenMP implementation in three ways:

• By statically linking its definition of ompt\_start\_tool into an OpenMP program;

• By introducing a dynamically-linked library that includes its definition of ompt\_start\_tool into the address space of the program; or

• By providing, in the tool-libraries-var ICV, the name of a dynamically-linked library that is appropriate for the OpenMP architecture and operating system used by the OpenMP program and that includes a definition of ompt\_start\_tool.

If the value of tool-var is enabled, the OpenMP implementation must check if a tool has provided an implementation of ompt\_start\_tool. The OpenMP implementation first checks if a tool-provided implementation of ompt\_start\_tool is available in the address space, either statically-linked into the OpenMP program or in a dynamically-linked library loaded in the address space. If multiple implementations of ompt\_start\_tool are available, the implementation will use the first tool-provided implementation of ompt\_start\_tool that it finds.

If the implementation does not find a tool-provided implementation of ompt\_start\_tool in the address space, it consults the tool-libraries-var ICV, which contains a (possibly empty) list of dynamically-linked libraries. As described in detail in Section 4.5.2, the libraries in tool-libraries-var are then searched for the first usable implementation of ompt\_start\_tool that one of the libraries in the list provides.

If the implementation finds a tool-provided definition of ompt\_start\_tool, it invokes that procedure; if a NULL pointer is returned, the OMPT interface state remains OMPT pending and the implementation continues to look for implementations of ompt\_start\_tool; otherwise a non-null pointer to a start\_tool\_result OMPT type structure is returned, the OMPT interface state changes to OMPT active and the OpenMP implementation makes the OMPT interface available as the program executes. In this case, as the OpenMP implementation completes its initialization, it initializes the OMPT interface.

If no tool can be found, the OMPT interface state changes to OMPT inactive.

## Cross References

• tool-libraries-var ICV, see Table 3.1

• tool-var ICV, see Table 3.1

• ompt\_start\_tool Procedure, see Section 32.2.1

• OMPT start\_tool\_result Type, see Section 33.30

## 32.2.3 Initializing a First-Party Tool

To initialize the OMPT interface, the OpenMP implementation invokes the OMPT-tool initializer that is specified in the initialize field of the start\_tool\_result structure that ompt\_start\_tool returns. This initialize callback is invoked prior to the occurrence of any OpenMP event.

An initialize callback uses the entry point specified in its lookup argument to look up pointers to OMPT entry points that the OpenMP implementation provides; this process is described in Section 32.2.3.1. Typically, an OMPT-tool initializer obtains a pointer to the set\_callback entry point and then uses it to perform callback registration for events, as described in Section 32.2.4.

An OMPT-tool initializer may use the enumerate\_states entry point to determine the thread states that an OpenMP implementation employs. Similarly, it may use the

enumerate\_mutex\_impls entry point to determine the mutual exclusion implementations that the OpenMP implementation employs.

If an OMPT-tool initializer returns a non-zero value, the OMPT interface state remains OMPT active for the execution; otherwise, the OMPT interface state changes to OMPT inactive.

## Cross References

• enumerate\_mutex\_impls Entry Point, see Section 36.3

• enumerate\_states Entry Point, see Section 36.2

• Binding Entry Points, see Section 32.2.3.1

• initialize Callback, see Section 34.1.1

• ompt\_start\_tool Procedure, see Section 32.2.1

• set\_callback Entry Point, see Section 36.4

• OMPT start\_tool\_result Type, see Section 33.30

## 32.2.3.1 Binding Entry Points

Routines that an OpenMP implementation provides to support OMPT are not defined as global symbols. Instead, they are defined as runtime entry points that a tool can only identify through the value returned in the lookup argument of the initialize callback. A tool can use this function\_lookup entry point to obtain a pointer to each of the other entry points that an OpenMP implementation provides to support OMPT. Once a tool has obtained a function\_lookup entry point, it may employ it at any point in the future.

For each OMPT entry point for the host device, Table 32.1 provides the string name by which it is known and its associated type signature. Implementations can provide additional implementation defined names and corresponding entry points.

During initialization, a tool should look up each entry point by name and assign the entry point to a pointer that it maintains so it can later invoke that entry point. The entry points described in Table 32.1 enable a tool to assess the thread states and mutual exclusion implementations that an implementation supports for callback registration, to inspect registered callbacks, to introspect OpenMP state associated with threads, and to use tracing to monitor computations that execute on target devices.

## Cross References

• enumerate\_mutex\_impls Entry Point, see Section 36.3

• enumerate\_states Entry Point, see Section 36.2

• finalize\_tool Entry Point, see Section 36.20

• function\_lookup Entry Point, see Section 36.1

• get\_callback Entry Point, see Section 36.5

• get\_num\_devices Entry Point, see Section 36.18

• get\_num\_places Entry Point, see Section 36.8

• get\_num\_procs Entry Point, see Section 36.7

TABLE 32.1: OMPT Callback Interface Runtime Entry Point Names and Their Type Signatures  
```csv
Entry Point String Name
"ompt_enumerate_states"
"ompt_enumerate_mutex_impls"
"ompt_set_callback"
"ompt_get_callback"
"ompt_get_thread_data"
"ompt_get_num_places"
"ompt_get_place_proc_ids"
"ompt_get_place_num"
"ompt_get_partition_place_nums"
"ompt_get_proc_id"
"ompt_get_state"
"ompt_get_parallel_info"
"ompt_get_task_info"
"ompt_get_task_memory"
"ompt_get_num_devices"
"ompt_get_num_procs"
"ompt_get_target_info"
"ompt_get_unique_id"
"ompt_finalize_tool"
enumerate_states
enumerate_mutex_impls
set_callback
get_callback
get_thread_data
get_num_places
get_place_proc_ids
get_place_num
get_partition_place_nums
get_proc_id
get_state
get_parallel_info
get_task_info
get_task_memory
get_num_devices
get_num_procs
get_target_info
get_unique_id
finalize_tool
```

• get\_parallel\_info Entry Point, see Section 36.14

• get\_partition\_place\_nums Entry Point, see Section 36.11

• get\_place\_num Entry Point, see Section 36.10

• get\_place\_proc\_ids Entry Point, see Section 36.9

• get\_proc\_id Entry Point, see Section 36.12

• get\_state Entry Point, see Section 36.13

• get\_target\_info Entry Point, see Section 36.17

• get\_task\_info Entry Point, see Section 36.15

• get\_task\_memory Entry Point, see Section 36.16

• get\_thread\_data Entry Point, see Section 36.6

• get\_unique\_id Entry Point, see Section 36.19

• initialize Callback, see Section 34.1.1

• set\_callback Entry Point, see Section 36.4

TABLE 32.2: Callbacks for which set\_callback Must Return ompt\_set\_always  
```txt
Callback Name
thread_begin
thread_end
parallel_begin
parallel_end
task_create
task_schedule
implicit_task
target_data_op_emi
target_emi
target_submit_emi
control_tool
device_initialize
device_finalize
device_load
device_unload
error
```

## 32.2.4 Monitoring Activity on the Host with OMPT

To monitor the execution of an OpenMP program on the host device, an OMPT-tool initializer must register to receive notification of events that occur as an OpenMP program executes. A tool can use the set\_callback entry point to perform callback registrations for events. The return codes for set\_callback use the set\_result OMPT type. If the set\_callback entry point is called outside an initialize OMPT callback, callback registration may fail for supported callbacks with a return value of ompt\_set\_error. All registered callbacks and all callbacks returned by get\_callback use the callback OMPT type as a dummy type signature.

For callbacks listed in Table 32.2, ompt\_set\_always is the only registration return code that is allowed. An OpenMP implementation must guarantee that the callback will be invoked every time that a runtime event that is associated with it occurs. Support for such callbacks is required in a minimal implementation of the OMPT interface.

For any other callbacks not listed in Table 32.2, the set\_callback entry point may return any non-error code. Whether an OpenMP implementation invokes a registered callback never, sometimes, or always is implementation defined. If registration for a callback allows a return code of ompt\_set\_never, support for invoking such a callback may not be present in a minimal implementation of the OMPT interface. The return code from callback registration indicates the implementation defined level of support for the callback.

Two techniques reduce the size of the OMPT interface. First, in cases where events are naturally paired, for example the beginning and end of a region, and the arguments needed by the callback at each region endpoint are identical, a tool registers a single callback for the pair of events, with

ompt\_scope\_begin or ompt\_scope\_end provided as an argument to identify for which region endpoint the callback is invoked. Second, when a class of events is amenable to uniform treatment, OMPT provides a single callback for that class of events; for example, a sync\_region\_wait callback is used for multiple kinds of synchronization regions, such as barrier, taskwait, and taskgroup regions. Some events, for example, those that correspond to sync\_region\_wait, use both techniques.

## Cross References

• get\_callback Entry Point, see Section 36.5

• initialize Callback, see Section 34.1.1

• OMPT scope\_endpoint Type, see Section 33.27

• set\_callback Entry Point, see Section 36.4

• OMPT set\_result Type, see Section 33.28

## 32.2.5 Tracing Activity on Target Devices

A target device may not initialize a full OpenMP runtime system. Without one, using a tool interface based on callbacks to monitor activity on a device may incur unacceptable overhead. Thus, OMPT defines a monitoring interface for tracing activity on target devices. This section details the use of that interface.

First, to prepare to trace device activity, a tool must register a device\_initialize callback. A tool may also register a device\_load callback to be notified when code is loaded onto a target device or a device\_unload callback to be notified when code is unloaded from a target device. A tool may also optionally register a device\_finalize callback.

When an OpenMP implementation initializes a target device, it dispatches the

device\_initialize callback (the device initializer) of the tool on the host device. If the OpenMP implementation or target device does not support tracing, the OpenMP implementation passes NULL to the device initializer of the tool for its lookup argument; otherwise, the OpenMP implementation passes a pointer to a device-specific function\_lookup entry point to the device\_initialize callback of the tool.

If the lookup argument of the device\_initialize of the tool is a non-null pointer, the tool may use it to determine the entry points in the tracing interface that are available for the device and may bind the returned function pointers to tool variables. Table 32.3 lists the names of runtime entry points that may be available for a device; an implementation may provide additional implementation defined names and corresponding entry points. The driver for the device provides the entry points that enable a tool to control the trace collection interface of the device. The native trace format that the interface uses may be device-specific and the available kinds of trace records are implementation defined.

Some devices may allow a tool to collect trace records in a standard trace format known as OMPT trace records. Each OMPT trace record serves as a substitute for an OMPT callback that is not appropriate to be dispatched on the device. The fields in each trace record type are defined in the description of the callback that the record represents. If this type of record is provided then the function\_lookup entry point returns values for the entry points set\_trace\_ompt and get\_record\_ompt, which support collecting and decoding OMPT traces. If the native trace format for a device is the OMPT format then tracing can be controlled using the entry points for native or OMPT tracing.

TABLE 32.3: OMPT Tracing Interface Runtime Entry Point Names and Their Type Signatures  
```csv
Entry Point String Name OMPT Type
"empt_get_device_num_procs" get_device_num_procs
"empt_get_device_time" get_device_time
"empt_translate_time" translate_time
"empt_set_trace_empt" set_trace_empt
"empt_set_trace_native" set_trace_native
"empt_get_buffer_limits" get_buffer_limits
"empt_start_trace" start_trace
"empt_pause_trace" pause_trace
"empt_flush_trace" flush_trace
"empt_stop_trace" stop_trace
"empt_advance_buffer_cursor" advance_buffer_cursor
"empt_get_record_type" get_record_type
"empt_get_record_empt" get_record_empt
"empt_get_record_native" get_record_native
"empt_get_record_abstract" get_record_abstract
```

The tool uses the set\_trace\_native and/or the set\_trace\_ompt runtime entry point to specify what types of events or activities to monitor on the device. The return codes for set\_trace\_ompt and set\_trace\_native use the set\_result OMPT type. If the set\_trace\_native or the set\_trace\_ompt entry point is called outside a device initializer, registration of supported callbacks may fail with a return code of ompt\_set\_error. After specifying the events or activities to monitor, the tool initiates tracing of device activity by invoking the start\_trace entry point. Arguments to start\_trace include two tool callbacks through which the OpenMP implementation can manage traces associated with the device. The buffer\_request callback allocates a bufer in which trace records that correspond to device activity can be deposited. The buffer\_complete callback processes a bufer of trace records from the device.

If the OpenMP implementation requires a trace bufer for device activity, it invokes the tool-supplied callback on the host device to request a new bufer. The OpenMP implementation then monitors the execution of OpenMP constructs on the device and records a trace of events or activities into a trace bufer. If possible, device trace records are marked with a host\_op\_id — an identifier that associates device activities with the target device operation that the host device initiated to cause these activities.

To correlate activities on the host device with activities on a target device, a tool can register a target\_submit\_emi callback. Before and after the host device initiates creation of an initial task on a device associated with a structured block for a target construct, the OpenMP

implementation dispatches the target\_submit\_emi callback on the host device in the thread that is executing the encountering task of the target construct. This callback provides the tool with a pair of identifiers: one that identifies the target region and a second that uniquely identifies the initial task associated with that region. These identifiers help the tool correlate activities on the target device with their target region.

When appropriate, for example, when a trace bufer fills or needs to be flushed, the OpenMP implementation invokes the tool-supplied buffer\_complete callback to process a non-empty sequence of trace records in a trace bufer that is associated with the device. The

buffer\_complete callback may return immediately, ignoring records in the trace bufer, or it may iterate through them using the advance\_buffer\_cursor entry point to inspect each trace record.

A tool may use the get\_record\_type entry point to inspect the type of the trace record at the current cursor position. Three entry points (get\_record\_ompt, get\_record\_native, and get\_record\_abstract) allow tools to inspect the contents of some or all trace records in a trace bufer. The get\_record\_native entry point uses the native trace format of the device. The get\_record\_abstract entry point decodes the contents of a native trace record and summarizes them as a record\_abstract OMPT type record. The get\_record\_ompt entry point can only be used to retrieve trace records in OMPT format.

Once device tracing has been started, a tool may pause or resume device tracing at any time by invoking pause\_trace with an appropriate flag value as an argument. Further, a tool may invoke the flush\_trace entry point for a device at any time between device initialization and finalization to cause the pending trace records for that device to be flushed.

At any time, a tool may use the start\_trace entry point to start or the stop\_trace entry point to stop device tracing. When device tracing is stopped, the OpenMP implementation eventually gathers all trace records already collected from device tracing and presents them to the tool using the bufer-completion callback.

An OpenMP implementation can be shut down while device tracing is in progress. When an OpenMP implementation is shut down, it finalizes each device. Device finalization occurs in three steps. First, the OpenMP implementation halts any tracing in progress for the device. Second, the OpenMP implementation flushes all trace records collected for the device and uses the buffer\_complete callback associated with that device to present them to the tool. Finally, the OpenMP implementation dispatches any device\_finalize callback registered for the device.

## Cross References

• advance\_buffer\_cursor Entry Point, see Section 37.11

• buffer\_complete Callback, see Section 35.6

• buffer\_request Callback, see Section 35.5

• device\_finalize Callback, see Section 35.2

• device\_initialize Callback, see Section 35.1

• device\_load Callback, see Section 35.3

• device\_unload Callback, see Section 35.4

• flush\_trace Entry Point, see Section 37.9

• function\_lookup Entry Point, see Section 36.1

• get\_buffer\_limits Entry Point, see Section 37.6

• get\_device\_num\_procs Entry Point, see Section 37.1

• get\_device\_time Entry Point, see Section 37.2

• get\_record\_abstract Entry Point, see Section 37.15

• get\_record\_native Entry Point, see Section 37.14

• get\_record\_ompt Entry Point, see Section 37.13

• get\_record\_type Entry Point, see Section 37.12

• pause\_trace Entry Point, see Section 37.8

• OMPT record\_abstract Type, see Section 33.24

• OMPT set\_result Type, see Section 33.28

• set\_trace\_native Entry Point, see Section 37.5

• set\_trace\_ompt Entry Point, see Section 37.4

• start\_trace Entry Point, see Section 37.7

• stop\_trace Entry Point, see Section 37.10

• translate\_time Entry Point, see Section 37.3

## 32.3 Finalizing a First-Party Tool
