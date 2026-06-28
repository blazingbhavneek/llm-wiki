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

## 27.5.2 omp\_destroy\_mempartitioner Routine

<table><tr><td>Name: omp_destroy_mepartitionerCategory: subroutine</td><td>Properties: all-device-threads-binding, memory-management-routine, memory-partitioning</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>partitioner</td><td>mepartitioner</td><td>C/C++ pointer, omp, intent(in)</td></tr></table>

## Prototypes

C / C++

<table><tr><td>C / C++</td></tr><tr><td>void omp_destroy_mepartitioner( const omp_mepartitioner_t *partitioner);</td></tr><tr><td>C / C++</td></tr></table>

C / C++

## Fortran

subroutine omp\_destroy\_mempartitioner(partitioner) integer (kind=omp\_mempartitioner\_kind), intent(in) :: & partitioner

## Fortran

## Effect

The efect of the omp\_destroy\_mempartitioner routine is to uninitialize a memory partitioner. Thus, the routine changes the state of the memory partitioner object represented by the partitioner argument to uninitialized and releases all resources associated with it.

## Restrictions

The restrictions to the omp\_destroy\_mempartitioner routine are as follows:

• The memory partitioner represented by the partitioner argument must be in the initialized state.

• Any allocator that references the memory partitioner object represented by the partitioner argument must be destroyed before this routine is called.

## Cross References

• Memory Allocators, see Section 8.2

• OpenMP mempartitioner Type, see Section 20.8.7

## 27.5.3 omp\_init\_mempartition Routine

<table><tr><td>Name: omp_init_mempartitionCategory: subroutine</td><td>Properties: all-device-threads-binding,iso_c_binding, memory-management-routine, memory-partitioning</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>partition</td><td>mmpartition</td><td>C/C++ pointer, omp, intent(out)</td></tr><tr><td>nparts</td><td>c_size_t</td><td>intent(in), iso_c, in-tent(in)</td></tr><tr><td>user_data</td><td>c_ptr</td><td>intent(in), iso_c, in-tent(in)</td></tr></table>

## Prototypes

C / C++

void omp\_init\_mempartition(omp\_mempartition\_t <sub>\*</sub>partition, size\_t nparts, const void <sub>\*</sub>user\_data);

C / C++

Fortran

subroutine omp\_init\_mempartition(partition, nparts, user\_data) & bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_size\_t, c\_ptr integer (kind=omp\_mempartition\_kind), intent(out) :: partition integer (kind=c\_size\_t), intent(in) :: nparts type (c\_ptr), intent(in) :: user\_data

Fortran

## Effect

The efect of the omp\_init\_mempartition routine is to initialize a memory partition object. Thus, the routine sets the memory partition object indicated by the partition argument to represent a memory partition of nparts parts and associates the user data indicated by the user\_data argument with it.

## Restrictions

The restrictions to the omp\_init\_mempartition routine are as follows:

• The memory partition represented by the partition argument must be in the uninitialized state.

• This routine must only be called by a procedure that is associated with the memory partitioner object that allocated the memory partition indicated by the partition argument.

## Cross References

• OpenMP Memory Management Types, see Section 20.8

• OpenMP mempartitioner Type, see Section 20.8.7

## 27.5.4 omp\_destroy\_mempartition Routine

<table><tr><td>Name: omp_destroy_mepartitionCategory: subroutine</td><td>Properties: all-device-threads-binding, memory-management-routine, memory-partitioning</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>partition</td><td>mmpartition</td><td>C/C++ pointer, omp, intent(in)</td></tr></table>

## Prototypes

C / C++

void omp\_destroy\_mempartition(

const omp\_mempartition\_t <sub>\*</sub>partition);

C / C++

Fortran

subroutine omp\_destroy\_mempartition(partition)

integer (kind=omp\_mempartition\_kind), intent(in) :: partition

Fortran

## Effect

The efect of the omp\_destroy\_mempartition routine is to uninitialize a memory partition object. Thus, the routine releases the memory partition indicated by the partition argument and all resources associated with it.

## Restrictions

The restrictions to the omp\_destroy\_mempartition routine are as follows:

• The memory partition represented by the partition argument must be in the initialized state.

