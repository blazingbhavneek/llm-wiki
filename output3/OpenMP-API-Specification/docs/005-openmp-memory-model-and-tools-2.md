3. The variable is flushed, with a strong flush, by the second thread; and

4. The value is read from the variable by the second thread.

If a flush is a release flush or acquire flush, it can enforce consistency between the views of memory of two synchronizing threads. A release flush guarantees that any prior operation that writes or reads a shared variable will appear to be completed before any operation that writes or reads the same shared variable and follows an acquire flush with which the release flush synchronizes (see Section 1.3.5 for more details on flush synchronization). A release flush will propagate the values of all shared variables in its temporary view to memory prior to the thread performing any subsequent atomic operation that may establish a synchronization. An acquire flush will discard any value of a shared variable in its temporary view to which the thread has not written since last performing a release flush, and it will load any value of a shared variable propagated by a release flush that synchronizes with it (according to the synchronizes-with relation) into its temporary view so that it may be subsequently read. Therefore, release flushes and acquire flushes may also be used to guarantee that a value written to a variable by one thread may be read by a second thread. To accomplish this, the programmer must ensure that the second thread has not written to the variable since its last acquire flush, and that the following sequence of events happen in this specific order:

1. The value is written to the variable by the first thread;

2. The first thread performs a release flush;

3. The second thread performs an acquire flush; and

4. The value is read from the variable by the second thread.

Note – OpenMP synchronization operations, described in Chapter 17 and in Chapter 28, are recommended for enforcing this order. Synchronization through variables is possible but is not recommended because the proper timing of flushes is dificult.

The flush properties that define whether a flush is a strong flush, a release flush, or an acquire flush are not mutually disjoint. A flush may be a strong flush and a release flush; it may be a strong flush and an acquire flush; it may be a release flush and an acquire flush; or it may be all three.

## 1.3.5 Flush Synchronization and Happens-Before Order

OpenMP supports thread synchronization with the use of release flushes and acquire flushes. For any such synchronization, a release flush is the source of the synchronization and an acquire flush is the sink of the synchronization, such that the release flush synchronizes with the acquire flush.

A release flush has one or more associated release sequences that define the set of modifications that may be used to establish a synchronization. A release sequence starts with an atomic operation that follows the release flush and modifies a shared variable and additionally includes any read-modify-write atomic operations that read a value taken from some modification in the release sequence. The following rules determine the atomic operation that starts an associated release sequence.

• If a release flush is performed on entry to an atomic operation, that atomic operation starts its release sequence.

• If a release flush is performed in an implicit flush region, an atomic operation that is provided by the implementation and that modifies an internal synchronization variable starts its release sequence.

• If a release flush is performed by an explicit flush region, any atomic operation that modifies a shared variable and follows the flush region in the program order of its thread starts an associated release sequence.

An acquire flush is associated with one or more prior atomic operations that read a shared variable and that may be used to establish a synchronization. The following rules determine the associated atomic operation that may establish a synchronization.

• If an acquire flush is performed on exit from an atomic operation, that atomic operation is its associated atomic operation.

• If an acquire flush is performed in an implicit flush region, an atomic operation that is provided by the implementation and that reads an internal synchronization variable is its associated atomic operation.

• If an acquire flush is performed by an explicit flush region, any atomic operation that reads a shared variable and precedes the flush region in the program order of its thread is an associated atomic operation.

The atomic scope of the internal synchronization variable that is used in implicit flush regions is the intersection of the thread-sets of the synchronizing flushes.

A release flush synchronizes with an acquire flush if the following conditions are satisfied:

• An atomic operation associated with the acquire flush reads a value written by a modification from a release sequence associated with the release flush; and

• The thread that performs each flush is in both of their respective thread-sets.

An operation X simply happens before an operation Y, that is, X precedes Y in simply happens-before order, if any of the following conditions are satisfied:

1. X and Y are performed by the same thread, and X precedes Y in the program order of the thread;

2. X synchronizes with Y according to the flush synchronization conditions explained above or according to the definition of the synchronizes with relation in the base language, if such a definition exists; or

3. Another operation, Z, exists such that X simply happens before Z and Z simply happens before Y.

