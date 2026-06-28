
This section describes OpenMP types related to synchronization, including locks.

## 20.9.1 OpenMP depend Type

<table><tr><td>Name: dependProperties: named-handle, omp, opaque</td><td>Base Type:implementation-defined-int</td></tr></table>

Type Definition

C / C++

typedef <implementation-defined-integral> omp\_depend\_t;

C / C++

Fortran

integer (kind=omp\_depend\_kind)

Fortran

The depend OpenMP type is an opaque type that represents depend objects.

## 20.9.2 OpenMP impex Type

<table><tr><td>Name: impexProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_not_impex</td><td>0</td><td>omp</td></tr><tr><td>omp_import</td><td>1</td><td>omp</td></tr><tr><td>omp_export</td><td>2</td><td>omp</td></tr><tr><td>omp_impex</td><td>3</td><td>omp</td></tr></table>

```txt
Type Definition
typedef enum omp_impex_t {
    omp_not_impex = 0,
    omp_import     = 1,
    omp_export     = 2,
    omp_impex      = 3
} omp_impex_t;
C / C++
C / C++
Fortran
integer (kind=omp_impex_kind), &
    parameter :: omp_not_impex = 0
integer (kind=omp_impex_kind), &
    parameter :: omp_import = 1
integer (kind=omp_impex_kind), &
    parameter :: omp_export = 2
integer (kind=omp_impex_kind), &
    parameter :: omp_impex = 3
```

The impex OpenMP type is an enumeration type that is used to specify whether the child tasks of a task may form a task dependence with respect to its dependence-compatible tasks. In particular, it is used to identify whether a task is an importing task and/or an exporting task. The valid constants must include those shown above.

## Cross References

• transparent Clause, see Section 17.9.6

## 20.9.3 OpenMP lock Type

<table><tr><td>Name: lockProperties: named-handle, opaque</td><td>Base Type: opaque</td></tr><tr><td colspan="2">Type DefinitionC / C++typedef &lt;implementation-defined&gt; omp_lock_t;C / C++Fortraninteger (kind=omp_lock_kind)Fortran</td></tr></table>

The lock OpenMP type is an opaque type that represents simple locks used in simple lock routines.

## 20.9.4 OpenMP nest\_lock Type

<table><tr><td>Name: nest_lockProperties: named-handle, opaque</td><td>Base Type: opaque</td></tr></table>

## Type Definition

C / C++

typedef <implementation-defined> omp\_nest\_lock\_t;

C / C++

Fortran

integer (kind=omp\_nest\_lock\_kind)

Fortran

The nest\_lock OpenMP type is an opaque type that represents nestable locks used in nestable lock routines.

## 20.9.5 OpenMP sync\_hint Type

<table><tr><td>Name: sync_hintProperties: omp</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_sync_hint_none</td><td>0x0</td><td>omp</td></tr><tr><td>omp_sync_hint_uncontended</td><td>0x1</td><td>omp</td></tr><tr><td>omp_sync_hint_contended</td><td>0x2</td><td>omp</td></tr><tr><td>omp_sync_hint_nonspeculative</td><td>0x4</td><td>omp</td></tr><tr><td>omp_sync_hint_speculative</td><td>0x8</td><td>omp</td></tr></table>

Type Definition

C / C++

typedef enum omp\_sync\_hint\_t {

omp\_sync\_hint\_none = 0x0,

omp\_sync\_hint\_uncontended = 0x1,

omp\_sync\_hint\_contended = 0x2,

omp\_sync\_hint\_nonspeculative = 0x4,

omp\_sync\_hint\_speculative = 0x8

} omp\_sync\_hint\_t;

C / C++

## Fortran

integer (kind=omp\_sync\_hint\_kind), & parameter :: omp\_sync\_hint\_none = & int(Z'0', kind=omp\_sync\_hint\_kind) integer (kind=omp\_sync\_hint\_kind), & parameter :: omp\_sync\_hint\_uncontended = & int(Z'1', kind=omp\_sync\_hint\_kind) integer (kind=omp\_sync\_hint\_kind), & parameter :: omp\_sync\_hint\_contended = & int(Z'2', kind=omp\_sync\_hint\_kind) integer (kind=omp\_sync\_hint\_kind), & parameter :: omp\_sync\_hint\_nonspeculative = & int(Z'4', kind=omp\_sync\_hint\_kind) integer (kind=omp\_sync\_hint\_kind), & parameter :: omp\_sync\_hint\_speculative = & int(Z'8', kind=omp\_sync\_hint\_kind)

