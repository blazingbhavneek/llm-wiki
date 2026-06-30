# oneapi_optimizations Source Lines 5735-6337

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source oneapi_optimizations:L5735-L6337

Citation: [oneapi_optimizations:L5735-L6337]

````text
## Using Libraries for GPU Offload

Several libraries are available with Intel<sup>®</sup> oneAPI Toolkits that can simplify the programming process by providing specialized APIs for use in optimized applications. This section provides steps on using the libraries, including code samples, for application accelerations. Detailed information about each library, including the available APIs, is available in the main documentation for the specific library.

• Using Performance Libraries

• Using Standard Library Functions in SYCL Kernels

• Efficiently Implementing Fourier Correlation Using oneAPI Math Kernel Library (oneMKL)

Boost Matrix Multiplication Performance with Intel<sup>®</sup> X<sup>e</sup> Matrix Extensions

## Using Performance Libraries

This section discusses using efficient functions from libraries like oneAPI Math Kernel Library (oneMKL) or oneAPI Deep Neural Network Library (oneDNN) instead of hand-coded alternatives. Unless you’re an expert studying a particular mathematical operation, it’s usually a bad idea to write your own version of that operation. For example, matrix multiplication is a common, straightforward mathematical operation:

$$
C _ {m, n} = A _ {m, k} \times B _ {k, n} = \sum^ {k} A _ {m, k} \times B _ {k, n}
$$

It’s also easy to implement with just a few lines of code:

```c
// Multiply matrices A and B
for (m = 0; m < M; m++) {
    for (n = 0; n < N; n++) {
        C[m][n] = 0.0;
        for (k = 0; k < K; k++) {
            C[m][n] += A[m][k] * B[k][n];
        }
    }
} // End matrix multiplication
```

However, this naive implementation won’t give the best possible performance. Simple visual inspection of the inner loop shows non-contiguous memory access for matrix B. Cache reuse, and hence performance, will be poor.

It’s not difficult to port the naive algorithm to SYCL to offload the matrix multiplication kernel to an accelerator. The following code initializes the queue to submit work to the default device and allocates space for the matrices in unified shared memory (USM):

```cpp
// Initialize SYCL queue
sycl::queue Q(sycl::default_selector_v);
auto sycl_device = Q.get_device();
auto sycl_context = Q.get_context();
std::cout << "Running on: "
       << Q.get_device().get_info<sycl::info::device::name>() << std::endl;

// Allocate matrices A, B, and C in USM
auto A = sycl::malloc_shared<float *>(M, sycl_device, sycl_context);
for (m = 0; m < M; m++)
    A[m] = sycl::malloc_shared<float>(K, sycl_device, sycl_context);

auto B = sycl::malloc_shared<float *>(K, sycl_device, sycl_context);
for (k = 0; k < K; k++)
    B[k] = sycl::malloc_shared<float>(N, sycl_device, sycl_context);

auto C = sycl::malloc_shared<float *>(M, sycl_device, sycl_context);
for (m = 0; m < M; m++)
    C[m] = sycl::malloc_shared<float>(N, sycl_device, sycl_context);

// Initialize matrices A, B, and C
```

Data in USM can be moved between host and device memories by the SYCL runtime. Explicit buffering is not required. To offload the computation to the default accelerator, it is converted to a SYCL kernel and submitted to the queue:

```rust
// Offload matrix multiplication kernel
Q.parallel_for(sycl::range<2>{M, N}, [=](sycl::id<2> id) {
    unsigned int m = id[0];
    unsigned int n = id[1];

    float sum = 0.0;
    for (unsigned int k = 0; k < K; k++)
        sum += A[m][k] * B[k][n];

    C[m][n] = sum;
}).wait(); // End matrix multiplication
```

However, simply offloading such code to an accelerator is unlikely to restore performance. In fact, performance could get worse. Badly written code is still badly written whether it runs on the host or a device.

