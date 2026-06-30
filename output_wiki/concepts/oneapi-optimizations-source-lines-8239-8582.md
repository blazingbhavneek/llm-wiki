# oneapi_optimizations Source Lines 8239-8582

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L8239-L8582

Citation: [oneapi_optimizations:L8239-L8582]

````text
## Compilation

oneAPI has multiple types of compilation. The main source to the application is compiled, and the offloaded kernels are compiled. For the kernels, this might be Ahead-Of-Time (AOT) or Just-In-Time (JIT).

In this section we cover topics related to this compilation and how it can impact the efficiency of the execution.

• Just-In-Time Compilation

• Ahead-Of-Time Compilation

• Specialization Constants

• Accuracy Versus Performance Tradeoffs in Floating-Point Computations

## Just-In-Time Compilation

The Intel<sup>®</sup> oneAPI SYCL Compiler converts a SYCL program into an intermediate language called SPIR-V and stores that in the binary produced by the compilation process. The advantage of producing this intermediate file instead of the binary is that this code can be run on any hardware platform by translating the SPIR-V code into the assembly code of the platform at runtime. This process of translating the intermediate code present in the binary is called JIT compilation (Just-In-Time compilation). JIT compilation can happen on demand at runtime. There are multiple ways in which this JIT compilation can be controlled. By default, all the SPIR-V code present in the binary is translated upfront at the beginning of the execution of the first offloaded kernel.

```cpp
#include <array>
#include <chrono>
#include <iostream>
#include <sycl/sycl.hpp>

// Array type and data size for this example.
constexpr size_t array_size = (1 << 16);
typedef std::array<int, array_size> IntArray;
```

```cpp
void VectorAdd1(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum) {
  sycl::range num_items{a.size()};

  sycl::buffer a_buf(a);
  sycl::buffer b_buf(b);
  sycl::buffer sum_buf(sum.data(), num_items);

  auto e = q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor a_acc(a_buf, h, sycl::read_only);
    sycl::accessor b_acc(b_buf, h, sycl::read_only);
    // Output accessor
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items,
                      [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
  });
  q.wait();
}

void VectorAdd2(sycl::queue &q, const IntArray &a, const IntArray &b,
        IntArray &sum) {
  sycl::range num_items{a.size()};

  sycl::buffer a_buf(a);
  sycl::buffer b_buf(b);
  sycl::buffer sum_buf(sum.data(), num_items);

  auto e = q.submit([&](auto &h) {
    // Input accessors
    sycl::accessor a_acc(a_buf; h, sycl::read_only);
    sycl::accessor b_acc(b_buf; h, sycl::read_only);
    // Output accessor
    sycl::accessor sum_acc(sum_buf; h, sycl::write_only, sycl::no_init);

    h.parallel_for(num_items,
                       [=](auto i) { sum_acc[i] = a_acc[i] + b_acc[i]; });
  });
  q.wait();
}

void InitializeArray(IntArray &a) {
  for (size_t i = 0; i < a.size(); i++)
    a[i] = i;
}

int main() {
  IntArray a, b, sum;

  InitializeArray(a);
  InitializeArray(b);

  sycl::queue q(sycl::default_selector_v,
              sycl::property::queue::enable_profiling{});

  std::cout << "Running on device: "
```

```cpp
<< q.get_device().get_info<sycl::info::device::name>() << "\n";
std::cout << "Vector size: " << a.size() << "\n";
auto start = std::chrono::steady_clock::now();
VectorAdd1(q, a, b, sum);
auto end = std::chrono::steady_clock::now();
std::cout << "Initial Vector add1 successfully completed on device - took "
       << (end - start).count() << " nano-secs\n";

start = std::chrono::steady_clock::now();
VectorAdd1(q, a, b, sum);
end = std::chrono::steady_clock::now();
std::cout << "Second Vector add1 successfully completed on device - took "
       << (end - start).count() << " nano-secs\n";

start = std::chrono::steady_clock::now();
VectorAdd2(q, a, b, sum);
end = std::chrono::steady_clock::now();
std::cout << "Initial Vector add2 successfully completed on device - took "
       << (end - start).count() << " nano-secs\n";

start = std::chrono::steady_clock::now();
VectorAdd2(q, a, b, sum);
end = std::chrono::steady_clock::now();
std::cout << "Second Vector add2 successfully completed on device - took "
       << (end - start).count() << " nano-secs\n";
return 0;
```

When the program above is compiled using the command below (assuming that the name of the source file is example.cpp):