An operation X happens before an operation Y if any of the following conditions are satisfied:

1. X happens before Y, as defined in the base language if such a definition exists; or

2. X simply happens before Y.

A variable with an initial value is treated as if the value is stored to the variable by an operation that happens before all operations that access or modify the variable in the program.

## 1.3.6 OpenMP Memory Consistency

The following rules guarantee an observable completion order for a given pair of memory operations in race-free programs, as seen by all afected threads. If both memory operations are strong flushes, the afected threads are all threads in both of their respective thread-sets. If exactly one of the memory operations is a strong flush, the afected threads are all threads in its thread-set. Otherwise, the afected threads are all threads.

• If two operations performed by diferent threads are sequentially consistent atomic operations or they are strong flushes that flush the same variable, then they must be completed as if in some sequential order, seen by all afected threads.

• If two operations performed by the same thread are sequentially consistent atomic operations or they access, modify, or, with a strong flush, flush the same variable, then they must be completed as if in the program order of that thread, as seen by all afected threads.

• If two operations are performed by diferent threads and one happens before the other, then they must be completed as if in that happens-before order, as seen by all afected threads, if:

– both operations access or modify the same variable;

– both operations are strong flushes that flush the same variable; or

– both operations are sequentially consistent atomic operations.

• Any two atomic operations from diferent atomic regions must be completed as if in the same order as the strong flushes implied in their regions, as seen by all afected threads

The flush operation can be specified using the flush directive, and is also implied at various locations in an OpenMP program; see Section 17.8.6 for details.

Note – Since flushes by themselves cannot prevent data races, explicit flushes are only useful in combination with non-sequentially consistent atomic constructs.

OpenMP programs that:

• Do not use non-sequentially consistent atomic constructs;

• Do not rely on the accuracy of a false result from omp\_test\_lock and omp\_test\_nest\_lock; and

• Correctly avoid data races as required in Section 1.3.1,

behave as though operations on shared variables were simply interleaved in an order consistent with the order in which they are performed by each thread. The relaxed consistency model is invisible for such programs, and any explicit flushes in such programs are redundant.

## 1.4 Tool Interfaces

The OpenMP API includes two tool interfaces, OMPT and OMPD, to enable development of high-quality, portable, tools that support monitoring, performance, or correctness analysis and debugging of OpenMP programs developed using any implementation of the OpenMP API. An implementation of the OpenMP API may difer from the abstract execution model described by its specification. The ability of tools that use OMPT or OMPD to observe such diferences does not constrain implementations of the OpenMP API in any way.

## 1.4.1 OMPT

The OMPT interface, which is intended for first-party tools, provides the following:

• A mechanism to initialize a first-party tool;

• Routines that enable a tool to determine the capabilities of an OpenMP implementation;

• Routines that enable a tool to examine OpenMP state information associated with a thread;

• Mechanisms that enable a tool to map implementation-level calling contexts back to their source-level representations;

• A callback interface that enables a tool to receive notification of OpenMP events;

• A tracing interface that enables a tool to trace activity on target devices; and

• A runtime library routine that an OpenMP program can use to control a tool.

OpenMP implementations may difer with respect to the thread states that they support, the mutual exclusion implementations that they employ, and the events for which tool callbacks are invoked. For some events, OpenMP implementations must guarantee that a registered callback will be invoked for each occurrence of the event. For other events, OpenMP implementations are permitted to invoke a registered callback for some or no occurrences of the event; for such events, however, OpenMP implementations are encouraged to invoke tool callbacks on as many occurrences of the event as is practical. Section 32.2.4 specifies the subset of OMPT callbacks that an OpenMP implementation must support for a minimal implementation of the OMPT interface.

With the exception of the omp\_control\_tool routine for tool control, all other routines in the OMPT interface are intended for use only by tools. For that reason, OMPT includes a Fortran binding only for omp\_control\_tool; all other OMPT functionality is supported with C syntax only.

## 1.4.2 OMPD

The OMPD interface is intended for third-party tools, which run as separate processes. An OpenMP implementation must provide an OMPD library that can be dynamically loaded and used by a third-party tool. A third-party tool, such as a debugger, uses the OMPD library to access OpenMP state of a program that has begun execution. OMPD defines the following:

