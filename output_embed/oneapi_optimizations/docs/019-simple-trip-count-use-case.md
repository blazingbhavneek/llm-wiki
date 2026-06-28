## Simple Trip Count Use Case

The following example performs a summation and uses specialization constants to set the trip count.

```cpp
#include <sycl/sycl.hpp>

class SpecializedKernel;

// Identify the specialization constant.
constexpr sycl::specialization_id<int> nx_sc;

int main(int argc, char *argv[]) {
  sycl::queue queue;

  std::cout << "Running on "
      << queue.get_device().get_info<sycl::info::device::name>() << "\n";

  std::vector<float> vec(1);
  {
    sycl::buffer<float> buf(vec.data(), vec.size());

    // Application execution stops here asking for input from user
    int Nx;
    if (argc > 1) {
      Nx = std::stoi(argv[1]);
    } else {
      Nx = 1024;
    }

    std::cout << "Nx = " << Nx << std::endl;

    queue.submit([&](sycl::handler &h) {
      sycl::accessor acc(buf, h, sycl::write_only, sycl::no_init);

      // set specialization constant with runtime variable
      h.set_specialization_constant<nx_sc>(Nx);

      h.single_task<SpecializedKernel>([=](sycl::kernel_handler kh) {
        // nx_sc value here will be input value provided at runtime and
        // can be optimized because JIT compiler now treats it as a constant.
        int runtime_const_trip_count = kh.get_specialization_constant<nx_sc>();
        int accum = 0;
        for (int i = 0; i < runtime_const_trip_count; i++) {
          accum = accum + i;
        }
    }
  }
}
```

```cpp
acc[0] = accum;
    });
});
}
std::cout << vec[0] << std::endl;
return 0;
}
```

The goal is to specialize the trip count variable Nx for the loop in the kernel. Since the user inputs the trip count after execution of the program starts, the host compiler does not know the value of Nx. The input value can be passed as a specialization constant to the JIT compiler, allowing the JIT compiler to apply some optimizations such as unrolling the loop.

Without the specialization constants feature, the variable Nx would need to be a constant expression for the whole program to achieve this. In this way, specialization constants can lead to more optimization and hence faster kernel code, by creating constant values from runtime variables.

In contrast, the host compiler cannot effectively optimize the example loop below where the trip count is not a constant, since it needs runtime checks for safety/legality.

```txt
for (int i = 0; i < Nx; i++) {
    // Optimizations are limited when Nx is not a constant.
}
```

## Modified STREAM Triad Application

In the following example (a modified STREAM Triad) we have the classic STREAM Triad with several multiply and add operations where the variable multiplier and the number of multiply-add operations are determined by an input variable.

Below is a snippet of the original kernel code run on the device. The runtime variable inner\_loop\_size is used to set the loop upper bound.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    h.parallel_for<non_specialized_kernel>(array_size / 2, [=](auto idx) {
        // set trip count to runtime variable
        auto runtime_trip_count_const = inner_loop_size;
        auto accum = 0;
        for (size_t j = 0; j < runtime_trip_count_const; j++) {
            auto multiplier = scalar * j;
            accum = accum + A0[idx] + B0[idx] * multiplier;
        }
        C0[idx] = accum;
    });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

In order to improve performance, we use the specialization constant feature to specialize the variable inner\_loop\_size. Below is a snippet of the kernel code run on the device - using a specialization constant.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    // set specialization constant using runtime variable
    h.set_specialization_constant<trip_sc>(inner_loop_size);
    h.parallel_for<specialized_kernel>(
        array_size / 2, [=](auto idx, sycl::kernel_handler kh) {
            // set trip count to the now known specialization constant
            auto runtime_trip_count_const =
                kh.get_specialization_constant<trip_sc>();
            auto accum = 0;
            for (size_t j = 0; j < runtime_trip_count_const; j++) {
                auto multiplier = scalar * j;
                accum = accum + A0[idx] + B0[idx] * multiplier;
            }
            C0[idx] = accum;
        });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

We finally compare the specialization trip count value with the following example that uses a regular constant value. Below is a snippet of the kernel code run on the device using a regular constant.

```cpp
auto q0_event = q.submit([&](sycl::handler &h) {
    h.parallel_for<regular_constant_kernel>(array_size / 2, [=](auto idx) {
        // set trip count to known regular constant
        size_t runtime_trip_count_const = 10;
        auto accum = 0;
        for (size_t j = 0; j < runtime_trip_count_const; j++) {
            auto multiplier = scalar * j;
            accum = accum + A0[idx] + B0[idx] * multiplier;
        }
        C0[idx] = accum;
    });
});

q.wait();

cl_ulong exec_time_ns0 =
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_end>() -
    q0_event
        .get_profiling_info<sycl::info::event_profiling::command_start>();

std::cout << "Execution time (iteration " << i
       << ") [sec]: " << (double)exec_time_ns0 * 1.0E-9 << "\n";
min_time_ns0 = std::min(min_time_ns0, exec_time_ns0);
```

