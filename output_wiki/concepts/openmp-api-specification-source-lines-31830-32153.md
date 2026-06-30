# OpenMP-API-Specification Source Lines 31830-32153

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L31830-L32153

Citation: [OpenMP-API-Specification:L31830-L32153]

````text
## B Features History

This appendix summarizes the major changes between OpenMP API versions since version 2.5.

## B.1 Deprecated Features

The following features were deprecated in Version 6.0:

Fortran

• Omitting the optional white space to separate adjacent keywords in the directive-name in free source form and fixed source form directives is deprecated (see Section 5.1.1 and Section 5.1.2).

## Fortran

• The syntax of the declare\_reduction directive that specifies the combiner expression in the directive argument was deprecated (see Section 7.6.14).

• The Fortran include file omp\_lib.h has been deprecated (see Chapter 20).

• The target, target\_data\_op, target\_submit and target\_map values of the callbacks OMPT types and the associated trace record OMPT type names were deprecated (see Section 33.6).

The ompt\_target\_data\_transfer\_to\_device, ompt\_target\_data\_transfer\_from\_device, ompt\_target\_data\_transfer\_to\_device\_async, and ompt\_target\_data\_transfer\_from\_device\_async values in the target\_data\_op OMPT type were deprecated (see Section 33.35).

• The target\_data\_op, target, target\_map and target\_submit callbacks and the associated trace record OMPT type names were deprecated (see Section 35.7, Section 35.8, Section 35.9 and Section 35.10).

## B.2 Version 5.2 to 6.0 Differences

• All features deprecated in versions 5.0, 5.1 and 5.2 were removed.

• Full support for C23, C++23, and Fortran 2023 was added (see Section 1.6).

• Full support of Fortran 2018 was completed (see Section 1.6).

• The environment variable syntax was extended to support initializing ICVs for the host device and non-host devices with a single environment variable (see Section 3.2 and Chapter 4).

• The handling of the nthreads-var ICV was updated (see Section 3.4) and the nthreads argument of the num\_threads clause was changed to a list (see Section 12.1.2) to support context-specific reservation of inner parallelism.

• Numeric abstract name values are now allowed for the OMP\_NUM\_THREADS, OMP\_THREAD\_LIMIT and OMP\_TEAMS\_THREAD\_LIMIT environment variables (see Section 4.1.3, Section 4.1.4 and Section 4.2.2).

• The environment variable OMP\_PLACES was extended to support an increment between consecutive places when creating a place list from an abstract name (see Section 4.1.6).

• The environment variable OMP\_AVAILABLE\_DEVICES was added and the environment variable OMP\_DEFAULT\_DEVICE was extended to support device selection by traits (see Section 4.3.7 and Section 4.3.8).

• The uid trait was added to the permissible traits in the environment variables OMP\_AVAILABLE\_DEVICES and OMP\_DEFAULT\_DEVICE and to the target device trait set (see Section 4.3.7, Section 4.3.8 and Section 9.2).

• The environment variable OMP\_THREADS\_RESERVE was added to reserve a number of structured threads and free-agent threads (see Section 4.3.10).

C++

• The decl attribute was added to improve the attribute syntax for declarative directives (see Section 5.1).

C++

• The OpenMP directive syntax was extended to include C attribute specifiers (see Section 5.1).

Fortran

• Support for directives with the pure property in DO CONCURRENT constructs has been added (see Section 5.1).

Fortran

• To improve consistency in clause format, all inarguable clauses were extended to take an optional argument for which the default value yields equivalent semantics to the existing inarguable semantics (see Section 5.2).

• The adjust\_args clause was extended to support positional specification of arguments (see Section 5.2.1 and Section 9.6.2)

## Fortran

• The definitions of locator list items and assignable OpenMP types were extended to include function references that have data pointer results (see Section 5.2.1).

Fortran

## C / C++

• The array section definition was extended to permit, where explicitly allowed, omission of the length when the size of the array dimension is not known (see Section 5.2.5).

## C / C++