Common, computationally demanding operations like matrix multiplication are well-studied. Experts have devised a number of algorithms that give better performance than naive implementations of the basic mathematical formulas. They also use tuning techniques like cache blocking and loop unrolling to achieve performance regardless of the shapes of matrices A and B.

oneMKL provides an optimized general matrix multiplication function (oneapi::mkl::blas::gemm) that gives high performance on the host processor or a variety of accelerator devices. The matrices are allocated in USM as before, and passed to the gemm function along with the device queue, matrix dimensions, and various other options:

```txt
// Offload matrix multiplication
float alpha = 1.0, beta = 0.0;
oneapi::mkl::transpose transA = oneapi::mkl::transpose::nontrans;
oneapi::mkl::transpose transB = oneapi::mkl::transpose::nontrans;
```

```cpp
sycl::event gemm_done;
std::vector<sycl::event> gemm_dependencies;
gemm_done = oneapi::mkl::blas::gemm(Q, transA, transB, M, N, K, alpha, A, M,
                             B, K, beta, C, M, gemm_dependencies);
gemm_done.wait();
```

The library function is more versatile than the naive implementations and is expected to give better performance. For example, the library function can transpose one or both matrices before multiplication, if necessary. This illustrates the separation of concerns between application developers and tuning experts. The former should rely on the latter to encapsulate common computations in highly-optimized libraries. The oneAPI specification defines many libraries to help create accelerated applications, e.g.:

• oneMKL for math operations

• Intel<sup>®</sup> oneAPI Data Analytics Library (oneDAL) for data analytics and machine learning

• oneDNN for the development of deep learning frameworks

• Intel<sup>®</sup> Video Processing Library (Intel<sup>®</sup> VPL) for video processing

Check whether your required operation is already available in a oneAPI library before creating your own implementation of it.

## Using Standard Library Functions in SYCL Kernels

Some, but not all, standard C++ functions can be called inside SYCL kernels. See Chapter 18 (Libraries) of Data Parallel C++ for an overview of supported functions. A simple example is provided here to illustrate what happens when an unsupported function is called from a SYCL kernel. The following program generates a sequence of random numbers using the rand() function:

```cpp
#include <iostream>
#include <random>
#include <sycl/sycl.hpp>

constexpr int N = 5;

extern SYCL_EXTERNAL int rand(void);

int main(void) {
#if defined CPU
    sycl::queue Q(sycl::cpu_selector_v);
#elif defined GPU
    sycl::queue Q(sycl::gpu_selector_v);
#else
    sycl::queue Q(sycl::default_selector_v);
#endif

    std::cout << "Running on: "
        << Q.get_device().get_info<sycl::info::device::name>() << std::endl;

    // Attempt to use rand() inside a DPC++ kernel
    auto test1 = sycl::malloc_shared<float>(N, Q.get_device(), Q.get_context());

    srand((unsigned)time(NULL));
    Q.parallel_for(N, [=](auto idx) {
        test1[idx] = (float)rand() / (float)RAND_MAX;
    }).wait();

    // Show the random number sequence
    for (int i = 0; i < N; i++)
        std::cout << test1[i] << std::endl;
```

```txt
// Cleanup
    sycl::free(test1, Q.get_context());
}
```

The program can be compiled to execute the SYCL kernel on the CPU (i.e., cpu\_selector), or GPU (i.e., gpu\_selector) devices. It compiles without errors on the two devices, and runs correctly on the CPU, but fails when run on the GPU:

```txt
$ icpx -fsycl -DCPU -std=c++17 external_rand.cpp -o external_rand
$ ./external_rand
Running on: Intel(R) Xeon(R) E-2176G CPU @ 3.70GHz
0.141417
0.821271
0.898045
0.218854
0.304283

$ icpx -fsycl -DGPU -std=c++17 external_rand.cpp -o external_rand
$ ./external_rand
Running on: Intel(R) Graphics Gen9 [0x3e96]
terminate called after throwing an instance of 'cl::sycl::compile_program_error'
  what():  The program was built for 1 devices
Build program log for 'Intel(R) Graphics Gen9 [0x3e96]':

error: undefined reference to `rand()'