Timings from the runs of the three different versions are displayed below. The stream size represents the size of arrays A0, B0, and C0. The inner trip count represents the value of the runtime\_trip\_count\_const variable set using the specialization constant.

Displayed below are timing outputs for example runs of the different versions using a stream size of 134217728 elements (1024 MB) and an inner trip count of 10 as inputs.

Run with runtime variable: Time in sec (fastest run): 0.00161008

Run with specialization constant: Time in sec (fastest run): 0.00156256

Run with constant value: Time in sec (fastest run): 0.00155104

The results, as expected, show that using the specialization constant improves the performance of the computation on the device from the execution time seen with the runtime variable to one that more closely matches the execution time seen with the constant value. Furthermore, analysis of the generated code shows the specialized version of the application unrolls the main loop due to it’s added capability to specialize the loop trip count & JIT compile it as a known constant. We witness about inner\_loop\_size times (thus 10 times in this example) as many floating-point add instructions in the main loop of the program using specialization constants as compared to the one using a runtime variable.

## Accuracy Versus Performance Tradeoffs in Floating-Point Computations

Programmers of floating-point applications typically aim for the following two objectives:

• Accuracy: Produce results that are “close” to the result of the exact calculation.

• Performance: Produce an application that runs as fast as possible.

The two objectives usually conflict. However, good programming practices and judicious use of compiler options allow you to control the tradeoffs.

For more information, see the article: Consistency of Floating-Point Results using the Intel Compiler or Why doesn’t my application always give the same answer?, by Dr. Martyn J. Corden and David Kreitzer (2018)

In this section, we present some mechanisms (compiler options and source-level changes) that allow the programmer to control the semantics (and hence the accuracy and performance) of floating-point computations on the host as well as on the device. We describe compiler options for OpenMP and SYCL programs, and describe source-level changes in SYCL.

## OpenMP

In OpenMP, the following -fp-model options may be used to control the semantics of floating-point computations on the host as well as on the device.

1. -fp-model=precise

This option tells the compiler to strictly adhere to value-safe optimizations when implementing floating-point calculations. It disables optimizations (such as re-association, multiply by reciprocal, and zero folding) that can change the result of floating-point calculations. The increased accuracy that comes with -fpmodel=precise may result in lower performance.

1. -fp-model=fast

This option is the default for both host and device compilations at -O2 and above. The option tells the compiler to use more aggressive optimizations when implementing floating-point calculations. These optimizations increase speed but may affect the accuracy or reproducibility of floating-point computations.

