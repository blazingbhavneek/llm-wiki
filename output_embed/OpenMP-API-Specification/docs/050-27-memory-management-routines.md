# 27 Memory Management Routines

This chapter describes OpenMP memory-management routines, which are OpenMP API routines that have the memory-management-routine property. These routines support memory management on the current device.

Fortran

The Fortran versions of the memory-management routines require an explicit interface and thus might not be provided in the deprecated include file omp\_lib.h.

Fortran

## 27.1 Memory Space Retrieving Routines

This section describes the memory-space-retrieving routines, which are routines that have the memory-space-retrieving property. Each of these routines returns a handle to a memory space that represents a set of storage resources accessible by one or more devices. For each storage resource the following requirements are true:

• The storage resource is accessible by each of the devices selected by the routine; and

• The storage resource is part of the memory space represented by the memspace argument in each of the devices selected by the routine.

If no set of storage resources matches the above requirements then the special value omp\_null\_mem\_space is returned. These routines have the all-device-threads binding property for each device selected by the routine. Thus, the binding thread set for a region that corresponds to a memory-space-retrieving routine is all threads on the devices selected by the routine.

The memory spaces returned by these routines are target memory spaces if any of the selected devices is not the current device.

For any memory-space-retrieving routine that takes a devs argument, if the array to which the argument points has more than ndevs values, the additional values are ignored.

## Restrictions

The restrictions to memory-space-retrieving routines are as follows:

• These routines must only be invoked on the host device.

• The memspace argument must be one of the predefined memory spaces.

• For any memory-space-retrieving routine that has a devs argument, the argument must point to an array that contains at least ndevs values.

• For any memory-space-retrieving routine that has a dev or devs argument, the value of the dev argument the ndevs values of the array to which devs points must be conforming device numbers.

## Cross References

• Memory Spaces, see Section 8.1

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 27.1.1 omp\_get\_devices\_memspace Routine

