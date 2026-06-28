
This chapter describes routines that specify and obtain information about thread afinity policies, which govern the placement of threads in the execution environment of OpenMP programs.

## 29.1 omp\_get\_proc\_bind Routine

<table><tr><td>Name: omp_get_proc_bindCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>proc_bind</td><td>default</td></tr></table>

## Prototypes

C / C++

omp\_proc\_bind\_t omp\_get\_proc\_bind(void);

C / C++

Fortran

integer (kind=omp\_proc\_bind\_kind) function omp\_get\_proc\_bind()

Fortran

## Effect

The efect of this routine is to return the value of the first element of the bind-var ICV of the current task, which will be used for the subsequent nested parallel regions that do not specify a proc\_bind clause. See Section 12.1.3 for the rules that govern the thread afinity policy.

## Cross References

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• bind-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

• OpenMP proc\_bind Type, see Section 20.10.1

## 29.2 omp\_get\_num\_places Routine

<table><tr><td>Name: omp_get_num_placesCategory: function</td><td>Properties: all-device-threads-binding</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_num\_places(void);

C / C++

Fortran

integer function omp\_get\_num\_places()

Fortran

## Effect

The omp\_get\_num\_places routine returns the number of places in the place list. This value is equivalent to the number of places in the place-partition-var ICV in the execution environment of the initial task.

Cross References

• place-partition-var ICV, see Table 3.1

## 29.3 omp\_get\_place\_num\_procs Routine

<table><tr><td>Name: omp_get_place_num_procsCategory: function</td><td>Properties: all-device-threads-binding,ICV-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>place_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_place\_num\_procs(int place\_num);

C / C++

Fortran

integer function omp\_get\_place\_num\_procs(place\_num)

Fortran

## Effect

The omp\_get\_place\_num\_procs routine returns the number of processors associated with the place numbered place\_num as per the place-partition-var ICV. The routine returns zero when place\_num is negative or is greater than or equal to the value returned by omp\_get\_num\_places.

## Cross References

• place-partition-var ICV, see Table 3.1

• omp\_get\_num\_places Routine, see Section 29.2

## 29.4 omp\_get\_place\_proc\_ids Routine

<table><tr><td colspan="2">Name: omp_get_place_proc_idsCategory: subroutine</td><td>Properties: all-device-threads-binding,ICV-retrieving</td></tr><tr><td colspan="3">Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>place_num</td><td>integer</td><td>default</td></tr><tr><td>ids</td><td>integer</td><td>pointer</td></tr><tr><td colspan="3">PrototypesC / C++void omp_get_place_proc_ids(int place_num, int *ids);C / C++Fortransubroutine omp_get_place_proc_ids(place_num, ids)integer place_num, ids(*)Fortran</td></tr></table>

## Effect

The omp\_get\_place\_proc\_ids routine returns the numerical identifiers of each processor associated with the place numbered place\_num as per the place-partition-var ICV. The numerical identifiers are non-negative and their meaning is implementation defined. The numerical identifiers are returned in the array ids and their order in the array is implementation defined. The array must be suficiently large to contain omp\_get\_place\_num\_procs(place\_num) integers; otherwise, the behavior is unspecified. The routine has no efect when place\_num has a negative value or a value greater than or equal to omp\_get\_num\_places.

Cross References

• OMP\_PLACES, see Section 4.1.6

• omp\_get\_num\_places Routine, see Section 29.2

• omp\_get\_place\_num\_procs Routine, see Section 29.3

## 29.5 omp\_get\_place\_num Routine

<table><tr><td colspan="2">Name: omp_get_place_numCategory: function</td><td colspan="2">Properties: default</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">integer</td><td>default</td></tr><tr><td colspan="4">PrototypesC / C++int omp_get_place_num(void);C / C++Fortraninteger function omp_get_place_num()Fortran</td></tr></table>

When the encountering thread is bound to a place, the omp\_get\_place\_num routine returns the place number associated with the thread. The returned value is between zero and one less than the value returned by omp\_get\_num\_places, inclusive. When the encountering thread is not bound to a place, the routine returns -1.