```batch
icpx -fsycl -03 -o example example.cpp
```

and run, the output generated will show that the first call to VectorAdd1 takes much longer than the calls to other kernels in the program due to the cost of JIT compilation, which gets invoked when vectorAdd1 is executed for the first time.

If the application contains multiple kernels, one can force eager JIT compilation or lazy JIT compilation using compile-time switches. Eager JIT compilation will invoke JIT compilation on all the kernels in the binary at the beginning of execution, while lazy JIT compilation will enable JIT complication only when the kernel is actually called during execution. In situations where certain kernels are not called, this has the advantage of not translating code that is never actually executed, which avoids unnecessary JIT compilation. This mode can be enabled during compilation using the following option:

-fsycl-device-code-split=<value>

where <value> is

• per\_kernel: generates code to do JIT compilation of a kernel only when it is called

• per\_source: generates code to do JIT compilation of all kernels in the source file when any of the kernels in the source file are called

• off: performs eager JIT compilation of all kernels in the application

• auto: the default, the compiler will use its heuristic to select the best way of splitting device code for JIT compilation

If the above program is compiled with this option:

```batch
icpx -fsycl -03 -o example vec1.cpp vec2.cpp main.cpp -fsycl-device-code-split=per_kernel
```

and run, then from the timings of the kernel executions it can be seen that the first invocations of VectorAdd1 and VectorAdd2 take longer, while the second invocations will take less time because they do not pay the cost of JIT compilation.

In the example above, we can put VectorAdd1 and VectorAdd2 in separate files and compile them with and without the per\_source option to see the impact on the execution times of the kernels. When compiled with

```batch
icpx -fsycl -O3 -o example vec1.cpp vec2.cpp main.cpp -fsycl-device-code-split=per_source
```

and run, the execution times of the kernels will show that the JIT compilation cost is paid at the first kernel invocation, while the subsequent kernel invocations do not pay the JIT compilation cost. But when the program is compiled with

```batch
icpx -fsycl -03 -o example vec1.cpp vec2.cpp main.cpp
```

and run, the execution times of the kernels will show that the JIT compilation cost is paid upfront at the first invocation of the kernel, and all subsequent kernels do not pay the cost of JIT compilation.

## Ahead-Of-Time Compilation

The overhead of JIT compilation at runtime can be avoided by Ahead-Of-Time (AOT) compilation. With AOT compilation, the binary will contain the actual assembly code of the platform that was selected at compile time instead of the SPIR-V intermediate code. The advantage is that we do not need to JIT compile the code from SPIR-V to assembly during execution, which makes the code run faster. The disadvantage is that now the code cannot run anywhere other than the platform for which it was compiled.

When compiling in Ahead-Of-Time (AOT) mode for an Intel<sup>®</sup> GPU, one need to add an extra compiler option (-Xs) to indicate the specific GPU target.

## AOT Compiler Options for SYCL

Intel<sup>®</sup> Data Center GPU Max Series:

```batch
icpx -fsycl -fsycl-targets=spir64_gen -Xs "-device pvc" source.c
```

## AOT Compiler Options for OpenMP

Intel<sup>®</sup> Data Center GPU Max Series:

```shell
icx -fiopenmp -fopenmp-targets=spir64_gen -Xs "-device pvc" source.c
```

## Notes

• The compiler options shown above can also be used when compiling OpenMP Fortran programs in AOT mode (using ifx).

• In JIT-mode, the Intel® Graphics Compiler knows the type of the hardware and will adjust automatically. The extra -revision\_id option is only needed for AOT mode.

## Specialization Constants

SYCL has a feature called specialization constants that can explicitly trigger JIT compilation to generate code from the intermediate SPIR-V code based on the run-time values of these specialization constants. These JIT compilation actions are done during the execution of the program when the values of these constants are known. This is different from the JIT compilation, which is triggered based on the options provided to - fsycl-device-code-split.

In the example below, the call to set\_specialization\_constant binds the value returned by the call to function get\_value, defined on line 10, to the SYCL kernel bundle. When the kernel bundle is initially compiled, this value is not known and so cannot be used for optimizations. At runtime, after function get\_value is executed, the value is known, so it is used by command groups handler to trigger JIT compilation of the specialized kernel with this value.

```cpp
#include <sycl/sycl.hpp>
#include <vector>
```

```txt
class specialized_kernel;
```

