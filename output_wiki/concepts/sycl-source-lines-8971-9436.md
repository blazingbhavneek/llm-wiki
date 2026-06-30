# sycl Source Lines 8971-9436

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source sycl:L8971-L9436

Citation: [sycl:L8971-L9436]

````text
## Libraries

We have spent the entire book promoting the art of writing our own code. Now we finally acknowledge that some great programmers have already written code that we can just use. Libraries are the best way to get our work done. This is not a case of being lazy—it is a case of having better things to do than reinvent the work of others.

This chapter covers three different sets of library functionality:

1. Built-in functions defined by the SYCL specification

2. The C++ standard library

3. C++17 parallel algorithms, supported by the oneAPI DPC++ Library (oneDPL)

SYCL defines a rich set of built-in functions that provide common functions shared by host and device code. All SYCL implementations support these functions, and so we can rely on key math libraries being available on all SYCL devices.

The C++ standard library is not guaranteed to be supported in device code by all SYCL implementations. However, the DPC++ compiler (and other compilers) support this as an extension to SYCL, and so we briefly discuss the limitations of that extension here.

Finally, the oneAPI DPC++ Library (oneDPL) provides a set of algorithms based on the C++17 algorithms, implemented in SYCL, to provide a high-productivity solution for SYCL programmers. This can minimize programming effort across CPUs, GPUs, and FPGAs. Although oneDPL is not part of SYCL 2020, since it is implemented on top of SYCL, it should be compatible with any SYCL 2020 compiler.

## Built-In Functions

SYCL provides a rich set of built-in functions with support for various data types. These built-in functions are available in the sycl namespace on host and device and can be classified as in the following:

• Floating-point math functions: asin, acos, log, sqrt, floor, etc.

• Integer functions: abs, max, min, etc.

• Common functions: clamp, smoothstep, etc.

• Geometric functions: cross, dot, distance, etc.

• Relational functions: isequal, isless, isfinite, etc.

The documentation for this extensive collection of functions can be found in the SYCL 2020 specification, and the online documentation at registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html in sections 4.17.5 through 4.17.9.

Some compilers may provide options to control the precision of these functions. For example, the DPC++ compiler provides several such options, including -mfma, -ffast-math, and -ffp-contract=fast. It is important to check the documentation of a SYCL implementation to understand the availability of similar options (and their default values).

Several of the SYCL built-in functions have equivalents in the C++ standard library (e.g., sycl::log and std::log). SYCL implementations are not required to support calling C++ standard library functions within device code, but some implementations (e.g., DPC++) do.

Figure 18-1 demonstrates the usage of both the C++ std::log function and SYCL built-in sycl::log function in device code. Using DPC++ compiler implementation, both functions produce the same numeric results. In the example, the built-in relational function sycl::isequal is used to compare the results of std::log and sycl::log.

```cpp
constexpr int size = 9;
std::array<float, size> a;
std::array<float, size> b;

bool pass = true;

for (int i = 0; i < size; ++i) {
    a[i] = i;
    b[i] = i;
}

queue q;

range sz{size};

buffer<float> bufA(a);
buffer<float> bufB(b);
buffer<bool> bufP(&pass, 1);

q.submit([&](handler &h) {
    accessor accA{bufA, h};
    accessor accB{bufB, h};
    accessor accP{bufP, h};

    h.parallel_for(size, [=](id<1> idx) {
        accA[idx] = std::log(accA[idx]);
        accB[idx] = sycl::log(accB[idx]);
        if (!sycl::isequal(accA[idx], accB[idx])) {
            accP[0] = false;
        }
    });
});

Figure 18-1. Using std::log and sycl::log
```

## Chapter 18 Libraries

Note that the SYCL 2020 specification does not mandate that a SYCL math function implementation must produce the exact same numeric result as its corresponding C and C++ standard math function for a given hardware target. The specification allows for certain variations in the implementation to account for the characteristics and limitations of different hardware platforms. Therefore, it is possible for a SYCL implementation to produce matching results in practice, as demonstrated in the code example shown in Figure 18-1.

## Use the sycl:: Prefix with Built-In Functions

