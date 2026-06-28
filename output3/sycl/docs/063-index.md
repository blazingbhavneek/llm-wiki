## Index

A Accelerated vs. Heterogeneous systems, 1 Accelerator devices GPU (see Graphics processing unit (GPU)) Ahead-of-time (AOT) compilation, 316 all\_of\_group, 242 Amdahl, Gene, 10 Amdahl’s Law, 10 Anonymous lambdas, 346–347 any\_of\_group, 242 Application programming interface (API), 264 See also Backend interoperability Array-of-Struct (AOS) structures, 442–444 Aspects, 52 See also Device aspects Asynchronous error, 139 host program execution, 35 queues (out-of-order), 21 Atomic operations

atomic\_fence, 542 atomic\_fence\_order\_ capabilities, 541 atomic\_fence\_scope\_ capabilities, 541 atomic\_memory\_order\_ capabilities, 540 atomic\_memory\_scope\_ capabilities, 541 atomic\_ref class, 543 cl::sycl::atomic class (deprecated in SYCL 2020), 543 cl::sycl::atomic (deprecated in SYCL 2020), 543 data races, 524 device-wide synchronization, 553–556 std::atomic class, 543 std::atomic\_ref class, 544–548 unified shared memory, 550

## B

Backend interoperability, 559 backends, 560 get\_native functions, 564–566 interop\_handle, 566

INDEX

Backend interoperability (cont.) kernels, 569–574 key benefits, 562 low-level API features, 576 Barrier synchronization, 530 Buffers, 67, 72, 78 accessor, 78–80, 180 access targets, 190 deduction tags, 195, 197 get\_access method, 192 modes, 190 name—access data, 198 placeholder accessor, 191, 197 coding preferences, 181 command group (CG), 207 myDoubles array, 183 properties, 186 context\_bound, 188 use\_host\_ptr, 187 use\_mutex, 187 set\_final\_data method, 189 set\_write\_back method, 189 USM (see Unified shared memory (USM))

## C

Cache-coherent non-uniform memory access (cc-NUMA), 419 Central processing units (CPUs) architecture, 420 cc-NUMA system, 419–421

hardware threads, 421 multicore, 419–421 multicore processors, 417 parallelism, 417 performance, 418–419 SIMD instruction hardware, 422–428 vectorization, 436–448 sockets, 421 thread-level parallelism, 428–436 Class template argument deduction (CTAD), 181 Clock frequency, 500–501 cl::sycl::atomic (deprecated in SYCL 2020), 543 Code execution, see Host devices Collective functions, communication broadcast function, 241 exclusive/inclusive scans, 244 features, 241 permute\_group\_by\_xor, 245 shift\_group\_left, 244 shuffle functions, 243–246 sub-groups, 245 vote functions, 242 XOR operation, 244 Command group (CG) actions, 203 description, 202, 203 event-based dependences, 203 execution, 213

linear dependence chains buffers/accessors, 207, 208 events, 207 in-order queues, 205, 206 task execution, 204 “Y” pattern accessors, 212 events, 210 in-order queues, 208, 209 out-of-order queues, 209, 210 Communication barrier function synchronization, 223–225 collective function, 225, 241–246 matrix multiplication kernel implicit/explicit cache, 229 sub-groups broadcast function, 237 collective functions, 237–239 definition, 235 ND-range parallel\_ for, 240–241 synchronization, 236 work-group local memory compiler optimizations, 226 info::device::local\_mem\_ type, 227 matrix multiplication kernel, 227–231 memory subsystems, 226 ND-range kernels, 231–235 Compile-time properties, 612–613

Concurrent vs. parallelism, 28–29 Contexts, 157, 319, 320, 576 copy method, 214 C++ programming, 5 asynchronous, 20 concurrency vs. parallelism, 22, 28–29 data-parallel programming, 6 deadlocks, 22 key attributes, 14 migrate CUDA code, 581 platform model, 321–322 poor algorithm design, 22 portability/performance portability, 26–28 std::memcpy, 19–22 C++ standard library CPU/GPU/FPGA coverage, 508, 509 cross-architecture portability, 510 DPC++ compiler, 509 memory model, 535 std::swap, 507, 508 SYCL devices, 507 CUDA migration (see Migrate CUDA code) Curious descriptors, 303 detailed enumeration code, 301–302 get\_info<>, 300–301 has() interface, 303