• This routine must only be called by a procedure that is associated with the memory partitioner object that allocated the memory partition indicated by the partition argument.

## Cross References

• OpenMP Memory Management Types, see Section 20.8

• OpenMP mempartitioner Type, see Section 20.8.7

## 27.5.5 omp\_mempartition\_set\_part Routine

<table><tr><td>Name: omp_mempartition_set_partCategory: function</td><td>Properties: all-device-threads-binding,iso_c_binding, memory-management-routine, memory-partitioning</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>partition</td><td>mmpartition</td><td>C/C++ pointer, omp, intent(out)</td></tr><tr><td>part</td><td>c_size_t</td><td>intent(in), iso_c</td></tr><tr><td>resource</td><td>integer</td><td>intent(in), iso_c</td></tr><tr><td>size</td><td>c_size_t</td><td>intent(in), iso_c</td></tr></table>

## Prototypes

C / C++

int omp\_mempartition\_set\_part(omp\_mempartition\_t <sub>\*</sub>partition, size\_t part, int resource, size\_t size);

C / C++

Fortran

integer function omp\_mempartition\_set\_part(partition, part, & resource, size) bind(c) use, intrinsic :: iso\_c\_binding, only : c\_size\_t integer (kind=omp\_mempartition\_kind), intent(out) :: partition integer (kind=c\_size\_t), intent(in) :: part, size integer, intent(in) :: resource

## Fortran

## Effect

The efect of the omp\_mempartition\_set\_part routine is to define the size and resource of a given part of a memory partition. Thus the routine defines the part number indicated by the part argument of the memory partition object indicated by the partition argument to be associated to the resource indicated by the resource argument and to be of size indicated by the size argument.

The size of all parts of a memory partition, except the last one, need to be a multiple of the page size that the memory space where the memory is being allocated supports. If the specified size cannot be supported by the specified resource, this routine returns negative one. Otherwise, it returns zero.

## Restrictions

The restrictions to the omp\_mempartition\_set\_part routine are as follows:

• The memory partition represented by the partition argument must be in the initialized state.

• This routine must only be called by a procedure that is associated with the memory partitioner object that allocated the memory partition indicated by the partition argument.

## Cross References

• Memory Spaces, see Section 8.1

• OpenMP Memory Management Types, see Section 20.8

• OpenMP mempartitioner Type, see Section 20.8.7

## 27.5.6 omp\_mempartition\_get\_user\_data Routine

<table><tr><td>Name: omp_mempartition_get_user_dataCategory: function</td><td>Properties: all-device-threads-binding,iso_c_binding, memory-management-routine, memory-partitioning</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>partition</td><td>mmpartition</td><td>intent(in), C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

void <sub>\*</sub>omp\_mempartition\_get\_user\_data(

const omp\_mempartition\_t <sub>\*</sub>partition);

C / C++

Fortran

type (c\_ptr) function omp\_mempartition\_get\_user\_data(partition) & bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_ptr

integer (kind=omp\_mempartition\_kind), intent(in) :: partition

## Fortran

## Effect

The efect of the omp\_mempartition\_get\_user\_data routine is to retrieve the user data that was associated with the memory partition when it was created. Thus, the routine returns the data associated with the memory partition object indicated by the partition argument.

Restrictions

The restrictions to the omp\_mempartition\_get\_user\_data routine are as follows:

• The memory partition represented by the partition argument must be in the initialized state.

• This routine must only be called by a procedure that is associated with the memory partitioner object that allocated the memory partition indicated by the partition argument.

## Cross References

• OpenMP Memory Management Types, see Section 20.8

• OpenMP mempartitioner Type, see Section 20.8.7

## 27.6 omp\_init\_allocator Routine

<table><tr><td>Name: omp_init_allocatorCategory: function</td><td>Properties: all-device-threads-binding,memory-management-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr><tr><td>ntraits</td><td>integer</td><td>intent(in)</td></tr><tr><td>traits</td><td>alloctrait</td><td>intent(in), pointer, omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_init\_allocator( omp\_memspace\_handle\_t memspace, int ntraits, const omp\_alloctrait\_t <sub>\*</sub>traits);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function & omp\_init\_allocator(memspace, ntraits, traits) integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace integer, intent(in) :: ntraits integer (kind=omp\_alloctrait\_kind), intent(in) :: traits(<sub>\*</sub>)