We strongly recommend invoking the SYCL built-in functions with an explicit sycl:: prepended to the name. Calling just sqrt() is not guaranteed to invoke the SYCL built-in on all implementations even if “using namespace sycl;” has been used.

SYCL built-in functions should always be invoked with an explicit sycl:: in front of the built-in name. Failure to follow this advice may result in strange and non-portable results.

When writing portable code, we recommend avoiding using namespace sycl; completely, in favor of explicitly using std:: and sycl:: namespaces. By being explicit, we remove the possibility of encountering unresolvable conflicts within certain SYCL implementations. This may also make code easier to debug in the future (e.g., if an implementation provides different precision guarantees for math functions in the std:: and sycl:: namespaces).

## The C++ Standard Library

As mentioned previously, the SYCL specification does not guarantee that functions from the C++ standard library will be supported in device code. However, there are several compilers that do support these functions: this simplifies the offloading of existing C++ code to SYCL devices and makes it easier to write libraries that use SYCL as an implementation detail (e.g., a user passing a function into a library can write that function without using any SYCL-specific features).

## YOUR MILEAGE MAY VARY

Since support in device code for functions from the std:: namespace varies across SYCL implementations, we cannot be sure that kernels employing the C++ standard library will be portable across multiple SYCL compilers and implementations.

The DPC++ compiler is compatible with a set of tested C++ standard APIs—we simply need to include the corresponding C++ header files and use the std namespace. All these APIs can be employed in device kernels the way they are employed in a typical C++ host application. Figure 18-2 shows an example of how to use std::swap in device code.

```cpp
CHAPTER 18    LIBRARIES

int main() {
    std::array<int, 2> arr{8, 9};
    buffer<int> buf{arr};

    {
        host_accessor host_A(buf);
        std::cout << "Before: " << host_A[0] << ", "
               << host_A[1] << "\n";
    } // End scope of host_A so that upcoming kernel can
        // operate on buf

    queue q;
    q.submit([&](handler &h) {
        accessor a{buf, h};
        h.single_task([=]) {
            // Call std::swap!
            std::swap(a[0], a[1]);
        });
    });

    host_accessor host_B(buf);
    std::cout << "After: " << host_B[0] << ", " << host_B[1]
                << "\n";
    return 0;
}

Sample output:
8, 9
9, 8
```

## Figure 18-2. Using std::swap in device code

Figure 18-3 lists C++ standard APIs with “Y” to indicate those that have been tested for use in SYCL kernels for CPU, GPU, and FPGA devices, at the time of writing. A blank indicates incomplete coverage (not all three device types) at the time of publication for this book.

<table><tr><td>C++ Standard API</td><td>libx46++</td><td>libx++</td><td>ISVC</td></tr><tr><td>atd::abs</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::acos</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::acosh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::add const</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::add cv</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::add volatile</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::alignment of</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::all of</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::any of</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::argy</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::array</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::asin</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::asinh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::assert</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::atan</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::atan2</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::atanh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::binary negate</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::binary search</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::bit and</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::bit not</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::bit or</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::bit xor</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::cbrt</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::cell</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::common type</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::complex</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::conditional</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::onj</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copy</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copy backward</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copy if</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copy n</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copysign</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::copysignf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::cos</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::cosh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::count</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::count if</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::decay</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::decimal</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::divides</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::enable if</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::equal range</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::equal tc</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::erf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::erfc</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::exp</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::exp</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::exp2</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::expml</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::extent</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fabs</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fdlm</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fill</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fill n</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::find</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::find if</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::find if not</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::floor</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fmax</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fmaxf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fmin</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fminf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::fmod</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>atd::for each</td><td>Y</td><td>Y</td><td>Y</td></tr></table>

