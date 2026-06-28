## List of Figures

32.1 First-Party Tool Activation Flow Chart 699

## List of Tables

3.1 ICV Scopes and Descriptions . . . . . . . . . . . . . . . . . . . . . . . . . . 115
3.2 ICV Initial Values . . . . . . . . . . . . . . . . . . . . . . . 118
3.3 Ways to Modify and to Retrieve ICV Values . . . . . . . . . . . . . . . . 121
3.4 ICV Override Relationships . . . . . . . . . . . . . . . 125

4.1 Predefined Place-list Abstract Names . . . . . . . . . . . . . . . 128
4.2 Available Field Types for Formatting OpenMP Thread Affinity Information . . . 137
4.3 Reservation Types for OMP\_THREADS\_RESERVE . . . . . . . . 142

5.1 Syntactic Properties for Clauses, Arguments and Modifiers . . . 159

7.1 Implicitly Declared C/C++ Reduction Identifiers . . . 244
7.2 Implicitly Declared Fortran Reduction Identifiers . . 245
7.3 Implicitly Declared C/C++ Induction Identifiers . . 246
7.4 Implicitly Declared Fortran Induction Identifiers . 246
7.5 Map-Type Decay of Map Type Combinations . 276

8.1 Predefined Memory Spaces . . . 304
8.2 Allocator Traits . 305
8.3 Predefined Allocators . 308

12.1 Affinity-related Symbols used in this Section . 390

13.1 work OMPT types for Worksharing-Loop . 415

14.1 task\_create Callback Flags Evaluation . 427

20.1 Routine Argument Properties . 535
20.2 Required Values of the interop\_property OpenMP Type . 542
20.3 Required Values for the interop\_rc OpenMP Type . 543
20.4 Allowed Key-Values for alloctrait OpenMP Type . 546
20.5 Standard Tool Control Commands . 566

32.1 OMPT Callback Interface Runtime Entry Point Names and Their Type Signatures . 702
32.2 Callbacks for which set\_callback Must Return empt\_set\_always . 703
32.3 OMPT Tracing Interface Runtime Entry Point Names and Their Type Signatures . 705

35.1 Association of dev1 and dev2 arguments for target data operations ..... 779
39.1 Mapping of Scope Type and OMPD Handles ..... 828

Part I Definitions

# 1 Overview of the OpenMP API

The collection of compiler directives, library routines, environment variables, and tool support that this document describes collectively define the specification of the OpenMP Application Program Interface (OpenMP API) for C, C++ and Fortran base programs. This specification provides a model for parallel programming that is portable across architectures from diferent vendors. Compilers from numerous vendors support the OpenMP API. More information about the OpenMP API can be found at the following web site: https://www.openmp.org.

The directives, routines, environment variables, and tool support that this document defines allow users to create, to manage, to debug and to analyze parallel programs while permitting portability. The directives extend the C, C++ and Fortran base languages with single program multiple data (SPMD) constructs, tasking constructs, device constructs, work-distribution constructs, and synchronization constructs, and they provide support for sharing, mapping and privatizing data. The functionality to control the runtime environment is provided by routines and environment variables. Compilers that support the OpenMP API often include command line options to enable or to disable interpretation of some or all OpenMP directives.

## 1.1 Scope

The OpenMP API covers only user-directed parallelization, wherein the programmer explicitly specifies the actions to be taken by the compiler and runtime system in order to execute the program in parallel. OpenMP-compliant implementations are not required to check for data dependences, data conflicts, data races, or deadlocks. Compliant implementations also are not required to check for any code sequences that cause a program to be classified as a non-conforming program. Application developers are responsible for correctly using the OpenMP API to produce a conforming program. The OpenMP API does not cover compiler-generated automatic parallelization.

## 1.2 Execution Model

