
## Figure 13-9. Common pattern: buffer creation from a host allocation

There are two common reasons to associate a buffer with existing host memory like Figure 13-9:

1. To simplify initialization of data in a buffer. We can just construct the buffer from host memory that we (or another part of the application) have already initialized.

2. To reduce the characters typed because closing scope with a ‘}’ is slightly more concise (though more error prone) than creating a host\_accessor to the buffer.

If we use a host allocation to dump or verify the output values from a kernel, we need to put the buffer allocation into a block scope (or other scopes) so that we can control when it is destructed. We must then make sure that the buffer is destroyed before we access the host allocation to obtain the kernel output. Figure 13-9 shows this done correctly, while Figure 13-10 shows a common bug where the output is accessed while the buffer is still alive.

Advanced users may prefer to use buffer destruction to return result data from kernels into a host memory allocation. But for most users, and especially new developers, it is recommended to use scoped host accessors.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create host containers to initialize on the host
std::vector<int> in_vec(N), out_vec(N);

// Initialize input and output vectors
for (int i = 0; i < N; i++) in_vec[i] = i;
std::fill(out_vec.begin(), out_vec.end(), 0);

// Create buffers using host allocations (vector in this
// case)
buffer in_buf{in_vec}, out_buf{out_vec};

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

// BUG!!! We're using the host allocation out_vec, but the
// buffer out_buf is still alive and owns that allocation!
// We will probably see the initialiation value (zeros)
// printed out, since the kernel probably hasn't even run
// yet, and the buffer has no reason to have copied any
// output back to the host even if the kernel has run.
for (int i = 0; i < N; i++)
    std::cout << "out_vec[" << i << "]=" << out_vec[i]
        << "\n";
```

## Figure 13-10. Common bug: reading data directly from host allocation during buffer lifetime

To avoid these bugs, we recommend using host accessors instead of buffer scoping when getting started using C++ with SYCL. Host accessors provide access to a buffer from the host, and once their constructor has finished running, we are guaranteed that any previous writes (e.g., from kernels submitted before the host\_accessor was created) to the buffer have executed and are visible. This book uses a mixture of both styles (i.e., host accessors and host allocations passed to the buffer constructor) to provide familiarity with both. Using host accessors tends to be less error prone when getting started. Figure 13-11 shows how a host accessor can be used to read output from a kernel, without destroying the buffer first.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create host containers to initialize on the host
std::vector<int> in_vec(N), out_vec(N);

// Initialize input and output vectors
for (int i = 0; i < N; i++) in_vec[i] = i;
std::fill(out_vec.begin(), out_vec.end(), 0);

// Create buffers using host allocations (vector in this
// case)
buffer in_buf{in_vec}, out_buf{out_vec};

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

// Check that all outputs match expected value
// Use host accessor! Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
    std::cout << "A[" << i << "]=" << A[i] << "\n";

Figure 13-11. Recommendation: Use a host accessor to read
kernel results
```

Host accessors can be used whenever a buffer is alive, such as at both ends of a typical buffer lifetime—for initialization of the buffer content and for reading of results from our kernels. Figure 13-12 shows an example of this pattern.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create buffers of size N
buffer<int> in_buf{N}, out_buf{N};

// Use host accessors to initialize the data
{  // CRITICAL: Begin scope for host_accessor lifetime!
  host_accessor in_acc{in_buf}, out_acc{out_buf};
  for (int i = 0; i < N; i++) {
    in_acc[i] = i;
    out_acc[i] = 0;
  }
} // CRITICAL: Close scope to make host accessors go out
  // of scope!

