## 8 Memory Management

This chapter defines directives, clauses and related concepts for managing memory used by OpenMP programs.

## 8.1 Memory Spaces

OpenMP memory spaces represent storage resources where variables can be stored and retrieved. Table 8.1 shows the list of predefined memory spaces. The selection of a given memory space expresses an intent to use storage with certain traits for the allocations. The actual storage resources that each memory space represents are implementation defined.

TABLE 8.1: Predefined Memory Spaces

<table><tr><td>Memory space name</td><td>Storage selection intent</td></tr><tr><td>omp_default_mem_space</td><td>Represents the system default storage</td></tr><tr><td>omp_large_cap_mem_space</td><td>Represents storage with large capacity</td></tr><tr><td>omp_const_mem_space</td><td>Represents storage optimized for variables with constant values</td></tr><tr><td>omp_high_bw_mem_space</td><td>Represents storage with high bandwidth</td></tr><tr><td>omp_low_lat_mem_space</td><td>Represents storage with low latency</td></tr></table>

Variables allocated in the omp\_const\_mem\_space memory space may be initialized through the firstprivate clause or with compile-time constants for static and constant variables. Implementation defined mechanisms to provide the constant value of these variables may also be supported.

## Restrictions

Restrictions to OpenMP memory spaces are as follows:

• Variables in the omp\_const\_mem\_space memory space may not be written.

## 8.2 Memory Allocators

OpenMP memory allocators can be used by an OpenMP program to make allocation requests. When a memory allocator receives a request to allocate storage of a certain size, an allocation of logically contiguous memory in the resources of its associated memory space of at least the size that was requested will be returned if possible. This allocation will not overlap with any other existing allocation from a memory allocator.

If an allocator is used to allocate memory for a variable with static storage duration that is not a local static variable then the task that requested the allocation is unspecified. If an allocator is used to allocate memory for a local static variable then the task that requested the allocation is considered to be the current task of the first thread that executes code in which the variable is visible.

The behavior of the allocation process can be afected by the allocator traits that the user specifies. Table 8.2 shows the allowed allocator traits, their possible values and the default value of each trait.

TABLE 8.2: Allocator Traits

<table><tr><td>Allocator Trait</td><td>Allowed Values</td><td>Default Value</td></tr><tr><td>sync_hint</td><td>contended, uncontended, serialized, private</td><td>contended</td></tr><tr><td>alignment</td><td>Non-negative integer powers of 2</td><td>1 byte</td></tr><tr><td>access</td><td>all, memspace, device, cgroup, pteam, thread</td><td>memspace</td></tr><tr><td>pool_size</td><td>Any positive integer</td><td>Implementation defined</td></tr><tr><td>fallback</td><td>default_mem_fb, null_fb, abort_fb, allocator_fb</td><td>See below</td></tr><tr><td>fb_data</td><td>An allocator handle</td><td>(none)</td></tr><tr><td>pinned</td><td>true,false</td><td>false</td></tr><tr><td>partition</td><td>environment, nearest, blocked, interleaved, partitioner</td><td>environment</td></tr><tr><td>pin_device</td><td>Conforming device number</td><td>(none)</td></tr><tr><td>preferred_device</td><td>Conforming device number</td><td>(none)</td></tr><tr><td>target_access</td><td>single, multiple</td><td>single</td></tr><tr><td>atomic_scope</td><td>all, device</td><td>device</td></tr></table>

table continued on next page

table continued from previous page

<table><tr><td>Allocator Trait</td><td>Allowed Values</td><td>Default Value</td></tr><tr><td>part_size</td><td>Positive integer value</td><td>Implementation defined</td></tr><tr><td>partitioner</td><td>A memory partitioner handle</td><td>(none)</td></tr><tr><td>partitioner_arg</td><td>An integer value</td><td>0</td></tr></table>

The sync\_hint trait describes the expected manner in which multiple threads may use the allocator. The values and their descriptions are:

• contended: high contention is expected on the allocator; that is, many tasks are expected to request allocations simultaneously;