INDEX

Custom memory systems memory access, 495, 497 optimization, 496 stages, 495, 496 static coalescing, 497 structure, 497

## D

Data management explicit, 70 implicit, 71 local accesses, 69 parallelism/feeding data, 67 Data movement accessor, 215 application performance, 213 command groups, 215 explicit, 167–169, 213 graph (see Graph scheduling) host and shared allocations, 215 implicit, 214 data migration, 169 data movement, 170 fine-grained control, 172–174 host allocations, 169 memcpy, 169 migration, 170–171 prefetch/mem\_advise, 173 shared allocations, 169 memcpy method, 167, 214 prefetch operation, 215 update\_host method, 214

Data parallelism architectures, 98 data-parallel kernels C++ classes, 109 descriptive programming, 105 execution space, 105–106 id class, 110–111 item class, 111–112 matrix multiplication, 108, 109 operations, 105 parallel\_for function, 107–109 range class, 109–110 simplified definition, 110 SPMD programming model, 105 device-specific optimizations, 98 hardware resources, 98 hierarchical data, 104 host/device code, 102–103 kernel-based programming, 101 kernel forms, 103–105 features, 132 flowchart, 130, 131 functionality, 130 language features, 102 loops vs. kernels, 99–101 multidimensional kernels, 101–102 ND-range, 104

performance/portability/ productivity, 99 programmer productivity, 98 sequential semantics, 99 two-dimensional range, 102 work-items data and execution ranges, 129 many-to-one mapping, 128–129 mapping computation, 128 one-to-one mapping, 128 Data-parallel programming, 13 Deadlock, 21 Debugging process compiler options, 324 deadlocking, 324 host/device, 323 queue profiling, 330–334 runtime error, 327–330 sycl::stream, 326 tracing and profiling tools, 334–335 Debugging technique, 21 Device aspects, 51, 296, 297 Device code, 34 Device-constant expression, 611 Device information all\_devices\_have\_ v<aspect>, 308 any\_device\_has\_v<aspect>, 308 compile-time properties vs. runtime, 308 correctness

device queries, 305–306 fetching parameters, 304 parameters, 304 custom device selectors, 298 descriptors, 303 enumeration method aspects, 296–297 curious, 300–302 custom device selector, 298–299 device class, 300 device query mechanisms, 300 device selectors, 294 get\_info<>, 300–301 implementation, 293 get\_info plus has(), 303 kernel specialization, 296 output program, 301 preferred solution, 299 robust application, 296 try-catch, 294, 295 kernels information descriptors, 303 kernel specialization, 309–311 properties, 291 specialization constants, 308 SYCL specification, 290 templated kernels, 308 tuning/optimization kernel queries, 308 Device selection, 36, 289, 291, 293, 298

## INDEX

Device-wide synchronization, 553 atomic references, 555 implementation, 553 ND-range, 554 Dining Philosophers problem, 21 Double-precision A times X Plus Y (DAXPY), 17–18 Download code samples, 313 Download SYCL compiler, 313 DPC++ compiler, 313, 503 See also oneAPI DPC++ Library (oneDPL) DPC++ Compatibility Tool (dpct) compiling and running program, 601–603 CUDA program, 599 helper functions, 602–603 migration code, 598–602 output process, 601–602 DPC++ Library (oneDPL), 606

## E

Error handling application strategies, 140–149 asynchronous definition, 138 detection/reporting, 141 devices, 149, 150 heterogeneous programming, 136 host program/task graph executions, 137 key capabilities, 135

safety, 135–136 std::function, 145 std::terminate, 142 synchronous definition, 137 types, 136–138 Execution policy, 606

## F

Fat binary, 315 Fencing memory model, 223 Field Programmable Gate Arrays (FPGAs) building blocks elements, 498 look-up tables, 498 math engines, 498 off-chip hardware, 499 on-chip memory, 499 routing fabric, 499, 500 custom memory systems, 495–497 data flow architectures, 462 definition, 451 kernels consume chip, 459–460 loop initiation interval incremental random number, 485, 486 iteration processes, 486, 487 iterations, 485 stages, 487, 488 pipeline parallelism