<table><tr><td>Name: omp_get_devices_memspaceCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-space-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>ndevs</td><td>integer</td><td>intent(in), positive</td></tr><tr><td>devs</td><td>integer</td><td>intent(in), pointer</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_devices\_memspace(int ndevs,

const int <sub>\*</sub>devs, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function &

omp\_get\_devices\_memspace(ndevs, devs, memspace)

integer, intent(in) :: ndevs, devs(<sub>\*</sub>)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_devices\_memspace routine is a memory-space-retrieving routine. The devices selected by the routine are those specified in the devs argument.

## Cross References

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.1.2 omp\_get\_device\_memspace Routine

<table><tr><td>Name: omp_get_device_memspaceCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-space-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>dev</td><td>integer</td><td>intent(in)</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_device\_memspace(int dev,

omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function &

omp\_get\_device\_memspace(dev, memspace)

integer, intent(in) :: dev

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_device\_memspace routine is a memory-space-retrieving routine. The device selected by the routine is the device specified in the dev argument.

Cross References

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

27.1.3 omp\_get\_devices\_and\_host\_memspace Routine

<table><tr><td>Name:omp_get_devices_and_host_memspaceCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-space-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>ndevs</td><td>integer</td><td>intent(in), positive</td></tr><tr><td>devs</td><td>integer</td><td>intent(in), pointer</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_devices\_and\_host\_memspace( int ndevs, const int <sub>\*</sub>devs, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function &

omp\_get\_devices\_and\_host\_memspace(ndevs, devs, memspace)

integer, intent(in) :: ndevs, devs(<sub>\*</sub>)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_devices\_and\_host\_memspace routine is a memory-space-retrieving routine. The devices selected by the routine are the host device and those specified in the devs argument.

## Cross References

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.1.4 omp\_get\_device\_and\_host\_memspace Routine

<table><tr><td>Name:omp_get_device_and_host_memspaceCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-space-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>dev</td><td>integer</td><td>intent(in)</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_device\_and\_host\_memspace(int dev, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function &

omp\_get\_device\_and\_host\_memspace(dev, memspace)

integer, intent(in) :: dev

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_device\_and\_host\_memspace routine is a memory-space-retrieving routine. The devices selected by the routine are the host device and the device specified in the dev argument.

## Cross References

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.1.5 omp\_get\_devices\_all\_memspace Routine

<table><tr><td>Name: omp_get_devices_all_memspaceCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-space-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_devices\_all\_memspace(

omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function &

omp\_get\_devices\_all\_memspace(memspace)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

Effect

The omp\_get\_devices\_all\_memspace routine is a memory-space-retrieving routine. The devices selected by the routine are all available devices.

Cross References

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.2 omp\_get\_memspace\_num\_resources Routine

<table><tr><td>Name: omp_get_memspace_num_resourcesCategory: function</td><td>Properties: all-device-threads-binding,memory-management-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

int omp\_get\_memspace\_num\_resources(

omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer function omp\_get\_memspace\_num\_resources(memspace)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_memspace\_num\_resources routine is a memory-management routine that returns the number of distinct storage resources that are associated with the memory space represented by the memspace handle.

Restrictions

The restrictions to the omp\_get\_memspace\_num\_resources routine are as follows:

• The memspace argument must be a valid memory space.

## Cross References

• Memory Spaces, see Section 8.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.3 omp\_get\_memspace\_pagesize Routine

<table><tr><td>Name: omp_get_memspace_pagesizeCategory: function</td><td>Properties: all-device-threads-binding,iso_c_binding, memory-management-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_size_t</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

size\_t omp\_get\_memspace\_pagesize(omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=c\_size\_t) function omp\_get\_memspace\_pagesize(& memspace) bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_size\_t

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_memspace\_pagesize routine is a memory-management routine that returns the page size that the memory space represented by the memspace handle supports.

## Restrictions

The restrictions to the omp\_get\_memspace\_pagesize routine are as follows:

• The memspace argument must be a valid memory space.

## Cross References

• Memory Spaces, see Section 8.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.4 omp\_get\_submemspace Routine

<table><tr><td>Name: omp_get_submemspaceCategory: function</td><td>Properties: all-device-threads-binding,memory-management-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>memspace_handle</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr><tr><td>num_resources</td><td>integer</td><td>intent(in), non-negative</td></tr><tr><td>resources</td><td>integer</td><td>intent(in), pointer</td></tr></table>

Prototypes

C / C++

omp\_memspace\_handle\_t omp\_get\_submemspace(

omp\_memspace\_handle\_t memspace, int num\_resources,

const int \*resources);

C / C++

Fortran

integer (kind=omp\_memspace\_handle\_kind) function & omp\_get\_submemspace(memspace, num\_resources, resources) integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace integer, intent(in) :: num\_resources, resources(\*)

Fortran

## Effect

The omp\_get\_submemspace routine is a memory-management routine that returns a new memory space that contains a subset of the resources of the original memory space. The new memory space represents only the resources of the memory space represented by the memspace handle that are specified by the resources argument. If num\_resources is zero or a memory space cannot be created for the requested resources, the special value omp\_null\_mem\_space is returned.

## Restrictions

The restrictions to the omp\_get\_submemspace routine are as follows:

• The memspace argument must be a valid memory space.

• The resources array must contain at least as many entries as specified by the num\_resources argument.

• The value of each entry of the resources array must be between 0 and one less than the number of resources associated with the memory space represented by the memspace argument.

## Cross References

• Memory Spaces, see Section 8.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.5 OpenMP Memory Partitioning Routines

This section describes the memory-partitioning routines, which are routines that have the memory-partitioning property. These routines provide mechanisms to create and to use memory partitioners.

27.5.1 omp\_init\_mempartitioner Routine

<table><tr><td>Name: omp_init_mepartitionerCategory: subroutine</td><td>Properties: all-device-threads-binding, memory-management-routine, memory-partitioning</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>partitioner</td><td>mepartitioner</td><td>C/C++ pointer, omp, intent(out)</td></tr><tr><td>lifetime</td><td>mepartitioner_lifetime</td><td>omp, intent(in)</td></tr><tr><td>compute_proc</td><td>mepartitioner_compute_proc</td><td>omp, procedure</td></tr><tr><td>release_proc</td><td>mepartitioner_release_proc</td><td>omp, procedure</td></tr></table>

## Prototypes

C / C++

void omp\_init\_mempartitioner(omp\_mempartitioner\_t <sub>\*</sub>partitioner, omp\_mempartitioner\_lifetime\_t lifetime, omp\_mempartitioner\_compute\_proc\_t compute\_proc, omp\_mempartitioner\_release\_proc\_t release\_proc);

C / C++

Fortran

subroutine omp\_init\_mempartitioner(partitioner, lifetime, &

compute\_proc, release\_proc)

integer (kind=omp\_mempartitioner\_kind), intent(out) :: & partitioner

intent(in) :: lifetime

procedure (omp\_mempartitioner\_compute\_proc\_t) compute\_proc procedure (omp\_mempartitioner\_release\_proc\_t) release\_proc

Fortran

## Effect

The omp\_init\_mempartitioner routine initializes the memory partitioner that the partitioner object represents with the lifetime specified by the lifetime argument, and the compute\_proc partition computation procedure and the release\_proc partition release procedure.

Once initialized the partitioner object can be associated with an allocator when the allocator is initialized with omp\_init\_allocator by using the omp\_atk\_partitioner trait. If the omp\_atk\_partition allocator trait is set to omp\_atv\_partitioner, then, for allocations that use the allocator, the number of memory parts of an allocation and how they are distributed across the storage resources are defined by a memory partition object that must be initialized in the compute\_proc provided in this routine through calls to the omp\_init\_mempartition and omp\_mempartition\_set\_part routines.

If the value of the lifetime argument is omp\_allocator\_mempartition then the memory partition object that is created through the compute\_proc procedure might be used for all allocations of an allocator that has the same allocation size. If the value of the lifetime argument is omp\_dynamic\_mempartition then a memory partition object will be initialized for every allocation.

## Restrictions

The restrictions to the omp\_init\_mempartitioner routine are as follows:

• The memory partitioner represented by the partitioner argument must be in the uninitialized state.

## Cross References

• Memory Allocators, see Section 8.2

• Memory Spaces, see Section 8.1

• OpenMP mempartitioner Type, see Section 20.8.7

• OpenMP mempartitioner\_compute\_proc Type, see Section 20.8.9

• OpenMP mempartitioner\_lifetime Type, see Section 20.8.8

• OpenMP mempartitioner\_release\_proc Type, see Section 20.8.10