• uncontended: low contention is expected on the allocator; that is, few tasks are expected to request allocations simultaneously;

• serialized: one task at a time will request allocations with the allocator. Requesting two allocations simultaneously when specifying serialized results in unspecified behavior; and

• private: the same thread will execute all tasks that request allocations with the allocator. Requesting an allocation from tasks that diferent threads execute, simultaneously or not, when specifying private results in unspecified behavior.

Allocated memory will be byte aligned to at least the value specified for the alignment trait of the allocator. Some directives and routines can specify additional requirements on alignment beyond those described in this section.

The access trait defines the access group of tasks that may access memory that is allocated by a memory allocator. If the value is all, the access group consists of all tasks that execute on all available devices. If the value is memspace, the access group consists of all tasks that execute on all devices that are associated with the allocator. If the value is device, the access group consists of all tasks that execute on the device where the allocation was requested. If the value is cgroup, the access group consists of all tasks in the same contention group as the task that requested the allocation. If the value is pteam, the access group consists of all current team tasks of the innermost enclosing parallel region in which the allocation was requested. If the value is thread, the access group consists of all tasks that are executed by the same thread that executed the allocation request. Memory returned by the allocator will be memory accessible by all tasks in the same access group as the task that requested the allocation. Attempts to access this memory from a task that is not in same access group results in unspecified behavior.

The total amount of storage in bytes that an allocator can use for allocation requests from tasks in the same access group is limited by the pool\_size trait. Requests that would result in using more storage than pool\_size will not be fulfilled by the allocator.

The fallback trait specifies how the memory allocator behaves when it cannot fulfill an allocation request. If the fallback trait is set to null\_fb, the allocator returns the value zero if it fails to allocate the memory. If the fallback trait is set to abort\_fb, the behavior is as if an error directive for which sev-level is fatal and action-time is execution is encountered if the allocation fails. If the fallback trait is set to allocator\_fb then when an allocation fails the request will be delegated to the allocator specified in the fb\_data trait. If the fallback trait is set to default\_mem\_fb then when an allocation fails another allocation will be tried in omp\_default\_mem\_space, which assumes all allocator traits to be set to their default values except for fallback trait, which will be set to null\_fb. The default value for the fallback trait is null\_fb for any allocator that is associated with a target memory space. Otherwise, the default value is default\_mem\_fb.

All memory that is allocated with an allocator for which the pinned trait is specified as true must remain in the same storage resource at the same location for its entire lifetime. If pin\_device is also specified then the allocation must be allocated in that device.

The partition trait describes the partitioning of allocated memory over the storage resources represented by the memory space associated with the allocator. The partitioning will be done in parts with a minimum size that is implementation defined. The values are:

• environment: the placement of allocated memory is determined by the execution environment;

• nearest: allocated memory is placed in the storage resource that is nearest to the thread that requests the allocation;

• blocked: allocated memory is partitioned into parts of approximately the same size with at most one part per storage resource; and

• interleaved: allocated memory parts are distributed in a round-robin fashion across the storage resources such that the size of each part is the value of the part\_size trait except possibly the last part, which can be smaller.

• partitioner: the number of memory parts and how they are distributed across the storage are defined by the memory partition object created by the memory partitioner specified by the partitioner trait.

The part\_size trait specifies the size of the parts allocated over the storage resources for some of the memory partition trait policies. The actual value of the trait might be rounded up to an implementation defined value to comply with hardware restrictions of the storage resources.

If the preferred\_device trait is specified then storage resources of the specified device are preferred to fulfill the allocation.

If the value of the target\_access trait is single then data from this allocator cannot be accessed on two diferent devices unless, for any given host device access, the entry and exit of the target region in which any accesses occur either both precede or both follow the host device access in happens-before order. Additionally, for any two target regions that may access data

from this allocator and execute on distinct devices, the entry and exit of one of the regions must precede those of the other in happens-before order. If the value of the target\_access trait is multiple then accesses of data from this allocator from diferent devices may be arbitrarily interleaved, provided that synchronization ensures data races do not occur.

