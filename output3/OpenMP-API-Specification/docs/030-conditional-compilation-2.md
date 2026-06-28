## 5.3 Conditional Compilation

In implementations that support a preprocessor, the \_OPENMP macro name is defined to have the decimal value yyyymm where yyyy and mm are the year and month designations of the version of the OpenMP API that the implementation supports.

Fortran

The OpenMP API requires Fortran lines to be compiled conditionally, as described in the following sections.

Fortran

## Restrictions

Restrictions to conditional compilation are as follows:

• A #define or a #undef preprocessing directive in user code must not define or undefine the \_OPENMP macro name.

Fortran

## 5.3.1 Free Source Form Conditional Compilation Sentinel

The following conditional compilation sentinel is recognized in free form source files:

## !\$

To enable conditional compilation, a line with a conditional compilation sentinel must satisfy the following criteria:

• The sentinel can appear in any column but must be preceded only by white space;

• The sentinel must appear as a single word with no intervening white space;

• Initial lines must have a blank character after the sentinel; and

• Continued lines must have an ampersand as the last non-blank character on the line, prior to any comment appearing on the conditionally compiled line.

Continuation lines can have an ampersand after the sentinel, with optional white space before and after the ampersand. If these criteria are met, the sentinel is replaced by two spaces. If these criteria are not met, the line is left unchanged.

Note – In the following example, the two forms for specifying conditional compilation in free source form are equivalent (the first line represents the position of the first 9 columns):

```c
!23456789
!$ iam = omp_get_thread_num() +          &
!$&     index

#ifdef _OPENMP
    iam = omp_get_thread_num() +          &
    &     index
#endif
```

Fortran

## 5.3.2 Fixed Source Form Conditional Compilation Sentinels

The following conditional compilation sentinels are recognized in fixed form source files:

```txt
! \$ | * \$ | c \$
```

To enable conditional compilation, a line with a conditional compilation sentinel must satisfy the following criteria:

• The sentinel must start in column 1 and appear as a single word with no intervening white space;

• After the sentinel is replaced with two spaces, initial lines must have a space or zero in column 6 and only white space and numbers in columns 1 through 5; and

• After the sentinel is replaced with two spaces, continuation lines must have a character other than a space or zero in column 6 and only white space in columns 1 through 5.

If these criteria are met, the sentinel is replaced by two spaces. If these criteria are not met, the line is left unchanged.

Note – In the following example, the two forms for specifying conditional compilation in fixed source form are equivalent (the first line represents the position of the first 9 columns):

```c
c23456789
!\$ 10 iam = omp_get_thread_num() +
!\$    &        index

#ifdef _OPENMP
    10 iam = omp_get_thread_num() +
        &        index
#endif
```