Cross References

• omp\_get\_num\_places Routine, see Section 29.2

## 29.6 omp\_get\_partition\_num\_places Routine

<table><tr><td colspan="2">Name: omp_get_partition_num_placesCategory: function</td><td colspan="2">Properties: ICV-retrieving</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">integer</td><td>default</td></tr></table>

Prototypes

C / C++

int omp\_get\_partition\_num\_places(void);

C / C++

Fortran

integer function omp\_get\_partition\_num\_places()

Fortran

Effect

The omp\_get\_partition\_num\_places routine returns the number of places in the place-partition-var ICV.

Cross References

• place-partition-var ICV, see Table 3.1

## 29.7 omp\_get\_partition\_place\_nums Routine

<table><tr><td>Name: omp_get_partition_place_numsCategory: subroutine</td><td>Properties: ICV-retrieving</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>place_nums</td><td>integer</td><td>pointer</td></tr></table>

Prototypes

C / C++

void omp\_get\_partition\_place\_nums(int <sub>\*</sub>place\_nums);

C / C++

Fortran

subroutine omp\_get\_partition\_place\_nums(place\_nums)

integer place\_nums(\*)

Fortran

## Effect

The omp\_get\_partition\_place\_nums routine returns the list of place numbers that correspond to the places in the place-partition-var ICV of the innermost implicit task. The array must be suficiently large to contain omp\_get\_partition\_num\_places integers; otherwise, the behavior is unspecified.

## Cross References

• place-partition-var ICV, see Table 3.1

• omp\_get\_partition\_num\_places Routine, see Section 29.6

## 29.8 omp\_set\_affinity\_format Routine

<table><tr><td>Name: omp_set_affinity_formatCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>format</td><td>char</td><td>pointer, intent(in)</td></tr></table>

## Prototypes

C / C++

void omp\_set\_affinity\_format(const char <sub>\*</sub>format);

C / C++

Fortran

subroutine omp\_set\_affinity\_format(format)

character(len=<sub>\*</sub>), intent(in) :: format

## Fortran

## Effect

The omp\_set\_affinity\_format routine sets the afinity format to be used on the device by setting the value of the afinity-format-var ICV. The value of the ICV is set by copying the character string specified by the format argument into the ICV on the current device.

This routine has the described efect only when called from a sequential part of the program. When called from within a parallel or teams region, the efect of this routine is implementation defined.

When called from a sequential part of the program, the binding thread set for an omp\_set\_affinity\_format region is the encountering thread. When called from within any parallel or teams region, the binding thread set (and binding region, if required) for the omp\_set\_affinity\_format region is implementation defined.

## Restrictions

Restrictions to the omp\_set\_affinity\_format routine are as follows:

• When called from within a target region the efect is unspecified.

<table><tr><td colspan="2">Name: omp_get_affinity_formatCategory: function</td><td colspan="2">Properties: ICV-retrieving</td></tr><tr><td colspan="4">Return Type and Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">size_t</td><td>default</td></tr><tr><td>buffer</td><td colspan="2">char</td><td>pointer, intent(out)</td></tr><tr><td>size</td><td colspan="2">size_t</td><td>default</td></tr></table>

## Cross References

• OMP\_AFFINITY\_FORMAT, see Section 4.3.5

• OMP\_DISPLAY\_AFFINITY, see Section 4.3.4

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• afinity-format-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

• teams Construct, see Section 12.2

## 29.9 omp\_get\_affinity\_format Routine

## Prototypes

C / C++

size\_t omp\_get\_affinity\_format(char <sub>\*</sub>bufer, size\_t size);

C / C++

Fortran

integer function omp\_get\_affinity\_format(bufer)

character(len=<sub>\*</sub>), intent(out) :: bufer

Fortran

## Effect

C / C++