If the value of the atomic\_scope trait is all then all storage locations of data from this allocator have an atomic scope that consists of all threads on the devices associated with the allocator. If the value is device then all storage locations have an atomic scope that consists of all threads on the device on which the atomic operation is performed.

Table 8.3 shows the list of predefined memory allocators and their associated memory spaces. The predefined memory allocators have default values for their allocator traits unless otherwise specified.

TABLE 8.3: Predefined Allocators

<table><tr><td>Allocator Name</td><td>Associated Memory Space</td><td>Non-Default Trait Values</td></tr><tr><td>omp_default_mem_alloc</td><td>omp_default_mem_space</td><td>fallback:null_fb</td></tr><tr><td>omp_large_cap_mem_alloc</td><td>omp_large_cap_mem_space</td><td>(none)</td></tr><tr><td>omp_const_mem_alloc</td><td>omp_const_mem_space</td><td>(none)</td></tr><tr><td>omp_high_bw_mem_alloc</td><td>omp_high_bw_mem_space</td><td>(none)</td></tr><tr><td>omp_low_lat_mem_alloc</td><td>omp_low_lat_mem_space</td><td>(none)</td></tr><tr><td>omp_cgroup_mem_alloc</td><td>Implementation defined</td><td>access:cgroup</td></tr><tr><td>omp_pteam_mem_alloc</td><td>Implementation defined</td><td>access:pteam</td></tr><tr><td>omp_thread_mem_alloc</td><td>Implementation defined</td><td>access:thread</td></tr></table>

If any operation of the base language causes a reallocation of a variable that is allocated with a memory allocator then that memory allocator will be used to deallocate the current memory and to allocate the new memory. For any allocatable subcomponents, the allocator that is used for the deallocation and allocation is unspecified.

## Restrictions

• If the pin\_device trait is specified, its value must be the device number of a device associated with the memory allocator.

• If the preferred\_device trait is specified, its value must be the device number of a device associated with the memory allocator.

• The omp\_cgroup\_mem\_alloc, omp\_pteam\_mem\_alloc, and omp\_thread\_mem\_alloc predefined memory allocators must not be used to allocate a variable with static storage duration unless the variable is a local static variable.

## 8.3 align Clause

<table><tr><td>Name: align</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>alignment</td><td>expression of integer type</td><td>constant, positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

allocate

## Semantics

The align clause is used to specify the byte alignment to use for allocations associated with the construct on which the clause appears. Specifically, each allocation is byte aligned to at least the maximum of the value to which alignment evaluates, the alignment trait of the allocator being used for the allocation, and the alignment required by the base language for the type of the variable that is allocated. On constructs on which the clause may appear, if it is not specified then the efect is as if it was specified with the alignment trait of the allocator being used for the allocation.

## Restrictions

Restrictions to the align clause are as follows:

• alignment must evaluate to a power of two.

## Cross References

• allocate Directive, see Section 8.5

• Memory Allocators, see Section 8.2

## 8.4 allocator Clause

<table><tr><td>Name: allocator</td><td>Properties: ICV-defaulted, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>allocator</td><td>expression of allocator_-handle type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

allocate

## Semantics

The allocator clause specifies the memory allocator to be used for allocations associated with the construct on which the clause appears. Specifically, the allocator to which allocator evaluates is used for the allocations. On constructs on which the clause may appear, if it is not specified then the efect is as if it was specified with the value of the def-allocator-var ICV.

## Cross References

• allocate Directive, see Section 8.5

• Memory Allocators, see Section 8.2

• def-allocator-var ICV, see Table 3.1

## 8.5 allocate Directive

<table><tr><td>Name: allocateCategory: declarative</td><td>Association: explicitProperties: pure</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Clauses

align, allocator

## Semantics

