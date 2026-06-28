# 31 Tool Support Routines

This chapter describes the OpenMP API routines that support the use of OpenMP tool interfaces.

## 31.1 omp\_control\_tool Routine

<table><tr><td>Name: omp_control_toolCategory: function</td><td>Properties: default</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>control_tool_result</td><td>default</td></tr><tr><td>command</td><td>control_tool</td><td>omp</td></tr><tr><td>modifier</td><td>integer</td><td>default</td></tr><tr><td>arg</td><td>void</td><td>C/C++ pointer</td></tr></table>

Prototypes

C / C++

omp\_control\_tool\_result\_t omp\_control\_tool(

omp\_control\_tool\_t command, int modifier, void <sub>\*</sub>arg);

C / C++

Fortran

integer (kind=omp\_control\_tool\_result\_kind) function &

omp\_control\_tool(command, modifier)

integer (kind=omp\_control\_tool\_kind) command

integer modifier

Fortran

## Effect

An OpenMP program may use the omp\_control\_tool routine to pass commands to a tool. An OpenMP program can use the routine to request: that a tool starts or restarts data collection when a code region of interest is encountered; that a tool pauses data collection when leaving the region of interest; that a tool flushes any data that it has collected so far; or that a tool ends data collection. Additionally, the omp\_control\_tool routine can be used to pass tool-specific commands to a particular tool.

Any values for modifier and arg are tool defined.

If the OMPT interface state is OMPT inactive, the OpenMP implementation returns

omp\_control\_tool\_notool. If the OMPT interface state is OMPT active, but no callback is registered for the tool-control event, the OpenMP implementation returns

omp\_control\_tool\_nocallback. An OpenMP implementation may return other

implementation defined negative values strictly smaller than -64; an OpenMP program may assume that any negative return value indicates that a tool has not received the command. A return value of omp\_control\_tool\_success indicates that the tool has performed the specified command. A return value of omp\_control\_tool\_ignored indicates that the tool has ignored the specified command. A tool may return other positive values strictly greater than 64 that are tool defined.

## Execution Model Events

The tool-control event occurs in the encountering thread inside the corresponding region.

## Tool Callbacks

A thread dispatches a registered control\_tool callback for each occurrence of a tool-control event. The callback executes in the context of the call that occurs in the user program. The callback may return any non-negative value, which will be returned to the OpenMP program by the OpenMP implementation as the return value of the omp\_control\_tool call that triggered the callback.

Arguments passed to the callback are those passed by the user to omp\_control\_tool. If the call is made in Fortran, the tool will be passed NULL as the third argument to the callback. If any of the standard commands is presented to a tool, the tool will ignore the modifier and arg argument values.

## Restrictions

Restrictions on access to the state of an OpenMP first-party tool are as follows:

• An OpenMP program may access the tool state modified by an OMPT callback only by using omp\_control\_tool.

## Cross References

• control\_tool Callback, see Section 34.8

• OpenMP control\_tool Type, see Section 20.12.1

• OpenMP control\_tool\_result Type, see Section 20.12.2

• OMPT Overview, see Chapter 32