<table><tr><td>C++ Standard API</td><td>libfek++</td><td>libc++</td><td>SVS</td></tr><tr><td>std::for each n</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::forward</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::frasp</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::generate</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::generate n</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::greater</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::greater equal</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::hypot</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::ilogb</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::imag</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::initializer list</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::integral constant</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is arithmetic</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is assignable</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is base of</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is base of union</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is compound</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is const</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is constructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is convertible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is copy assignable</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is copy constructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is default constructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is destructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is empty</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is fundamental</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is heap</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is heap until</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is literal type</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is membar pointer</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is move assignable</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is move constructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is object</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is parmutator</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is pod</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is reference</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is signe</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is scalar</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is signed</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is sorted</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is sorted until</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is standard layout</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is is inf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is trivially assignable</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is trivially constructible</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is trivially copyable</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is unsigned</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::is volatile</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::isgreater</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::isprestarequal</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::isinf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::isless</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::islessequal</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::lsnan</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::lsunordered</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::ldeep</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::less</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::less equal</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::lgamma</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::log</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::logle</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::loglr</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::log2</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::logb</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::logical and</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::logical not</td><td>Y</td><td>Y</td><td>Y</td></tr></table>

<table><tr><td>C++ Standard API</td><td>libx46++</td><td>libx++</td><td>CSV</td></tr><tr><td>std::logical or</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::lower bound</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::make heap</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::min</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::minus</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::modf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::modulus</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::move</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::move</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::move backward</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::move if noexcept</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::multiplies</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::nan</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::nanf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::nearbyint</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::nearbyintf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::negate</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::nextafter</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::none of</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::norm</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::not equal tc</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::not1/2</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::numeric limits(&gt;::infinite)</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::numeric limits(&gt;::lowest)</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::numeric limits(&gt;::quiet)</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::numeric limits(&gt;::quiet Na)</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::optional</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::pair</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::partial sort</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::partial sort copy</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::plus</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::polar</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::pop heap</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::pow</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::proi</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::push heap</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::rank</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::ratic</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::real</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::reduce</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::ref/cref</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::reference wrapper</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remainder</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remove all extents</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remove const</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remove tv</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remove extent</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::remove volatile</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::rempo</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::round</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::roundf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::sin</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::sinh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::sort</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::swap</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::tan</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::tanh</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::tgamma</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::transform</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::trunc</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::unconf</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::tuple</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::unary negate</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>std::upper bound</td><td>Y</td><td>Y</td><td>Y</td></tr></table>

Figure 18-3. Library support with CPU/GPU/FPGA coverage (at time of book publication)

The tested standard C++ APIs are supported in libstdc++ (GNU) with gcc 7.5.0+ and libc++ (LLVM) with clang 11.0+ and MSVC Standard C++ Library with Microsoft Visual Studio 2019+ for the host CPU as well.

On Linux, GNU libstdc++ is the default C++ standard library for the DPC++ compiler, so no compilation or linking option is required. If we want to use libc++, use the compile options -stdlib=libc++ -nostdinc++ to leverage libc++ and to not include C++ std headers from the system. The DPC++ compiler has been verified using libc++ in SYCL kernels on Linux, but the runtime needs to be rebuilt with libc++ instead of libstdc++. Details are in https://intel.github.io/llvm-docs/ GetStartedGuide.html#build-dpc-toolchain-with-libc-library. Because of these extra steps, libc++ is not the recommended C++ standard library for us to use in general, without a specific reason to do so.

To achieve cross-architecture portability, if a std:: function is not marked with “Y” in Figure 18-3, we need to be careful that we don’t create functional incorrectness (or build failures) for our application as it runs on target devices that we haven’t tested on!

## oneAPI DPC++ Library (oneDPL)

C++17 introduced parallel versions of the algorithms defined in the C++ standard library. Unlike their serial counterparts, each of the parallel algorithms accepts an execution policy as its first argument—this execution policy denotes how an algorithm may execute.

Loosely speaking, an execution policy communicates to an implementation whether it can parallelize the algorithm using threads, SIMD instructions, or both. We can pass one of the values seq, unseq, par, or par\_unseq as the execution policy, with meanings shown in Figure 18-4.

<table><tr><td>Execution Policy</td><td>Meaning</td></tr><tr><td>seq</td><td>Sequential execution.</td></tr><tr><td>unseq</td><td>Unsequenced SIMD execution. This policy requires that all functions provided are safe to execute in SIMD.</td></tr><tr><td>par</td><td>Parallel execution by multiple threads.</td></tr><tr><td>par_unseq</td><td>Combined effect of unseq and par.</td></tr></table>

## Figure 18-4. Execution policies