Fortran

## Effect

The omp\_init\_allocator routine creates a new allocator that is associated with the memspace memory space and returns a handle to it. All allocations through the created allocator will behave according to the allocator traits specified in the traits argument. The number of traits in the traits argument is specified by the ntraits argument. If the special omp\_atv\_default value is used for a given trait, then its value will be the default value specified in Table 8.2 for that trait.

If memspace has the value omp\_null\_mem\_space, the efect of this routine will be as if the value of memspace was omp\_default\_mem\_space. If memspace is

omp\_default\_mem\_space and the traits argument is an empty set, this routine will always return a handle to an allocator. Otherwise, if an allocator based on the requirements cannot be created then the special omp\_null\_allocator handle is returned.

## Restrictions

The restrictions to the omp\_init\_allocator routine are as follows:

• Each allocator trait must be specified at most once.

• The memspace argument must be a valid memory space handle or the value omp\_null\_mem\_space.

• If the ntraits argument is positive then the traits argument must specify at least ntraits traits.

• The use of an allocator returned by this routine on devices other than the one on which it was created results in unspecified behavior.

• Unless a requires directive with the dynamic\_allocators clause is present in the same compilation unit, using this routine in a target region results in unspecified behavior.

• If the memspace handle represents a target memory space, the values omp\_atv\_device, omp\_atv\_cgroup, omp\_atv\_pteam or omp\_atv\_thread must not be specified for the omp\_atk\_access allocator trait.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocators, see Section 8.2

• Memory Spaces, see Section 8.1

• OpenMP memspace\_handle Type, see Section 20.8.11

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 27.7 omp\_destroy\_allocator Routine

<table><tr><td>Name: omp_destroy_allocatorCategory: subroutine</td><td>Properties: all-device-threads-binding,memory-management-routine</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

void omp\_destroy\_allocator(omp\_allocator\_handle\_t allocator);

C / C++

Fortran

subroutine omp\_destroy\_allocator(allocator)

integer (kind=omp\_allocator\_handle\_kind), intent(in) :: & allocator

Fortran

## Effect

The omp\_destroy\_allocator routine releases all resources used to implement the allocator handle. If allocator is omp\_null\_allocator then this routine has no efect.

## Restrictions

The restrictions to the omp\_destroy\_allocator routine are as follows:

• The allocator argument must not represent a predefined memory allocator.

• Accessing any memory allocated by the allocator after this call results in unspecified behavior.

• Unless a requires directive with the dynamic\_allocators clause is present in the same compilation unit, using this routine in a target region results in unspecified behavior.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocators, see Section 8.2

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 27.8 Memory Allocator Retrieving Routines

This section describes the memory-allocator-retrieving routines, which are routines that have the memory-allocator-retrieving property. Each of these routines returns a handle to a predefined memory allocator that represents the default memory allocator for a given device for a certain kind of memory. If the implementation does not have a predefined allocator that satisfies the request, then the special value omp\_null\_allocator is returned. For any memory-allocator-retrieving routine that takes a devs argument, if the array to which the argument points has more than ndevs values, the additional values are ignored. Each of these routines returns an allocator that may be used anywhere that requires a predefined allocator specified in Table 8.3. The allocator is associated with a target memory space if any of the selected devices is not the current device.

## Restrictions

The restrictions to memory-allocator-retrieving routines are as follows:

• These routines must only be invoked on the host device.

• The memspace argument must not be one of the predefined memory spaces.

• For any memory-allocator-retrieving routine that has a devs argument, the argument must point to an array that contains at least ndevs values.

• For any memory-allocator-retrieving routine that has a dev or devs argument, the value of the dev argument the ndevs values of the array to which devs points must be conforming device numbers.

## Cross References

• Memory Allocators, see Section 8.2

• Memory Spaces, see Section 8.1

## 27.8.1 omp\_get\_devices\_allocator Routine

