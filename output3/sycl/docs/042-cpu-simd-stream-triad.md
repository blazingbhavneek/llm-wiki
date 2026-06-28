Like other parallel processing hardware (e.g., GPUs), it is important to give the CPU a sufficiently large set of data elements to process. To demonstrate the importance of exploiting multilevel parallelism to handle a large set of data, consider a simple C++ STREAM Triad program, as shown in Figure 16-4.

```c
// C++ STREAM Triad workload
// __restrict is used to denote no memory aliasing among
// arguments
template <typename T>
double triad(T* __restrict VA, T* __restrict VB,
            T* __restrict VC, size_t array_size,
            const T scalar) {
    double ts = timer_start();
    for (size_t id = 0; id < array_size; id++) {
        VC[id] = VA[id] + scalar * VB[id];
    }
    double te = timer_end();
    return (te - ts);
}
```

Figure 16-4. STREAM Triad C++ loop

## A NOTE ABOUT STREAM TRIAD WORKLOAD

The STREAM Triad workload (www.cs.virginia.edu/stream) is an important and popular benchmark workload that CPU vendors use to demonstrate memory bandwidth capabilities. We use the STREAM Triad kernel to demonstrate code generation of a parallel kernel and the way that it is scheduled to achieve significantly improved performance through the techniques described in this chapter. STREAM Triad is a relatively simple workload but is sufficient to show many of the optimizations in an understandable way. There is a STREAM implementation from the University of Bristol, called BabelStream, that includes a C++ with SYCL version.

## Chapter 16 Programming for CPUs

The STREAM Triad loop may be trivially executed on a CPU using a single CPU core for serial execution. A good C++ compiler will perform loop vectorization to generate SIMD code for the CPU that has hardware to exploit instruction-level SIMD parallelism. For example, for an Intel Xeon processor with AVX-512 support, the Intel C++ compiler generates SIMD code as shown in Figure 16-5. Critically, the compiler’s transformation of the code reduced the number of loop iterations by doing more work per loop iteration (using SIMD instructions and loop unrolling).

Figure 16-5. AVX-512 assembly code for STREAM Triad C++ loop

As shown in Figure 16-5, the compiler was able to exploit instructionlevel parallelism in two ways. First is by using SIMD instructions, exploiting instruction-level data parallelism, in which a single instruction can process eight double-precision data elements simultaneously in parallel (per instruction). Second, the compiler applied loop unrolling to get the outof-order execution effect of these instructions that have no dependences between them, based on hardware multiway instruction scheduling.

If we try to execute this function on a CPU, it will probably run well for small array sizes—not great, though, since it does not utilize any multicore or threading capabilities of the CPU. If we try to execute this function with a large array size on a CPU, however, it will likely perform very poorly because the single thread will only utilize a single CPU core and will be bottlenecked when it saturates the memory bandwidth of that core.

## Exploiting Thread-Level Parallelism

To improve the performance of the STREAM Triad kernel, we can compute on a range of data elements that can be processed in parallel, by converting the loop to a parallel\_for kernel.

The body of this STREAM Triad SYCL parallel kernel looks exactly like the body of the STREAM Triad loop that executes in serial C++ on the CPU, as shown in Figure 16-6.

```cpp
constexpr int num_runs = 10;
constexpr size_t scalar = 3;

double triad(const std::vector<float>& vecA,
            const std::vector<float>& vecB,
            std::vector<float>& vecC) {
    assert(vecA.size() == vecB.size() &&
        vecB.size() == vecC.size());
    const size_t array_size = vecA.size();
    double min_time_ns = std::numeric_limits<double>::max();

    queue q{property::queue::enable_profiling{}};
    std::cout << "Running on device: "
           << q.get_device().get_info<info::device::name>()
           << "\n";

    buffer<float> bufA(vecA);
    buffer<float> bufB(vecB);
    buffer<float> bufC(vecC);

    for (int i = 0; i < num_runs; i++) {
        auto Q_event = q.submit([&](handler& h) {
            accessor A{bufA, h};
            accessor B{bufB, h};
            accessor C{bufC, h};

            h.parallel_for(array_size, [=](id<1> idx) {
                C[idx] = A[idx] + B[idx] * scalar;
            });
        });

        double exec_time_ns =
            Q_event.get_profiling_info<
                info::event_profiling::command_end>() -
            Q_event.get_profiling_info<
                info::event_profiling::command_start>();

        std::cout << "Execution time (iteration " << i
            << ") [sec]: "
            << (double)exec_time_ns * 1.0E-9 << "\n";
        min_time_ns = std::min(min_time_ns, exec_time_ns);
    }

    return min_time_ns;
}
```

## Figure 16-6. SYCL STREAM Triad parallel\_for kernel code
