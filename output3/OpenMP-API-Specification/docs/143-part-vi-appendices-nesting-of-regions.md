
• When the device clause is specified with the ancestor device-modifier on the target construct, the nowait clause may now also be specified (see Section 15.2, Section 15.8 and Section 17.6).

• The target\_data directive description was updated to make it a composite construct, to include a taskgroup region and to make the clauses that may appear on it reflect its constituent constructs and the taskgroup region (see Section 15.7).

• The prefer-type modifier of the init clause was updated to allow preferences other than foreign runtime identifiers (see Section 16.1.3).

• The do\_not\_synchronize argument for the nowait clause (see Section 17.6) and nogroup clause (see Section 17.7) was updated to permit non-constant expressions.

• The memscope clause was added to the atomic and flush constructs to allow the binding thread set to span multiple devices (see Section 17.8.4, Section 17.8.5 and Section 17.8.6).

• The transparent clause was added to support multi-generational task dependence graphs (see Section 17.9.6).

• The cancel construct was extended to complete tasks that have not yet been fulfilled through an event variable and the omp\_fulfill\_event routine was restricted such that an event handle must be fulfilled before execution continues beyond a barrier (see Section 18.2 and Section 23.2.1).

• The rules for compound-directive names were simplified to be more intuitive and to allow more valid combinations of immediately nested constructs (see Section 19.1).

• The omp\_is\_free\_agent and omp\_ancestor\_is\_free\_agent routines were added to test whether the encountering thread, or the ancestor thread, is a free-agent thread (see Section 23.1.4 and Section 23.1.5).

• The omp\_get\_device\_from\_uid and omp\_get\_uid\_from\_device routines were added to convert between unique identifiers and device numbers of devices (see Section 24.7 and Section 24.8).

• The omp\_get\_device\_num\_teams, omp\_set\_device\_num\_teams, omp\_get\_device\_teams\_thread\_limit, and omp\_set\_device\_teams\_thread\_limit routine were added to support getting and setting the nteams-var and teams-thread-limit-var ICVs for specific devices (see Section 24.11, Section 24.12, Section 24.13, and Section 24.14).

• The omp\_target\_memset and omp\_target\_memset\_async routines were added to fill memory in a device data environment of a device (see Section 25.8.1 and Section 25.8.2).

## Fortran

• Fortran versions of the runtime routines to operate on interoperability objects were added (see Chapter 26).

Fortran

• New routines were added to obtain memory spaces and memory allocators to allocate remote and shared memory (see Chapter 27).

• The omp\_get\_memspace\_num\_resources routine was added to support querying the number of available resources of a memory space (see Section 27.2).

• The omp\_get\_memspace\_pagesize routine was added to obtain the page size supported by a given memory space (see Section 27.3).

• The omp\_get\_submemspace routine was added to obtain a memory space with a subset of the original storage resources (see Section 27.4).

• The omp\_init\_mempartitioner, omp\_destroy\_mempartitioner, omp\_init\_mempartition, omp\_destroy\_mempartition, omp\_mempartition\_set\_part, omp\_mempartition\_get\_user\_data routines were added to manipulate the mempartitioner and mempartition objects (see Section 27.5).

• The set of callbacks for which set\_callback must return ompt\_set\_always no longer includes the target\_data\_op, target, target\_map and target\_submit callbacks, which were deprecated (see Section 32.2.4, Section 35.7, Section 35.8, Section 35.9 and Section 35.10).

• The more general values ompt\_target\_data\_transfer and ompt\_target\_data\_transfer\_async were added to the target\_data\_op OMPT type and supersede the values ompt\_target\_data\_transfer\_to\_device, ompt\_target\_data\_transfer\_from\_device, ompt\_target\_data\_transfer\_to\_device\_async and ompt\_target\_data\_transfer\_from\_device\_async (see Section 33.35). The superseded values were deprecated.

• The get\_buffer\_limits entry point was added to the OMPT device tracing interface so that a first-party tool can obtain an upper limit on the sizes of the trace bufers that it should make available to the implementation (see Section 37.6).

## B.3 Version 5.1 to 5.2 Differences

• Major reorganization and numerous changes were made to improve the quality of the specification of OpenMP syntax and to increase consistency of restrictions and their wording. These changes frequently result in the possible perception of diferences to preceding versions of the OpenMP specification. However, those diferences almost always resolve ambiguities, which may nonetheless have implications for existing implementations and programs.

• The explicit-task-var ICV replaced the implicit-task-var ICV, with the opposite meaning and semantics (see Chapter 3). The omp\_in\_explicit\_task routine was added to query if a code region is executed from an explicit task region (see Section 23.1.2).

