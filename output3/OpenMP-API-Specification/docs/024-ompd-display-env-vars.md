
This section defines environment variables that afect operation of the OMPD tool interface.

## 4.6.1 OMP\_DEBUG

The OMP\_DEBUG environment variable sets the debug-var ICV, which controls whether an OpenMP runtime collects information that an OMPD library may need to support a tool. The value of this environment variable must be one of the following:

## enabled | disabled

If OMP\_DEBUG is set to any value other than enabled or disabled then the behavior is implementation defined.

## Example:

export OMP\_DEBUG=enabled

## Cross References

• Enabling Runtime Support for OMPD, see Section 38.3.1

• OMPD Overview, see Chapter 38

• debug-var ICV, see Table 3.1

## 4.7 OMP\_DISPLAY\_ENV

The OMP\_DISPLAY\_ENV environment variable instructs the runtime to display the information as described in the omp\_display\_env routine section (Section 30.4). The value of the OMP\_DISPLAY\_ENV environment variable may be set to one of these values:

## true | false | verbose

If the environment variable is set to true, the efect is as if the omp\_display\_env routine is called with the verbose argument set to false at the beginning of the program. If the environment variable is set to verbose, the efect is as if the omp\_display\_env routine is called with the verbose argument set to true at the beginning of the program. If the environment variable is undefined or set to false, the runtime does not display any information. For all values of the environment variable other than true, false, and verbose, the displayed information is unspecified.

## Example:

## export OMP\_DISPLAY\_ENV=true

For the output of the above example, see Section 30.4.