oneDPL extends the standard execution policies to provide support for SYCL devices. These SYCL-aware execution policies specify not only how an algorithm should execute, but also where it should execute. A SYCLaware policy inherits a standard C++ execution policy, encapsulates a SYCL device or queue, and allows us to set an optional kernel name. SYCLaware execution policies can be used with all standard C++ algorithms that support execution policies according to the C++17 standard.

oneDPL is not tied to any single SYCL compiler, it is designed to support all SYCL compilers.

Before we can use oneDPL and its SYCL-aware execution policies, we need to add some additional header files. Which headers we include will depend on the algorithms we intend to use, some common examples include:

• #include <oneapi/dpl/algorithm>

• #include <oneapi/dpl/numeric>

• #include <oneapi/dpl/memory>

## SYCL Execution Policy

Currently, only algorithms with the parallel unsequenced policy (par\_ unseq) can be safely offloaded to SYCL devices. This restriction stems from the forward progress guarantees provided by work-items in SYCL, which are incompatible with the requirements of other execution policies (e.g., par).

There are three steps to using a SYCL execution policy:

1. Add #include <oneapi/dpl/execution> into our code.

2. Create a policy object by providing a standard policy type, a class type for a unique kernel name

```txt
as a template argument (optional), and one of the following constructor arguments:
A SYCL queue
A SYCL device
A SYCL device selector
An existing policy object with a different kernel name
```

3. Pass the created policy object to an algorithm.

A oneapi::dpl::execution::dpcpp\_default object is a predefined device\_policy created with a default kernel name and default queue. This can be used to create custom policy objects or passed directly when invoking an algorithm if the default choices are sufficient.

```cpp
Figure 18-5 shows examples that assume use of the using namespace oneapi::dpl::execution; directive when referring to policy classes and functions.

auto policy_b = device_policy<parallel_unsequenced_policy,
            class PolicyB>{
    sycl::device{sycl::gpu_selector{}}};
std::for_each(policy_b, ...);
auto policy_c =
    device_policy<parallel_unsequenced_policy,
            class PolicyC>{sycl::default_selector{}};
std::for_each(policy_c, ...);
auto policy_d =
    make_device_policy<class PolicyD>(default_policy);
std::for_each(policy_d, ...);
auto policy_e =
    make_device_policy<class PolicyE>(sycl::queue{});
std::for_each(policy_e, ...);
```

## Figure 18-5. Creating execution policies

## Using oneDPL with Buffers

The algorithms in the C++ standard library are all based on iterators. To support passing SYCL buffers into these algorithms, oneDPL defines two special helper functions: oneapi::dpl::begin and oneapi::dpl::end.

These functions accept a SYCL buffer and return an object of an unspecified type that satisfies the following requirements:

• Is CopyConstructible, CopyAssignable, and comparable with operators == and !=.

• The following expressions are valid: a + n, a – n, and a – b, where a and b are objects of the type and n is an integer value.

Has a get\_buffer method with no arguments. The method returns the SYCL buffer passed to oneapi::dpl::begin and oneapi::dpl::end functions.

Note that using these helper functions requires us to add #include <oneapi/dpl/iterator> to our code. This functionality is not included by default, because these iterators are not required when using USM (which we will revisit shortly).

The code in Figure 18-6 shows how to use the std::fill function in conjunction with the begin/end helpers to fill a SYCL buffer. Note that the algorithm is in the std:: namespace, and only the execution policy is in a nonstandard namespace—this is not a typo! The C++ standard library explicitly permits implementations to define their own execution policies to support coding patterns like this.

```txt
CHAPTER 18 LIBRARIES
```

```cpp
#include <oneapi/dpl/algorithm>
#include <oneapi/dpl/execution>
#include <oneapi/dpl/iterator>
#include <sycl/sycl.hpp>

int main() {
    sycl::queue q;
    sycl::buffer<int> buf{1000};

    auto buf_begin = oneapi::dpl::begin(buf);
    auto buf_end = oneapi::dpl::end(buf);

    auto policy = oneapi::dpl::execution::make_device_policy<
        class fill>(q);
    std::fill(policy, buf_begin, buf_end, 42);

    return 0;
}
```

