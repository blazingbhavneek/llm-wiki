# OpenMP-API-Specification Source Lines 20174-20541

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L20174-L20541

Citation: [OpenMP-API-Specification:L20174-L20541]

````text
## 20.8.3 OpenMP alloctrait\_key Type

<table><tr><td>Name: alloctrait_keyProperties: omp</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_atk_sync_hint</td><td>1</td><td>omp</td></tr><tr><td>omp_atk_alignment</td><td>2</td><td>omp</td></tr><tr><td>omp_atk_access</td><td>3</td><td>omp</td></tr><tr><td>omp_atk_pool_size</td><td>4</td><td>omp</td></tr><tr><td>omp_atk_fallback</td><td>5</td><td>omp</td></tr><tr><td>omp_atk_fb_data</td><td>6</td><td>omp</td></tr><tr><td>omp_atk_pinned</td><td>7</td><td>omp</td></tr><tr><td>omp_atk_partition</td><td>8</td><td>omp</td></tr><tr><td>omp_atk_pin_device</td><td>9</td><td>omp</td></tr><tr><td>omp_atk_preferred_device</td><td>10</td><td>omp</td></tr><tr><td>omp_atk_device_access</td><td>11</td><td>omp</td></tr><tr><td>omp_atk_target_access</td><td>12</td><td>omp</td></tr><tr><td>omp_atk_atomic_scope</td><td>13</td><td>omp</td></tr><tr><td>omp_atk_part_size</td><td>14</td><td>omp</td></tr><tr><td>omp_atk_partitioner</td><td>15</td><td>omp</td></tr><tr><td>omp_atk_partitioner_arg</td><td>16</td><td>omp</td></tr></table>

<table><tr><td colspan="2">typedef enum omp alloctrait_key_t {</td></tr><tr><td>omp_atk_sync_hint</td><td>= 1,</td></tr><tr><td>omp_atk_alignment</td><td>= 2,</td></tr><tr><td>omp_atk_access</td><td>= 3,</td></tr><tr><td>omp_atk_pool_size</td><td>= 4,</td></tr><tr><td>omp_atk_fallback</td><td>= 5,</td></tr><tr><td>omp_atk_fb_data</td><td>= 6,</td></tr><tr><td>omp_atk_pinned</td><td>= 7,</td></tr><tr><td>omp_atk_partition</td><td>= 8,</td></tr><tr><td>omp_atk_pin_device</td><td>= 9,</td></tr><tr><td>omp_atk_preferred_device</td><td>= 10,</td></tr><tr><td>omp_atk_device_access</td><td>= 11,</td></tr><tr><td>omp_atk_target_access</td><td>= 12,</td></tr><tr><td>omp_atk_atomic_scope</td><td>= 13,</td></tr><tr><td>omp_atk_part_size</td><td>= 14,</td></tr><tr><td>omp_atk_partitioner</td><td>= 15,</td></tr><tr><td>omp_atk_partitioner_arg</td><td>= 16</td></tr><tr><td colspan="2">} omp alloctrait_key_t;</td></tr></table>

```fortran
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_sync_hint = 1
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_alignment = 2
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_access = 3
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_pool_size = 4
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_fallback = 5
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_fb_data = 6
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_pinned = 7
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_partition = 8
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_pin_device = 9
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_preferred_device = 10
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_device_access = 11
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_target_access = 12
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_atomic_scope = 13
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_part_size = 14
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_partitioner = 15
integer (kind=omp alloctrait_key_kind), &
  parameter :: omp_atk_partitioner_arg = 16
```

## Fortran

The alloctrait\_key OpenMP type represents an allocator trait as described in Table 20.4. The valid constants for this OpenMP type must include those shown above.

## C++

The omp.h header file also defines a class template that models the memory allocator concept in the omp::allocator namespace for each value of the alloctrait\_key OpenMP type. The names in this class do not include either the omp\_ prefix or the \_alloc sufix.