• An interface that an OMPD library exports, which a tool can use to access OpenMP state of a program that has begun execution;

• A callback interface that a tool provides to the OMPD library so that the library can use it to access the OpenMP state of a program that has begun execution; and

• A small number of symbols that must be defined by an OpenMP implementation to help the tool find the correct OMPD library to use for that OpenMP implementation and to facilitate notification of events.

Chapter 38, Chapter 39, Chapter 40, Chapter 41, and Chapter 42 describe OMPD in detail.

## 1.5 OpenMP Compliance

The OpenMP API defines constructs that operate in the context of the base language that is supported by an implementation. If the implementation of the base language does not support a language construct that appears in this document, a compliant implementation is not required to support it, with the exception that for Fortran, the implementation must allow case insensitivity for directive and routine names, and it must allow identifiers of more than six characters. An implementation of the OpenMP API is compliant if and only if it compiles and executes all other conforming programs, and supports the tool interfaces, according to the syntax and semantics laid out in Chapters 1 through 42. All appendices as well as text designated as a note or comment (see Section 1.7) are for information purposes only and are not part of the specification.

All library, intrinsic and built-in procedures provided by the base language must be thread-safe procedures in a compliant implementation. In addition, the implementation of the base language must also be thread-safe. For example, ALLOCATE and DEALLOCATE statements must be thread-safe in Fortran. Unsynchronized concurrent use of such procedures by diferent threads must produce correct results (although not necessarily the same as serial execution results, as in the case of random number generation procedures).

Starting with Fortran 90, variables with explicit initialization have the SAVE attribute implicitly. This is not the case in Fortran 77. However, a compliant OpenMP Fortran implementation must give such a variable the SAVE attribute, regardless of the underlying base language version.

Appendix A lists certain aspects of the OpenMP API that are implementation defined. A compliant implementation must define and document its behavior for each of the items in Appendix A.

## 1.6 Normative References

• ISO/IEC 9899:1990, Information Technology - Programming Languages - C. This OpenMP API specification refers to ISO/IEC 9899:1990 as C90.

• ISO/IEC 9899:1999, Information Technology - Programming Languages - C. This OpenMP API specification refers to ISO/IEC 9899:1999 as C99.

• ISO/IEC 9899:2011, Information Technology - Programming Languages - C. This OpenMP API specification refers to ISO/IEC 9899:2011 as C11.

• ISO/IEC 9899:2018, Information Technology - Programming Languages - C. This OpenMP API specification refers to ISO/IEC 9899:2018 as C18.

• ISO/IEC 9899:2024, Information Technology - Programming Languages - C. This OpenMP API specification refers to ISO/IEC 9899:2024 as C23.

• ISO/IEC 14882:1998, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:1998 as C++98.

• ISO/IEC 14882:2011, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:2011 as C++11.

• ISO/IEC 14882:2014, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:2014 as C++14.

• ISO/IEC 14882:2017, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:2017 as C++17.

• ISO/IEC 14882:2020, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:2020 as C++20.

• ISO/IEC 14882:2024, Information Technology - Programming Languages - C++. This OpenMP API specification refers to ISO/IEC 14882:2024 as C++23.

• ISO/IEC 1539:1980, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539:1980 as Fortran 77.

• ISO/IEC 1539:1991, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539:1991 as Fortran 90.

• ISO/IEC 1539-1:1997, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539-1:1997 as Fortran 95.

• ISO/IEC 1539-1:2004, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539-1:2004 as Fortran 2003.

• ISO/IEC 1539-1:2010, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539-1:2010 as Fortran 2008.

• ISO/IEC 1539-1:2018, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539-1:2018 as Fortran 2018.

• ISO/IEC 1539-1:2023, Information Technology - Programming Languages - Fortran. This OpenMP API specification refers to ISO/IEC 1539-1:2023 as Fortran 2023.

• Where this OpenMP API specification refers to C, C++ or Fortran, reference is made to the base language supported by the implementation.

## 1.7 Organization of this Document