error: backend compiler failed build.
-11 (CL_BUILD_PROGRAM_FAILURE)
Aborted
```

The failure occurs during Just-In-Time (JIT) compilation because of an undefined reference to rand(). Even though this function is declared SYCL\_EXTERNAL, there’s no SYCL equivalent to the rand() function on the GPU device.

Fortunately, the SYCL library contains alternatives to many standard C++ functions, including those to generate random numbers. The following example shows equivalent functionality using the Intel<sup>®</sup> oneAPI DPC ++ Library (oneDPL) and the Intel<sup>®</sup> oneAPI Math Kernel Library (oneMKL):

```cpp
#include <iostream>
#include <oneapi/dpl/random>
#include <oneapi/mkl/rng.hpp>
#include <sycl/sycl.hpp>

int main(int argc, char **argv) {
  unsigned int N = (argc == 1) ? 20 : std::stoi(argv[1]);
  if (N < 20)
    N = 20;

  // Generate sequences of random numbers between [0.0, 1.0] using oneDPL and
  // oneMKL
  sycl::queue Q(sycl::gpu_selector_v);
  std::cout << "Running on: "
      << Q.get_device().get_info<sycl::info::device::name>() << std::endl;

  auto test1 = sycl::malloc_shared<float>(N, Q.get_device(), Q.get_context());
  auto test2 = sycl::malloc_shared<float>(N, Q.get_device(), Q.get_context());

  std::uint32_t seed = (unsigned)time(NULL); // Get RNG seed value

  // oneDPL random number generator on GPU device
```

```cpp
clock_t start_time = clock(); // Start timer

Q.parallel_for(N, [=](auto idx) {
    oneapi::dpl::minstd_rand rng_engine(seed, idx); // Initialize RNG engine
    oneapi::dpl::uniform_real_distribution<float>
        rng_distribution;                 // Set RNG distribution
    test1[idx] = rng_distribution(rng_engine); // Generate RNG sequence
}).wait();

clock_t end_time = clock(); // Stop timer
std::cout << "oneDPL took " << float(end_time - start_time) / CLOCKS_PER_SEC
       << " seconds to generate " << N
       << " uniformly distributed random numbers." << std::endl;

// oneMKL random number generator on GPU device
start_time = clock(); // Start timer

oneapi::mkl::rng::mcg31m1 engine(
    Q, seed); // Initialize RNG engine, set RNG distribution
oneapi::mkl::rng::uniform<float, oneapi::mkl::rng::uniform_method::standard>
    rng_distribution(0.0, 1.0);
oneapi::mkl::rng::generate(rng_distribution, engine, N, test2)
    .wait(); // Generate RNG sequence

end_time = clock(); // Stop timer
std::cout << "oneMKL took " << float(end_time - start_time) / CLOCKS_PER_SEC
       << " seconds to generate " << N
       << " uniformly distributed random numbers." << std::endl;

// Show first ten random numbers from each method
std::cout << std::endl
       << "oneDPL"
       << "\t"
       << "oneMKL" << std::endl;
for (int i = 0; i < 10; i++)
    std::cout << test1[i] << " " << test2[i] << std::endl;

// Show last ten random numbers from each method
std::cout << "..." << std::endl;
for (size_t i = N - 10; i < N; i++)
    std::cout << test1[i] << " " << test2[i] << std::endl;

// Cleanup
sycl::free(test1, Q.get_context());
sycl::free(test2, Q.get_context());
```

The necessary oneDPL and oneMKL functions are included in <oneapi/dpl/random> and <oneapi/mkl/ rng.hpp>, respectively. The oneDPL and oneMKL examples perform the same sequence of operations: get a random number seed from the clock, initialize a random number engine, select the desired random number distribution, then generate the random numbers. The oneDPL code performs device offload explicitly using a SYCL kernel. In the oneMKL code, the mkl::rng functions handle the device offload implicitly.

Efficiently Implementing Fourier Correlation Using oneAPI Math Kernel Library (oneMKL)

Now that straightforward use of oneMKL kernel functions has been covered, let’s look at a more complex mathematical operation: cross-correlation. Cross-correlation has many applications, e.g.: measuring the similarity of two 1D signals, finding the best translation to overlay similar images, volumetric medical image segmentation, etc.

Consider the following simple signals, represented as vectors of ones and zeros:

```txt
Signal 1:   0  0  0  0  0  1  1  0
Signal 2:   0  0  1  1  0  0  0  0
```

The signals are treated as circularly shifted versions of each other, so shifting the second signal three elements relative to the first signal will give the maximum correlation score of two:

```txt
Signal 1: 0 0 0 0 0 1 1 0
Signal 2:                 0 0 1 1 0 0 0 0

Correlation: (1 * 1) + (1 * 1) = 2
```

Shifts of two or four elements give a correlation score of one. Any other shift gives a correlation score of zero. This is computed as follows:

$$
\operatorname{corr} _ {\alpha} = \sum_ {i = 0} ^ {N - 1} \operatorname{sig1} _ {i} \times \operatorname{sig2} _ {i + \alpha}
$$

where $N$ is the number of elements in the signal vectors and is the shift of $s i g 2$ relative to $s i g 1$

Real signals contain more data (and noise) but the principle is the same whether you are aligning 1D signals, overlaying 2D images, or performing 3D volumetric image registration. The goal is to find the translation that maximizes correlation. However, the brute force summation shown above requires $N$ multiplications and

![](images/36b68a0fb13d17df563487af4fa724563dc6ae9f473aa8c4b95ec3f1f7c84ffb.jpg)

additions for every $N$ shifts. In 1D, 2D, and 3D, the problem is $O ( N ^ { 2 } )$ $O ( N ^ { 4 } )$ , respectively.

The Fourier correlation algorithm is a much more efficient way to perform this computation because it takes advantage of the $O ( N l o g N )$ of the Fourier transform:

```txt
corr = IDFT(DFT(sig1) * CONJG(DFT(sig2)))
```

where DFT is the discrete Fourier transform, IDFT is the inverse DFT, and CONJG is the complex conjugate. The Fourier correlation algorithm can be composed using oneMKL, which contains optimized forward and backward transforms and complex conjugate multiplication functions. Therefore, the entire computation can be performed on the accelerator device.

In many applications, only the final correlation result matters, so this is all that has to be transferred from the device back to the host.

In the following example, two artificial signals will be created on the device, transformed in-place, and then correlated. The host will retrieve the final result and report the optimal translation and correlation score. Conventional wisdom suggests that buffering would give the best performance because it provides explicit control over data movement between the host and the device.

To test this hypothesis, let’s generate two input signals:

```cpp
// Create buffers for signal data. This will only be used on the device.
sycl::buffer<float> sig1_buf{N + 2};
sycl::buffer<float> sig2_buf{N + 2};

// Declare container to hold the correlation result (computed on the device,
// used on the host)
std::vector<float> corr(N + 2);
```

Random noise is often added to signals to prevent overfitting during neural network training, to add visual effects to images, or to improve the detectability of signals obtained from suboptimal detectors, etc. The buffers are initialized with random noise using a simple random number generator in oneMKL:

```cpp
// Open new scope to trigger update of correlation result
{
    sycl::buffer<float> corr_buf(corr);

    // Initialize the input signals with artificial data
    std::uint32_t seed = (unsigned)time(NULL); // Get RNG seed value
    oneapi::mkl::rng::mcg31m1 engine(Q, seed); // Initialize RNG engine
                                      // Set RNG distribution
    oneapi::mkl::rng::uniform<float, oneapi::mkl::rng::uniform_method::standard>
        rng_distribution(-0.00005, 0.00005);

    oneapi::mkl::rng::generate(rng_distribution, engine, N, sig1_buf); // Noise
    oneapi::mkl::rng::generate(rng_distribution, engine, N, sig2_buf);
```

Notice that a new scope is opened and a buffer, corr\_buf, is declared for the correlation result. When this buffer goes out of scope, corr will be updated on the host.

An artificial signal is placed at opposite ends of each buffer, similar to the trivial example above:

```cpp
Q.submit([&](sycl::handler &h) {
  sycl::accessor sig1_acc{sig1_buf, h, sycl::write_only};
  sycl::accessor sig2_acc{sig2_buf, h, sycl::write_only};
  h.single_task<>([=]() {
    sig1_acc[N - N / 4 - 1] = 1.0;
    sig1_acc[N - N / 4] = 1.0;
    sig1_acc[N - N / 4 + 1] = 1.0; // Signal
    sig2_acc[N / 4 - 1] = 1.0;
    sig2_acc[N / 4] = 1.0;
    sig2_acc[N / 4 + 1] = 1.0;
  });
}); // End signal initialization
```

Now that the signals are ready, let’s transform them using the DFT functions in oneMKL:

```c
// Initialize FFT descriptor
oneapi::mkl::dft::descriptor<oneapi::mkl::dft::precision::SINGLE,
        oneapi::mkl::dft::domain::REAL>
    transform_plan(N);
transform_plan.commit(Q);

// Perform forward transforms on real arrays
oneapi::mkl::dft::compute_forward(transform_plan, sig1_buf);
oneapi::mkl::dft::compute_forward(transform_plan, sig2_buf);
```

A single-precision, real-to-complex forward transform is committed to the SYCL queue, then an in-place DFT is performed on the data in both buffers. The result of must now be multiplied by . This could be done with a hand-coded kernel:

```cpp
Q.submit([&](sycl::handler &h)
{
    sycl::accessor sig1_acc{sig1_buf, h, sycl::read_only};
    sycl::accessor sig2_acc{sig2_buf, h, sycl::read_only};
    sycl::accessor corr_acc{corr_buf, h, sycl::write_only};

    h.parallel_for<>(sycl::range<1>{N/2}, [=](auto idx)
    {
        corr_acc[idx*2+0] = sig1_acc[idx*2+0] * sig2_acc[idx*2+0] +
                      sig1_acc[idx*2+1] * sig2_acc[idx*2+1];
        corr_acc[idx*2+1] = sig1_acc[idx*2+1] * sig2_acc[idx*2+0] -
                      sig1_acc[idx*2+0] * sig2_acc[idx*2+1];
    });
});
```

However, this basic implementation is unlikely to give optimal cross-architecture performance. Fortunately, the oneMKL function, oneapi::mkl::vm::mulbyconj, can be used for this step. The mulbyconj function expects std::complex<float> input, but the buffers were initialized as the float data type. Even though they contain complex data after the forward transform, the buffers will have to be recast:

```rust
auto sig1_buf_cplx =
    sig1_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
auto sig2_buf_cplx =
    sig2_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
auto corr_buf_cplx =
    corr_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
oneapi::mkl::vm::mulbyconj(Q, N / 2, sig1_buf_cplx, sig2_buf_cplx,
                    corr_buf_cplx);
```

The IDFT step completes the computation:

```txt
// Perform backward transform on complex correlation array
oneapi::mkl::dft::compute_backward(transform_plan, corr_buf);
```

When the scope that was opened at the start of this example is closed, the buffer holding the correlation result goes out of scope, forcing an update of the host container. This is the only data transfer between the host and the device.

The complete Fourier correlation implementation using explicit buffering is included below:

```cpp
#include <iostream>
#include <mkl.h>
#include <oneapi/mkl/dft.hpp>
#include <oneapi/mkl/rng.hpp>
#include <oneapi/mkl/vm.hpp>
#include <sycl/sycl.hpp>

int main(int argc, char **argv) {
  unsigned int N = (argc == 1) ? 32 : std::stoi(argv[1]);
  if ((N % 2) != 0)
    N++;
  if (N < 32)
    N = 32;

  // Initialize SYCL queue
  sycl::queue Q(sycl::default_selector_v);
  std::cout << "Running on: "
```

```cpp
<< Q.get_device().get_info<sycl::info::device::name>() << std::endl;
// Create buffers for signal data. This will only be used on the device.
sycl::buffer<float> sig1_buf{N + 2};
sycl::buffer<float> sig2_buf{N + 2};

// Declare container to hold the correlation result (computed on the device,
// used on the host)
std::vector<float> corr(N + 2);

// Open new scope to trigger update of correlation result
{
    sycl::buffer<float> corr_buf(corr);

    // Initialize the input signals with artificial data
    std::uint32_t seed = (unsigned)time(NULL); // Get RNG seed value
    oneapi::mkl::rng::mcg31m1 engine(Q, seed); // Initialize RNG engine
                                      // Set RNG distribution
    oneapi::mkl::rng::uniform<float, oneapi::mkl::rng::uniform_method::standard>
        rng_distribution(-0.00005, 0.00005);

    oneapi::mkl::rng::generate(rng_distribution, engine, N, sig1_buf); // Noise
    oneapi::mkl::rng::generate(rng_distribution, engine, N, sig2_buf);

    Q.submit([&](sycl::handler &h) {
        sycl::accessor sig1_acc{sig1_buf, h, sycl::write_only};
        sycl::accessor sig2_acc{sig2_buf, h, sycl::write_only};
        h.single_task<>(=]() {
            sig1_acc[N - N / 4 - 1] = 1.0;
            sig1_acc[N - N / 4] = 1.0;
            sig1_acc[N - N / 4 + 1] = 1.0; // Signal
            sig2_acc[N / 4 - 1] = 1.0;
            sig2_acc[N / 4] = 1.0;
            sig2_acc[N / 4 + 1] = 1.0;
        });
    }); // End signal initialization

    clock_t start_time = clock(); // Start timer

    // Initialize FFT descriptor
    oneapi::mkl::dft::descriptor<oneapi::mkl::dft::precision::SINGLE,
                             oneapi::mkl::dft::domain::REAL>
        transform_plan(N);
    transform_plan.commit(Q);

    // Perform forward transforms on real arrays
    oneapi::mkl::dft::compute_forward(transform_plan, sig1_buf);
    oneapi::mkl::dft::compute_forward(transform_plan, sig2_buf);

    // Compute: DFT(sig1) * CONJG(DFT(sig2))
    auto sig1_buf_cplx =
        sig1_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
    auto sig2_buf_cplx =
        sig2_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
    auto corr_buf_cplx =
        corr_buf.template reinterpret<std::complex<float>, 1>|((N + 2) / 2);
    oneapi::mkl::vm::mulbyconj(Q, N / 2, sig1_buf_cplx, sig2_buf_cplx,
                            corr_buf_cplx);
```

```cpp
// Perform backward transform on complex correlation array
oneapi::mkl::dft::compute_backward(transform_plan, corr_buf);

clock_t end_time = clock(); // Stop timer
std::cout << "The 1D correlation (N = " << N << ") took "
       << float(end_time - start_time) / CLOCKS_PER_SEC << " seconds."
       << std::endl;

} // Buffer holding correlation result is now out of scope, forcing update of
// host container

// Find the shift that gives maximum correlation value
float max_corr = 0.0;
int shift = 0;
for (unsigned int idx = 0; idx < N; idx++) {
    if (corr[idx] > max_corr) {
        max_corr = corr[idx];
        shift = idx;
    }
}
int _N = static_cast<int>(N);
shift =
    (shift > _N / 2) ? shift - _N : shift; // Treat the signals as circularly
                                      // shifted versions of each other.
std::cout << "Shift the second signal " << shift
       << " elements relative to the first signal to get a maximum, "
       "normalized correlation score of "
       << max_corr / N << "." << std::endl;
```

The Fourier correlation algorithm will now be reimplemented using Unified Shared Memory (USM) to compare to explicit buffering. Only the differences in the two implementations will be highlighted. First, the signal and correlation arrays are allocated in USM, then initialized with artificial data:

```c
// Initialize signal and correlation arrays
auto sig1 = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);
auto sig2 = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);
auto corr = sycl::malloc_shared<float>(N + 2, sycl_device, sycl_context);