```cpp
// const static identifier of specialization constant
const static sycl::specialization_id<float> value_id;

// Fetch a value at runtime.
float get_value() { return 10; };

int main() {
    sycl::queue queue;

    std::vector<float> vec(1);
    {
        sycl::buffer<float> buffer(vec.data(), vec.size());
        queue.submit([&](auto &cgh) {
            sycl::accessor acc(buffer, cgh, sycl::write_only, sycl::no_init);

            // Set value of specialization constant.
            cgh.template set_specialization_constant<value_id>(get_value());

            // Runtime builds the kernel with specialization constant
            // replaced by the literal value provided in the preceding
            // call of `set_specialization_constant<value_id Range`
            cgh.template single_task<specialized_kernel>(
                [=](sycl::kernel_handler kh) {
                    const float val = kh.get_specialization_constant<value_id>();
                    acc[0] = val;
                });
            });
        }
        queue.wait_and_throw();

        std::cout << vec[0] << std::endl;

        return 0;
    }
```

The specialized kernel at line 24 will eventually become the code shown below:

```txt
cgh.single_task<specialized_kernel>(
    [=]() { acc[0] = 10; });
```

This JIT compilation also has an impact on the amount of time it takes to execute a kernel. This is illustrated by the example below:

```cpp
#include <chrono>
#include <sycl/sycl.hpp>
#include <vector>

class specialized_kernel;
class literal_kernel;

// const static identifier of specialization constant
const static sycl::specialization_id<float> value_id;

// Fetch a value at runtime.
float get_value() { return 10; };

int main() {
    sycl::queue queue;
```

```cpp
// Get kernel ID from kernel class qualifier
sycl::kernel_id specialized_kernel_id =
    sycl::get_kernel_id<specialized_kernel>();

// Construct kernel bundle with only specialized_kernel in the input state
sycl::kernel_bundle kb_src =
    sycl::get_kernel_bundle<sycl::bundle_state::input>(
        queue.get_context(), {specialized_kernel_id});
// set specialization constant value
kb_src.set_specialization_constant<value_id>(get_value());

auto start = std::chrono::steady_clock::now();
// build the kernel bundle for the set value
sycl::kernel_bundle kb_exe = sycl::build(kb_src);
auto end = std::chrono::steady_clock::now();
std::cout << "specialization took - " << (end - start).count()
       << " nano-secs\n";

std::vector<float> vec{0, 0, 0, 0, 0};
sycl::buffer<float> buffer1(vec.data(), vec.size());
sycl::buffer<float> buffer2(vec.data(), vec.size());
start = std::chrono::steady_clock::now();
{
    queue.submit([&](auto &cgh) {
        sycl::accessor acc(buffer1, cgh, sycl::write_only, sycl::no_init);

        // use the precompiled kernel bundle in the executable state
        cgh.use_kernel_bundle(kb_exe);

        cgh.template single_task<specialized_kernel>(
            [=](sycl::kernel_handler kh) {
                float v = kh.get_specialization_constant<value_id>();
                acc[0] = v;
            });
        });
    queue.wait_and_throw();
}
end = std::chrono::steady_clock::now();

{
    sycl::host_accessor host_acc(buffer1, sycl::read_only);
    std::cout << "result1 (c): " << host_acc[0] << "\" << host_acc[1] << " "
                      << host_acc[2] << " " << host_acc[3] << " " << host_acc[4]
                      << std::endl;
}
std::cout << "execution took : " << (end - start).count() << " nano-secs\n";

start = std::chrono::steady_clock::now();
{
    queue.submit([&](auto &cgh) {
        sycl::accessor acc(buffer2, cgh, sycl::write_only, sycl::no_init);
        cgh.template single_task<literal_kernel>|([=]() { acc[0] = 20; });
    });
    queue.wait_and_throw();
}
end = std::chrono::steady_clock::now();

{
```

```cpp
sycl::host_accessor host_acc(buffer2, sycl::read_only);
    std::cout << "result2 (c): " << host_acc[0] << " " << host_acc[1] << " "
           << host_acc[2] << " " << host_acc[3] << " " << host_acc[4]
           << std::endl;
}
std::cout << "execution took - " << (end - start).count() << " nano-secs\n";
}
```

Looking at the runtimes reported by each of the timing messages, it can be seen that the initial translation of the kernel takes a long time, while the actual execution of the JIT-compiled kernel takes less time. The same kernel which had not been precompiled to the executable state takes longer because this kernel will have been JIT-compiled by the runtime before actually executing it.

Below we provide some examples showing simple use cases and applications of specialization constants.
````
