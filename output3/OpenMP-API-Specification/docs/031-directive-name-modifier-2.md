
Fortran

## 5.4 directive-name-modifier Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Clauses

absent, acq\_rel, acquire, adjust\_args, affinity, align, aligned, allocate, allocator, append\_args, apply, at, atomic\_default\_mem\_order, bind, capture, collapse, collector, combiner, compare, contains, copyin, copyprivate, default, defaultmap, depend, destroy, detach, device, device\_safesync, device\_type, dist\_schedule, doacross, dynamic\_allocators, enter, exclusive, fail, filter, final, firstprivate, from, full, grainsize, graph\_id, graph\_reset, has\_device\_addr, hint, holds, if, in\_reduction, inbranch, inclusive, indirect, induction, inductor, init, init\_complete, initializer, interop, is\_device\_ptr, lastprivate, linear, link, local, map, match, memscope, mergeable, message, no\_openmp, no\_openmp\_constructs, no\_openmp\_routines, no\_parallelism, nocontext, nogroup, nontemporal, notinbranch, novariants, nowait, num\_tasks, num\_teams, num\_threads, order, ordered, otherwise, partial, permutation, priority, private, proc\_bind, read, reduction, relaxed, release, replayable, reverse\_offload, safelen, safesync, schedule, self\_maps, seq\_cst, severity, shared, simd, simdlen, sizes, task\_reduction, thread\_limit, threads, threadset, to, transparent, unified\_address, unified\_shared\_memory, uniform, untied, update, update, use, use\_device\_addr, use\_device\_ptr, uses\_allocators, weak, when, write

## Semantics

The directive-name-modifier is a universal modifier that can be used on any clause. The directive-name-modifier specifies directive-name, which is the directive name of a directive, construct or constituent construct to which the clause applies. If the directive name is that of a compound construct, then the leaf constructs to which the clause applies are determined as specified in Section 19.2. If no directive-name-modifier is specified then the efect is as if a directive-name-modifier was specified with the directive name of the directive on which the clause appears.

## Restrictions

Restrictions to the directive-name-modifier are as follows:

• The directive-name-modifier must specify the directive name of either the directive on which the clause appears or a constituent directive of that directive.

## Cross References

• absent Clause, see Section 10.6.1.1

• acq\_rel Clause, see Section 17.8.1.1

• acquire Clause, see Section 17.8.1.2

• adjust\_args Clause, see Section 9.6.2

• affinity Clause, see Section 14.10

• align Clause, see Section 8.3
• aligned Clause, see Section 7.12
• allocate Clause, see Section 8.6
• allocator Clause, see Section 8.4
• append\_args Clause, see Section 9.6.3
• apply Clause, see Section 11.1
• at Clause, see Section 10.2
• atomic\_default\_mem\_order Clause, see Section 10.5.1.1
• bind Clause, see Section 13.8.1
• capture Clause, see Section 17.8.3.1
• full Clause, see Section 11.9.1
• partial Clause, see Section 11.9.2
• collapse Clause, see Section 6.4.5
• collector Clause, see Section 7.6.19
• combiner Clause, see Section 7.6.15
• compare Clause, see Section 17.8.3.2
• contains Clause, see Section 10.6.1.2
• copyin Clause, see Section 7.8.1
• copyprivate Clause, see Section 7.8.2
• default Clause, see Section 7.5.1
• defaultmap Clause, see Section 7.9.9
• depend Clause, see Section 17.9.5
• destroy Clause, see Section 5.7
• detach Clause, see Section 14.11
• device Clause, see Section 15.2
• device\_safesync Clause, see Section 10.5.1.7
• device\_type Clause, see Section 15.1
• dist\_schedule Clause, see Section 13.7.1
• doacross Clause, see Section 17.9.7

• dynamic\_allocators Clause, see Section 10.5.1.2

• enter Clause, see Section 7.9.7