The storage for each list item that appears in the allocate directive is provided an allocation through the memory allocator as determined by the allocator clause with an alignment as determined by the align clause. The scope of this allocation is that of the list item in the base language. At the end of the scope for a given list item the memory allocator used to allocate that list item deallocates the storage.

For allocations that arise from this directive the null\_fb value of the fallback allocator trait behaves as if the abort\_fb had been specified.

## Restrictions

Restrictions to the allocate directive are as follows:

• An allocate directive must appear in the same scope as the declarations of each of its list items and must follow all such declarations.

• A declared variable may appear as a list item in at most one allocate directive in a given compilation unit.

• allocate directives that appear in a target region must specify an allocator clause unless a requires directive with the dynamic\_allocators clause is present in the same compilation unit.

## C / C++

• If a list item has static storage duration, the allocator clause must be specified and the allocator expression in the clause must be a constant expression that evaluates to one of the predefined memory allocator values.

• A variable that is declared in a namespace or global scope may only appear as a list item in an allocate directive if an allocate directive that lists the variable follows a declaration that defines the variable and if all allocate directives that list it specify the same allocator.

• A list item must not be a function parameter.

C / C++ C

• After a list item has been allocated, the scope that contains the allocate directive must not end abnormally, such as through a call to the longjmp function.

• After a list item has been allocated, the scope that contains the allocate directive must not end abnormally, such as through a call to the longjmp function, other than through C++ exceptions.

• A variable that has a reference type must not appear as a list item in an allocate directive.

• A list item that is specified in an allocate directive must not be a coarray or have a coarray as an ultimate component, or have the ALLOCATABLE, or POINTER attribute.

• If a list item has the SAVE attribute, either explicitly or implicitly, or is a common block name then the allocator clause must be specified and only predefined memory allocator parameters can be used in the clause.

• A variable that is part of a common block must not be specified as a list item in an allocate directive, except implicitly via the named common block.

• A named common block may appear as a list item in at most one allocate directive in a given compilation unit.

• If a named common block appears as a list item in an allocate directive, it must appear as a list item in an allocate directive that specifies the same allocator in every compilation unit in which the common block is used.

• An associate name must not appear as a list item in an allocate directive.

• A list item must not be a dummy argument.

## Cross References

• align Clause, see Section 8.3

• allocator Clause, see Section 8.4

• Memory Allocators, see Section 8.2

## 8.6 allocate Clause

<table><tr><td>Name: allocate</td><td>Properties: all-privatizing</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>allocator-simple-modifier</td><td>list</td><td>expression of OpenMP allocator_handle type</td><td>exclusive, unique</td></tr><tr><td>allocator-complex-modifier</td><td>list</td><td>Complex, name: allocatorArguments: allocator expression of al-locator_handle type (default)</td><td>unique</td></tr><tr><td>align-modifier</td><td>list</td><td>Complex, name: alignArguments: alignment expression of integer type (constant, positive)</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

allocators, distribute, do, for, parallel, scope, sections, single, target, target\_data, task, taskgroup, taskloop, teams

## Semantics

The allocate clause specifies the memory allocator to be used to obtain storage for a variable list. If a list item in the clause also appears in a data-sharing attribute clause on the same directive that privatizes the list item, allocations that arise from that list item in the clause will be provided by the memory allocator. If the allocator-simple-modifier is specified, the behavior is as if the allocator-complex-modifier is instead specified with allocator-simple-modifier as its allocator argument. The allocator-complex-modifier and align-modifier have the same syntax and semantics for the allocate clause as the allocator and align clauses have for the allocate directive. For allocations that arise from this clause, the null\_fb value of the fallback allocator trait behaves as if the abort\_fb value had been specified.

## Restrictions

Restrictions to the allocate clause are as follows:

• For any list item that is specified in the allocate clause on a directive other than the allocators directive, a data-sharing attribute clause that may create a private copy of that list item must be specified on the same directive.

• For task, taskloop or target directives, allocation requests to memory allocators with the access trait set to thread result in unspecified behavior.

• allocate clauses that appear on a target construct or on constructs in a target region must specify an allocator-simple-modifier or allocator-complex-modifier unless a