## Figure 18-6. Using std::fill

The code in Figure 18-7 shows an even simpler version of this code, using a default policy and ordinary (host-side) iterators. In this case, a temporary SYCL buffer is created, and the data is copied to this buffer. After processing of the temporary buffer on a device is complete, the data is copied back to the host. Working directly with existing SYCL buffers (where possible) is recommended to reduce data movement between the host and device and any unnecessary overhead of buffer creations and destructions.

```cpp
#include <oneapi/dpl/algorithm>
#include <oneapi/dpl/execution>
#include <oneapi/dpl/iterator>
#include <sycl/sycl.hpp>

int main() {
    std::vector<int> v(100000);
    std::fill(oneapi::dpl::execution::dpcpp_default,
        v.begin(), v.end(), 42);

    if (v[788] == 42)
        std::cout << "passed" << std::endl;
    else
        std::cout << "failed" << std::endl;

    return 0;
}
```

## Figure 18-7. Using std::fill with default policy and host-side iterators

Figure 18-8 shows an example which performs a binary search of the input sequence for each of the values in the search sequence provided. As the result of a search for the i<sup>th</sup> element of the search sequence, a Boolean value indicating whether the search value was found in the input sequence is assigned to the i<sup>th</sup> element of the result sequence. The algorithm returns an iterator that points to one past the last element of the result sequence that was assigned a result. The algorithm assumes that the input sequence has been sorted by the comparator provided. If no comparator is provided, then a function object that uses operator< to compare the elements will be used.

The complexity of the preceding description highlights that we should leverage library functions where possible, instead of writing our own implementations of similar algorithms which may take significant debugging and tuning time. Authors of the libraries that we can take advantage of are often experts in the internals of the device architectures we are targeting and may have access to information that we do not, so we should always leverage optimized libraries when they are available.

```cpp
CHAPTER 18    LIBRARIES

#include <oneapi/dpl/algorithm>
#include <iostream>
#include <oneapi/dpl/execution>
#include <oneapi/dpl/iterator>
#include <sycl/sycl.hpp>

using namespace sycl;

int main() {
    buffer<uint64_t, 1> kB{range<1>(10)};
    buffer<uint64_t, 1> vB{range<1>(5)};
    buffer<uint64_t, 1> rB{range<1>(5)};
    {
        host_accessor k{kB};
        host_accessor v{vB};

        // Initialize data, sorted
        k[0] = 0;
        k[1] = 5;
        k[2] = 6;
        k[3] = 6;
        k[4] = 7;
        k[5] = 7;
        k[6] = 8;
        k[7] = 8;
        k[8] = 9;
        k[9] = 9;

        v[0] = 1;
        v[1] = 6;
        v[2] = 3;
        v[3] = 7;
        v[4] = 8;
    }

    // create dpc++ iterators
    auto k_beg = oneapi::dpl::begin(kB);
    auto k_end = oneapi::dpl::end(kB);
    auto v_beg = oneapi::dpl::begin(vB);
    auto v_end = oneapi::dpl::end(vB);
    auto r_beg = oneapi::dpl::begin(rB);

    // create named policy from existing one
    auto policy = oneapi::dpl::execution::make_device_policy<
        class bSearch>(oneapi::dpl::execution::dpcpp_default);
```

## Figure 18-8. Using binary\_search

```cpp
// call algorithm
oneapi::dpl::binary_search(policy, k_beg, k_end, v_beg,
                             v_end, r_beg);

// check data
host_accessor r{rB};
if ((r[0] == false) && (r[1] == true) &&
    (r[2] == false) && (r[3] == true) && (r[4] == true)) {
  std::cout << "Passed. \nRun on "
         << policy.queue()
             .get_device()
             .get_info<info::device::name>()
         << "\n";
} else
  std::cout << "failed: values do not match.\n";

  return 0;
}
```

## Figure 18-8. (continued)

The code example shown in Figure 18-8 demonstrates the three typical steps when using oneDPL in conjunction with SYCL buffers:

1. Create SYCL iterators from our buffers.

2. Create a named policy from an existing policy.

3. Invoke the parallel algorithm.

## Using oneDPL with USM

