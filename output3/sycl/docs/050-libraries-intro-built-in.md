
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
