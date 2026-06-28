
Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>saved</td><td>list</td><td>Keyword: saved</td><td>default</td></tr></table>

## Clauses

firstprivate

## Semantics

If the saved modifier is present in a data-environment attribute clause that is specified on a replayable construct then its original list items of a replay execution are defined by the saved data environment of the replayable construct. The saved modifier has no efect if specified in a clause that does not appear on a replayable construct.

## Cross References

• firstprivate Clause, see Section 7.5.4

• taskgraph Construct, see Section 14.3

## 7.3 threadprivate Directive

<table><tr><td>Name: threadprivateCategory: declarative</td><td>Association: explicitProperties: pure</td></tr></table>

## Arguments

threadprivate(list)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Semantics

The threadprivate directive specifies that variables have the threadprivate attribute and therefore they are replicated with each thread having its own copy. Unless otherwise specified, each copy of a threadprivate variable is initialized once, in the manner specified by the program, but at an unspecified point in the program prior to the first reference to that copy. The storage of all copies of a threadprivate variable is freed according to how variables with static storage duration are handled in the base language, but at an unspecified point in the program.

C++

Each copy of a block-scope threadprivate variable that has a dynamic initializer is initialized the first time its thread encounters its definition; if its thread does not encounter its definition, whether it is initialized is unspecified. If it is initialized, its initialization occurs at an unspecified point in the program.

The content of a threadprivate variable can change across a task scheduling point if the executing thread switches to another task that modifies the variable. For more details on task scheduling, see Section 1.2 and Chapter 14.

In parallel regions, references by the primary thread are to the copy of the variable of the thread that encountered the parallel region.

During a sequential part, references are to the copy of the variable of the initial thread. The values of data in the copy for the initial thread are guaranteed to persist between any two consecutive references to the threadprivate variable in the program, provided that no teams construct that is not nested inside of a target construct is encountered between the references and that the initial thread is not executing code inside of a teams region. For initial threads that are executing code inside of a teams region, the values of data in the copies of a threadprivate variable for those initial threads are guaranteed to persist between any two consecutive references to the variable inside that teams region.

The values of data in the threadprivate variables of threads that are not initial threads are guaranteed to persist between two consecutive active parallel regions only if all of the following conditions hold:

• Neither parallel region is nested inside another explicit parallel region;

• The sizes of the teams used to execute both parallel regions are the same;

• The thread afinity policies used to execute both parallel regions are the same;

• The value of the dyn-var ICV in the enclosing task region is false at entry to both parallel regions;

• No teams construct that is not nested inside of a target construct is encountered between the parallel regions;

• No construct with an order clause that specifies concurrent is encountered between the parallel regions; and

• Neither the omp\_pause\_resource nor omp\_pause\_resource\_all routine is called.

If these conditions all hold, and if a threadprivate variable is referenced in both regions, then threads with the same thread number in their respective regions reference the same copy of that variable.

![](images/1ce4686592f533de1a9666912686ec04dddf994e932d1fe0f8af9a4f9c0ef944.jpg)

If the above conditions hold, the storage duration, lifetime, and value of a copy of a threadprivate variable that does not appear in any copyin clause on the corresponding construct of the second region spans the two consecutive active parallel regions. Otherwise, the storage duration, lifetime, and value of the copy of the variable in the second region is unspecified.

C / C++

## Fortran

If the above conditions hold, the definition, association, or allocation status of a copy of a threadprivate variable or a variable in a threadprivate common block that is not afected by any copyin clause that appears on the corresponding construct of the second region (a variable is afected by a copyin clause if the variable appears in the copyin clause or it is in a common block that appears in the copyin clause) spans the two consecutive active parallel regions. Otherwise, the definition and association status of a copy of the variable in the second region are undefined, and the allocation status of an allocatable variable are implementation defined.

If a threadprivate variable or a variable in a threadprivate common block is not afected by any copyin clause that appears on the corresponding construct of the first parallel region in which it is referenced, the copy of the variable inherits the declared type parameter and the default parameter values from the original variable. The variable or any subobject of the variable is initially defined or undefined according to the following rules:

• If it has the ALLOCATABLE attribute, each copy created has an initial allocation status of unallocated;

• If it has the POINTER attribute, each copy has the same association status as the initial association status; and

• If it does not have either the POINTER or the ALLOCATABLE attribute:

– If it is initially defined, either through explicit initialization or default initialization, each copy created is so defined;

– Otherwise, each copy created is undefined.

Fortran

The order in which any constructors for diferent threadprivate variables of class type are called is unspecified. The order in which any destructors for diferent threadprivate variables of class type are called is unspecified. A variable that is part of an aggregate variable may appear in a threadprivate directive only if it is a static data member of a C++ class.

C++

## Restrictions

Restrictions to the threadprivate directive are as follows:

• A thread must not reference a copy of a threadprivate variable that belongs to another thread.

• A threadprivate variable must not appear as the base variable of a list item in any clause except for the copyin and copyprivate clauses.

• An OpenMP program in which an untied task accesses threadprivate memory is non-conforming.

• Each list item must be a file-scope, namespace-scope, or static block-scope variable.

• No list item may have an incomplete type.

• The address of a threadprivate variable must not be an address constant.

• If the value of a variable referenced in an explicit initializer of a threadprivate variable is modified prior to the first reference to any instance of the threadprivate variable, the behavior is unspecified.

• A threadprivate directive for file-scope variables must appear outside any definition or declaration, and must lexically precede all references to any of the variables in its argument list.

• A threadprivate directive for namespace-scope variables must appear outside any definition or declaration other than the namespace definition itself and must lexically precede all references to any of the variables in its argument list.

• Each variable in the argument list of a threadprivate directive at file, namespace, or class scope must refer to a variable declaration at file, namespace, or class scope that lexically precedes the directive.

• A threadprivate directive for a static block-scope variable must appear in the scope of the variable and not in a nested scope. The directive must lexically precede all references to any of the variables in its argument list.

• Each variable in the argument list of a threadprivate directive in block scope must refer to a variable declaration in the same scope that lexically precedes the directive. The variable must have static storage duration.

• If a variable is specified in a threadprivate directive in one compilation unit, it must be specified in a threadprivate directive in every compilation unit in which it is declared.

C / C++

C++

• A threadprivate directive for static class member variables must appear in the class definition, in the same scope in which the member variables are declared, and must lexically precede all references to any of the variables in its argument list.

• A threadprivate variable must not have an incomplete type or a reference type.

• A threadprivate variable with class type must have:

– An accessible, unambiguous default constructor in the case of default initialization without a given initializer;

– An accessible, unambiguous constructor that accepts the given argument in the case of direct initialization; and

– An accessible, unambiguous copy constructor in the case of copy initialization with an explicit initializer.

• Each list item must be a named variable or a named common block; a named common block must appear between slashes.

• The list argument must not include any coarrays or associate names.

• The threadprivate directive must appear in the declaration section of a scoping unit in which the common block or variable is declared.

• If a threadprivate directive that specifies a common block name appears in one compilation unit, then such a directive must also appear in every other compilation unit that contains a COMMON statement that specifies the same name. It must appear after the last such COMMON statement in the compilation unit.

• If a threadprivate variable or a threadprivate common block is declared with the BIND attribute, the corresponding C entities must also be specified in a threadprivate directive in the C program.

• A variable may only appear as an argument in a threadprivate directive in the scope in which it is declared. It must not be an element of a common block or appear in an EQUIVALENCE statement.

• A variable that appears as an argument in a threadprivate directive must be declared in the scope of a module or have the SAVE attribute, either explicitly or implicitly.

• The efect of an access to a threadprivate variable in a DO CONCURRENT construct is unspecified.

## Cross References

• copyin Clause, see Section 7.8.1

• dyn-var ICV, see Table 3.1

• order Clause, see Section 12.3

• Determining the Number of Threads for a parallel Region, see Section 12.1.1