// Submit the kernel to the queue
q.submit([&](handler& h) {
  accessor in{in_buf, h};
  accessor out{out_buf, h};

  h.parallel_for(range{N},
              =[=(id<1> idx) { out[idx] = in[idx]; });
});

// Check that all outputs match expected value
// Use host accessor!  Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
  std::cout << "A[" << i << "]=" << A[i] << "\n";

Figure 13-12. Recommendation: Use host accessors for buffer
initialization and reading of results
```

## Chapter 13 Practical Tips

One final detail to mention is that host accessors sometime cause an opposite bug in applications, because they also have a lifetime. While a host\_accessor to a buffer is alive, the runtime will not allow that buffer to be used by any devices! The runtime does not analyze our host programs to determine when they might access a host accessor, so the only way for it to know that the host program has finished accessing a buffer is for the host\_accessor destructor to run. As shown in Figure 13-13, this can cause applications to appear to hang if our host program is waiting for some kernels to run (e.g., queue::wait() or acquiring another host accessor) and if the SYCL runtime is waiting for our earlier host accessor(s) to be destroyed before it can run kernels that use a buffer.

When using host accessors, be sure that they are destroyed when no longer needed to unlock use of the buffer by kernels or other host accessors.

```cpp
constexpr size_t N = 1024;

// Set up queue on any available device
queue q;

// Create buffers using host allocations (vector in this
// case)
buffer<int> in_buf{N}, out_buf{N};

// Use host accessors to initialize the data
host_accessor in_acc{in_buf}, out_acc{out_buf};
for (int i = 0; i < N; i++) {
    in_acc[i] = i;
    out_acc[i] = 0;
}

// BUG: Host accessors in_acc and out_acc are still alive!
// Later q submits will never start on a device, because
// the runtime doesn't know that we've finished accessing
// the buffers via the host accessors. The device kernels
// can't launch until the host finishes updating the
// buffers, since the host gained access first (before the
// queue submissions). This program will appear to hang!
// Use a debugger in that case.

// Submit the kernel to the queue
q.submit([&](handler& h) {
    accessor in{in_buf, h};
    accessor out{out_buf, h};

    h.parallel_for(range{N},
            [=](id<1> idx) { out[idx] = in[idx]; });
});

std::cout << "This program will deadlock here!!! Our "
              "host_accessors used\n"
        << " for data initialization are still in "
              "scope, so the runtime won't\n"
        << " allow our kernel to start executing on "
              "the device (the host could\n"
        << " still be initializing the data that is "
              "used by the kernel). The next line\n"
        << " of code is acquiring a host accessor for "
              "the output, which will wait for\n"
        << " the kernel to run first. Since in_acc "
              "and out_acc have not been\n"
        << " destructed, the kernel is not safe for "
              "the runtime to run, and we deadlock.\n";

// Check that all outputs match expected value
// Use host accessor! Buffer is still in scope / alive
host_accessor A{out_buf};

for (int i = 0; i < N; i++)
    std::cout << "A[" << i << "]=" << A[i] << "\n";
```

## Figure 13-13. Deadlock (bug—it hangs!) from improper use of host\_ accessors

## Multiple Translation Units

When we want to call functions inside a kernel that are defined in a different translation unit, those functions need to be labeled with SYCL\_EXTERNAL. Without this decoration, the compiler will only compile a function for use outside of device code (making it illegal to call that external function from within device code).

There are a few restrictions on SYCL\_EXTERNAL functions that do not apply if we define the function within the same translation unit:

• SYCL\_EXTERNAL can only be used on functions.

• SYCL\_EXTERNAL functions cannot use raw pointers as parameter or return types. Explicit pointer classes must be used instead.

• SYCL\_EXTERNAL functions cannot call a parallel\_ for\_work\_item method.

• SYCL\_EXTERNAL functions cannot be called from within a parallel\_for\_work\_group scope.

If we try to compile a kernel that is calling a function that is not inside the same translation unit and is not declared with SYCL\_EXTERNAL, then we can expect a compile error similar to

error: SYCL kernel cannot call an undefined function without SYCL\_EXTERNAL attribute

If the function itself is compiled without a SYCL\_EXTERNAL attribute, we can expect to see either a link or runtime failure such as

terminate called after throwing an instance of '...compile\_ program\_error'...

error: undefined reference to ...

SYCL does not require compilers to support SYCL\_EXTERNAL; it is an optional feature in general. DPC++ supports SYCL\_EXTERNAL.

## Performance Implication of Multiple Translation Units

An implication of the compilation model (see earlier in this chapter) is that if we scatter our device code into multiple translation units, that may trigger more invocations of just-in-time compilation than if our device code is colocated. This is highly implementation-dependent and is subject to changes over time as implementations mature.

Such effects on performance are minor enough to ignore through most of our development work, but when we get to fine-tuning to maximize code performance, there are two things we can consider to mitigate these effects: (1) group device code together in the same translation unit, and (2) use ahead-of-time compilation to avoid just-in-time compilation effects entirely. Since both of these require some effort on our part, we only do this when we have finished our development and are trying to squeeze every ounce of performance out of our application. When we do resort to this detailed tuning, it is worth testing changes to observe their effect on the exact SYCL implementation that we are using.

## When Anonymous Lambdas Need Names

SYCL allows for assigning names to lambdas in case tools need it and for debugging purposes (e.g., to enable displays in terms of user-defined names). Naming lambdas is optional per the SYCL 2020 specification. Throughout most of this book, anonymous lambdas are used for kernels because names are not needed when using C++ with SYCL (except for passing of compile options as described with lambda naming discussion in Chapter 10).

When we have an advanced need to mix SYCL tools from multiple vendors in a codebase, the tooling may require that we name lambdas. This is done by adding a <class uniquename> to the SYCL action construct in which the lambda is used (e.g., parallel\_for). This naming allows tools from multiple vendors to interact in a defined way within a single compilation and can also help by displaying kernel names that we define within debug tools and layers.

We also need to name kernels if we want to use kernel queries. The SYCL standards committee was unable to find a solution to requiring this in the SYCL 2020 standard. For instance, querying a kernel’s preferred\_work\_group\_size\_multiple requires us to call the get\_info() member function of the kernel class, which requires an instance of the kernel class, which ultimately requires that we know the name (and kernel\_id) of the kernel in order to extract a handle to it from the relevant kernel\_bundle.

## Summary

Popular culture today often refers to tips as life hacks. Unfortunately, programming culture often assigns a negative connotation to hack, so the authors refrained from naming this chapter “SYCL Hacks.” Undoubtedly, this chapter has just touched the surface of what practical tips can be given for using C++ with SYCL. More tips can be shared by all of us as we learn together how to make the most out of C++ with SYCL.

![](images/5886d8b65391ce71bb7c94aa095bc22c514037b2f6a34fdce4623ad8a3fd3c49.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
