## 37 Device Tracing Entry Points

The second set of OMPT entry points enables a tool to trace activities on a device. When directed by the tracing interface, an OpenMP implementation will trace activities on a device, collect bufers of trace records, and invoke callbacks on the host device to process these trace records. This chapter defines that set of entry points.

Several OMPT entry points have a device argument. This argument is a pointer to an OpenMP object that represents the target device. Callbacks in the device tracing interface use a pointer to this device object to identify the device being addressed.

## 37.1 get\_device\_num\_procs Entry Point

<table><tr><td>Name: get_device_num_procsCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

C / C++

C / C++

## Semantics

The get\_device\_num\_procs entry point, which has the get\_device\_num\_procs OMPT type, enables a tool to retrieve the number of processors that are available on the device at the time the entry point is called. This value may change between the time that it is determined and the time that it is read in the calling context due to system actions outside the control of the OpenMP implementation.

## Cross References

• OMPT device Type, see Section 33.11

## 37.2 get\_device\_time Entry Point

Type Signature

<table><tr><td>Name: get_device_timeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>device_time</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

typedef ompt\_device\_time\_t (<sub>\*</sub>ompt\_get\_device\_time\_t) ( ompt\_device\_t <sub>\*</sub>device);

C / C++

## Semantics

Host devices and target devices are typically distinct and run independently. If the host device and any target devices are diferent hardware components, they may use diferent clock generators. For this reason, a common time base for ordering host-side and device-side events may not be available. The get\_device\_time entry point, which has the get\_device\_time OMPT type, enables a tool to retrieve the current time on the device specified by the device argument. A tool can use the information retrieved by get\_device\_time to align time stamps from diferent devices.

## Cross References

• OMPT device Type, see Section 33.11

• OMPT device\_time Type, see Section 33.12

## 37.3 translate\_time Entry Point

<table><tr><td>Name: translate_timeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>double</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>time</td><td>device_time</td><td>OMPT</td></tr></table>

Type Signature

C / C++

typedef double (<sub>\*</sub>ompt\_translate\_time\_t) (ompt\_device\_t <sub>\*</sub>device, ompt\_device\_time\_t time);

## Semantics

The translate\_time entry point, which has the translate\_time OMPT type, enables a tool to translate a time value, specified by the time argument, obtained from the device specified by the device argument to a corresponding time value on the host device. The returned value for the host time has the same meaning as the value returned from omp\_get\_wtime.

Cross References

• OMPT device Type, see Section 33.11

• OMPT device\_time Type, see Section 33.12

• omp\_get\_wtime Routine, see Section 30.3.1

## 37.4 set\_trace\_ompt Entry Point

<table><tr><td>Name: set_trace_omptCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>set_result</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>enable</td><td>integer</td><td>OMPT, unsigned</td></tr><tr><td>etype</td><td>integer</td><td>OMPT, unsigned</td></tr></table>

## Type Signature

C / C++

typedef ompt\_set\_result\_t (<sub>\*</sub>ompt\_set\_trace\_ompt\_t) ( ompt\_device\_t <sub>\*</sub>device, unsigned int enable, unsigned int etype);

C / C++

## Semantics

A tool uses the set\_trace\_ompt entry point, which has the set\_trace\_ompt OMPT type, to enable or to disable the recording of standard trace records for one or more types of events that the etype argument indicates. If the value of etype is zero then the invocation applies to all events. If etype is positive then it applies to the event in the callbacks OMPT type that matches that value. The enable argument indicates whether tracing should be enabled or disabled for the events that etype specifies; a positive value indicates that recording should be enabled while a value of zero indicates that recording should be disabled. If etype specifies any of the events that correspond to the target\_data\_op\_emi or target\_submit\_emi callbacks then tracing, if supported, is enabled or disabled for those events when they occur on the host device. If etype specifies any other events then tracing, if supported, is enabled or disabled for those events when they occur on the specified target device. The return value of set\_trace\_ompt indicates the outcome of enabling or disabling the recording of the trace records and can be any value in the set\_result OMPT type except ompt\_set\_sometimes\_paired.