• To support greater specificity on compound constructs, all clauses were extended to accept the directive-name-modifier, which identifies the constituent directives to which the clause applies (see Section 5.4).

• To allow specification of all modifiers of the init clause, extensions to the interop operation of the append\_args clause were added (see Section 5.6 and Section 9.6.3).

• The init clause was added to the depobj construct, and the construct now permits repeatable init, update, and destroy clauses (see Section 5.6 and Section 17.9.3).

• The syntax that omits the argument to the destroy clause for the depobj construct was undeprecated (see Section 5.7).

## Fortran

• Atomic structured blocks were extended to allow the BLOCK construct, pointer assignments and two intrinsic functions for enum and enumeration types (see Section 6.3.3).

• conditional-update-statement was extended to allow more forms and comparisons (see Section 6.3.3).

## Fortran

• The concept of canonical loop sequences and the looprange clause were defined (see Section 6.4.2 and Section 6.4.7).

## Fortran

• For polymorphic types, restrictions were changed and behavior clarified for data-sharing attribute clauses and data-mapping attribute clauses (see Chapter 7).

## Fortran

• The saved modifier, the replayable clause, and the taskgraph construct were added to support the recording and eficient replay execution of a sequence of task-generating constructs (see Section 7.2, Section 14.6, and Section 14.3).

• The default clause is now allowed on the target directive, and, similarly to the defaultmap clause, now accepts the variable-category modifier (see Section 7.5.1).

• The semantics of the use\_device\_ptr and use\_device\_addr clauses on a target\_data construct were altered to imply a reference count update on entry and exit from the region for the corresponding objects that they reference in the device data environment (see Section 7.5.8 and Section 7.5.10).

• Support for induction operations was added (see Section 7.6) through the induction clause (see Section 7.6.13) and the declare\_induction directive (see Section 7.6.17), which supports user-defined induction.

• Support for reductions over private variables with the reduction clause has been added (see Section 7.6).

C++

• The circumstances under which implicitly declared reduction identifiers are supported for variables of class type were clarified (see Section 7.6.3 and Section 7.6.6).

C++

• The scan directive was extended to accept the init\_complete clause to enable the identification of an initialization phase within the final-loop-body of an enclosing simd construct or worksharing-loop construct (or a composite construct that combines them) (see Section 7.7 and Section 7.7.3).

• The storage map-type modifier was added as the preferred map-type when the mapping operation only allocates or releases storage on the target device (see Section 7.9.1).

• The ref modifier was added to the map clause to add more control over how the clause afects list items that are C++ references or Fortran pointer/allocatable variables (see Section 7.9.5 and Section 7.9.6).

• The property of the map-type modifier was changed to default so that it can be freely placed and omitted even if other modifiers are used (see Section 7.9.6).

• The self map-type-modifier was added to the map clause and the self implicit-behavior was added to the defaultmap clause to request explicitly that the corresponding list item refers to the same object as the original list item (see Section 7.9.6 and Section 7.9.9).

• The map clause was extended to permit mapping of assumed-size arrays (see Section 7.9.6).

• The delete keyword on the map clause was reformulated to be the delete-modifier (see Section 7.9.6).

## Fortran

• The automap modifier was added to the enter clause to support automatic mapping and unmapping of Fortran allocatable variables when allocated and deallocated, respectively (see Section 7.9.7).

## Fortran

• The groupprivate directive was added to specify that variables should be privatized with respect to a contention group (see Section 7.13).

• The local clause was added to the declare\_target directive to specify that variables should be replicated locally for each device (see Section 7.14).

• The allocator trait omp\_atk\_part\_size was added to specify the size of the omp\_atv\_interleaved allocator partitions (see Section 8.2).

• The omp\_atk\_pin\_device, omp\_atk\_preferred\_device and omp\_atk\_target\_access memory allocator traits were defined to provide greater control of memory allocations that may be accessible from multiple devices (see Section 8.2).

• The device value of the access allocator trait was defined as the default access allocator trait and to provide the semantics that an allocator with the trait corresponds to memory that all threads on a specific device can access. The semantics of an allocator with the all value were updated to correspond to memory that all threads in the system can access (see Section 8.2).

