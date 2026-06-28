For a given construct, a data-sharing attribute of a variable that implies the private attribute, and additionally, the final value of the variable may be assigned to the variable that has the same name in the enclosing data environment of the construct. 230, 64, 211

## lastprivate variable

A private variable that has the lastprivate attribute with respect to a given construct. 909

## leaf construct

For a given construct, a construct that corresponds to one of the leaf directives of the executable directive. 20, 32, 46, 61, 82, 174, 318, 516, 528–531, 918

## leaf directive

For a given directive, the directive itself if it is not a compound directive, or a directive from which the compound directive is composed that is not itself a compound directive. 35, 64, 527

## leaf-directive name

The directive name of a leaf directive. 525, 525, 527, 919

## league

The set of teams formed by a teams construct, each of which is associated with a diferent contention group. 4, 105, 116, 253, 394, 395, 421–423, 581, 725, 758

## lexicographic order

The total order of two logical iteration vectors $\omega _ { a } = ( i _ { 1 } , \ldots , i _ { n } )$ and $\omega _ { b } = ( j _ { 1 } , \ldots , j _ { n } )$ denoted by $\omega _ { a } \leq _ { \mathrm { l e x } } \omega _ { b }$ , where either $\omega _ { a } = \omega _ { b }$ or ∃m $\in \{ 1 , \ldots , n \}$ such that $i _ { m } < j _ { m }$ and $i _ { k } = j _ { k }$ for all $k \in \{ 1 , \ldots , m - 1 \}$ . 380, 381

## linear attribute

For a given loop-nest-associated construct, a data-sharing attribute of a variable that is equivalent to an induction attribute for which the induction operation is a linear recurrence, where the binary operator ⊕ is + and the step expression s is a loop-invariant integer expression. 232, 64

## linear variable

A private variable that has the linear attribute with respect to a given construct. 232

## list

A comma-separated set. 22, 39, 40, 64, 85, 158, 162, 163, 345, 349, 387, 444, 700, 886

## list item

A member of a list. 21, 23, 33, 37, 39, 40, 46, 47, 49, 51, 61, 63, 65, 68–71, 73, 76, 80, 82, 83, 86, 87, 98, 109, 112, 141, 158–160, 162–165, 168–170, 210–212, 214, 217–222, 225–231, 233–239, 241, 243–245, 247–250, 252–254, 256–259, 267–270, 272–276, 279–291, 294–296, 300–303, 311–313, 315, 328, 332, 333, 338, 339, 345–349, 363, 364, 372–374, 378–380, 401, 421, 424, 430, 436, 437, 444, 445, 454, 456, 459, 461–464, 466, 499, 500, 507–509, 521, 522, 528–531, 534, 875, 888, 897, 899, 900, 904, 905, 910, 916

## local static variable

A variable with static storage duration that for C/C++ has block scope and for Fortran is declared in the specification part of a procedure or BLOCK construct. 305, 309

## locator list

An argument list that consists of locator list items. 162, 160, 295, 437

## locator list item

A list item that refers to storage locations in memory and is one of the items specifically identified in Section 5.2.1. 163, 65, 162–164, 181, 435, 437, 505, 506, 508, 510

## lock

An OpenMP variable that is used in lock routines to enforce mutual exclusion. 65, 66, 74, 75, 80, 97, 109, 110, 449, 496, 501, 504, 558, 561, 663–668, 670–676, 734, 742, 769, 788, 795, 893, 913

## lock-acquiring property

The property that a routine may acquire a lock by putting it into the locked state. 670, 65, 663, 670, 671

## lock-acquiring routine

A routine that has the lock-acquiring property. 670, 449, 663, 670, 675, 765–768

## lock-destroying property

The property that a routine destroys a lock by putting it into the uninitialized state. 667, 65, 668, 669

## lock-destroying routine

A routine that has the lock-destroying property. 667, 668, 669, 767

## locked state

The lock state that indicates the lock has been set by some task. 663, 65, 66, 673

## lock-initializing property

The property that a routine initializes a lock by putting it into the unlocked state. 664, 65, 664–667

## lock-initializing routine

A routine that has the lock-initializing property. 664, 664–667, 765, 766

## lock property

The property that a routine operates on locks. 663, 66

## lock-releasing property

The property that a routine may unset a lock by returning it to the unlocked state. 672, 66, 663, 673, 674