## Cross References

• OMPT callbacks Type, see Section 33.6

• OMPT device Type, see Section 33.11

• Tracing Activity on Target Devices, see Section 32.2.5

• OMPT set\_result Type, see Section 33.28

## 37.5 set\_trace\_native Entry Point

<table><tr><td>Name: set_trace_nativeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>set_result</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>enable</td><td>integer</td><td>default</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef ompt\_set\_result\_t (<sub>\*</sub>ompt\_set\_trace\_native\_t) ( ompt\_device\_t <sub>\*</sub>device, int enable, int flags);

C / C++

## Semantics

A tool uses the set\_trace\_native entry point, which has the set\_trace\_native OMPT type, to enable or to disable the recording of native trace records. The enable argument indicates whether this invocation should enable or disable recording of events. The flags argument specifies the kinds of native device monitoring to enable or to disable. Each kind of monitoring is specified by a flag bit. Flags can be composed by using logical or to combine enumeration values of the native\_mon\_flag OMPT type. The return value of set\_trace\_native indicates the outcome of enabling or disabling the recording of the trace records and can be any value in the set\_result OMPT type except ompt\_set\_sometimes\_paired.

This interface is designed for use by a tool that cannot directly use native control procedures for the device. If a tool can directly use the native control procedures then it can invoke them directly using pointers that the function\_lookup entry point associated with the device provides and that are described in the documentation string that is provided to its device\_initialize callback.

## Cross References

• OMPT device Type, see Section 33.11

• Tracing Activity on Target Devices, see Section 32.2.5

• OMPT native\_mon\_flag Type, see Section 33.21

• OMPT set\_result Type, see Section 33.28

## 37.6 get\_buffer\_limits Entry Point

<table><tr><td>Name: get_buffer_limitsCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>max_concurrent_allocs</td><td>integer</td><td>pointer</td></tr><tr><td>recommended_bytes</td><td>size_t</td><td>pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_get\_buffer\_limits\_t) (ompt\_device\_t <sub>\*</sub>device, int \*max\_concurrent\_allocs, size\_t \*recommended\_bytes);

C / C++

## Semantics

The get\_buffer\_limits entry point, which has the get\_buffer\_limits OMPT type, enables a tool to retrieve the maximum number of concurrent bufer allocations and the recommended size of any bufer allocation that will be requested of the tool for a specified device. The max\_concurrent\_allocs points to a location in which the entry point returns the maximum number of bufer allocations that the implementation may request for tracing activity on the target device without the implementation performing callback dispatch of buffer\_complete callbacks with its bufer\_owned argument set to a non-zero value for any of the bufers. The recommended\_bytes argument points to a location in which the entry point returns the recommended bufer size of the bufer to be returned by the tool when the implementation dispatches a buffer\_request callback for the target device.

A tool may use this entry point prior to a call to the start\_trace entry point to determine the total size of the bufers that the implementation would need for tracing activity on the device at any given time. The limits that this entry point returns remain the same on each successive invocation unless the stop\_trace entry point is called for the same target device between the successive invocations.

## Cross References

• buffer\_complete Callback, see Section 35.6

• buffer\_request Callback, see Section 35.5

• OMPT device Type, see Section 33.11

• start\_trace Entry Point, see Section 37.7

• stop\_trace Entry Point, see Section 37.10

## 37.7 start\_trace Entry Point

<table><tr><td>Name: start_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>request</td><td>buffer_request</td><td>OMPT, procedure</td></tr><tr><td>complete</td><td>buffer_complete</td><td>OMPT, procedure</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_start\_trace\_t) (ompt\_device\_t <sub>\*</sub>device, ompt\_callback\_buffer\_request\_t request, ompt\_callback\_buffer\_complete\_t complete);

C / C++

## Semantics

The start\_trace entry point, which has the start\_trace OMPT type, enables a tool to start tracing of activity on a specified device. The request argument specifies a callback that supplies a bufer in which a device can deposit events. The complete argument specifies a callback that the OpenMP implementation invokes to empty a bufer that contains trace records.