<table><tr><td>7</td><td colspan="2">Type Definition</td><td>C / C++</td></tr><tr><td>8</td><td colspan="3">typedef enum omp alloctrait_value_t {</td></tr><tr><td>9</td><td>omp_atv_default</td><td>= -1,</td><td></td></tr><tr><td>10</td><td>omp_atv_false</td><td>= 0,</td><td></td></tr><tr><td>11</td><td>omp_atv_true</td><td>= 1,</td><td></td></tr><tr><td>12</td><td>omp_atv_contended</td><td>= 3,</td><td></td></tr></table>

## Cross References

• Memory Allocators, see Section 8.2

20.8.4 OpenMP alloctrait\_value Type

<table><tr><td>Name: alloctrait_valueProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_atv_default</td><td>-1</td><td>omp</td></tr><tr><td>omp_atv_false</td><td>0</td><td>omp</td></tr><tr><td>omp_atv_true</td><td>1</td><td>omp</td></tr><tr><td>omp_atv_contended</td><td>3</td><td>omp</td></tr><tr><td>omp_atv_uncontended</td><td>4</td><td>omp</td></tr><tr><td>omp_atv_serialized</td><td>5</td><td>omp</td></tr><tr><td>omp_atv_private</td><td>6</td><td>omp</td></tr><tr><td>omp_atv_device</td><td>7</td><td>omp</td></tr><tr><td>omp_atv_thread</td><td>8</td><td>omp</td></tr><tr><td>omp_atv_pteam</td><td>9</td><td>omp</td></tr><tr><td>omp_atv_cgroup</td><td>10</td><td>omp</td></tr><tr><td>omp_atv_default_mem_fb</td><td>11</td><td>omp</td></tr><tr><td>omp_atv_null_fb</td><td>12</td><td>omp</td></tr><tr><td>omp_atv_abort_fb</td><td>13</td><td>omp</td></tr><tr><td>omp_atv_allocator_fb</td><td>14</td><td>omp</td></tr><tr><td>omp_atv_environment</td><td>15</td><td>omp</td></tr><tr><td>omp_atv_nearest</td><td>16</td><td>omp</td></tr><tr><td>omp_atv_filtered</td><td>17</td><td>omp</td></tr><tr><td>omp_atv_interleaved</td><td>18</td><td>omp</td></tr><tr><td>omp_atv_all</td><td>19</td><td>omp</td></tr><tr><td>omp_atv_single</td><td>20</td><td>omp</td></tr><tr><td>omp_atv_multiple</td><td>21</td><td>omp</td></tr><tr><td>omp_atv_memspace</td><td>22</td><td>omp</td></tr><tr><td>omp_atv_partitioner</td><td>23</td><td>omp</td></tr></table>

```c
omp_atv_uncontended = 4,
omp_atv_serialized = 5,
omp_atv_private = 6,
omp_atv_device = 7,
omp_atv_thread = 8,
omp_atv_pteam = 9,
omp_atv_cgroup = 10,
omp_atv_default_mem_fb = 11,
omp_atv_null_fb = 12,
omp_atv_abort_fb = 13,
omp_atv_allocator_fb = 14,
omp_atv_environment = 15,
omp_atv_nearest = 16,
omp_atv_filtered = 17,
omp_atv_interleaved = 18,
omp_atv_all = 19,
omp_atv_single = 20,
omp_atv_multiple = 21,
omp_atv_memspace = 22,
omp_atv_partitioner = 23
} omp_alloctrait_value_t;
```

```fortran
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_cgroup = 10
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_default_mem_fb = 11
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_null_fb = 12
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_abort_fb = 13
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_allocator_fb = 14
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_environment = 15
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_nearest = 16
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_filtered = 17
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_interleaved = 18
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_all = 19
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_single = 20
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_multiple = 21
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_memspace = 22
integer (kind=omp alloctrait_value_kind), &
    parameter :: omp_atv_partitioner = 23
```

The alloctrait\_value OpenMP type represents semantic values of allocator traits as described in Table 20.4. The valid constants for this OpenMP type must include those shown above.

## Cross References

• Memory Allocators, see Section 8.2

## 20.8.5 OpenMP alloctrait\_val Type

<table><tr><td>Name: alloctrait_valProperties: omp</td><td>Base Type: intptr</td></tr></table>

## Type Definition

C / C++

typedef omp\_intptr\_t omp\_alloctrait\_val\_t;

C / C++

Fortran

integer (kind=c\_intptr\_t)

Fortran

The alloctrait\_val OpenMP type represents the values that may be assigned to the value field of the alloctrait\_val OpenMP type. Any of the semantic values of the

alloctrait\_value OpenMP type may be used for the alloctrait\_val OpenMP type; in addition, other numeric values may be used for it as appropriate for the specified key of the alloctrait OpenMP type.

## 20.8.6 OpenMP mempartition Type

<table><tr><td>Name: mempartitionProperties: named-handle, omp, opaque</td><td>Base Type: opaque</td></tr></table>

## Type Definition

C / C++

typedef <implementation-defined> omp\_mempartition\_t;

C / C++

Fortran

integer (kind=omp\_mempartition\_kind)

Fortran

The mempartition OpenMP type is an opaque type that represents memory partitions.

## 20.8.7 OpenMP mempartitioner Type

<table><tr><td>Name: mempartitionerProperties: named-handle, omp, opaque</td><td>Base Type: opaque</td></tr></table>

## Type Definition

C / C++

typedef <implementation-defined> omp\_mempartitioner\_t;

C / C++

Fortran

integer (kind=omp\_mempartitioner\_kind)

Fortran

The mempartitioner OpenMP type is an opaque type that represents memory partitioners.

## 20.8.8 OpenMP mempartitioner\_lifetime Type

<table><tr><td>Name: mempartitioner_lifetimeProperties: omp</td><td>Base Type: enumeration</td></tr></table>

<table><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_static_mepartition</td><td>1</td><td>omp</td></tr><tr><td>omp_allocator_mepartition</td><td>2</td><td>omp</td></tr><tr><td>omp_dynamic_mepartition</td><td>3</td><td>omp</td></tr></table>

## Type Definition

C / C++

typedef enum omp\_mempartitioner\_lifetime\_t {

omp\_static\_mempartition = 1,

omp\_allocator\_mempartition = 2,

omp\_dynamic\_mempartition = 3

} omp\_mempartitioner\_lifetime\_t;

C / C++

Fortran

integer (kind=omp\_mempartitioner\_lifetime\_kind), &

parameter :: omp\_static\_mempartition = 1

integer (kind=omp\_mempartitioner\_lifetime\_kind), &

parameter :: omp\_allocator\_mempartition = 2

integer (kind=omp\_mempartitioner\_lifetime\_kind), &

parameter :: omp\_dynamic\_mempartition = 3

Fortran

The mempartitioner\_lifetime OpenMP type represents the lifetime of a memory partitioner. The valid constants for the mempartitioner\_lifetime OpenMP type must include those shown above.

## 20.8.9 OpenMP mempartitioner\_compute\_proc Type

<table><tr><td>Name: mempartitioner_compute_procCategory: subroutine pointer</td><td>Properties: iso_c_binding, omp</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>omp</td></tr><tr><td>allocation_size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>partitioner_arg</td><td>alloctrait_val</td><td>omp, value</td></tr><tr><td>partition</td><td>mmpartition</td><td>C/C++ pointer, omp</td></tr></table>

## Type Signature

typedef void (<sub>\*</sub>omp\_mempartitioner\_compute\_proc\_t) ( omp\_memspace\_handle\_t memspace, size\_t allocation\_size, omp\_alloctrait\_val\_t partitioner\_arg, omp\_mempartition\_t <sub>\*</sub>partition);

```fortran
abstract interface
  subroutine omp_mempartitioner_compute_proc_t(memspace, &
    allocation_size, partitioner_arg, partition) bind(c)
    use, intrinsic :: iso_c_binding, only : c_size_t
    integer (kind=omp_memspace_handle_kind) memspace
    integer (kind=c_size_t), value :: allocation_size
    integer (kind=omp alloctrait_val_kind), value :: &
      partitioner_arg
    integer (kind=omp_mempartition_kind) partition
  end subroutine
end interface
```

## Fortran

The mempartitioner\_compute\_proc OpenMP type represents a partition computation procedure. When used through the omp\_init\_mempartition and omp\_mempartition\_set\_part routines, the procedure will be passed the following arguments in the listed order:

• The memory space associated with the allocator to be used for the memory allocation;

• The size of the allocation in bytes;

• If the omp\_atk\_partitioner\_arg trait was specified for the allocator, its specified value, otherwise, the value zero; and

• A memory partition object to be initialized

If the sum of the sizes of the parts specified in the memory partition object after executing the procedure is not equal to the allocation\_size argument, the behavior is unspecified.

If the associated memory partitioner has been created with a call to omp\_init\_mempartitioner with the value of the lifetime argument set to omp\_static\_mempartition then the memory partition object computed by an invocation to the procedure might be used for the allocations of any allocators that have the partitioner memory partitioner object associated with them if the allocations have the same size and the same memory space. The number of times that the compute\_proc procedure is invoked is unspecified.

## Cross References

• OpenMP alloctrait\_val Type, see Section 20.8.5

• OpenMP mempartition Type, see Section 20.8.6

• OpenMP memspace\_handle Type, see Section 20.8.11

• omp\_init\_mempartition Routine, see Section 27.5.3

• omp\_mempartition\_set\_part Routine, see Section 27.5.5

## 20.8.10 OpenMP mempartitioner\_release\_proc Type

<table><tr><td>Name: mempartitioner_release_procCategory: subroutine pointer</td><td>Properties: iso_c_binding, omp</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>partition</td><td>mmpartition</td><td>C/C++ pointer, omp</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>omp\_mempartitioner\_release\_proc\_t) (

omp\_mempartition\_t <sub>\*</sub>partition);

