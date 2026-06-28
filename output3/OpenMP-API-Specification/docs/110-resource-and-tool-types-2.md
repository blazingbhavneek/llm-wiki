
This section describes OpenMP types related to resource-relinquishing routines.

20.11.1 OpenMP pause\_resource Type

<table><tr><td>Name: pause_resourceProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_pause_soft</td><td>1</td><td>omp</td></tr><tr><td>omp_pause_hard</td><td>2</td><td>omp</td></tr><tr><td>omp_pause_stop_tool</td><td>3</td><td>omp</td></tr></table>

## Type Definition

C / C++

typedef enum omp\_pause\_resource\_t {

omp\_pause\_soft = 1,

omp\_pause\_hard = 2,

omp\_pause\_stop\_tool = 3

} omp\_pause\_resource\_t;

C / C++

Fortran

integer (kind=omp\_pause\_resource\_kind), &

parameter :: omp\_pause\_soft = 1

integer (kind=omp\_pause\_resource\_kind), &

parameter :: omp\_pause\_hard = 2

integer (kind=omp\_pause\_resource\_kind), &

parameter :: omp\_pause\_stop\_tool = 3

## Fortran

The pause\_resource OpenMP type is used in resource-relinquishing routines to specify the resources that the instance of the routine relinquishes. The valid constants for the pause\_resource OpenMP type must include those shown above.

When specified and successful, the omp\_pause\_hard value results in a hard pause, which implies that the OpenMP state is not guaranteed to persist across the resource-relinquishing routine call. A hard pause may relinquish any data allocated by OpenMP on specified devices, including data allocated by device memory routines as well as data present on the devices as a result of a declare target directive or map-entering constructs. A hard pause may also relinquish any data associated with a threadprivate directive. When relinquished and when applicable, base language appropriate deallocation/finalization is performed. When relinquished and when applicable, mapped variables on a device will not be copied back from the device to the host device.

When specified and successful, the omp\_pause\_soft value results in a soft pause for which the OpenMP state is guaranteed to persist across the resource-relinquishing routine call, with the exception of any data associated with a threadprivate directive, which may be relinquished across the call. When relinquished and when applicable, base language appropriate deallocation/finalization is performed.

Note – A hard pause may relinquish more resources, but may resume processing regions more slowly. A soft pause allows regions to restart more quickly, but may relinquish fewer resources. An OpenMP implementation will reclaim resources as needed for regions encountered after the resource-relinquishing routine region. Since a hard pause may unmap data on the specified devices, appropriate mapping operations are required before using data on the specified devices after the resource-relinquishing routine region.

When specified and successful, the omp\_pause\_stop\_tool value implies the efects described above for the omp\_pause\_hard value. Additionally, unless otherwise specified, the value implies that the implementation will shutdown the OMPT interface as if program execution is ending.

## 20.12 OpenMP Tool Types

This section describes OpenMP types that support the use of tools.

## 20.12.1 OpenMP control\_tool Type

```txt
Name: control_tool
Properties: omp
Base Type: enumeration
Values
Name
omp_control_tool_start
omp_control_tool_pause
omp_control_tool_flush
omp_control_tool_end
Value
1
2
3
4
Properties
omp
omp
omp
omp
omp
omp
C / C++
typedef enum omp_control_tool_t {
    omp_control_tool_start = 1,
    omp_control_tool_pause = 2,
    omp_control_tool_flush = 3,
    omp_control_tool_end = 4
} omp_control_tool_t;
C / C++
Fortran
integer (kind=omp_control_tool_kind), &
    parameter :: omp_control_tool_start = 1
integer (kind=omp_control_tool_kind), &
    parameter :: omp_control_tool_pause = 2
integer (kind=omp_control_tool_kind), &
    parameter :: omp_control_tool_flush = 3
integer (kind=omp_control_tool_kind), &
    parameter :: omp_control_tool_end = 4
Fortran
The control_tool OpenMP type is used in tool support routines to specify tool commands.
Table 20.5 describes the actions that standard commands request from a tool. The valid constants for the control_tool OpenMP type must include those shown above.
```

Tool-defined values for the control\_tool OpenMP type must be greater than or equal to 64 and less than or equal to 2147483647 (INT32\_MAX). Tools must ignore control\_tool values that they are not explicitly designed to handle. Other values accepted by a tool for the control\_tool OpenMP type are tool defined.

TABLE 20.5: Standard Tool Control Commands

<table><tr><td>Command</td><td>Action</td></tr><tr><td>omp_control_tool_start</td><td>Start or restart monitoring if it is off. If monitoring is already on, this command is idempotent. If monitoring has already been turned off permanently, this command will have no effect.</td></tr><tr><td>omp_control_tool_pause</td><td>Temporarily turn monitoring off. If monitoring is already off, it is idempotent.</td></tr><tr><td>omp_control_tool_flush</td><td>Flush any data buffered by a tool. This command may be applied whether monitoring is on or off.</td></tr><tr><td>omp_control_tool_end</td><td>Turn monitoring off permanently; the tool finalizes itself and flushes all output.</td></tr></table>

20.12.2 OpenMP control\_tool\_result Type

<table><tr><td>Name: control_tool_resultProperties: omp</td><td colspan="2">Base Type: enumeration</td></tr><tr><td colspan="3">Values</td></tr><tr><td>Name</td><td>Value</td><td>Properties</td></tr><tr><td>omp_control_tool_notool</td><td>-2</td><td>omp</td></tr><tr><td>omp_control_tool_nocallback</td><td>-1</td><td>omp</td></tr><tr><td>omp_control_tool_success</td><td>0</td><td>omp</td></tr><tr><td>omp_control_tool_ignored</td><td>1</td><td>omp</td></tr><tr><td colspan="3">Type DefinitionC / C++typedef enum omp_control_tool_result_t {omp_control_tool_notool = -2,omp_control_tool_nocallback = -1,omp_control_tool_success = 0,omp_control_tool_ignored = 1} omp_control_tool_result_t;</td></tr></table>

## Fortran

integer (kind=omp\_control\_tool\_result\_kind), & parameter :: omp\_control\_tool\_notool = -2 integer (kind=omp\_control\_tool\_result\_kind), & parameter :: omp\_control\_tool\_nocallback = -1 integer (kind=omp\_control\_tool\_result\_kind), & parameter :: omp\_control\_tool\_success = 0 integer (kind=omp\_control\_tool\_result\_kind), & parameter :: omp\_control\_tool\_ignored = 1

## Fortran

The control\_tool\_result OpenMP type is used in tool support routines to specify the results of tool commands. The valid constants for the control\_tool\_result OpenMP type must include those shown above.

# 21 Parallel Region Support Routines