A compliant implementation must follow the abstract execution model that the supported base language and OpenMP specification define, as observable from the results of user code in a conforming program. These results do not include output from external monitoring tools or tools that use the OpenMP tool interfaces (i.e., OMPT and OMPD), which may reflect deviations from the execution model such as the unprescribed use of additional native threads, SIMD instruction, alternate loop transformations, or other target devices to facilitate parallel execution of the program.

The OpenMP API includes several directives. Some directives allow customization of base language declarations while other directives specify details of program execution. Such executable directives may be lexically associated with base language code. Each executable directive and any such associated base language code forms a construct. An OpenMP program executes regions, which consist of all code encountered by native threads.

Some regions are implicit but many are explicit regions, which correspond to a specific instance of a construct or routine. Execution is composed of nested regions since a given region may encounter additional constructs and routines. References to regions, particularly explicit regions or nested regions, that correspond to a specific type of construct or routine usually include the name of that construct or routine to identify the type of region that results.

With the OpenMP API, multiple threads execute tasks defined implicitly or explicitly by OpenMP directives and their associated user code, if any. An implementation may use multiple devices for a given execution of an OpenMP program. Concurrent execution of threads may result in diferent numeric results because of changes in the association of numeric operations.

Each device executes a set of one or more contention groups. Each contention group consists of a set of tasks that an associated set of threads, an OpenMP thread pool, executes. The lifetime of the OpenMP thread pool is the same as that of the contention group. The threads that are associated with each contention group are distinct from threads associated with any other contention group. Threads cannot migrate to execute tasks of a diferent contention group.

Each OpenMP thread pool has an initial thread, which may be the thread that starts execution of a region that is not nested within any other region, or which may be the thread that starts execution of the structured block associated with a target or teams construct. Each initial thread executes sequentially; the code that it encounters is part of an implicit task region, called an initial task region, that is generated by the implicit parallel region that surrounds all code executed by the initial thread. The other threads in the OpenMP thread pool associated with a contention group are unassigned threads. An implicit task is assigned to each of those threads. When a task encounters a parallel construct, some of the unassigned threads become assigned threads that are assigned to the team of that parallel region.

The thread that executes the implicit parallel region that surrounds the whole program executes on the host device. An implementation may support other devices besides the host device. If supported, these devices are available to the host device for ofloading code and data. Each device has its own contention groups.

A task that encounters a target construct generates a new target task; its region encloses the target region. The target task is complete after the target region completes execution. When a target task executes, an initial thread executes the enclosed target region. The initial thread executes sequentially, as if the target region is part of an initial task region that an implicit parallel region generates. The initial thread may execute on the requested target device, if it is available. If the target device does not exist or the implementation does not support it, all target regions associated with that device execute on the host device. Otherwise, the implementation ensures that the target region executes as if it were executed in the data environment of the target device unless an if clause is present and the if clause expression evaluates to false.

The teams construct creates a league of teams, where each team is an initial team that comprises an initial thread that executes the teams region and that executes a distinct contention group from those of initial threads. Each initial thread executes sequentially, as if the code encountered is part of an initial task region that is generated by an implicit parallel region associated with each team. Whether the initial threads concurrently execute the teams region is unspecified, and a program that relies on their concurrent execution for the purposes of synchronization may deadlock.

Any thread that encounters a parallel construct becomes the primary thread of the new team that consists of itself and zero or more additional unassigned threads that are then assigned to that team as team-worker threads. Those threads remain assigned threads for the lifetime of that team. A set of implicit tasks, one per thread, is generated. The code inside the parallel construct defines the code for each implicit task. A diferent thread in the team is assigned to each implicit task, which is tied, that is, only that assigned thread ever executes it. The task region of the task being executed by the encountering thread is suspended, and each member of the new team executes its implicit task. The primary thread is the parent thread of any thread that executes a task that is bound to the parallel region. An implicit barrier occurs at the end of the parallel region. Only the primary thread resumes execution beyond the end of that region, resuming the suspended task region. The other threads again become unassigned threads. A single program can specify any number of parallel constructs.

