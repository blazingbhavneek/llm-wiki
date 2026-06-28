## Cross References

• omp\_display\_env Routine, see Section 30.4

# 5 Directive and Construct Syntax

This chapter describes the syntax of directives and clauses and their association with base language code. Directives are specified with various base language mechanisms that allow compilers to ignore the directives and conditionally compiled code if support of the OpenMP API is not provided or enabled. A compliant implementation must provide an option or interface that ensures that underlying support of all directives and conditional compilation mechanisms is enabled. In the remainder of this document, the phrase OpenMP compilation is used to mean a compilation with these OpenMP features enabled.

## Restrictions

Restrictions on OpenMP programs include:

• Unless otherwise specified, a program must not depend on any ordering of the evaluations of the expressions that appear in the clauses specified on a directive.

• Unless otherwise specified, a program must not depend on any side efects of the evaluations of the expressions that appear in the clauses specified on a directive.

C / C++

• The use of omp as the first preprocessing token of a pragma directive must be for OpenMP directives that are defined in this specification; OpenMP reserves these uses for OpenMP directives.

• The use of omp as the attribute namespace of an attribute specifier, or as the optional namespace qualifier within a sequence attribute, must be for OpenMP directives that are defined in this specification; OpenMP reserves these uses for such directives.

• The use of ompx as the first preprocessing token of a pragma directive must be for implementation defined extensions to the OpenMP directives; OpenMP reserves these uses for such extensions.

• The use of ompx as the attribute namespace of an attribute specifier, or as the optional namespace qualifier within a sequence attribute, must be for implementation defined extensions to the OpenMP directives; OpenMP reserves these uses for such extensions.

C / C++

Fortran

• In free form source files, the !\$omp sentinel must be used for OpenMP directives that are defined in this specification; OpenMP reserves these uses for such directives.

• In fixed form source files, sentinels that end with omp must be used for OpenMP directives that are defined in this specification; OpenMP reserves these uses for such directives.

• In free form source files, the !\$ompx sentinel must be used for implementation defined extensions to the OpenMP directives; OpenMP reserves these uses for such extensions.

• In fixed form source files, sentinels that end with omx must be used for implementation defined extensions to the OpenMP directives; OpenMP reserves these uses for such extensions.

## Fortran

• A clause name must be the name of a clause that is defined in this specification except for those that begin with ompx\_, which may be used for implementation defined extensions and which OpenMP reserves for such extensions.

• OpenMP reserves names that begin with the omp\_, ompt\_ and ompd\_ prefixes for names defined in this specification so OpenMP programs must not declare names that begin with them.

• OpenMP reserves names that begin with the ompx\_ prefix for implementation defined extensions so OpenMP programs must not declare names that begin with it.

C++

• OpenMP programs must not declare a namespace with the omp, ompx, ompt or ompd names, as these are reserved for the OpenMP implementation.

C++

Restrictions on explicit regions (that arise from executable directives) are as follows:

C++

• A throw executed inside a region that arises from a thread-limiting construct must cause execution to resume within the same region, and the same thread that threw the exception must catch it. If the directive also has the exception-aborting property then whether the exception is caught or the throw results in runtime error termination is implementation defined.

C++

Fortran

• A directive may not appear in a pure or simple procedure unless it has the pure property.

• A directive may not appear in a WHERE or FORALL construct.

• A directive may not appear in a DO CONCURRENT construct unless it has the pure property.

• If more than one image is executing the program, any image control statement, ERROR STOP statement, FAIL IMAGE statement, NOTIFY WAIT statement, collective subroutine call or access to a coindexed object that appears in an explicit region will result in unspecified behavior.

Fortran

## 5.1 Directive Format
