# 42 OMPD Breakpoint Symbol Names

The OpenMP implementation must define several symbols through which execution must pass when particular events occur and data collection for OMPD is enabled. A third-party tool can enable notification of an event by setting a breakpoint at the address of the symbol.

OMPD symbols have external C linkage and do not require demangling or other transformations to look up their names to obtain the address in the OpenMP program. While each OMPD symbol conceptually has a function type signature, it may not be a function. It may be a labeled location.

## 42.1 ompd\_bp\_thread\_begin Breakpoint

## Format

C

void ompd\_bp\_thread\_begin(void);

C

## Semantics

When starting a native thread that will be used as an OpenMP thread, the implementation must execute ompd\_bp\_thread\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_thread\_begin at every native-thread-begin and initial-thread-begin event. This execution occurs before the thread starts the execution of any OpenMP region.

## 42.2 ompd\_bp\_thread\_end Breakpoint

## Format

C

void ompd\_bp\_thread\_end(void);

C

## Semantics

When terminating an OpenMP thread or a native thread that has been used as an OpenMP thread, the implementation must execute ompd\_bp\_thread\_end. Thus, the OpenMP implementation must execute ompd\_bp\_thread\_end at every native-thread-end and initial-thread-end event. This execution occurs after the thread completes the execution of all OpenMP regions. After executing ompd\_bp\_thread\_end, any thread\_handle that was acquired for this thread is invalid and should be released by calling ompd\_rel\_thread\_handle.

## Cross References

• ompd\_rel\_thread\_handle Routine, see Section 41.8.4

## 42.3 ompd\_bp\_device\_begin Breakpoint

## Format

void ompd\_bp\_device\_begin(void);

## Semantics

When initializing a device for execution of target regions, the implementation must execute ompd\_bp\_device\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_device\_begin at every device-initialize event. This execution occurs before the work associated with any OpenMP region executes on the device.

## Cross References

• Device Initialization, see Section 15.4

• target Construct, see Section 15.8

## 42.4 ompd\_bp\_device\_end Breakpoint

## Format

void ompd\_bp\_device\_end(void);

## Semantics

When terminating use of a device, the implementation must execute ompd\_bp\_device\_end. Thus, the OpenMP implementation must execute ompd\_bp\_device\_end at every device-finalize event. This execution occurs after the device executes all OpenMP regions. After execution of ompd\_bp\_device\_end, any address\_space\_handle that was acquired for this device is invalid and should be released by calling ompd\_rel\_address\_space\_handle.

Cross References

• Device Initialization, see Section 15.4

• ompd\_rel\_address\_space\_handle Routine, see Section 41.8.1

## 42.5 ompd\_bp\_parallel\_begin Breakpoint

Format

void ompd\_bp\_parallel\_begin(void);

C

## Semantics

Before starting execution of a parallel region, the implementation must execute ompd\_bp\_parallel\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_parallel\_begin at every parallel-begin event. When the implementation reaches ompd\_bp\_parallel\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the parallel region that is beginning and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the parallel construct.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• parallel Construct, see Section 12.1

## 42.6 ompd\_bp\_parallel\_end Breakpoint

## Format ormat

C void ompd\_bp\_parallel\_end(void); C

## Semantics

After finishing execution of a parallel region, the implementation must execute ompd\_bp\_parallel\_end. Thus, the OpenMP implementation must execute ompd\_bp\_parallel\_end at every parallel-end event. When the implementation reaches ompd\_bp\_parallel\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the parallel region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the parallel construct. After execution of ompd\_bp\_parallel\_end, any parallel\_handle that was acquired for the parallel region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• parallel Construct, see Section 12.1

## 42.7 ompd\_bp\_teams\_begin Breakpoint

## Format

void ompd\_bp\_teams\_begin(void);

C

## Semantics

Before starting execution of a teams region, the implementation must execute ompd\_bp\_teams\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_teams\_begin at every teams-begin event. When the implementation reaches ompd\_bp\_teams\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the teams region that is beginning and the binding task set for

ompd\_get\_curr\_task\_handle is the encountering task for the teams construct.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• teams Construct, see Section 12.2

## 42.8 ompd\_bp\_teams\_end Breakpoint

## Format

void ompd\_bp\_teams\_end(void);

## Semantics

After finishing execution of a teams region, the implementation must execute ompd\_bp\_teams\_end. Thus, the OpenMP implementation must execute ompd\_bp\_teams\_end at every teams-end event. When the implementation reaches ompd\_bp\_teams\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the teams region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the encountering task for the teams construct. After execution of ompd\_bp\_teams\_end, any parallel\_handle that was acquired for the teams region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• teams Construct, see Section 12.2

## 42.9 ompd\_bp\_task\_begin Breakpoint

## Format

C

void ompd\_bp\_task\_begin(void);

C

## Semantics

Before starting execution of a task region, the implementation must execute ompd\_bp\_task\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_task\_begin immediately before starting execution of a structured block that is associated with a non-merged task. When the implementation reaches ompd\_bp\_task\_begin, the binding task set for ompd\_get\_curr\_task\_handle is the task that is scheduled to execute.

## Cross References

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

## 42.10 ompd\_bp\_task\_end Breakpoint

## Format

C

void ompd\_bp\_task\_end(void);

C

## Semantics

After finishing execution of a task region, the implementation must execute ompd\_bp\_task\_end. Thus, the OpenMP implementation must execute ompd\_bp\_task\_end immediately after completion of a structured block that is associated with a non-merged task. When the implementation reaches ompd\_bp\_task\_end, the binding task set for ompd\_get\_curr\_task\_handle is the task that finished execution. After execution of ompd\_bp\_task\_end, any task\_handle that was acquired for the task region is invalid and should be released by calling ompd\_rel\_task\_handle.

## Cross References

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_task\_handle Routine, see Section 41.8.3

## 42.11 ompd\_bp\_target\_begin Breakpoint

Format

C

void ompd\_bp\_target\_begin(void);

C

## Semantics

Before starting execution of a target region, the implementation must execute ompd\_bp\_target\_begin. Thus, the OpenMP implementation must execute ompd\_bp\_target\_begin at every initial-task-begin event that results from the execution of an initial task enclosing a target region. When the implementation reaches ompd\_bp\_target\_begin, the binding region for ompd\_get\_curr\_parallel\_handle is the target region that is beginning and the binding task set for ompd\_get\_curr\_task\_handle is the initial task on the device.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• target Construct, see Section 15.8

## 42.12 ompd\_bp\_target\_end Breakpoint

## Format

void ompd\_bp\_target\_end(void);

## Semantics

After finishing execution of a target region, the implementation must execute ompd\_bp\_target\_end. Thus, the OpenMP implementation must execute ompd\_bp\_target\_end at every initial-task-end event that results from the execution of an initial task enclosing a target region. When the implementation reaches ompd\_bp\_target\_end, the binding region for ompd\_get\_curr\_parallel\_handle is the target region that is ending and the binding task set for ompd\_get\_curr\_task\_handle is the initial task on the device. After execution of ompd\_bp\_target\_end, any parallel\_handle that was acquired for the target region is invalid and should be released by calling ompd\_rel\_parallel\_handle.

## Cross References

• ompd\_get\_curr\_parallel\_handle Routine, see Section 41.5.1

• ompd\_get\_curr\_task\_handle Routine, see Section 41.6.1

• ompd\_rel\_parallel\_handle Routine, see Section 41.8.2

• target Construct, see Section 15.8