// Initialize input signals with artificial data
std::uint32_t seed = (unsigned)time(NULL); // Get RNG seed value
oneapi::mkl::rng::mcg31m1 engine(Q, seed); // Initialize RNG engine
// Set RNG distribution
oneapi::mkl::rng::uniform<float, oneapi::mkl::rng::uniform_method::standard>
rng_distribution(-0.00005, 0.00005);

// Warning: These statements run on the device.
auto evt1 =
oneapi::mkl::rng::generate(rng_distribution, engine, N, sig1); // Noise
auto evt2 = oneapi::mkl::rng::generate(rng_distribution, engine, N, sig2);
evt1.wait();
evt2.wait();

// Warning: These statements run on the host, so sig1 and sig2 will have to be
// updated on the device.
sig1[N - N / 4 - 1] = 1.0;
sig1[N - N / 4] = 1.0;
sig1[N - N / 4 + 1] = 1.0; // Signal
```

```javascript
sig2[N / 4 - 1] = 1.0;
sig2[N / 4] = 1.0;
sig2[N / 4 + 1] = 1.0;
```

The rest of the implementation is largely the same except that pointers to USM are passed to the oneMKL functions instead of SYCL buffers:

```txt
// Perform forward transforms on real arrays
evt1 = oneapi::mkl::dft::compute_forward(transform_plan, sig1);
evt2 = oneapi::mkl::dft::compute_forward(transform_plan, sig2);