backward communication, 480 efficient utilization, 474 generation function, 477 loop-carried data dependence, 479–481 loop initiation interval, 483–488 ND-range execution model, 475–478 spatial implementation, 481–483 stages, 472–474 successive iterations, 482 work-item, 475 pipes automatic selection, 493 blocking/non-blocking, 494 FIFO, 489, 490 information, 495 kernels, 491, 492 modular design/access, 490 parameterization, 492, 493 properties, 489 types, 491 runtime device ahead-of-time, 470–471 fpga\_selector, 467 SYCL, 452 Fine-grained specialization, 610 First-in first-out (FIFO), 489, 490 Functors, 255–258 Future Direction, 605

## G

Generic address spaces, 610 Graphics processing unit (GPU) accessing global memory, 405–409 caches/memory, 385 compilation process, 317 compute bound, 405 execution resources, 384 fixed functions, 384 hide latency, 398–399 high-level building blocks, 384–385 instruction streams, 399 memory bound, 405 occupancy, 399 offloading kernels abstraction, 400 cost of, 403–404 device memory/remote memory/host memory, 404 SYCL runtime library, 400 optimization math functions, 413 small data types, 412, 413 performance, 383 SIMD instructions, 391 simpler processors advantage, 386 features, 386 matrix multiplication, 386–388, 391 oneMKL project, 387

## INDEX

Graphics processing unit (GPU) (cont.) parallelism, 389–391 processor resources, 390 task kernel, 388 tradeoffs, 386 specialized functions/ extensions, 414 sub-group collective functions, 412 work-group local memory, 409–411 Graph scheduling CG (see Command group (CG)) data dependences, 202 data movement, 213–216 host synchronization, 216–218 Group algorithms, 115, 366 Gustafson, John, 10

## H

Hello, world!, 6–7 Heterogeneous system, 1 Host code, 33 Host devices cpu\_selector\_v, 45 development/debugging/ deployment, 43–46 device code classes, 61 host tasks, 63–65 submission, 56 task graph, 55–57

device selection, 51 aspects, 51–53 mechanisms, 54 GPU, 45–50 queue class, 58 queues, 37–42 single-source file device code, 34–35 Host tasks, 63

## I

id class, 110 Images, 72 In-order queues, 84 invoke\_simd, 609 item class, 111

## J

Just-in-time (JIT) compilation, 316

## K

Kernels accelerator types, 250 accessing outputs/data initialization, 336 advantages/disadvantages, 249 ahead-of-time (AOT), 259 correctness, 306–307 direct programming, 370 enumeration method, 296 explicit/selective object, 262

interoperability, 264 API-defined objects, 569, 570 non-SYCL source languages, 571–574 set\_arg() and set\_args() interfaces, 570 source/intermediate representation, 569 SPIR-V, 573 just-in-time (JIT), 259 kernel objects/kernel bundles, 259 matrix multiplication, 227–231 memory model, 528 named function object definition, 255–258 elements, 256 operator() function, 256–258 optional attributes, 258 object files, 259 precompiled kernel bundle, 260 querying kernels, 263 representation, 249 tuning/optimization, 308

## L

Lambda expressions, 23 anonymous, 26 anonymous/unnamed function objects/closures, 251 capture-list, 23 data parallelism, 102, 103 demonstration code, 25

elements, 252–255 function object, 26 identification, 254–255 implicit/explicit, 254 kernels, 249 named function objects, 256–259 parameters, 24 template parameter, 254 unnamed parameter, 255 Libraries built-in functions host and device, 504 host/device, 504 sycl::, 506 C++ standard library, 507–510 SYCL implementations, 503

## M

Map pattern, 351–352, 370 Math array type (marray), 271–273 marray class, 267, 271, 273 Masking and predication, 394 Matrix multiply and accumulate (MMA), 597 Memory (consistency) model acquire-release ordering, 533 atomic/non-atomic operations, 531–532 atomic operations, 534 atomic\_ref class, 531 barrier function synchronization, 223

INDEX