parallel regions may be arbitrarily nested inside each other. If nested parallelism is disabled, or is not supported by the OpenMP implementation, then the new team that is formed by a thread that encounters a parallel construct inside a parallel region will consist only of the encountering thread. However, if nested parallelism is supported and enabled, then the new team can consist of more than one thread. A parallel construct may include a proc\_bind clause to specify the places to use for the threads in the team within the parallel region.

When any team encounters a partitioned worksharing construct, the work inside the construct is divided into work partitions, each of which is executed by one member of the team, instead of the work being executed redundantly by each thread. An implicit barrier occurs at the end of any region that corresponds to a worksharing construct for which the nowait clause is not specified. Redundant execution of code by every thread in the team resumes after the end of the worksharing construct. Regions that correspond to team-executed constructs, including all worksharing regions and barrier regions, are executed by the current team such that all threads in the team execute the team-executed regions in the same order.

When a loop construct is encountered, the logical iterations of the collapsed loops, which are the afected loops as specified by the collapse clause, are executed in the context of its encountering threads, as determined according to its binding region. If the loop region binds to a teams region, the region is encountered by the set of primary thread that execute the teams region. If the loop region binds to a parallel region, the region is encountered by the team that execute the parallel region. Otherwise, the region is encountered by a single thread. If the loop region

binds to a teams region, the encountering threads may continue execution after the loop region without waiting for all iterations to complete; the iterations are guaranteed to complete before the end of the teams region. Otherwise, all iterations must complete before the encountering threads continue execution after the loop region. All threads that encounter the loop construct may participate in the execution of the iterations. Only one thread may execute any given iteration.

When any thread encounters a simd construct, the iterations of the loop associated with the construct may be executed concurrently using the SIMD lanes that are available to the thread.

When any thread encounters a task-generating construct, one or more explicit tasks are generated. Explicitly generated tasks are scheduled onto threads of the binding thread set of the task, subject to the availability of the threads to execute work. Thus, execution of the new task could be immediate, or deferred until later according to task scheduling constraints and thread availability. Completion of all explicit tasks bound to a given parallel region is guaranteed before the primary thread leaves the implicit barrier at the end of the region. Completion of a subset of all explicit tasks bound to a given parallel region may be specified through the use of task synchronization constructs. Completion of all explicit tasks bound to an implicit parallel region is guaranteed when the associated initial task completes. The initial task on the host device that begins a typical OpenMP program is guaranteed to end by the time that the program exits.

Threads are allowed to suspend the current task region at a task scheduling point in order to execute a diferent task. Thus, each task consists of a set of one or more subtasks that each correspond to the portion of the task region between any two consecutive task scheduling points that the task encounters. If the task region of a tied task is suspended, the initially assigned thread later resumes execution of the next subtask of the suspended task region. If the task region of an untied task is suspended, any thread in the binding thread set of the task may resume execution of its next subtask.

OpenMP threads are logical execution entities that are mapped to native threads for actual execution. OpenMP does not dictate the details of the implementation of native threads and, instead, specifies requirements on the thread state of OpenMP threads. As long as those requirements are met, a compliant implementation may map the same OpenMP thread diferently (i.e., to diferent native threads) for diferent portions of its execution (e.g., for the execution of diferent subtasks). Similarly, while the lifetime of an OpenMP thread and its OpenMP thread pool is identical to that of the associated contention group, OpenMP does not specify the lifetime of any native threads to which it is mapped. Native threads may be created at any time and may be terminated at any time.

The cancel construct can alter the previously described flow of execution in a region. The efect of the cancel construct depends on the cancel-directive-name that is specified on it. If a task encounters a cancel construct with a taskgroup clause, then the explicit task activates cancellation and continues execution at the end of its task region, which implies completion of that task. Any other task in that taskgroup that has begun executing completes execution unless it encounters a cancellation point, including one that corresponds to a cancellation point construct, in which case it continues execution at the end of its explicit task region, which implies its completion. Other tasks in that taskgroup region that have not begun execution are aborted, which implies their completion.