## Fortran

The sync\_hint OpenMP type is used to specify synchronization hints. The omp\_init\_lock\_with\_hint and omp\_init\_nest\_lock\_with\_hint routines provide hints about the expected dynamic behavior or suggested implementation of a lock. Synchronization hints may also be provided for atomic and critical directives by using the hint clause. The efect of a hint does not change the semantics of the associated construct or routine; if ignoring the hint changes the program semantics, the result is unspecified.

Synchronization hints can be combined by using the + or | operators in C/C++ or the + operator in Fortran. Combining omp\_sync\_hint\_none with any other synchronization hint is equivalent to specifying the other synchronization hint.

The intended meaning of each synchronization hint is:

• omp\_sync\_hint\_uncontended: low contention is expected in this operation, that is, few threads are expected to perform the operation simultaneously in a manner that requires synchronization;

• omp\_sync\_hint\_contended: high contention is expected in this operation, that is, many threads are expected to perform the operation simultaneously in a manner that requires synchronization;

• omp\_sync\_hint\_speculative: the programmer suggests that the operation should be implemented using speculative techniques such as transactional memory; and

• omp\_sync\_hint\_nonspeculative: the programmer suggests that the operation should not be implemented using speculative techniques such as transactional memory.

Note – Future OpenMP specifications may add additional synchronization hints to the sync\_hint OpenMP type. Implementers are advised to add implementation defined synchronization hints starting from the most significant bit of the type and to include the name of the implementation in the name of the added synchronization hint to avoid name conflicts with other OpenMP implementations.

## Restrictions

Restrictions to the synchronization hints are as follows:

• The omp\_sync\_hint\_uncontended and omp\_sync\_hint\_contended values may not be combined.

• The omp\_sync\_hint\_nonspeculative and omp\_sync\_hint\_speculative values may not be combined.

## Cross References

• atomic Construct, see Section 17.8.5

• critical Construct, see Section 17.2

• hint Clause, see Section 17.1

• omp\_init\_lock\_with\_hint Routine, see Section 28.1.3

• omp\_init\_nest\_lock\_with\_hint Routine, see Section 28.1.4

## 20.10 OpenMP Affinity Support Types

This section describes OpenMP types that support afinity mechanisms.

## 20.10.1 OpenMP proc\_bind Type

<table><tr><td>Name: proc_bindProperties: omp</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_proc_bind_false</td><td>0</td><td>omp</td></tr><tr><td>omp_proc_bind_true</td><td>1</td><td>omp</td></tr><tr><td>omp_proc_bind_primary</td><td>2</td><td>omp</td></tr><tr><td>omp_proc_bind_close</td><td>3</td><td>omp</td></tr><tr><td>omp_proc_bind_spread</td><td>4</td><td>omp</td></tr></table>

```txt
Type Definition
C / C++
typedef enum omp_proc_bind_t {
    omp_proc_bind_false = 0,
    omp_proc_bind_true = 1,
    omp_proc_bind_primary = 2,
    omp_proc_bind_close = 3,
    omp_proc_bind_spread = 4
} omp_proc_bind_t;

C / C++
Fortran
integer (kind=omp_proc_bind_kind), &
    parameter :: omp_proc_bind_false = 0
integer (kind=omp_proc_bind_kind), &
    parameter :: omp_proc_bind_true = 1
integer (kind=omp_proc_bind_kind), &
    parameter :: omp_proc_bind_primary = 2
integer (kind=omp_proc_bind_kind), &
    parameter :: omp_proc_bind_close = 3
integer (kind=omp_proc_bind_kind), &
    parameter :: omp_proc_bind_spread = 4
```

The proc\_bind OpenMP type is used in routines that modify or retrieve the value of the bind-var ICV. The valid constants for the proc\_bind type must include those shown above.

Cross References

• bind-var ICV, see Table 3.1

## 20.11 OpenMP Resource Relinquishing Types