Memory (consistency) model (cont.) barriers/memory fences, 529–530 C++ thread, 524 core concepts, 525 data races/ synchronization, 526–529 features/capabilities, 523 heterogeneous systems, 524 instructions/microoperations, 526 Kernel, 528 memory model (see Memory model) memory ordering, 532–534 parallel application development, 527 reorder operations, 532 sequential execution, 526 SYCL specifications, 525 Memory model atomic and fence operations, 540 atomic\_fence function, 542 atomics (see Atomic operations) barriers and fences, 542 C++ standard library, 535 concepts, 534 development approaches, 541 language features, 535 load operations, 538 memory\_order enumeration class, 536–538

memory\_scope enumeration class, 539–541 querying device capabilities, 540–542 SYCL memory models, 536 Migrate CUDA code, 579 C++ code, 581 cooperative groups, 596 features, 595 global variables, 595 group algorithms, 596 matrix multiplication hardware, 597–599 memory model, 589 atomic operations, 590–592 equivalent barrier, 590 fences, 591–593 miscellaneous differences contexts, 593 error checking/error handling, 594 item classes vs. built-in variables, 592, 593 multiple targets vs. single device targets, 579–581 porting tools/ techniques, 598–602 real-world SYCL code, 581 similarities/differences, 583 barrier deadlock, 589 contiguous dimension, 585 execution model, 584 forward progress guarantees, 588

independent thread scheduling, 588 in-order vs. out-oforder, 584–585 sub-group size (warp sizes), 587 standardization process, 595 terminology, 583 thread block cluster, 596 Multiarchitecture binary, 315 Multiple translation units, 344–345 multi\_ptr, 612

## N

N-dimensional range (ND-range) communication/ synchronization, 221 data-parallel kernel, 360 device-wide synchronization, 554 get\_global\_id() function, 123 get\_local\_id() function, 123 group class, 124–126 group\_barrier function, 233 kernels form execution range, 113–114 explicit, 113 forward progress guarantees, 116 implementationdefined, 114 prescriptive construct, 113 shuffle operations, 118

SIMD lane, 120 sub-groups, 113, 117–120 task-based programming model, 117 vectorization, 117 work-groups, 113, 115–117 work-items, 113, 115, 116 local accessor, 231–232 nd\_item class, 124–125 nd\_range class, 122, 123 parallel\_for, 121 pipeline parallelism, 475–478 sub\_group class, 126–127 synchronization functions, 232–233 two-dimensional range, 222 work-groups/work-item, 221–222, 233–235 nd\_range class, 122 See also N-dimensional range (ND-range) none\_of\_group, 242

## O

oneAPI DPC++ Library (oneDPL), 510 binary\_search, 516 error handling model, 520 policy and host-side iterators, 515 Online resources, 313 Out-of-order queues, 84, 92

INDEX

## P

Pack, 377–379 Pack pattern, 358–359 parallel\_for, 107 Parallel patterns direct programming gather/scatter operations, 377 map pattern, 370 pack, 377–379 reduction patterns, 373–374 stencil pattern, 371–373 hardware devices, 350 high-level overview, 350 map pattern, 351–352 pack, 358 properties, 349 reduction, 356–358 scan, 356–357 stencil, 352–354 STL’s algorithms, 367 unpack, 359 vendor-provided libraries, 370 Parallel programming Amdahl, Gene/Gustafson, John, 10 data-parallel programming, 13 heterogeneous system, 11 Think Parallel, 9 See also Data parallelism Performance portability, 98, 290 Platform model

advantages, 320 compilation process ahead-of-time/just-in-time options, 319 offload bundler/ unbundler, 319 Portability, 98, 317 Predication and masking, 394 printf and sycl::stream, 326 Profiling queues, 330

## Q

Queues definition, 37–39 device selector, 41 device\_selector class, 41–42 in-order vs. out-of-order, 21 member functions, 39 multiple queues, 40, 41 out-of-order vs. in-order, 21 profiling, 330 work execution, 39, 40

## R

Race condition, 19 range class, 109 Read-after-Write (RAW), 202 reducer class, 363 Reduction, 354 reduction class, 361 Reduction library, 360

Reduction patterns, 356–358, 373–374 Resources online, 313

## S