If a task encounters a cancel construct with any other cancel-directive-name clause, it activates cancellation of the innermost enclosing region of the type specified and the thread continues execution at the end of that region. Tasks check if cancellation has been activated for their region at cancellation points and, if so, also resume execution at the end of the canceled region.

If cancellation has been activated, regardless of the cancel-directive-name clauses, threads that are waiting inside a barrier other than an implicit barrier at the end of the canceled region exit the barrier and resume execution at the end of the canceled region. This action can occur before the other threads reach that barrier.

OpenMP specifies circumstances that cause error termination. If compile-time error termination is specified, the efect is as if the program encounters an error directive on which a severity clause specifies a sev-level argument of fatal and an at clause specifies an action-time argument of compilation. If runtime error termination is specified, the efect is as if the program encounters an error directive on which a severity clause specifies a sev-level argument of fatal and an at clause specifies an action-time argument of execution.

A construct that creates a data environment creates it at the time that the construct is encountered. The description of a construct defines whether it creates a data environment. Synchronization constructs and routines are available in the OpenMP API to coordinate tasks and their data accesses. In addition, routines and environment variables are available to control or to query the runtime environment of OpenMP programs. The scope of OpenMP synchronization mechanisms may be limited to the contention group of the encountering task. Except where explicitly specified any efect of the mechanisms between contention groups is implementation defined. Section 1.3 details the OpenMP memory model, including the efect of these features.

The OpenMP specification makes no guarantee that input or output to the same file is synchronous when executed in parallel. In this case, the programmer is responsible for synchronizing input and output processing with the assistance of synchronization constructs or routines.

Each native thread that enables the execution of a task by an OpenMP thread executes on a hardware thread. A hardware thread executes a stream of instructions defined by a given task region, so that only one OpenMP thread may execute on a hardware thread at a time. A set of consecutive hardware threads may form a progress unit. Hardware threads execute distinct streams of instructions unless they are part of the same progress unit. Threads that execute in the same progress unit may execute from a common stream of instructions, with serialized execution of diverging code paths that occur due to conditional statements. A program that relies on concurrent execution of such diverging code paths for the purposes of synchronization may deadlock.

All concurrency semantics defined by the base language with respect to base language threads apply to OpenMP threads, unless otherwise specified. An OpenMP thread makes progress when it performs a flush operation, performs input or output processing, terminates, or makes progress as defined by the base language. OpenMP threads will eventually make progress in the absence of dependence cycles, unless otherwise specified by the base language. A dependence cycle may be implicitly introduced between synchronizing threads where concurrent execution is not guaranteed. Threads may therefore not make progress if the program includes synchronizing threads that

descend from diferent initial teams formed by a teams construct or if the program includes synchronizing divergent threads from the same team that execute on the same progress unit. The generation and execution of explicit tasks by threads in the current team does not prevent any of the threads from making progress if executing the explicit tasks as included tasks would ensure that they make progress.

Each device is identified by a device number. The device number for the host device is the value of the total number of non-host devices, while each non-host device has a unique device number that is greater than or equal to zero and less than the device number for the host device. Additionally, the predefined identifier omp\_initial\_device can be used as an alias for the host device and the predefined identifier omp\_invalid\_device can be used to specify an invalid device number. A conforming device number is either a non-negative integer that is less than or equal to the value returned by omp\_get\_num\_devices or equal to omp\_initial\_device or omp\_invalid\_device.

A signal handler may only execute directives and routines that have the async-signal-safe property.

## 1.3 Memory Model

## 1.3.1 Structure of the OpenMP Memory Model