Under normal operating conditions, every event bufer that a tool callback provides for a device is returned to the tool before the OpenMP runtime shuts down. If an exceptional condition terminates execution of an OpenMP program, the runtime may not return bufers provided for the device. An invocation of start\_trace returns one if the entry point succeeds and zero otherwise.

## Cross References

• buffer\_complete Callback, see Section 35.6

• buffer\_request Callback, see Section 35.5

• OMPT device Type, see Section 33.11

## 37.8 pause\_trace Entry Point

<table><tr><td>Name: pause_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>begin_pause</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_pause\_trace\_t) (ompt\_device\_t <sub>\*</sub>device, int begin\_pause);

C / C++

## Semantics

The pause\_trace entry point, which has the pause\_trace OMPT type, enables a tool to pause or to resume tracing on a device. The begin\_pause argument indicates whether to pause or to resume tracing. To resume tracing, zero should be supplied for begin\_pause; to pause tracing, any other value should be supplied. An invocation of pause\_trace returns one if it succeeds and zero otherwise. Redundant pause or resume commands are idempotent and will return the same value as the prior command.

## Cross References

• OMPT device Type, see Section 33.11

## 37.9 flush\_trace Entry Point

<table><tr><td>Name: flush_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_flush\_trace\_t) (ompt\_device\_t <sub>\*</sub>device);

C / C++

## Semantics

The flush\_trace entry point, which has the flush\_trace OMPT type, enables a tool to cause the OpenMP implementation to issue a sequence of zero or more buffer\_complete callbacks to deliver all trace records that have been collected prior to the flush for the specified device. An invocation of flush\_trace returns one if the entry point succeeds and zero otherwise.

## Cross References

• OMPT device Type, see Section 33.11

## 37.10 stop\_trace Entry Point

Type Signature

<table><tr><td>Name: stop_traceCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr></table>

<table><tr><td></td><td>C / C++</td></tr><tr><td colspan="2">typedef int (*ompt_stop_trace_t) (ompt_device_t *device);</td></tr><tr><td></td><td>C / C++</td></tr></table>

## Semantics

The stop\_trace entry point, which has the stop\_trace OMPT type, provides a superset of the functionality of the flush\_trace entry point. Specifically, the stop\_trace entry point stops tracing for the specified device in addition to flushing pending trace records. An invocation of stop\_trace returns one if the entry point succeeds and zero otherwise.

Cross References

• OMPT device Type, see Section 33.11

• flush\_trace Entry Point, see Section 37.9

## 37.11 advance\_buffer\_cursor Entry Point

<table><tr><td>Name: advance_buffer_cursorCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device</td><td>device</td><td>OMPT, pointer</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>size</td><td>size_t</td><td>default</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr><tr><td>next</td><td>buffer_cursor</td><td>OMPT, opaque, pointer</td></tr></table>

## Type Signature

typedef int (<sub>\*</sub>ompt\_advance\_buffer\_cursor\_t) ( ompt\_device\_t <sub>\*</sub>device, ompt\_buffer\_t <sub>\*</sub>bufer, size\_t size, ompt\_buffer\_cursor\_t current, ompt\_buffer\_cursor\_t <sub>\*</sub>next);

C / C++

## Semantics

The advance\_buffer\_cursor entry point, which has the advance\_buffer\_cursor OMPT type, enables a tool to advance the trace bufer pointer for the bufer that the bufer argument indicates to the next trace record. The size argument indicates the size of bufer in bytes. The current argument is an OpenMP object that indicates the current position, while the next argument returns an OpenMP object with the next value. An invocation of advance\_buffer\_cursor returns true if the advance is successful and the next position in the bufer is valid. Otherwise, it returns false.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT device Type, see Section 33.11

## 37.12 get\_record\_type Entry Point

<table><tr><td>Name: get_record_typeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT</td></tr></table>

## Type Signature

C / C++

typedef ompt\_record\_t (<sub>\*</sub>ompt\_get\_record\_type\_t) ( ompt\_buffer\_t <sub>\*</sub>bufer, ompt\_buffer\_cursor\_t current);

C / C++

## Semantics