## lock-releasing routine

A routine that has the lock-releasing property. 672, 449, 663, 672, 673, 767, 768

## lock routine

A routine that has the lock property. 663, 65, 535, 663, 893

## lock state

The state of a lock that determines if it can be set. 663, 65, 109, 110, 663, 672–674

## lock-testing property

The property that a routine that may set a lock by putting it into the locked state does not suspend execution of the task that executes the routine if it cannot set the lock. 675, 66, 675, 676

## lock-testing routine

A routine that has the lock-testing property. 675, 675, 766–768

## logical iteration

An instance of the executed loop body of a canonical loop nest, or a DO CONCURRENT loop in Fortran, denoted by a number in the logical iteration space of the loops that indicates an order in which the logical iteration would be executed relative to the other logical iterations in a sequential execution. 4, 20, 32, 33, 47, 50, 59, 61, 66, 67, 92, 94, 99, 107, 111, 204, 205, 253, 370, 371, 375, 377–382, 401, 429–433, 534, 719, 754, 889, 890, 905, 907, 910, 912, 916

## logical iteration space

For a canonical loop nest, or a DO CONCURRENT loop in Fortran, the sequence $0 , \ldots , N - 1$ where N is the number of distinct logical iterations. 204, 32, 47, 55, 59, 66, 107, 204, 374, 377–380, 534

## logical iteration vector

An n-tuple $( i _ { 1 } , \ldots , i _ { n } )$ that identifies a logical iteration of a canonical loop nest, where n is the loop nest depth and $i _ { k }$ is the logical iteration number of the $k ^ { \mathrm { t h } }$ loop, from outermost to innermost. 64, 66, 88, 205, 380, 381, 905

## logical iteration vector space

The set of logical iteration vectors that each correspond to a logical iteration of a canonical loop nest. 205, 379, 381

## loop body

A structured block that encompasses the executable statements that are iteratively executed by a loop statement. 197, 62, 63, 66, 378, 434

## loop-collapsing construct

A loop-nest-associated construct for which some number of outer loops of the associated loop nest may be collapsed loops. 31, 32, 205, 219, 220, 233, 398

## loop-iteration variable

For a loop of a canonical loop nest, var as defined in Section 6.4.1. A C++ range-based for-statement has no loop-iteration variable. 67, 171, 196, 200–205, 211–213, 230, 233, 371, 424, 434, 512, 513, 529, 531, 916

## loop-iteration vector

An n-tuple $( i _ { 1 } , \ldots , i _ { n } )$ that identifies a logical iteration of the afected loops of a loop-nest-associated directive, where n is the number of afected loops and $i _ { k }$ is the value of the loop-iteration variable of the $k ^ { \mathrm { t h } }$ afected loop, from outermost to innermost. 67, 203, 204, 512, 513

## loop-iteration vector space

The set of loop-iteration vectors that each corresponds to a logical iteration of the afected loops of a loop-nest-associated directive. 204, 203, 204

## loop-nest-associated construct

A loop-nest-associated directive and its associated loop nest. 60, 62, 64, 67, 92, 94, 97, 113, 154, 205, 234, 259, 372, 373, 380, 381, 404, 512, 531

## loop-nest-associated directive

An executable directive for which the associated user code must be a canonical loop nest. 153, 20, 23, 67, 152, 153, 198, 203, 211, 212, 233, 258, 371, 372, 375, 377, 379–381, 399, 416, 417, 420, 423, 429, 516

## loop nest depth

For a canonical loop nest, the maximal number of loops, including the outermost loop, that can be afected by a loop-nest-associated directive. 66, 203, 206, 374

## loop schedule

The manner in which the collapsed iterations of afected loops are to be distributed among a set of threads that cooperatively execute the afected loops. 205, 35, 92, 94, 205, 398, 404, 414, 420, 423, 905

## loop-sequence-associated construct

A loop-sequence-associated directive and its associated canonical loop sequence. 68, 207

## loop-sequence-associated directive

An executable directive for which the associated user code must be a canonical loop sequence. 153, 23, 67, 152, 371, 374

## loop sequence length

For a canonical loop sequence, the number of consecutive canonical loop nests regardless of their nesting into blocks. 203, 208

## loop-sequence-transforming construct

A loop-sequence-associated construct with the loop-transforming property. 371