The OpenMP API provides a relaxed-consistency, shared-memory model. All OpenMP threads have access to a place to store and to retrieve variables, called the memory. A given storage location in the memory may be associated with one or more devices, such that only threads on associated devices have access to it. In addition, each thread is allowed to have its own temporary view of the memory. The temporary view of memory for each thread is not a required part of the OpenMP memory model, but can represent any kind of intervening structure, such as machine registers, cache, or other local storage, between the thread and the memory. The temporary view of memory allows the thread to cache variables and thereby to avoid going to memory for every reference to a variable. Each thread also has access to another type of memory that must not be accessed by other threads, called threadprivate memory.

A directive that accepts data-sharing attribute clauses determines two kinds of access to variables used in the associated structured block of the directive: shared variables and private variables. Each variable referenced in the structured block has an original variable, which is the variable by the same name that exists in the OpenMP program immediately outside the construct. Each reference to a shared variable in the structured block becomes a reference to the original variable. For each private variable referenced in the structured block, a new version of the original variable (of the same type and size) is created in memory for each task or SIMD lane that executes code associated with the directive. Creation of the new version does not alter the value of the original variable. However, attempts to access the original variable from within the region that corresponds to the directive result in unspecified behavior; see Section 7.5.3 for additional details. References to a private variable in the structured block refer to the private version of the original variable for the current task or SIMD lane. The relationship between the value of the value of the original variable and the initial or final value of the private version depends on the exact clause that specifies it. Details of this issue, as well as other issues with privatization, are provided in Chapter 7.

The minimum size at which a memory update may also read and write back adjacent variables that are part of an aggregate variable is implementation defined but is no larger than the base language requires.

A single access to a variable may be implemented with multiple load or store instructions and, thus, is not guaranteed to be an atomic operation with respect to other accesses to the same variable. Accesses to variables smaller than the implementation defined minimum size or to C or C++ bit-fields may be implemented by reading, modifying, and rewriting a larger unit of memory, and may thus interfere with updates of variables or fields in the same unit of memory.

Two memory operations are considered unordered if the order in which they must complete, as seen by their afected threads, is not specified by the memory consistency guarantees listed in Section 1.3.6. If multiple threads write to the same memory unit (defined consistently with the above access considerations) then a data race occurs if the writes are unordered. Similarly, if at least one thread reads from a memory unit and at least one thread writes to that same memory unit then a data race occurs if the read and write are unordered. If a data race occurs then the result of the OpenMP program is unspecified behavior.

A private variable in a task region that subsequently generates an inner nested parallel region is permitted to be made shared for implicit tasks in the inner parallel region. A private variable in a task region can also be shared by an explicit task region generated during its execution. However, the programmer must use synchronization that ensures that the lifetime of the variable does not end before completion of the explicit task region sharing it. Any other access by one task to the private variables of another task results in unspecified behavior.

A storage location in memory that is associated with a given device has a device address that may be dereferenced by a thread executing on that device, but it may not be generally accessible from other devices. A diferent device may obtain a device pointer that refers to this device address. The manner in which an OpenMP program can obtain the referenced device address from a device pointer, outside of mechanisms specified by OpenMP, is implementation defined. Unless otherwise specified, the atomic scope of a storage location is all threads on the current device.

## 1.3.2 Device Data Environments

When an OpenMP program begins, an implicit target\_data region for each device surrounds the whole program. Each device has a device data environment that is defined by its implicit target\_data region. Any declare target directives and directives that accept data-mapping attribute clauses determine how an original storage block in a data environment is mapped to a corresponding storage block in a device data environment. Additionally, if a variable with static storage duration has original storage that is accessible on a device, and the variable is not a device-local variable, it may be treated as if its storage is mapped with a persistent self map in the implicit target\_data region of the device; whether this happens is implementation defined.

When an original storage block is mapped to a device data environment and a corresponding storage block is not present in the device data environment, a new corresponding storage block (of the same type and size as the original storage block) is created in the device data environment. Conversely, the original storage block becomes the corresponding storage block of the new storage block in the device data environment of the device that performs a mapping operation.