The omp\_get\_affinity\_format routine returns the number of characters in the afinity-format-var ICV on the current device, excluding the terminating null byte (’\0’) and, if size is non-zero, writes the value of the afinity-format-var ICV on the current device to bufer followed by a null byte. If the return value is larger or equal to size, the afinity format specification is truncated, with the terminating null byte stored to bufer [size-1]. If size is zero, nothing is stored and bufer may be NULL.

C / C++

## Fortran

The omp\_get\_affinity\_format routine returns the number of characters that are required to hold the afinity-format-var ICV on the current device and writes the value of the afinity-format-var ICV on the current device to bufer. If the return value is larger than len(bufer), the afinity format specification is truncated.

## Fortran

If the bufer argument does not conform to the specified format then the result is implementation defined.

When called from a sequential part of the program, the binding thread set for an omp\_get\_affinity\_format region is the encountering thread. When called from within any parallel or teams region, the binding thread set (and binding region, if required) for the omp\_get\_affinity\_format region is implementation defined.

## Restrictions

Restrictions to the omp\_get\_affinity\_format routine are as follows:

• When called from within a target region the efect is unspecified.

## Cross References

• afinity-format-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

• target Construct, see Section 15.8

• teams Construct, see Section 12.2

## 29.10 omp\_display\_affinity Routine

<table><tr><td>Name: omp_display_affinityCategory: subroutine</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>format</td><td>char</td><td>pointer, intent(in)</td></tr></table>

## Prototypes

C / C++

void omp\_display\_affinity(const char <sub>\*</sub>format);

C / C++

Fortran

subroutine omp\_display\_affinity(format) character(len=<sub>\*</sub>), intent(in) :: format

## Fortran

## Effect

The omp\_display\_affinity routine prints the thread afinity information of the encountering thread in the format specified by the format argument, followed by a new-line. If the format is NULL (for C/C++) or a zero-length string (for Fortran and C/C++), the value of the afinity-format-var ICV is used. If the format argument does not conform to the specified format then the result is implementation defined.

## Restrictions

Restrictions to the omp\_display\_affinity routine are as follows:

• When called from within a target region the efect is unspecified.

## Cross References

• afinity-format-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 29.11 omp\_capture\_affinity Routine

<table><tr><td>Name: omp_capture_affinityCategory: function</td><td>Properties: default</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>size_t</td><td>default</td></tr><tr><td>buffer</td><td>char</td><td>pointer, intent(out)</td></tr><tr><td>size</td><td>size_t</td><td>default</td></tr><tr><td>format</td><td>char</td><td>pointer, intent(in)</td></tr></table>

## Prototypes

C / C++

size\_t omp\_capture\_affinity(char <sub>\*</sub>bufer, size\_t size, const char <sub>\*</sub>format);

C / C++

Fortran

integer function omp\_capture\_affinity(bufer, format) character(len=<sub>\*</sub>), intent(out) :: bufer character(len=<sub>\*</sub>), intent(in) :: format

Fortran

## Effect

C / C++

The omp\_capture\_affinity routine returns the number of characters in the entire thread afinity information string excluding the terminating null byte (’\0’). If size is non-zero, it writes the thread afinity information of the encountering thread in the format specified by the format argument into the character string bufer followed by a null byte. If the return value is larger or equal to size, the thread afinity information string is truncated, with the terminating null byte stored to bufer [size-1]. If size is zero, nothing is stored and bufer may be NULL. If the format is NULL or a zero-length string, the value of the afinity-format-var ICV is used.

C / C++

Fortran

The omp\_capture\_affinity routine returns the number of characters required to hold the entire thread afinity information string and prints the thread afinity information of the encountering thread into the character string bufer with the size of len(bufer) in the format specified by the format argument. If the format is a zero-length string, the value of the afinity-format-var ICV is used. If the return value is larger than len(bufer), the thread afinity information string is truncated. If the format is a zero-length string, the value of the afinity-format-var ICV is used.

Fortran

If the format argument does not conform to the specified format then the result is implementation defined.

## Restrictions

Restrictions to the omp\_capture\_affinity routine are as follows:

• When called from within a target region the efect is unspecified.

## Cross References

• afinity-format-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 30 Execution Control Routines