requires directive with the dynamic\_allocators clause is present in the same compilation unit.

## Cross References

• align Clause, see Section 8.3

• allocator Clause, see Section 8.4

• allocators Construct, see Section 8.7

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• Memory Allocators, see Section 8.2

• parallel Construct, see Section 12.1

• scope Construct, see Section 13.2

• sections Construct, see Section 13.3

• single Construct, see Section 13.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskgroup Construct, see Section 17.4

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 8.7 allocators Construct

<table><tr><td>Name: allocatorsCategory: executable</td><td>Association: block : allocatorProperties: default</td></tr></table>

## Clauses

allocate

## Semantics

The allocators construct specifies that if a variable that is to be allocated by the associated allocate-stmt, appears as a list item in an allocate clause on the directive an allocator is used to allocate storage for the variable according to the semantics of the allocate clause. If a variable

that is to be allocated does not appear as a list item in an allocate clause, the allocation is performed according to the base language implementation. The list items that appear in an allocate clause may include structure elements.

## Restrictions

Restrictions to the allocators construct are as follows:

• A list item that appears in an allocate clause must appear as one of the variables that is allocated by the allocate-stmt in the associated allocator structured block.

• A list item must not be a coarray or have a coarray as an ultimate component.

## Cross References

• allocate Clause, see Section 8.6

• Memory Allocators, see Section 8.2

• OpenMP Allocator Structured Blocks, see Section 6.3.1

Fortran

## 8.8 uses\_allocators Clause

<table><tr><td>Name: uses_allocators</td><td>Properties: data-environment attribute, data-sharing attribute</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>allocator</td><td>expression of allocator_-handle type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>mem-space</td><td>allocator</td><td>Complex, name: memspaceArguments:memspace-handleexpression ofmemspace_handle type (default)</td><td>default</td></tr><tr><td>traits-array</td><td>allocator</td><td>Complex, name: traitsArguments:traitsvariable of alloctraitarray type (default)</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target

## Semantics

The uses\_allocators clause enables the use of the specified allocator in the region associated with the directive on which the clause appears. The clause has no efect for an allocator argument value of omp\_null\_allocator. If allocator is an identifier that matches the name of a predefined allocator (see Table 8.3), that predefined allocator will be available for use in the region. Otherwise, the efect is as if allocator is specified on a private clause. The resulting corresponding list item is assigned the result of a call to omp\_init\_allocator at the beginning of the associated region with arguments memspace-handle, the number of traits in the traits array, and traits. If mem-space is not specified or omp\_null\_mem\_space is specified, the efect is as if memspace-handle is specified as omp\_default\_mem\_space. If traits-array is not specified, the efect is as if traits is specified as an empty array. Further, at the end of the associated region, the efect is as if this allocator is destroyed as if by a call to omp\_destroy\_allocator.

More than one clause-argument-specification may be specified.

## Restrictions

• The allocator expression must be a base language identifier.

• If allocator is an identifier that matches the name of a predefined allocator, no modifiers may be specified.

• If allocator is not the name of a predefined allocator and is not omp\_null\_allocator, it must be a variable.

• The allocator argument must not appear in other data-sharing attribute clauses or data-mapping attribute clauses on the same construct.

## C / C++

• The traits argument for the traits-array modifier must be a constant array, have constant values and be defined in the same scope as the construct on which the clause appears.

C / C++

Fortran

• The traits argument for the traits-array modifier must be a named constant of rank one.

Fortran

• The memspace-handle argument for the mem-space modifier must be an identifier that matches one of the predefined memory space names.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• OpenMP alloctrait Type, see Section 20.8.2

• Memory Allocators, see Section 8.2

• Memory Spaces, see Section 8.1

• OpenMP memspace\_handle Type, see Section 20.8.11

• omp\_destroy\_allocator Routine, see Section 27.7

• omp\_init\_allocator Routine, see Section 27.6

• target Construct, see Section 15.8