• The omp\_atv\_partitioner value was added to the possible values of the omp\_atk\_partition allocator trait to allow ad-hoc user partitions (see Section 8.2).

• The uses\_allocators clause was extended to permit more than one clause-argument-specification (see Section 8.8).

• The need\_device\_addr modifier was added to the adjust\_args clause to support adjustment of arguments passed by reference (see Section 9.6.2).

• The dispatch construct was extended with the interop clause to support appending arguments specific to a call site (see Section 9.7 and Section 9.7.1).

C / C++

• A declare\_target directive that specifies list items must now be placed at the same scope as the declaration of those list items, and if the directive does not specify list items then it is treated as declaration-associated (see Section 9.9.1).

C / C++

• The message and severity clauses were added to the parallel directive to support customization of any error termination associated with the directive (see Section 10.3, Section 10.4, and Section 12.1).

• The self\_maps requirement clause was added to require that all mapping operations are self maps (see Section 10.5.1.6).

• The assumption clause group was extended with the no\_openmp\_constructs clause to support identification of regions in which no constructs will be encountered (see Section 10.6.1 and Section 10.6.1.5).

• A restriction for loop-transforming constructs was added that the generated loop must not be a doacross-afected loop, which implies that, in an unroll construct with an unroll-factor of one, a stand-alone ordered directive is now non-conforming (see Chapter 11, Section 11.9 and Section 17.10.1).

• The apply clause was added to enable more flexible composition of loop-transforming constructs (see Section 11.1).

• The sizes clause was updated to allow non-constant list items (see Section 11.2).

• The fuse construct was added to fuse two or more loops in a canonical loop sequence (see Section 11.3).

• The interchange construct was added to permute the order of loops in a loop nest (see Section 11.4).

• The reverse construct was added to reverse the iteration order of a loop (see Section 11.5).

• The split loop-transforming construct was added to apply index-set splitting to canonical loop nests (see Section 11.6).

• The stripe loop-transforming construct was added to apply striping to canonical loop nests (see Section 11.7).

• The tile construct was extended to allow grid loops and tile loops to be afected by the same construct (see Section 11.8).

• The prescriptiveness modifier was added to the num\_threads clause and strict semantics were defined for the clause (see Section 12.1.2).

• To control which synchronizing threads are guaranteed to make progress eventually, the safesync clause on the parallel construct (see Section 12.1.5), the omp\_curr\_progress\_width identifier (see Section 20.1) and the omp\_get\_max\_progress\_width routine were addded (see Section 24.6).

• To make the loop construct and other constructs that specify the order clause with concurrent ordering more usable, calls to procedures in the region may now contain certain OpenMP directives (see Section 12.3).

• To support a wider range of synchronization choices, the atomic construct was added to the constructs that may be encountered inside a region that corresponds to a construct with an order clause that specifies concurrent (see Section 12.3).

• The constructs that may be encountered during the execution of a region that corresponds to a construct on which the order clause is specified with concurrent ordering, when the corresponding regions are not strictly nested regions, are no longer restricted (see Section 12.3).

## Fortran

• The workdistribute directive was added to support Fortran array expressions in teams constructs (see Section 13.5).

• The loop construct was extended to allow a DO CONCURRENT loop as the collapsed loop (see Section 13.8).

## Fortran

• The taskloop construct now includes the task\_iteration directive as a subsidiary directive so that the tasks that it generates can include the semantics of the affinity and depend clauses (see Section 14.2, Section 14.2.3, Section 14.10 and Section 17.9.5).

• The threadset clause was added to task-generating constructs to specify the binding thread set of the generated task (see Section 14.8).

• The priority clause was added to the target\_enter\_data, target\_exit\_data, target\_data, target and target\_update directives (see Section 14.9, Section 15.5, Section 15.6, Section 15.7, Section 15.8 and Section 15.9).

• The device\_type clause was added to the clauses that may appear on the target construct (see Section 15.1 and Section 15.8).

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
````