## Fortran

• Expanded the directives that may be encountered in a pure procedure (see Chapter 5) by adding the pure property to metadirectives (see Section 9.4.3), assumption directives (see Section 10.6), the nothing directive (see Section 10.7), the error directive (see Section 10.1) and loop-transforming constructs (see Chapter 11).

Fortran

• For OpenMP directives, the omp sentinel and, for implementation defined directives that extend the OpenMP directives, the ompx sentinel for C/C++ and free source form Fortran and the omx sentinel for fixed source form Fortran (to accommodate character position requirements) were reserved (see Chapter 5. Reserved clause names that begin with the ompx\_ prefix for implementation defined clauses on OpenMP directives (see Chapter 5. Reserved names in the base language that start with the omp\_,ompt\_, ompd\_ and ompx\_ prefixes and reserved the omp, ompx, ompt and ompd namespaces for the OpenMP runtime API and for implementation defined extensions to that API (see Chapter 5.

• Allowed any clause that can be specified on a paired end directive to be specified on the directive (see Section 5.1), including, in Fortran, the copyprivate clause (see Section 7.8.2) and the nowait clause (see Section 17.6).

• Allowed the if clause on the teams construct (see Section 5.5 and Section 12.2).

• For consistency with the syntax of other definitions of the clause, the syntax of the destroy clause on the depobj construct with no argument was deprecated (see Section 5.7).

• For consistency with the syntax of other clauses, the syntax of the linear clause that specifies its argument and linear-modifier as linear-modifier(list) was deprecated and the step modifier was added for specifying the linear step (see Section 7.5.6).

• The minus (-) operator for reductions was deprecated (see Section 7.6.6).

• The syntax of modifiers without comma separators in the map clause was deprecated (see Section 7.9.6).

• To support the complete range of user-defined mappers and to improve consistency of map clause usage, the declare\_mapper directive was extended to accept iterator modifiers and the present map-type-modifier (see Section 7.9.6 and Section 7.9.10).

• Mapping of a pointer list item was updated such that if a matched candidate is not found in the data environment, firstprivate semantics apply and the pointer retains its original value (see Section 7.9.6).

• The enter clause was added as a synonym for the to clause on declare target directives, and the corresponding to clause was deprecated to reduce parsing ambiguity (see Section 7.9.7 and Section 9.9).

## Fortran

• The allocators construct was added to support the use of OpenMP allocators for variables that are allocated by a Fortran ALLOCATE statement, and the application of allocate directives to an ALLOCATE statement was deprecated (see Section 8.7).

Fortran

• To support the full range of allocators and to improve consistency with the syntax of other clauses, the argument that specified the arguments of the uses\_allocators clause as a comma-separated list in which each list item is a clause-argument-specification of the form allocator[(traits)] was deprecated (see Section 8.8).

• To improve code clarity and to reduce ambiguity in this specification, the otherwise clause was added as a synonym for the default clause on metadirectives and the corresponding default clause syntax was deprecated (see Section 9.4.2).

Fortran

• For consistency with other constructs with associated base language code, the dispatch construct was extended to allow an optional paired end directive to be specified (see Section 9.7).

Fortran

C / C++

• To improve overall syntax consistency and to reduce redundancy, the delimited form of the declare\_target directive was deprecated (see Section 9.9.2).

C / C++

• The behavior of the order clause with the concurrent argument was changed so that it only afects whether a loop schedule is reproducible if a modifier is explicitly specified (see Section 12.3).

• Support for the allocate and firstprivate clauses on the scope directive was added (see Section 13.2).

• The work OMPT type values for worksharing-loop constructs were added (see Section 13.6).

• To simplify usage, the map clause on a target\_enter\_data or target\_exit\_data, construct now has a default map type that provides the same behavior as the to or from map types, respectively (see Section 15.5 and Section 15.6).

• The interop construct was updated to allow the init clause to accept an interop\_type in any position of the modifier list (see Section 16.1).

• The doacross clause was added as a synonym for the depend clause with the keywords source and sink as dependence-type modifiers and the corresponding depend clause syntax was deprecated to improve code clarity and to reduce parsing ambiguity. Also, the omp\_cur\_iteration keyword was added to represent a logical iteration vector that refers to the current logical iteration (see Section 17.9.7).

• The omp\_pause\_stop\_tool value was added to the pause\_resource OpenMP type (see Section 20.11.1).

## B.4 Version 5.0 to 5.1 Differences

• Full support of C11, C++11, C++14, C++17, C++20 and Fortran 2008 was completed (see Section 1.6).

• Various changes throughout the specification were made to provide initial support of Fortran 2018 (see Section 1.6).

• To support device-specific ICV settings the environment variable syntax was extended to support device-specific environment variables (see Section 3.2 and Chapter 4).

• The OMP\_PLACES syntax was extended (see Section 4.1.6).

• The OMP\_NUM\_TEAMS and OMP\_TEAMS\_THREAD\_LIMIT environment variables were added to control the number and size of teams on the teams construct (see Section 4.2.1 and Section 4.2.2).

• The OpenMP directive syntax was extended to include C++ attribute specifiers (see Section 5.1).

• The omp\_all\_memory reserved locator was added (see Section 5.2.2), and the depend clause was extended to allow its use (see Section 17.9.5).

• Support for private and firstprivate as an argument to the default clause in C and C++ was added (see Section 7.5.1).

• The has\_device\_addr clause was added to the target construct to allow access to variables or array sections that already have a device address (see Section 7.5.9 and Section 15.8).

• Support was added so that iterators may be defined and used in map clauses (see Section 7.9.6) or in data-motion clauses on a target\_update directive (see Section 15.9).

• The present argument was added to the defaultmap clause (see Section 7.9.9).

• Support for the align clause on the allocate directive and allocator and align modifiers on the allocate clause was added (see Chapter 8).

• The target\_device trait set was added to the OpenMP context (see Section 9.1), and the target\_device selector set was added to context selectors (see Section 9.2).

• For C/C++, the declare variant directives were extended to support elision of preprocessed code and to allow enclosed function definitions to be interpreted as function variants (see Section 9.6).

• The declare\_variant directive was extended with new clauses (adjust\_args and append\_args) that support adjustment of the interface between the original function and its function variants (see Section 9.6.4).

• The dispatch construct was added to allow users to control when variant substitution happens and to define additional information that can be passed as arguments to function variants (see Section 9.7).

• Support was added for indirect calls to the device version of a procedure in target regions (see Section 9.9).

• To allow users to control the compilation process and runtime error actions, the error directive was added (see Section 10.1).

• Assumption directives were added to allow users to specify invariants (see Section 10.6).

• To support clarity in metadirectives, the nothing directive was added (see Section 10.7).

• Loop-transforming constructs were added (see Chapter 11).

• The masked construct was added to support restricting execution to a specific thread to replace the deprecated master construct (see Section 12.5).

• The scope directive was added to support reductions without requiring a parallel or worksharing region (see Section 13.2).

• The grainsize and num\_tasks clauses for the taskloop construct were extended with a strict prescriptiveness modifier to ensure a deterministic distribution of logica iterations to tasks (see Section 14.2).

• The thread\_limit clause was added to the target construct to control the upper bound on the number of threads in the created contention group (see Section 15.8).

• The interop directive was added to enable portable interoperability with foreign execution contexts (see Section 16.1). Runtime routines that facilitate use of interoperability objects were also added (see Chapter 26).

• The nowait clause was added to the taskwait directive to support insertion of non-blocking join operations in a task dependence graph (see Section 17.5).

• Specification of the seq\_cst clause on a flush construct was allowed, with the same meaning as a flush construct without a list and without a clause (see Section 17.8.1.5 and Section 17.8.6).

• Support was added for compare-and-swap and (for C and C++) minimum and maximum atomic operations through the compare clause. Support was also added for the specification of the memory order to apply to a failed atomic conditional update with the fail clause (see Section 17.8.3.2 and Section 17.8.3.3).

• To support inout sets, the inoutset task-dependence-type modifier was added to the depend clause (see Section 17.9.5).

• For the alloctrait\_key OpenMP type, the omp\_atv\_serialized value was added and the omp\_atv\_default value was changed (see Section 20.8).

• The omp\_set\_num\_teams and omp\_set\_teams\_thread\_limit routines were added to control the number of teams and the size of those teams on the teams construct (see Section 22.2 and Section 22.6). Additionally, the omp\_get\_max\_teams and omp\_get\_teams\_thread\_limit routines were added to retrieve the values that will be used in the next teams construct (see Section 22.4 and Section 22.5).

• The omp\_target\_is\_accessible routine was added to test whether a host address is accessible from a given device (see Section 25.2.2).

• The omp\_get\_mapped\_ptr routine was added to support obtaining the device pointer that is associated with a host pointer for a given device (see Section 25.2.3).

• To support asynchronous device memory management, omp\_target\_memcpy\_async and omp\_target\_memcpy\_rect\_async routines were added (see Section 25.7.3 and Section 25.7.4).

• The omp\_calloc, omp\_realloc, omp\_aligned\_alloc and omp\_aligned\_calloc routines were added (see Chapter 27).

• The omp\_display\_env routine was added to provide information about ICVs and settings of environment variables (see Section 30.4).

• The ompt\_scope\_beginend value was added to the scope\_endpoint OMPT type to indicate the coincident beginning and end of a scope (see Section 33.27).

• The ompt\_state\_wait\_barrier\_implementation and ompt\_state\_wait\_barrier\_teams values were added to the state OMPT type (see Section 33.31).

• The ompt\_sync\_region\_barrier\_implicit\_workshare, ompt\_sync\_region\_barrier\_implicit\_parallel, and ompt\_sync\_region\_barrier\_teams values were added to the sync\_region OMPT type (see Section 33.33).

• Values for asynchronous data transfers were added to the target\_data\_op OMPT type (see Section 33.35).

• The error callback was added (see Section 34.2).

• The target\_data\_op\_emi, target\_emi, target\_map\_emi, and target\_submit\_emi callbacks were added to support external monitoring interfaces (see Section 35.7, Section 35.8, Section 35.9 and Section 35.10).

## B.5 Version 4.5 to 5.0 Differences

• The memory model was extended to distinguish diferent types of flushes according to specified flush properties (see Section 1.3.4) and to define a happens-before order based on synchronizing flushes (see Section 1.3.5).

• Various changes throughout the specification were made to provide initial support of C11, C++11, C++14, C++17 and Fortran 2008 (see Section 1.6).

• Full support of Fortran 2003 was completed (see Section 1.6).

• The target-ofload-var ICV (see Chapter 3) and the OMP\_TARGET\_OFFLOAD environment variable (see Section 4.3.9) were added to support runtime control of the execution of device constructs.

• Control over whether nested parallelism is enabled or disabled was integrated into the max-active-levels-var ICV (see Section 3.2), the default value of which was made implementation defined, unless determined according to the values of the OMP\_NUM\_THREADS (see Section 4.1.3) or OMP\_PROC\_BIND (see Section 4.1.7) environment variables.

• The OMP\_DISPLAY\_AFFINITY (see Section 4.3.4) and OMP\_AFFINITY\_FORMAT (see Section 4.3.5) environment variables and the omp\_set\_affinity\_format (see Section 29.8), omp\_get\_affinity\_format (see Section 29.9),

omp\_display\_affinity (see Section 29.10), and omp\_capture\_affinity (see Section 29.11) routines were added to provide OpenMP runtime thread afinity information.

• The omp\_set\_nested and omp\_get\_nested routines and the OMP\_NESTED environment variable were deprecated.

• Support for array shaping (see Section 5.2.4) and for array sections with non-unit strides in C and C++ (see Section 5.2.5) was added to facilitate specification of discontiguous storage, and the target\_update construct (see Section 15.9) and the depend clause (see Section 17.9.5) were extended to allow the use of shape-operators (see Section 5.2.4).

• The iterator modifier (see Section 5.2.6) was added to support expressions in a list that expand to multiple expressions.

• The canonical loop nest form was defined for Fortran and, for all base languages, extended to permit non-rectangular loops (see Section 6.4.1).

• The relational-op in a canonical loop nest for C/C++ was extended to include != (see Section 6.4.1).

• To support conditional assignment to lastprivate variables, the conditional modifier was added to the lastprivate clause (see Section 7.5.5).

• The semantics of the use\_device\_ptr clause for pointer variables was clarified and the use\_device\_addr clause for using the device address of non-pointer variables inside the target\_data construct was added (see Section 7.5.8, Section 7.5.10 and Section 15.7).

• The inscan modifier for the reduction clause (see Section 7.6.10) and the scan directive (see Section 7.7) were added to support inclusive scan and exclusive scan computations.

• To support task reductions, the task modifier was added to the reduction clause (see Section 7.6.10), the task\_reduction clause (see Section 7.6.11) was added to the taskgroup construct (see Section 17.4), and the in\_reduction clause (see Section 7.6.12) was added to the task (see Section 14.1) and target (see Section 15.8) constructs.

• To support taskloop reductions, the reduction (see Section 7.6.10) and in\_reduction (see Section 7.6.12) clauses were added to the taskloop construct (see Section 14.2).

• The description of the map clause was modified to clarify the mapping order when multiple map-type modifiers are specified for a variable or structure members of a variable on the same construct. The close-modifier was added as a hint for the runtime to allocate memory close to the target device (see Section 7.9.6).

• The capability to map C/C++ pointer variables and to assign the address of device memory that is mapped by an array section to them was added. Support for mapping of Fortran pointer and allocatable variables, including pointer and allocatable components of variables, was added (see Section 7.9.6).

• All uses of the map clause (see Section 7.9.6), as well as the to and from clauses on the target\_update construct (see Section 15.9) and the depend clause on task-generating constructs (see Section 17.9.5) were extended to allow any lvalue expression as a list item for C/C++.

• The defaultmap clause (see Section 7.9.9) was extended to allow specification of the data-mapping attributes or data-sharing attributes for any of the scalar, aggregate, pointer, or allocatable classes on a per-region basis. Additionally, the none argument was added to support the requirement that all variables referenced in the construct must be explicitly mapped or privatized.

• The declare\_mapper directive was added to support mapping of data types with direct and indirect members (see Section 7.9.10).

• Predefined memory spaces, predefined memory allocators and allocator traits and directives, clauses and routines (see Chapter 8 and Chapter 27) to use them were added to support diferent kinds of memories.

• Metadirectives (see Section 9.4) and declare variant directives (see Section 9.6) were added to support selection of directive variants and function variants at a call site, respectively, based on compile-time traits of the enclosing context.

• Support for nested declare target directives was added (see Section 9.9).

• To reduce programmer efort, implicit declare target directives for some procedures were added (see Section 9.9 and Section 15.8).

• The requires directive (see Section 10.5) was added to support applications that require implementation-specific features.

• The teams construct (see Section 12.2) was extended to support execution on the host device without an enclosing target construct (see Section 15.8).

• The loop construct and the order clause with the concurrent argument were added to support compiler optimization and parallelization of loops for which logical iterations may execute in any order, including concurrently (see Section 12.3 and Section 13.8).

• The collapse of afected loops that are imperfectly nested loops was defined for simd constructs (see Section 12.4), worksharing-loop constructs (see Section 13.6), distribute constructs (see Section 13.7) and taskloop constructs (see Section 14.2).

• The simd construct (see Section 12.4) was extended to accept the if and nontemporal clauses and, with the concurrent argument, order clauses and to allow the use of atomic constructs within it.

• The default ordering-modifier for the schedule clause on worksharing-loop constructs when the kind argument is not static and the ordered clause does not appear on the construct was changed to nonmonotonic (see Section 13.6.3).

• The clauses that can be specified on the task construct (see Section 14.1) were extended with the affinity clause (see Section 14.10) to support hints that indicate data afinity of explicit tasks.

• To support execution of detachable tasks, the detach clause for the task construct (see Section 14.1) and the omp\_fulfill\_event routine (see Section 23.2.1) were added.

• The taskloop construct (see Section 14.2) was added to the list of constructs that can be canceled by the cancel constructs (see Section 18.2).

• To support reverse-ofload regions, the ancestor modifier was added to the device clause for the target construct (see Section 15.2 and Section 15.8).

• The target\_update construct (see Section 15.9) was modified to allow array sections that specify discontiguous storage.

• The taskwait construct was extended to accept the depend clause (see Section 17.5 and Section 17.9.5).

• To support acquire and release semantics with weak memory ordering, the acq\_rel, acquire, and release clauses (see Section 17.8.1) were added to the atomic construct (see Section 17.8.5) and flush construct (see Section 17.8.6), and the memory ordering semantics of implicit flushes on various constructs and routines were clarified (see Section 17.8.7).

• The atomic construct was extended with the hint clause (see Section 17.8.5).

• To support mutually exclusive inout sets, a mutexinoutset task-dependence-type was added to the depend clause (see Section 17.9.1 and Section 17.9.5).

• The depend clause (see Section 17.9.5) was extended to support iterator modifiers and to support depend objects that can be created with the new depobj construct (see Section 17.9.3).

• New combined constructs (master taskloop, parallel master, parallel master taskloop, master taskloop simd and parallel master taskloop simd) (see Section 19.1) were added.

• Lock hints were renamed to synchronization hints, and the old names were deprecated (see Section 20.9.5).

• The omp\_get\_supported\_active\_levels routine was added to query the number of active levels of parallelism supported by the implementation (see Section 21.11).

• The omp\_get\_device\_num routine (see Section 24.4) was added to support determination of the device on which a thread is executing.

• The omp\_pause\_resource and omp\_pause\_resource\_all routines were added to allow the runtime to relinquish resources used by OpenMP (see Section 30.2.1 and Section 30.2.2).

• Support for a first-party tool interface (see Chapter 32) was added.

• Support for a third-party tool interface (see Chapter 38) was added.

• Stubs for runtime library routines (previously Appendix A) were moved to a separate document.

• Interface declarations (previously Appendix B) were moved to a separate document.

## B.6 Version 4.0 to 4.5 Differences

• Support for several features of Fortran 2003 was added (see Section 1.6).

• The OMP\_MAX\_TASK\_PRIORITY environment variable was added to control the maximum task priority value allowed (see Section 4.3.11).

• The if clause was extended to accept a directive-name-modifier that allows it to apply to combined constructs (see Section 5.4 and Section 5.5).

• An argument was added to the ordered clause of the worksharing-loop construct and the ordered construct was modified to support doacross loop nests (see Section 6.4.6, Section 13.6 and Section 17.10.2)

• The implicitly determined data-sharing attribute for scalar variables in target regions was changed to firstprivate (see Section 7.1.1).

• Use of some C++ reference types was allowed in some data-sharing attribute clauses (see Section 7.5).

• The private, firstprivate and defaultmap clauses were added to the target construct (see Section 7.5.3, Section 7.5.4, Section 7.9.9 and Section 15.8).

• The linear-modifier was added to the linear clause (see Section 7.5.6).

• The linear clause was added to the worksharing-loop construct (see Section 7.5.6 and Section 13.6).

• To support interaction with native device implementations, the is\_device\_ptr clause was added to the target construct and the use\_device\_ptr clause was added to the target\_data construct (see Section 7.5.7, Section 7.5.8, Section 15.7 and Section 15.8).

• Semantics for reductions on C/C++ array sections were added and restrictions on the use of arrays and pointers in reductions were removed (see Section 7.6.10).

• Support was added to the map clause to handle structure elements (see Section 7.9.6).

• To support unstructured data mapping for devices, the map clause (see Section 7.9.6) was updated and the target\_enter\_data (see Section 15.5) and target\_exit\_data (see Section 15.6) constructs were added.

• The declare\_target directive was extended to allow mapping of global variables to be deferred to specific device executions and to allow an extended-list to be specified in C/C++ (see Section 9.9).

• The simdlen clause was added to the simd construct to support specification of the exact number of logical iterations desired per SIMD chunk (see Section 12.4).

• To support the use of the simd construct on loops with loop-carried backward dependences with or without a worksharing-loop construct, clauses were added to the ordered construct (see Section 12.4, Section 13.6) and Section 17.10).

• The task construct was extended to accept hints that the priority clause specifies (see Section 14.1 and Section 14.9).

• The taskloop construct was added to support nestable parallel loops that create explicit tasks (see Section 14.2).

• To improve support for asynchronous execution of target regions, the target construct was extended to accept the nowait and depend clauses (see Section 15.8, Section 17.6 and Section 17.9.5).

• The hint clause was added to the critical construct (see Section 17.2).

• The source and sink dependence types were added to the depend clause to support doacross loop nests (see Section 17.9.5).

• To support a more complete set of compound constructs for devices, the compound constructs target parallel, target parallel for (C/C++), target parallel for simd (C/C++), target parallel do (Fortran) and target parallel do simd (Fortran) were added (see Section 19.1).

• The omp\_get\_max\_task\_priority routine was added to return the maximum supported task priority value (see Section 23.1.1).

• Device memory routines were added to allow explicit memory allocations, deallocations and transfers and memory associations (see Chapter 25).

• The lock API was extended with lock routines that support storing a hint with a lock to select a desired lock implementation for the intended usage of the lock by the application code (see Section 28.1.3 and Section 28.1.4).

• Query routines for thread afinity were added (see Section 29.2 to Section 29.7).

• C/C++ grammar (previously Appendix B) was moved to a separate document.

## B.7 Version 3.1 to 4.0 Differences

• Various changes throughout the specification were made to provide initial support of Fortran 2003 (see Section 1.6).

• The OMP\_PLACES environment variable (see Section 4.1.6), the proc\_bind clause (see Section 12.1.3), and the omp\_get\_proc\_bind routine (see Section 29.1) were added to support thread afinity policies.

• The OMP\_CANCELLATION environment variable (see Section 4.3.6), the cancel construct (see Section 18.2), the cancellation point construct (see Section 18.3), and the omp\_get\_cancellation routine (see Section 30.1) were added to support the concept of cancellation.

• The OMP\_DEFAULT\_DEVICE environment variable (see Section 4.3.8), device constructs (see Chapter 15), and the omp\_get\_num\_teams, omp\_get\_team\_num, omp\_set\_default\_device, omp\_get\_default\_device, omp\_get\_num\_devices, and omp\_is\_initial\_device routines (see Chapter 22 and Chapter 24) were added to support execution on devices.

• The OMP\_DISPLAY\_ENV environment variable (see Section 4.7) was added to display the value of ICVs associated with the OpenMP environment variables.

• C/C++ array syntax was extended to support array sections (see Section 5.2.5).

• The reduction clause (see Section 7.6.10) was extended and the declare\_reduction construct (see Section 7.6.14) was added to support user-defined reductions.

• SIMD directives were added to support SIMD parallelism (see Section 12.4).

• Implementation defined task scheduling points for untied tasks were removed (see Section 14.14).

• The taskgroup construct (see Section 17.4) was added to support deep task synchronization.

• The atomic construct was extended to support atomic captured updates with the capture clause, to allow new atomic update forms, and to support sequentially consistent atomic operations with the seq\_cst clause (see Section 17.8.1.5, Section 17.8.3.1 and Section 17.8.5).

• The depend clause (see Section 17.9.5) was added to support task dependences.

• Examples (previously Appendix A) were moved to a separate document

## B.8 Version 3.0 to 3.1 Differences

• The bind-var ICV (see Section 3.1) and the OMP\_PROC\_BIND environment variable (see Section 4.1.7) were added to support control of whether threads are bound to processors.

• The nthreads-var ICV was modified to be a list of the number of threads to use at each nested parallel region level (see Section 3.1) and the algorithm for determining the number of threads used in a parallel region was modified to handle a list (see Section 12.1.1).

• Data environment restrictions were changed to allow intent(in) and const-qualified types for the firstprivate clause (see Section 7.5.4).

• Data environment restrictions were changed to allow Fortran pointers in firstprivate (see Section 7.5.4) and lastprivate (see Section 7.5.5) clauses.

• New reduction operators min and max were added for C/C++ (see Section 7.6.3).

• The mergeable and final clauses (see Section 14.5 and Section 14.7) were added to the task construct (see Section 14.1) to support optimization of task data environments.

• The taskyield construct was added to allow user-defined task scheduling points (see Section 14.12).

• The atomic construct was extended to include read, write, and capture forms, and an update clause was added to apply the already existing form of the atomic construct (see Section 17.8.2, Section 17.8.3.1 and Section 17.8.5).

• The nesting restrictions were clarified to disallow closely nested regions within an atomic region so that an atomic region can be consistently defined with other regions to include all code in the atomic construct (see Section 19.1).

• The omp\_in\_final routine was added to support specialization of final task regions (see Section 23.1.3).

• Descriptions of examples (previously Appendix A) were expanded and clarified.

• Incorrect use of omp\_integer\_kind in Fortran interfaces was replaced with selected\_int\_kind(8).

## B.9 Version 2.5 to 3.0 Differences

• The concept of tasks was added to the execution model (see Section 1.2 and Chapter 2).

• The OpenMP memory model was extended to cover atomicity of memory accesses (see Section 1.3.1). The description of the behavior of volatile in terms of flushes was removed.

• The definition of active parallel region was changed so that a parallel region is active if it is executed by a team to which more than one thread is assigned (see Chapter 2).

• The definition of the nest-var, dyn-var, nthreads-var and run-sched-var ICVs were modified to provide one copy of these ICVs per task instead of one copy for the whole OpenMP program (see Section 3.1). The omp\_set\_num\_threads and omp\_set\_dynamic routines were specified to support their use from inside a parallel region (see Section 21.1 and Section 21.7).

• The thread-limit-var ICV, the OMP\_THREAD\_LIMIT environment variable and the omp\_get\_thread\_limit routine were added to support control of the maximum number of threads (see Section 3.1, Section 4.1.4 and Section 21.5).

• The max-active-levels-var ICV, the OMP\_MAX\_ACTIVE\_LEVELS environment variable and the omp\_set\_max\_active\_levels and omp\_get\_max\_active\_levels routines, and were added to support control of the number of nested active parallel regions (see Section 3.1, Section 4.1.5, Section 21.12 and Section 21.13).

• The stacksize-var ICV and the OMP\_STACKSIZE environment variable were added to support control of thread stack sizes (see Section 3.1 and Section 4.3.2).

• The wait-policy-var ICV and the OMP\_WAIT\_POLICY environment variable were added to control the desired behavior of waiting threads (see Section 3.1 and Section 4.3.3).

• Predetermined data-sharing attributes were defined for Fortran assumed-size arrays (see Section 7.1.1).

• Static class member variables were allowed in threadprivate directives (see Section 7.3).

• Invocations of constructors and destructors for private and threadprivate class type variables were clarified (see Section 7.3, Section 7.5.3, Section 7.5.4, Section 7.8.1 and Section 7.8.2).

• The use of Fortran allocatable arrays was allowed in private, firstprivate, lastprivate, reduction, copyin and copyprivate clauses (see Section 7.3, Section 7.5.3, Section 7.5.4, Section 7.5.5, Section 7.6.10, Section 7.8.1 and Section 7.8.2).

• Support for firstprivate was added to the default clause in Fortran (see Section 7.5.1).

• Implementations were precluded from using the storage of the original list item to hold the new list item on the primary thread for list item in the private clause, and the value was made well defined on exit from the parallel region if no attempt is made to reference the original list item inside the parallel region (see Section 7.5.3).

• Determination of the number of threads in parallel regions was updated (see Section 12.1.1).

• The assignment of logical iterations to threads in a worksharing-loop construct with a static schedule kind was made deterministic (see Section 13.6).

• The worksharing-loop construct was extended to support association with more than one perfectly nested loop through the collapse clause (see Section 13.6).

• Loop-iteration variables for worksharing-loop constructs were allowed to be random access iterators or of unsigned integer type (see Section 13.6).

• The schedule kind auto was added to allow the implementation to choose any possible mapping of logical iterations in a worksharing-loop constructs to threads in the team (see Section 13.6).

• The task construct was added to support explicit tasks (see Section 14.1).

• The taskwait construct was added to support task synchronization (see Section 17.5).

• The omp\_set\_schedule and omp\_get\_schedule routines were added to set and to retrieve the value of the run-sched-var ICV (see Section 21.9 and Section 21.10).

• The omp\_get\_level routine was added to return the number of nested parallel regions that enclose the task that contains the call (see Section 21.14).

• The omp\_get\_ancestor\_thread\_num routine was added to return the thread number of the ancestor thread of the current thread (see Section 21.15).

• The omp\_get\_team\_size routine was added to return the size of the team to which the ancestor thread of the current thread belongs (see Section 21.16).

• The omp\_get\_active\_level routine was added to return the number of active parallel regions that enclose the task that contains the call (see Section 21.17).

• Lock ownership was defined in terms of tasks instead of threads (see Chapter 28).

## C Nesting of Regions

This appendix describes a set of restrictions on the nesting of regions. The restrictions on nesting are as follows:

• A teams region must be strictly nested either within the implicit parallel region that surrounds the whole OpenMP program or within a target region. If a teams construct is nested within a target construct, that target construct must contain no statements, declarations or directives outside of the teams construct (see Section 12.2).

• Only regions that are generated by teams-nestable constructs or teams-nestable routines may be strictly nested regions of teams regions (see Section 12.2).

• The only routines for which a call may be nested inside a region that corresponds to a construct on which the order clause is specified with concurrent as the ordering argument are order-concurrent-nestable routines (see Section 12.3).

• Only regions that correspond to order-concurrent-nestable constructs or order-concurrent-nestable routines may be strictly nested regions of regions that correspond to constructs on which the order clause is specified with concurrent as the ordering argument (see Section 12.3).

• The only OpenMP constructs that can be encountered during execution of a simd region are SIMDizable constructs (see Section 12.4).

• A team-executed region may not be closely nested inside a partitioned worksharing region, a region that corresponds to a thread-exclusive construct, or a region that corresponds to a task-generating construct that is not a team-generating construct. This follows from various restrictions requiring, in general, that team-executed regions (which include worksharing regions and barrier regions) are executed by all threads in a team or by none at all (see Chapter 13 and Section 17.3.1).

• A distribute region must be strictly nested inside a teams region (see Section 13.7).

• A loop region that binds to a teams region must be strictly nested inside a teams region (see Section 13.8.1).

• During execution of a target region, other than target constructs for which a device clause on which the ancestor device-modifier appears, device-afecting constructs must not be encountered (see Section 15.8).

• A critical region must not be nested (closely or otherwise) inside a critical region with the same name (see Section 17.2).

• OpenMP constructs may not be encountered during execution of an atomic region (see Section 17.8.5).

• An ordered region that corresponds to an ordered construct with the threads or doacross clause may not be closely nested inside a critical, ordered, loop, task, or taskloop region (see Section 17.10).