The corresponding storage block in the device data environment may share storage with the original storage block. Writes to the corresponding storage block may alter the value of the original storage block. Section 1.3.6 discusses the impact of this possibility on memory consistency. When a task executes in the context of a device data environment, references to the original storage block refer to the corresponding storage block in the device data environment. If an original storage block is not currently mapped and a corresponding storage block does not exist in the device data environment then accesses to the original storage block result in unspecified behavior unless the unified\_shared\_memory clause is specified on a requires directive for the compilation unit.

The relationship between the value of the original storage block and the initial or final value of the corresponding storage block depends on the map-type. Details of this issue, as well as other issues with mapping a variable, are provided in Section 7.9.6.

The original storage block in a data environment and a corresponding storage block in a device data environment may share storage. Without intervening synchronization data races can occur.

If a storage block has a corresponding storage block with which it does not share storage, a write to a storage location designated by the storage block causes the value at the corresponding storage block to become undefined.

## 1.3.3 Memory Management

The host device, and other devices that an implementation may support, have attached storage resources where variables are stored. These resources can have diferent traits. A memory space in an OpenMP program represents a set of these storage resources. Memory spaces are defined according to a set of traits, and a single resource may be exposed as multiple memory spaces with diferent traits or may be part of multiple memory spaces. In any device, at least one memory space is guaranteed to exist.

An OpenMP program can use a memory allocator to allocate memory in which to store variables. This memory will be allocated from the storage resources of the memory space associated with the memory allocator. Memory allocators are also used to deallocate previously allocated memory. When a memory allocator is not used to allocate memory, OpenMP does not prescribe the storage resource for the allocation; the memory for the variables may be allocated in any storage resource.

## 1.3.4 The Flush Operation

The memory model has relaxed-consistency because the temporary view of memory of a thread is not required to be consistent with memory at all times. A value written to a variable can remain in that temporary view until it is forced to memory at a later time. Likewise, a read from a variable may retrieve the value from that temporary view, unless it is forced to read from memory. OpenMP flush operations are used to enforce consistency between the temporary view of memory of a thread and memory, or between the temporary views of multiple threads.

A flush has an associated thread-set that constrains the threads for which it enforces memory consistency. Consistency is only guaranteed to be enforced between the view of memory of these threads. Unless otherwise specified, the thread-set of a flush only includes all threads on the current device.

If a flush is a strong flush, it enforces consistency between the temporary view of a thread and memory. A strong flush is applied to a set of variable called the flush-set. A strong flush restricts how an implementation may reorder memory operations. Implementations must not reorder the code for a memory operation for a given variable, or the code for a flush for the variable, with respect to a strong flush that refers to the same variable.

If a thread has performed a write to its temporary view of a shared variable since its last strong flush of that variable then, when it executes another strong flush of the variable, the strong flush does not complete until the value of the variable has been written to the variable in memory. If a thread performs multiple writes to the same variable between two strong flushes of that variable, the strong flush ensures that the value of the last write is written to the variable in memory. A strong flush of a variable executed by a thread also causes its temporary view of the variable to be discarded, so that if its next memory operation for that variable is a read, then the thread will read from memory and capture the value in its temporary view. When a thread executes a strong flush, no later memory operation by that thread for a variable in the flush-set of that strong flush is allowed to start until the strong flush completes. The completion of a strong flush executed by a thread is defined as the point at which all writes to the flush-set performed by the thread before the strong flush are visible in memory to all other threads, and at which the temporary view of the flush-set of that thread is discarded.

A strong flush provides a guarantee of consistency between the temporary view of a thread and memory. Therefore, a strong flush can be used to guarantee that a value written to a variable by one thread may be read by a second thread. To accomplish this, the programmer must ensure that the second thread has not written to the variable since its last strong flush of the variable, and that the following sequence of events are completed in this specific order:

1. The value is written to the variable by the first thread;

2. The variable is flushed, with a strong flush, by the first thread;