• exclusive Clause, see Section 7.7.2

• fail Clause, see Section 17.8.3.3

• filter Clause, see Section 12.5.1

• final Clause, see Section 14.7

• firstprivate Clause, see Section 7.5.4

• from Clause, see Section 7.10.2

• grainsize Clause, see Section 14.2.1

• graph\_id Clause, see Section 14.3.1

• graph\_reset Clause, see Section 14.3.2

• has\_device\_addr Clause, see Section 7.5.9

• hint Clause, see Section 17.1

• holds Clause, see Section 10.6.1.3

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• inbranch Clause, see Section 9.8.1.1

• inclusive Clause, see Section 7.7.1

• indirect Clause, see Section 9.9.3

• induction Clause, see Section 7.6.13

• inductor Clause, see Section 7.6.18

• init Clause, see Section 5.6

• init\_complete Clause, see Section 7.7.3

• initializer Clause, see Section 7.6.16

• interop Clause, see Section 9.7.1

• is\_device\_ptr Clause, see Section 7.5.7

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• link Clause, see Section 7.9.8

local Clause, see Section 7.14
map Clause, see Section 7.9.6
match Clause, see Section 9.6.1
memscope Clause, see Section 17.8.4
mergeable Clause, see Section 14.5
message Clause, see Section 10.3
no\_openmp Clause, see Section 10.6.1.4
no\_openmp\_constructs Clause, see Section 10.6.1.5
no\_openmp\_routines Clause, see Section 10.6.1.6
no\_parallelism Clause, see Section 10.6.1.7
nocontext Clause, see Section 9.7.3
nogroup Clause, see Section 17.7
nontemporal Clause, see Section 12.4.1
notinbranch Clause, see Section 9.8.1.2
novariants Clause, see Section 9.7.2
nowait Clause, see Section 17.6
num\_tasks Clause, see Section 14.2.2
num\_teams Clause, see Section 12.2.1
num\_threads Clause, see Section 12.1.2
order Clause, see Section 12.3
ordered Clause, see Section 6.4.6
otherwise Clause, see Section 9.4.2
permutation Clause, see Section 11.4.1
priority Clause, see Section 14.9
private Clause, see Section 7.5.3
proc\_bind Clause, see Section 12.1.4
read Clause, see Section 17.8.2.1
reduction Clause, see Section 7.6.10
relaxed Clause, see Section 17.8.1.3

• release Clause, see Section 17.8.1.4

• replayable Clause, see Section 14.6

• reverse\_offload Clause, see Section 10.5.1.3

• safelen Clause, see Section 12.4.2

• safesync Clause, see Section 12.1.5

• schedule Clause, see Section 13.6.3

• self\_maps Clause, see Section 10.5.1.6

• seq\_cst Clause, see Section 17.8.1.5

• severity Clause, see Section 10.4

• shared Clause, see Section 7.5.2

• simd Clause, see Section 17.10.3.2

• simdlen Clause, see Section 12.4.3

• sizes Clause, see Section 11.2

• task\_reduction Clause, see Section 7.6.11

• thread\_limit Clause, see Section 15.3

• threads Clause, see Section 17.10.3.1

• threadset Clause, see Section 14.8

• to Clause, see Section 7.10.1

• transparent Clause, see Section 17.9.6

• unified\_address Clause, see Section 10.5.1.4

• unified\_shared\_memory Clause, see Section 10.5.1.5

• uniform Clause, see Section 7.11

• untied Clause, see Section 14.4

• update Clause, see Section 17.8.2.2

• update Clause, see Section 17.9.4

• use Clause, see Section 16.1.2

• use\_device\_addr Clause, see Section 7.5.10

• use\_device\_ptr Clause, see Section 7.5.8

• uses\_allocators Clause, see Section 8.8

• weak Clause, see Section 17.8.3.4

• when Clause, see Section 9.4.1

• write Clause, see Section 17.8.2.3