In C/C++, the -fp-model=fast option is equivalent to the -ffast-math option. With this option (at -O2 and above), all 7 fast-math flags (nnan, ninf, nsz, arcp, contract, afn, reassoc) are set by the C/C++ front-end. (See https://llvm.org/docs/LangRef.html#fast-math-flags for a description of the fast-math flags in LLVM.)

In Fortran, on the other hand, the language rules dictate that we cannot set the nnan flag (No NaNs) by default. So the -fp-model=fast option (at -O2 and above) only sets the other 6 fast-math flags (ninf, nsz, arcp, contract, afn, reassoc). To set all 7 fast-math flags in Fortran, use the -ffast-math option.

```batch
1. -Xopenmp-target-backend "-options -cl-fast-relaxed-math"
```

The -fp-model=fast (or -ffast-math) option does not enable native math instructions on the Intel GPU (Intel<sup>®</sup> Data Center GPU Max Series). You need to compile with -Xopenmp-target-backend “-options - cl-fast-relaxed-math” to get native math instructions on the GPU. Native math instructions give even lower accuracy than what is allowed with -fp-model=fast.

-Xopenmp-target-backend “-options -cl-fast-relaxed-math” passes the -cl-fast-relaxed-math option to the backend in the compilation tool chain for the device. -cl-fast-relaxed-math relaxes the precision of commonly used math functions on the device. It offers a quick way to get performance gains for kernels with many math library function calls, as long as the accuracy requirements are satisfied by what is provided through native math instructions.

The -cl-fast-relaxed-math option affects the compilation of the entire program and does not permit fine control of the resulting numeric accuracy.

Note that Intel GPUs support native for single precision (float, real) only.

## Notes (OpenMP):

• When -fp-model is specified on the compilation command line (outside of the -fopenmptargets=spir64=”…” set of options), the -fp-model option applies to both the host and the device compilations. For example, the following compilation command specifies -fp-model=precise for both the host and the device compilations:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -fp-model=precise
```

You can specify different \`\`-fp-model\`\` keywords for the host and the device compilations as shown below.

• To specify -fp-model=fast for the host compilation, and -fp-model=precise for the device compilation:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64="-fp-model=precise" -fp-model=fast
Or:
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64="-fp-model=precise"
(No need to specify ``-fp-model=fast`` since it is the default at -O2 or higher.)
```

• To specify -fp-model=precise for the host compilation, and -fp-model=fast for the device compilation:

```shell
icx/icpx/ifx -O3 -fiopenmp -fopenmp-targets=spir64="-fp-model=fast" -fp-model=precise
```

• To specify -fp-model=fast for the host compilation, and relaxed-math for the device compilation:

```txt
icx/icpx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -Xopenmp-target-backend "-options -cl-fast-relaxed-math" -fp-model=fast
Or:
icx/ifx -O2 -fiopenmp -fopenmp-targets=spir64 -Xopenmp-target-backend "-options -cl-fast-relaxed-math"
(No need to explicitly specify ``-fp-model=fast`` since it is the default at -O2 or higher.)
```

• You can combine the fast, precise, and relaxed-math options with -fimf-precision=low (medium or high) option to fine-tune precision on the host side. The -fimf-precision option is not supported on the device side currently.

The following table shows a summary of how to set the various options (precise, fast-math, relaxed math) in OpenMP to (a) both the host and the device (second column); (b) to the host only (third column); and (c) to the device only (fourth column).

OpenMP - Summary of Options

<table><tr><td>Floating Point Semantics</td><td>Apply to Host and Device Compilations</td><td>Apply to Host Compilation Only</td><td>Apply to Device Compilation Only</td></tr><tr><td>Precise</td><td>-fp-model=precise</td><td>-fp-model=precise, and specify ``-fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=fast&quot;</td><td>-fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=precise&quot;</td></tr><tr><td>Fast-math</td><td>-fp-model=fast (default)</td><td>-fp-model=fast, and specify -fiopenmp -fopenmp-targets=spir64=&quot;-fp-model= precise&quot;</td><td>-fp-model=precise, and specify -fiopenmp -fopenmp-targets=spir64=&quot;-fp-model=fast&quot;</td></tr><tr><td>Relaxed-math (native instructions)</td><td>Applies to device only</td><td>Applies to device only</td><td>-Xopenmp-target-backend &quot;-options -cl-fast-relaxed-math&quot;</td></tr></table>

## SYCL

In SYCL, as in OpenMP, the -fp-model=fast and -fp-model=precise options may be used for both host and device compilations.

In SYCL, -fp-model=fast option is equivalent to the -ffast-math option, and is the default for both host and device compilations at -O2 and above.

To specify relaxed-math for device compilation, use the compiler option -Xsycl-target-backend “- options -cl-fast-relaxed-math”. You need to compile with this option to get native math instructions on the GPU.

Note that SYCL (and Intel GPUs) support native for single precision (float, real) only.

## Notes (SYCL):

• When -fp-model is specified on the compilation command line (outside of any -Xsycl-target option), the -fp-model option applies to both the host and the device compilations. For example, the following compilation command specifies -fp-model=precise for both the host and the device compilations:

```txt
icx/icpx/ifx -fsycl -fp-model=precise

You can specify different ``-fp-model`` keywords for the host and device compilations as shown below.
```

• To specify -fp-model=fast for the host compilation, and -fp-model=precise for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=precise" -fp-model=fast
Or:
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=precise"
(No need to specify ``-fp-model=fast`` since it is the default at -02 or higher.)
```

• To specify -fp-model=precise for the host compilation, and -fp-model=fast for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-frontend "-fp-model=fast" -fp-model=precise
```

• To specify -fp-model=fast for the host compilation, and relaxed-math for the device compilation:

```txt
icx/icpx -fsycl -Xsycl-target-backend "-options -cl-fast-relaxed-math" -fp-model=fast
Or:
icx/icpx -fsycl -Xsycl-target-backend "-options -cl-fast-relaxed-math"
(No need to specify ``-fp-model=fast`` since it is the default at -02 or higher.)
```

The following table shows a summary of how to set the various options (math, fast-math, relaxed math) in SYCL to (a) both the host and the device (second column); (b) to the host only (third column); and (c) to the device only (fourth column).

SYCL - Summary of Options

<table><tr><td>Floating Point Semantics</td><td>Apply to Host and Device Compilations</td><td>Apply to Host Compilation Only</td><td>Apply to Device Compilation Only</td></tr><tr><td>Precise</td><td>-fp-model=precise</td><td>-fp-model=precise, and specify -Xsycl-target-frontend &quot;-fp-mode=fast&quot;</td><td>-Xsycl-target-frontend &quot;-fp-model=precise&quot;</td></tr><tr><td>Fast-math</td><td>-fp-model=fast (default)</td><td>-fp-model=fast, and specify -Xsycl-target-frontend &quot;-fp-model=precise&quot;</td><td>-fp-model=precise, and specify -Xsycl-target-frontend &quot;-fp-model=fast&quot;</td></tr><tr><td>Relaxed-math (native instructions)</td><td>Applies to device only</td><td>Applies to device only</td><td>-Xsycl-target-backend &quot;-options -cl-fast-relaxed-math&quot;</td></tr></table>

## Guidelines

In general, here are some guidelines for which options to use:

• Do not specify inconsistent options. The result will be unpredictable.

• The most commonly used option is -fp-model=fast for both host and device.

• Use relaxed-math for best performance on the device.

• Use -fp-model=precise for highest precision.