Trace records for a device may be in one of two forms: native trace format, which may be device-specific, or standard trace format, in which each trace record corresponds to an OpenMP event and most fields in the trace record structure are the arguments that would be passed to the callback for the event. For the bufer specified by the bufer argument, the get\_record\_type entry point, which has the get\_record\_type OMPT type, enables a tool to inspect the type of a trace record at the position that the current argument specifies and to determine whether the trace record is an OMPT trace record, a native trace record, or is an invalid record, which is returned if the cursor is out of bounds.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT record Type, see Section 33.23

## 37.13 get\_record\_ompt Entry Point

<table><tr><td>Name: get_record_emptCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record_ompt</td><td>pointer</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr></table>

## Type Signature

C / C++

typedef ompt\_record\_ompt\_t <sub>\*</sub>(<sub>\*</sub>ompt\_get\_record\_ompt\_t) ( ompt\_buffer\_t <sub>\*</sub>bufer, ompt\_buffer\_cursor\_t current);

C / C++

## Semantics

The get\_record\_ompt entry point, which has the get\_record\_ompt OMPT type, enables a tool to obtain a pointer to an OMPT trace record from a trace bufer associated with a device. The pointer may point to storage in the bufer indicated by the bufer argument or it may point to a trace record in thread-local storage in which the information extracted from a trace record was

assembled. The information available for an event depends upon its type. The current argument is an OpenMP object that indicates the position from which to extract the trace record. The return value of the record\_ompt OMPT type includes a field of the any\_record\_ompt OMPT type, which is a union that can represent information for any OMPT trace record type. Another call to the entry point may overwrite the contents of the fields in a trace record returned by a prior invocation.

## Cross References

• OMPT any\_record\_ompt Type, see Section 33.2

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT device Type, see Section 33.11

• OMPT record\_ompt Type, see Section 33.26

## 37.14 get\_record\_native Entry Point

<table><tr><td colspan="2">Name: get_record_nativeCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="3">Return Type and Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>buffer</td><td>buffer</td><td>OMPT, pointer</td></tr><tr><td>current</td><td>buffer_cursor</td><td>OMPT, opaque</td></tr><tr><td>host_op_id</td><td>id</td><td>OMPT, pointer</td></tr><tr><td colspan="3">Type SignatureC / C++typedef void *(*ompt_get_record_native_t) (empt_buffer_t *buffer, ompt_buffer_cursor_t current,empt_id_t *host_op_id);</td></tr></table>

C / C++

## Semantics

The get\_record\_native entry point, which has the get\_record\_native OMPT type, enables a tool to obtain a pointer to a native trace record from a trace bufer associated with a device. The pointer may point to storage in the bufer indicated by the bufer argument or it may point to a trace record in thread-local storage in which the information extracted from a trace record was assembled. The information available for a native event depends upon its type. The current argument is an OpenMP object that indicates the position from which to extract the trace record. If the entry point returns a non-null pointer result, it will also set the object to which the host\_op\_id argument points to a host-side identifier for the operation that is associated with the trace record on the target device and was created when the operation was initiated by the host device. Another cal to the entry point may overwrite the contents of the fields in a trace record returned by a prior invocation.

## Cross References

• OMPT buffer Type, see Section 33.3

• OMPT buffer\_cursor Type, see Section 33.4

• OMPT id Type, see Section 33.18

## 37.15 get\_record\_abstract Entry Point

<table><tr><td>Name: get_record_abstractCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>record_abstract</td><td>pointer</td></tr><tr><td>native_record</td><td>void</td><td>pointer</td></tr></table>

## Type Signature

C / C++

(<sub>\*</sub>ompt\_get\_record\_abstract\_t) (void <sub>\*</sub>native\_record);

C / C++

## Semantics

An OpenMP implementation may execute on a device that logs trace records in a native trace format that a tool cannot interpret directly. The get\_record\_abstract entry point, which has the get\_record\_abstract OMPT type, enables a tool to translate a native trace record to which the native\_record argument points into a standard form.

## Cross References

• OMPT record\_abstract Type, see Section 33.24

Part V