## loop-transforming construct

A loop-transforming directive and its associated loop nest or associated canonical loop sequence. 371, 54, 76, 108, 197, 203, 205, 370–374, 378, 431, 900, 901, 904, 907

## loop-transforming directive

A directive with the loop-transforming property. 54, 68, 108, 371, 373, 374, 379

## loop-transforming property

The property that a construct is replaced by the loops that result from applying the transformation as defined by its directive to its afected loops. 68, 369, 374, 375, 377, 379–381

## loosely structured block

For Fortran, a block of zero or more executable constructs (including OpenMP constructs), where the first executable construct (if any) is not a Fortran BLOCK construct, with a single entry at the top and a single exit at the bottom. 99, 153

## M

## map-entering clause

A map clause that, if it appears on a map-entering construct, specifies that the reference counts of corresponding list items are increased and, as a result, those list items may enter the device data environment. 275, 68, 283, 285, 361, 455

## map-entering construct

A construct that has the map-entering property. 68, 274, 281, 283, 284, 287, 527, 564

## map-entering map type

A map-type that specifies the clause on which it is specified is a map-entering clause. 275, 275

## map-entering property

A property of a construct that it may include mapping operations that allocate storage on the target device and that result in assignment to the corresponding list item from the original list item. 68, 275, 454, 458, 460

## map-exiting clause

A map clause that, if it appears on a map-exiting construct, specifies that the reference counts of corresponding list items are decreased and, as a result, those list items may exit the device data environment. 275, 69, 457

## map-exiting construct

A construct that has the map-exiting property. 69, 274, 284, 527

## map-exiting map type

A map-type that specifies the clause on which it is specified is a map-exiting clause. 275, 275

## map-exiting property

A property of a construct that it may include mapping operations that release storage on the target device and that result in assignment from the corresponding list item to the original list item. 69, 275, 456, 458, 460

## mappable storage block

A storage block, derived from the list items of map clauses specified on a data-mapping construct, for which a corresponding storage block in a device data environment is created, removed, or otherwise referenced by the construct. 283, 284, 287, 296

## mappable type

A type that is valid for a mapped variable. If a type is composed from other types (such as the type of an array element or a structure element) and any of the other types are not mappable types then the type is not a mappable type.

For C, the type must be a complete type.

For C++, the type must be a complete type; in addition, for class types:

• All member functions accessed in any target region must appear in a declare target directive.

For Fortran, no restrictions on the type except that for derived types:

• All type-bound procedures accessed in any target region must appear in a declare\_target directive.

COMMENT: Pointer types are mappable types but the memory block to which the pointer refers is not mapped.

69, 287, 290, 291, 296

## mapped address range

For a given original list item, the address range that starts from its starting address and ends with its ending address. 280, 71, 281

## mapped variable

An original variable in a data environment with a corresponding variable in a device data environment. The original and corresponding variables may share storage. 38, 49, 69, 70, 82, 98, 464, 564

## mapper

An operation that defines how variables of given type are to be mapped or updated with respect to a device data environment. 41, 48, 111, 183, 274–276, 278, 281–283, 287, 293–296, 298, 299

## mapper identifier

An OpenMP identifier that specifies the name of a user-defined mapper. 278, 278, 295

## mapping operation

An operation that establishes or removes a correspondence between a variable in one data environment and another variable in a device data environment. 9, 23, 25, 69, 70, 95, 275, 283, 284, 286, 361, 564, 734, 739, 899, 900

## map type

A categorization of a data-mapping clause that determines whether the mapping operations that result from that clause include assignments between the original storage and corresponding storage of its list items. 61, 82, 109, 283, 284

## map-type decay

A process applied to input map type, according to an underlying map type, that results in an output map type. 275, 61, 82, 275, 281, 459

## map-type-modifying property

The property that a modifier that combines with a map-type to determine details of a mapping operation. 280, 282

## matchable candidate

A mapped variable for which corresponding storage was created in a device data environment. 280, 71, 281

## matched candidate

A matchable candidate that, due to a matching mapped address range or extended address range, may determine the lower bound and length to use for a given assumed-size array that is a list item in a map clause. 281, 236, 281, 287, 904

## matching taskgraph record

A finalized taskgraph record that has a matching value for the scalar expression that identifies a taskgraph region. 436, 92, 435–439

## memory