// Compute: DFT(sig1) * CONJG(DFT(sig2))
oneapi::mkl::vm::mulbyconj(
    Q, N / 2, reinterpret_cast<std::complex<float> *>(sig1),
    reinterpret_cast<std::complex<float> *>(sig2),
    reinterpret_cast<std::complex<float> *>(corr), {evt1, evt2})
    .wait();

// Perform backward transform on complex correlation array
oneapi::mkl::dft::compute_backward(transform_plan, corr).wait();
```

It is also necessary to free the allocated memory:

```txt
sycl::free(sig1, sycl_context);
sycl::free(sig2, sycl_context);
sycl::free(corr, sycl_context);
```

The USM implementation has a more familiar syntax. It is also conceptually simpler because it relies on implicit data transfer handled by the SYCL runtime. However, a programmer error hurts performance.

Notice the warning messages in the previous code snippets. The oneMKL random number generation engine is initialized on the device, so sig1 and sig2 are initialized with random noise on the device. Unfortunately, the code adding the artificial signal runs on the host, so the SYCL runtime has to make the host and device data consistent. The signals used in Fourier correlation are usually large, especially in 3D imaging applications, so unnecessary data transfer degrades performance.

Updating the signal data directly on the device keeps the data consistent, thereby avoiding the unnecessary data transfer:

```txt
Q.single_task<>([=]() {
    sig1[N - N / 4 - 1] = 1.0;
    sig1[N - N / 4] = 1.0;
    sig1[N - N / 4 + 1] = 1.0; // Signal
    sig2[N / 4 - 1] = 1.0;
    sig2[N / 4] = 1.0;
    sig2[N / 4 + 1] = 1.0;
}).wait();
```

The explicit buffering and USM implementations now have equivalent performance, indicating that the SYCL runtime is good at avoiding unnecessary data transfers (provided the programmer pays attention to data consistency).
````