Scaling, 11 Scan pattern, 356–357 Single instruction, multiple data (SIMD), 98, 608 addition, 285 central processing units hardware thread, 423 instruction-level parallelism, 423 multilevel parallelism, 425 multiple calculations, 422 parallel processing hardware, 425 performance benefit, 422 STREAM Triad program, 425–427 thread-level parallelism, 424 vectorization, 436–448 x86 architecture, 422 convenience types, 281, 283 hardware instructions, 271 mental model, 269 vectors, 269 Single program, multiple data (SPMD), 105, 393, 608 programming models, 269 Single-source, 31

Specialization mechanism, 611 SPMD/SIMD programming styles, 608–610 Standard Template Library (STL), 606 std::simd, 608 Stencil pattern, 352–354, 371–373 stream (sycl::stream), 326 Structure-of-Arrays (SOA), 443 Sub-group, 113 Submit, 39 SYCL\_EXTERNAL, 344 SYCLomatic tool, 598–602 SYCL standard, 1, 2, 313 Synchronization accessors, 217 barrier function, 223–225 device-wide, 553 events, 216 graph execution, 216 ND-range kernel, 232–233 queue objects, 216 sub-groups communication, 236 thread-level parallelism, 431 use\_mutex, 217 vectors, 438 Synchronous, 139 error, 139 error handling catch exceptions, 144 definition, 137 sub-buffer, 139

INDEX

Synchronous (cont.) sycl::exception, 143 try-catch structure, 143–144 unhandled C++ exception, 141 queues (in-order), 21

## T

Task graph data command groups, 84 data dependences, 86 depends\_on() method, 85 disjoint dependences, 82 events, 85 execution, 80 host device, 55–57 Read-after-Read (RAR) scenario, 88 Thread-level parallelism affinity insight, 431–434 elements, 430 exploiting parallelism, 435 mapping, 430 memory, 435–436 parallel\_for kernel code, 428, 429 SYCL program, 430 TBB partitioner, 434 work-group scheduling, 430 throw\_asynchronous, 148 Timing and profiling, 330

Tracing and profiling tools interfaces, 334 Translation unit, 31, 344, 345

## U

Unified shared memory (USM), 67, 92, 153 advantage of, 72 allocation types, 73 atomic operations, 550 characteristics, 154 communication, 225–227 data initialization, 165–166 data initialization and data movement, 165 definition, 154 device allocation, 154, 157 host allocation, 155 malloc, 72 memory allocation, 156 aligned\_malloc functions, 164 C++ allocator–style, 158, 162–163 C++-style, 158, 160–161 context object, 157 C-style, 158–159 deallocation, 164–165 malloc functions, 158 new/malloc/allocators, 156 memset function, 166 movement (see Data movement) queries, 174–177

shared allocation, 155 unified virtual address, 73 Unit-stride/fastest moving dimension, 585–586 Unpack pattern, 359, 379–380

## V

vec class, 267, 273 Vectors convenience types, 268 address escaping, 284 compilers, 281 hardware implementation, 280 hardware instruction, 282 implicit, 282 kernel execution, 281 memory access, 283 parallelism, 281, 282 SIMD/SPMD instructions, 281 work-items, 282 CPU SIMD AOS (Array-of-Struct) structures, 442–444 computational complexity, 448 data type impact, 444–446 destination register, 441 execution model, 437–440 gather/scatter instructions, 445

hardware, 436–448 instruction stream, 436 masking and cost, 440–442 single\_task, 446–448 sub-group barrier, 438 unit-stride vector, 444 work-items/work-group, 438 data collection, 268–269 elements/element type, 274 explicit code, 269 implicit, 270 instruction/clock cycle, 270 interoperability/backend-native functions, 276 load() member function, 274 load/store operations, 274–276 memory layout, 281 NumElements parameter, 274 scalar operations, 267 SIMD mappings, 269 SIMD types, 284–285 store() member function, 274 sub-group barriers and shuffles, 269–271 swizzled\_vec\_\_ class, 279 swizzle operations, 276–279 swizzles, 273 SYCL 1.2.1 specification, 268 vec class, 274 work-item, 270 Virtual functions, 17 Vote functions, 242

INDEX

W, X

wait, 7, 19, 20, 39

wait\_and\_throw, 39, 148

Warp matrix multiplication and accumulation (WMMA), 597

Websites, 313

Work-group, 113

Work-group barriers, 115 Work-group local memory, 115 Work-item, 113 Write-after-Read (WAR), 202

Y, Z

“Y” pattern, 204, 205, 211