C / C++

Fortran

abstract interface

subroutine omp\_mempartitioner\_release\_proc\_t(partition) & bind(c)

integer (kind=omp\_mempartition\_kind) partition

end subroutine

end interface

## Fortran

The mempartitioner\_release\_proc OpenMP type represents a partition release procedure. When an implementation finishes using a memory partition object that was created with the procedure used as the compute\_proc argument for a call to the omp\_init\_mempartitioner routine to which the represented release procedure was the release\_proc argument, that release procedure will be called with the memory partition object as its argument. The procedure can then release the object and its resources using the omp\_destroy\_mempartition routine. The implementation will invoke the release\_proc at most once for each memory partition object.

## Cross References

• OpenMP mempartition Type, see Section 20.8.6

• omp\_init\_mempartitioner Routine, see Section 27.5.1

## 20.8.11 OpenMP memspace\_handle Type

```txt
Name: memspace_handle
Properties: omp
Base Type: enumeration
Values
Name
Value
Properties
omp_null_mem_space
0
omp
omp_default_mem_space
1
omp_large_cap_mem_space
2
omp_const_mem_space
3
omp_high_bw_mem_space
4
omp_low_lat_mem_space
5
omp
Type Definition
C / C++
typedef enum omp_memspace_handle_t {
    omp_null_mem_space = 0,
    omp_default_mem_space = 1,
    omp_large_cap_mem_space = 2,
    omp_const_mem_space = 3,
    omp_high_bw_mem_space = 4,
    omp_low_lat_mem_space = 5
} omp_memspace_handle_t;
C / C++
Fortran
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_null_mem_space = 0
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_default_mem_space = 1
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_large_cap_mem_space = 2
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_const_mem_space = 3
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_high_bw_mem_space = 4
integer (kind=omp_memspace_handle_kind), &
parameter :: omp_low_lat_mem_space = 5
```

The memspace\_handle OpenMP type represents an allocator as described in Table 8.1. This OpenMP type must be an implementation defined (for C++ possibly scoped) enum type and its valid constants must include those shown above.
````