<table><tr><td>Name: omp_get_devices_allocatorCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-allocator-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>ndevs</td><td>integer</td><td>intent(in), positive</td></tr><tr><td>devs</td><td>integer</td><td>intent(in), pointer</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_devices\_allocator(int ndevs, const int <sub>\*</sub>devs, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function &

omp\_get\_devices\_allocator(ndevs, devs, memspace)

integer, intent(in) :: ndevs, devs(<sub>\*</sub>)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_devices\_allocator routine is a memory-allocator-retrieving routine. The devices selected by the routine are those specified in the devs argument.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocator Retrieving Routines, see Section 27.8

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.8.2 omp\_get\_device\_allocator Routine

<table><tr><td>Name: omp_get_device_allocatorCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-allocator-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>dev</td><td>integer</td><td>intent(in)</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_device\_allocator(int dev, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function &

omp\_get\_device\_allocator(dev, memspace)

integer, intent(in) :: dev

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_device\_allocator routine is a memory-allocator-retrieving routine. The device selected by the routine is the device specified in the dev argument.

Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocator Retrieving Routines, see Section 27.8

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.8.3 omp\_get\_devices\_and\_host\_allocator Routine

<table><tr><td>Name:omp_get_devices_and_host_allocatorCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-allocator-retrieving</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>ndevs</td><td>integer</td><td>intent(in), positive</td></tr><tr><td>devs</td><td>integer</td><td>intent(in), pointer</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_devices\_and\_host\_allocator( int ndevs, const int <sub>\*</sub>devs, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function &

omp\_get\_devices\_and\_host\_allocator(ndevs, devs, memspace)

integer, intent(in) :: ndevs, devs(<sub>\*</sub>)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_devices\_and\_host\_allocator routine is a memory-allocator-retrieving routine. The devices selected by the routine are the host device and those specified in the devs argument.

Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocator Retrieving Routines, see Section 27.8

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.8.4 omp\_get\_device\_and\_host\_allocator Routine

<table><tr><td>Name:omp_get_device_and_host_allocatorCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-allocator-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>dev</td><td>integer</td><td>intent(in)</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_device\_and\_host\_allocator(int dev, omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function &

omp\_get\_device\_and\_host\_allocator(dev, memspace)

integer, intent(in) :: dev

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_device\_and\_host\_allocator routine is a memory-allocator-retrieving routine. The devices selected by the routine are the host device and the device specified in the dev argument.

Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocator Retrieving Routines, see Section 27.8

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.8.5 omp\_get\_devices\_all\_allocator Routine

<table><tr><td>Name: omp_get_devices_all_allocatorCategory: function</td><td>Properties: all-device-threads-binding, memory-management-routine,memory-allocator-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr><tr><td>memspace</td><td>memspace_handle</td><td>intent(in), omp</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_devices\_all\_allocator(

omp\_memspace\_handle\_t memspace);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function &

omp\_get\_devices\_all\_allocator(memspace)

integer (kind=omp\_memspace\_handle\_kind), intent(in) :: memspace

Fortran

## Effect

The omp\_get\_devices\_all\_allocator routine is a memory-allocator-retrieving routine. The devices selected by the routine are all available devices.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Space Retrieving Routines, see Section 27.1

• OpenMP memspace\_handle Type, see Section 20.8.11

## 27.9 omp\_set\_default\_allocator Routine

<table><tr><td colspan="2">Name: omp_set_default_allocatorCategory: subroutine</td><td>Properties: binding-implicit-task-binding, memory-management-routine</td></tr><tr><td colspan="3">Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>omp, intent(in)</td></tr><tr><td colspan="3">PrototypesC / C++void omp_set_default_allocator(omp_allocator_handle_t allocator);C / C++Fortran</td></tr><tr><td colspan="3">subroutine omp_set_default_allocator(allocator)integer (kind=omp_allocator_handle_kind), intent(in) :: &amp; allocatorFortran</td></tr></table>

## Effect

The efect of the omp\_set\_default\_allocator is to set the value of the def-allocator-var ICV of the binding implicit task to the value specified in the allocator argument. Thus, it sets the default memory allocator to be used by allocation calls, allocate clauses and allocate and allocators directives that do not specify an allocator. This routine has the binding-implicit-task binding property so the binding task set for an omp\_set\_default\_allocator region is the binding implicit task.

## Restrictions

The restrictions to the omp\_set\_default\_allocator routine are as follows:

• The allocator argument must be a valid memory allocator handle.

## Cross References

• allocate Clause, see Section 8.6

• allocate Directive, see Section 8.5

• OpenMP allocator\_handle Type, see Section 20.8.1

• allocators Construct, see Section 8.7

• Memory Allocators, see Section 8.2

• def-allocator-var ICV, see Table 3.1

## 27.10 omp\_get\_default\_allocator Routine

<table><tr><td>Name: omp_get_default_allocatorCategory: function</td><td>Properties: binding-implicit-task-binding, memory-management-routine</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>allocator_handle</td><td>default</td></tr></table>

## Prototypes

C / C++

omp\_allocator\_handle\_t omp\_get\_default\_allocator(void);

C / C++

Fortran

integer (kind=omp\_allocator\_handle\_kind) function & omp\_get\_default\_allocator()

## Fortran

## Effect

The omp\_get\_default\_allocator routine returns the value of the def-allocator-var ICV of the binding implicit task, which is a handle to the memory allocator to be used by allocation calls, allocate clauses and allocate and allocators directives that do not specify an allocator. This routine has the binding-implicit-task binding property, so the binding task set for an omp\_get\_default\_allocator region is the binding implicit task.

## Cross References

• allocate Clause, see Section 8.6

• allocate Directive, see Section 8.5

• OpenMP allocator\_handle Type, see Section 20.8.1

• allocators Construct, see Section 8.7

• Memory Allocators, see Section 8.2

• def-allocator-var ICV, see Table 3.1

## 27.11 Memory Allocating Routines

This section describes the memory-allocating routines, which are routines that have the memory-allocating-routine property. Each of these routines requests a memory allocation from the memory allocator that its allocator argument specifies. If the allocator argument is omp\_null\_allocator, the routine uses the memory allocator specified by the def-allocator-var ICV of the binding implicit task. Upon success, these routines return a pointer to the allocated memory. Otherwise, the behavior that the omp\_atk\_fallback trait of the allocator specifies is followed. Pointers returned by these routines are considered device pointers if at least one of the devices associated with the allocator that the allocator argument represents is not the current device.

OpenMP provides several kinds of memory-allocating routines. The memory allocated by raw-memory-allocating routines, which have the raw-memory-allocating-routine property, is uninitialized. The memory allocated by zeroed-memory-allocating routines, which have the zeroed-memory-allocating-routine property, is set to zero before the routine returns.

The memory allocated by aligned-memory-allocating routines, which have the aligned-memory-allocating-routine property, is byte-aligned to at least the maximum of the alignment required by malloc, the omp\_atk\_alignment trait of the allocator and the value of their alignment argument. The memory allocated by all other memory-allocating routines is byte-aligned to at least the maximum of the alignment required by malloc and the omp\_atk\_alignment trait of the allocator.

Raw-memory-allocating routines request a memory allocation of size bytes from the specified memory allocator. Zeroed-memory-allocating routines request a memory allocation for an array of nmemb elements, each of which has a size of size bytes. If any of the size or nmemb arguments are zero, these routines return NULL.

Memory-reallocating routines deallocate the memory to which the ptr argument points and request a new memory allocation of size bytes from the memory allocator that is specified by the allocator argument. If the free\_allocator argument is omp\_null\_allocator, the implementation will determine that value automatically. If the allocator argument is omp\_null\_allocator, the

behavior is as if the memory allocator that allocated the memory to which ptr argument points is passed to the allocator argument. Upon success, each of these routines returns a (possibly moved) pointer to the allocated memory and the contents of the new object will be the same as that of the old object prior to deallocation, up to the minimum size of the old allocated size and size. Any bytes in the new object beyond the old allocated size will have unspecified values. If the allocation failed, the behavior that the omp\_atk\_fallback trait of the allocator specifies will be followed. If ptr is NULL, a memory-reallocating routine behaves the same as a raw-memory-allocating routine with the same size and allocator arguments. If size is zero, a memory-reallocating routine returns NULL and the old allocation is deallocated. If size is not zero, the old allocation will be deallocated if and only if the routine returns a non-null value.

The C++ version of all memory-allocating routines have the overloaded property since they are overloaded routines for which the allocator argument may be omitted, in which case the efect is as if omp\_null\_allocator is specified.

![](images/4d5adb41886ddb79b86288fbd96da0a6526401cb332b1beb5e50d0a9512d223f.jpg)

## Restrictions

The restrictions to memory-allocating routines are as follows:

• Unless the unified\_address clause is specified or the current device is an associated device of the allocator, pointer arithmetic is not supported on the pointer that a memory-allocating routine returns.

• Each allocator and free\_allocator argument must be a constant expression that evaluates to a handle that represents a predefined memory allocator.

• The value of the alignment argument to an aligned-memory-allocating routine must be a power of two.

• The value of a size argument to an aligned-memory-allocating routine must be a multiple of the alignment argument.

• The value of the ptr argument to a memory-reallocating routine must have been returned by a memory-allocating routine.

• If the free\_allocator argument is specified for a memory-reallocating routine, it must be the memory allocator to which the previous allocation request was made.

• Using a memory-reallocating routine on memory that was already deallocated or that was allocated by an allocator that has already been destroyed with omp\_destroy\_allocator results in unspecified behavior.

• Unless a requires directive with the dynamic\_allocators clause is present in the same compilation unit, memory-allocating routines that appear in target regions must not pass omp\_null\_allocator as the allocator or free\_allocator argument.

## Cross References

• Memory Allocators, see Section 8.2

• def-allocator-var ICV, see Table 3.1

• omp\_destroy\_allocator Routine, see Section 27.7

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 27.11.1 omp\_alloc Routine

<table><tr><td>Name: omp_allocCategory: function</td><td>Properties: iso_c_binding, memory-allocating-routine, memory-management-routine, overloaded, raw-memory-allocating-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

## Prototypes

void <sub>\*</sub>omp\_alloc(size\_t size, omp\_allocator\_handle\_t allocator);

void <sub>\*</sub>omp\_alloc(size\_t size,

C++

omp\_allocator\_handle\_t allocator = omp\_null\_allocator);

C++

Fortran

type (c\_ptr) function omp\_alloc(size, allocator) bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_ptr, c\_size\_t

integer (kind=c\_size\_t), value :: size

integer (kind=omp\_allocator\_handle\_kind), value :: allocator

Fortran

## Effect

The omp\_alloc routine is a raw-memory-allocating routine.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

## 27.11.2 omp\_aligned\_alloc Routine

<table><tr><td>Name: omp_aligned_allocCategory: function</td><td>Properties: aligned-memory-allocating-routine, iso_c_binding,memory-allocating-routine, memory-management-routine, overloaded, raw-memory-allocating-routine</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>alignment</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

![](images/13c018584191cf5c7a79e0579256c0db6ef99a3d8cddaca017286adc1bce9c9e.jpg)

type (c\_ptr) function omp\_aligned\_alloc(alignment, size, & allocator) bind(c) use, intrinsic :: iso\_c\_binding, only : c\_ptr, c\_size\_t integer (kind=c\_size\_t), value :: alignment, size integer (kind=omp\_allocator\_handle\_kind), value :: allocator

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

## 27.11.3 omp\_calloc Routine

<table><tr><td>Name: omp_callocCategory: function</td><td>Properties: iso_c_binding, memory-allocating-routine, memory-management-routine, overloaded, zeroed-memory-allocating-routine</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>nmemb</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

Prototypes

void <sub>\*</sub>omp\_calloc(size\_t nmemb, size\_t size,

omp\_allocator\_handle\_t allocator);

C++

void <sub>\*</sub>omp\_calloc(size\_t nmemb, size\_t size,

omp\_allocator\_handle\_t allocator = omp\_null\_allocator);

C++

Fortran

type (c\_ptr) function omp\_calloc(nmemb, size, allocator) & bind(c) use, intrinsic :: iso\_c\_binding, only : c\_ptr, c\_size\_t integer (kind=c\_size\_t), value :: nmemb, size integer (kind=omp\_allocator\_handle\_kind), value :: allocator

Fortran

Effect

The omp\_calloc routine is a zeroed-memory-allocating routines.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

27.11.4 omp\_aligned\_calloc Routine

<table><tr><td>Name: omp_aligned_callocCategory: function</td><td>Properties: aligned-memory-allocating-routine, iso_c_binding,memory-allocating-routine, memory-management-routine, overloaded,zeroed-memory-allocating-routine</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>alignment</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>nmemb</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

## Prototypes

C

void <sub>\*</sub>omp\_aligned\_calloc(size\_t alignment, size\_t nmemb, size\_t size, omp\_allocator\_handle\_t allocator);

C

C++

void <sub>\*</sub>omp\_aligned\_calloc(size\_t alignment, size\_t nmemb,

size\_t size,

omp\_allocator\_handle\_t allocator = omp\_null\_allocator);

C++

Fortran

type (c\_ptr) function omp\_aligned\_calloc(alignment, nmemb, size, & allocator) bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_ptr, c\_size\_t

integer (kind=c\_size\_t), value :: alignment, nmemb, size

integer (kind=omp\_allocator\_handle\_kind), value :: allocator

Fortran

## Effect

The omp\_aligned\_calloc routine is a zeroed-memory-allocating routine and an aligned-memory-allocating routine.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

27.11.5 omp\_realloc Routine

<table><tr><td>Name: omp_reallocCategory: function</td><td>Properties: iso_c_binding, memory-allocating-routine, memory-management-routine, memory-reallocating-routine, overloaded</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>c_ptr</td><td>default</td></tr><tr><td>ptr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>size</td><td>c_size_t</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr><tr><td>free_allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

## Prototypes

void <sub>\*</sub>omp\_realloc(void <sub>\*</sub>ptr, size\_t size,

omp\_allocator\_handle\_t allocator,

omp\_allocator\_handle\_t free\_allocator);

C

C++

void <sub>\*</sub>omp\_realloc(void <sub>\*</sub>ptr, size\_t size,

omp\_allocator\_handle\_t allocator = omp\_null\_allocator,

omp\_allocator\_handle\_t free\_allocator = omp\_null\_allocator);

C++

Fortran

type (c\_ptr) function omp\_realloc(ptr, size, allocator, &

free\_allocator) bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_ptr, c\_size\_t

type (c\_ptr), value :: ptr

integer (kind=c\_size\_t), value :: size integer (kind=omp\_allocator\_handle\_kind), value :: allocator, & free\_allocator

Fortran

## Effect

The omp\_realloc routine is a memory-reallocating routine.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

## 27.12 omp\_free Routine

<table><tr><td>Name: omp_freeCategory: subroutine</td><td>Properties: iso_c_binding, memory-management-routine, overloaded</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>ptr</td><td>c_ptr</td><td>iso_c, value</td></tr><tr><td>allocator</td><td>allocator_handle</td><td>value, omp</td></tr></table>

## Prototypes

void omp\_free(void <sub>\*</sub>ptr, omp\_allocator\_handle\_t allocator);

C

C++

void omp\_free(void <sub>\*</sub>ptr,

omp\_allocator\_handle\_t allocator = omp\_null\_allocator);

C++

Fortran

subroutine omp\_free(ptr, allocator) bind(c)

use, intrinsic :: iso\_c\_binding, only : c\_ptr

type (c\_ptr), value :: ptr

integer (kind=omp\_allocator\_handle\_kind), value :: allocator

Fortran

## Effect

The omp\_free routine deallocates the memory to which the ptr argument points. If the allocator argument is omp\_null\_allocator, the implementation will determine that value automatically. If ptr is NULL, no operation is performed.

C++

The C++ version of the omp\_free routine has the overloaded property since it is an overloaded routine for which the allocator argument may be omitted, in which case the efect is as if omp\_null\_allocator is specified.

C++

## Restrictions

The restrictions to the omp\_free routine are as follows:

• The ptr argument must have been returned by a memory-allocating routine.

• If the allocator argument is specified it must be the memory allocator to which the allocation request was made.

• Using omp\_free on memory that was already deallocated or that was allocated by an allocator that has already been destroyed with omp\_destroy\_allocator results in unspecified behavior.

## Cross References

• OpenMP allocator\_handle Type, see Section 20.8.1

• Memory Allocating Routines, see Section 27.11

• Memory Allocators, see Section 8.2

• omp\_destroy\_allocator Routine, see Section 27.7

## 28 Lock Routines