In this section, we explore two ways to use oneDPL in combination with USM:

• Through USM pointers

• Through USM allocators

Unlike with buffers, we can directly use USM pointers as the iterators passed to an algorithm. Specifically, we can pass the pointers to the start and (one past the) end of the allocation to a parallel algorithm. It is important to be sure that the execution policy and the allocation itself were created for the same queue or context, to avoid undefined behavior at runtime. (Remember that this is not oneDPL specific, and we must always pay close attention to contexts when using USM!)

If the same USM allocation is to be processed by several algorithms, we can either use an in-order queue or explicitly wait for completion of each algorithm before using the same allocation in the next one (this is typical operation ordering when using USM). We should also be careful to ensure that we wait for completion before accessing the data on the host, as shown in Figure 18-9.

```cpp
#include <oneapi/dpl/algorithm>
#include <oneapi/dpl/execution>
#include <sycl/sycl.hpp>

int main() {
    sycl::queue q;
    const int n = 10;
    int* h_head = sycl::malloc_host<int>(n, q);
    int* d_head = sycl::malloc_device<int>(n, q);
    std::fill(oneapi::dpl::execution::make_device_policy(q),
            d_head, d_head + n, 78);
    q.wait();

    q.memcpy(h_head, d_head, n * sizeof(int));
    q.wait();

    if (h_head[8] == 78)
        std::cout << "passed" << std::endl;
    else
        std::cout << "failed" << std::endl;

    sycl::free(h_head, q);
    sycl::free(d_head, q);
    return 0;
}
```  
Figure 18-9. Using oneDPL with a USM pointer

Alternatively, we can use std::vector with a USM allocator as shown in Figure 18-10. With this approach, std::vector manages its own memory (as normal) but allocates any memory it needs via an internal call to sycl::malloc\_shared. The begin() and end() member functions then return iterators that step through a USM allocation. This style of programming is very convenient, especially when migrating existing C++ code that already makes use of containers and algorithms.

```cpp
#include <oneapi/dpl/algorithm>
#include <oneapi/dpl/execution>
#include <sycl/sycl.hpp>

int main() {
    sycl::queue q;
    const int n = 10;
    sycl::usm_allocator<int, sycl::usm::alloc::shared> alloc(
        q);
    std::vector<int, decltype(alloc)> vec(n, alloc);

    std::fill(oneapi::dpl::execution::make_device_policy(q),
            vec.begin(), vec.end(), 78);
    q.wait();

    return 0;
}
```  
Figure 18-10. Using oneDPL with a USM allocator

## Error Handling with SYCL Execution Policies

As detailed in Chapter 5, the SYCL error handling model supports two types of errors. With synchronous errors, the runtime throws exceptions, while asynchronous errors are only processed by an asynchronous error handler at specified times during program execution.

For algorithms executed with SYCL-aware execution policies, the handling of all errors (synchronous or asynchronous) is the responsibility of the caller. Specifically,

• No exceptions are thrown explicitly by algorithms.

Exceptions thrown by the runtime on the host CPU, including SYCL synchronous exceptions, are passed through to the caller.

SYCL asynchronous errors are not handled by oneDPL, so must be handled (if any handling is desired) by the caller using the usual SYCL asynchronous exception mechanisms.

## Summary

We should use libraries wherever possible in our heterogeneous applications, to avoid wasting time rewriting and testing common functions and parallel patterns. We should leverage the work of others rather than writing everything ourselves, and we should use that approach wherever practical to simplify application development and (often) to realize superior performance.

This chapter has briefly introduced three sets of library functionality that we think every SYCL developer should be familiar with:

1. The SYCL built-in functions, for common math operations

2. The standard C++ library, for other common operations

3. The C++17 parallel algorithms (supported by oneDPL), for complete kernels

With any library, it is important to understand which devices, compilers, and implementations are tested and supported before relying upon them in production. This is not SYCL-specific advice, but worth remembering—the number of potential targets for a portable programming solution like SYCL is huge, and it is our responsibility as programmers to identify which libraries are aligned with our goals.

![](images/52829c4a6095b4e6562b9b6f55629dd2b06544db953777569446568604fcdd5a.jpg)

cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
````
