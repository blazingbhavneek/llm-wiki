```txt
simd<int, 8> hue, tmp;
simd_mask<8> vmask;
simd<unsigned short, 8> maxChannel, minChannel;
...
```

```javascript
// R>B>G
vmask = ((maxChannel == RED) & (minChannel == GREEN));
tmp = adjustHue(436906);
hue.merge(tmp, vmask);
// B>R>G
vmask = ((maxChannel == BLUE) & (minChannel == GREEN));
tmp = adjustHue(349525);
hue.merge(tmp, vmask);
```

Since the simd\_mask evaluation involves a common condition, the code can be refactored and rewritten as follows:

```txt
simd<int, 8> hue, tmp;
simd_mask<8> vmask;
simd<unsigned short, 8> maxChannel, minChannel;
...
vmask = (minChannel == GREEN);
if (vmask.any()) {
    // R>B>G
    tmp = adjustHue(436906);
    hue.merge(tmp, (maxChannel == RED) & vmask);
    //B>R>G
    tmp = adjustHue(349525);
    hue.merge(tmp, (maxChannel == BLUE) & vmask);
}
```

The advantage of this approach is that when input data contains few pixels with minimal green channel, vmask.any() will evaluate to false for most threads and allow them to exit early, therefore increasing performance and saving power.

## Math Functions

For compute-intensive applications, utilizing fast math instructions when applicable can enhance performance significantly. X<sup>e</sup> GPU Architecture provides native hardware support for common math instructions. During code generation, compiler has the capability to perform pattern matching to produce native math instructions, but it’s not always guaranteed. When programmers want to have explicit control of which native math intrinsic functions should be invoked for the specific code, they can use the math function APIs provided in ESIMD. Note that the precision of such math functions is limited to the accuracy provided by hardware implementation and may not match the standard SYCL specification. It is at the programmer’s discretion to choose the right intrinsic function to match the result precision requirement.

For example, to perform an arbitrary combination of Boolean operations for three variables, the ESIMD programmer can use the bfn API as illustrated in the following kernel:

```matlab
constexpr bfn_t F = ~bfn_t::x | bfn_t::y ^ bfn_t::z;
...
simd<unsigned int, 16> va;
simd<unsigned int, 16> vb;
simd<unsigned int, 16> vc;
simd<unsigned int, 16> vd;
...
vd = bfn<F>(va, vb, vc);
```

This will be mapped to a single three-source bfn instruction to perform the Boolean expression “\~s0| s1^s2”, instead of separate Boolean logic instructions:

```txt
bfn.(~s0|s1^s2) (16|M0) r4.0<1>:ud r1.0<1;0>:ud r3.0<1;0>:ud r2.0<1>:ud
```

Another useful feature is the reduction function. For a given simd object, the compiler produces the optimal code sequence on the target device to apply the specified operation to all scalar elements. Note that the order of element-wise operations is not guaranteed, and the result correctness should not depend on a particular computation order. An example to compute the sum of all scalar elements in a simd vector is shown below:

```rust
simd<unsigned int, 64> va;
int sum;
...
sum = reduce<int>(va, std::plus<>());
```

For a complete list of math APIs available in ESIMD, please refer to:

DPC++ Runtime: ESIMD math operations. (intel.github.io)

## Memory Functions

ESIMD provides a rich set of APIs to support various memory access functions. Some of these APIs are defined at high level and have more portable interface for common GPU device targets. For instance, the following code shows how to use the copy\_from() / copy\_to() method to read data from memory to a simd object or write the value to memory. In this case, the compiler will determine the memory access message type based on the access pattern and runtime target:

```txt
// Src and Dst are USM pointers defined in the host code
simd<unsigned int, 32> va;
va.copy_from(Src + offset);
va.copy_to(Dst + offset);
```

Other APIs are defined at lower level and more closely resemble the underlying X<sup>e</sup> GPU memory system operations. This enables programmers to have full control of the message types and attributes for performance tuning purposes. One of the most useful features is the block load/store function. Depending on input dimension, ESIMD supports both 1D and 2D block messages. For example, the following code shows how to perform a 2D block load/store from/to the global memory:

```c
constexpr uint32_t width = SurfaceWidth * sizeof(float) - 1;
constexpr uint32_t height = SurfaceHeight - 1;
constexpr uint32_t pitch = SurfacePitch * sizeof(float) - 1;
config_2d_mem_access<int, BlockWidth, BlockHeight, NumBlocks>
    payload(input, width, height, pitch, x, y);
auto data = lsc_load_2d(payload);
...
payload.set_data_pointer(output);
lsc_store_2d(payload, data);
```

Line 1-3 computes the width, height, and pitch of the 2D block stored in memory. Line 4 is a convenience API used to create the 2D block message payload, which contains the block width, height, pitch as well as x and y coordinates. The benefit of refactoring this out is to avoid the redundant payload fields setting, since some of these fields, such as width and pitch, are rarely changed and can be shared across multiple messages. Line 5 performs the 2D block load, which will save the returned data in GRF for subsequent Vector Engine computation. Line 6 updates the output memory address in payload setting. Line 7 performs the 2D block store to write back the GRF values to memory.

Compared with alternative SYCL implementation with default per-lane gather/scatter operation, explicit programming of block load/store in ESIMD has a couple of advantages. First, the block memory operation is more efficient since it accesses consecutive memory locations and facilitates data coalescing. Second, the maximum GRF return size allowed for the 2D block message is larger than the scattered message. This reduces the total number of messages required to load the same amount of data, therefore avoiding potential stalls due to contention in the message queue and memory arbiter. Third, the message payload size is smaller, which reduces GRF pressure as well as load-store unit bus traffic. This is because the block

message payload only contains two scalars for the starting x and y coordinates for the whole block, while scattered message payload must specify the staring coordinates for each lane respectively. Fourth, it saves additional instructions required to compute the addresses per-lane, which can be quite expensive especially with 64-bit addresses.

Furthermore, by loading the data into GRF block directly with the expected layout, better SIMD computation throughput can be achieved, which can be seen from the linear filter kernel example described in the previous section. 2D block message is commonly used to load input matrix data for Dot-Product-Accumulate-Systolic (DPAS) operation to achieve peak performance for GEMM kernel implementation, which is critical for machine learning workloads. For popular data types such as FP16 and INT8, DPAS expects matrix B to be laid out in GRF in Vector Neural Network Instructions (VNNI) format. This can be achieved conveniently by specifying the transform mode in 2D block message. If the data is loaded by scattered messages per-lane, since the return data is written to separate GRF block for each lane, it will require substantially more instructions to shuffle the data in place, degrading the performance.

To help hide memory access latency, ESIMD also provides APIs for programmers to explicit insert prefetch to bring data closer in memory system hierarchy. The following code shows how to add a prefetch for 2D block load. It’s often inserted at a distance to allow sufficient other useful work to be done in-between or performed cross loop iterations:

```txt
constexpr uint32_t width = SurfaceWidth * sizeof(float) - 1;
constexpr uint32_t height = SurfaceHeight - 1;
constexpr uint32_t pitch = SurfacePitch * sizeof(float) - 1;
config_2d_mem_access<int, BlockWidth, BlockHeight, NumBlocks>
    payload(input, width, height, pitch, x, y);
lsc_prefetch_2d(payload);
...
auto data = lsc_load_2d(payload);
```

Another useful feature is to add cache hints to indicate if the data should be cached, uncached, streamed, or follow other cache control policies. ESIMD fully exposes the underlying hardware message options to allow programmers to set the preferred cache control policy at different cache levels. The following code shows how to add cache hints to the 2D block prefetch and load from the previous example. The last two template parameters are added to specify that the data should be cached in both L1 and L2 caches:

```cpp
constexpr uint32_t width = SurfaceWidth * sizeof(float) - 1;
constexpr uint32_t height = SurfaceHeight - 1;
constexpr uint32_t pitch = SurfacePitch * sizeof(float) - 1;
config_2d_mem_access<int, BlockWidth, BlockHeight, NumBlocks>
    payload(input, width, height, pitch, x, y);
lsc_prefetch_2d<int, BlockWidth, BlockHeight, NumBlocks, false,
    false, cache_hint::cached, cache_hint::cached>(payload);
...
auto data = lsc_load_2d<int, BlockWidth, BlockHeight, NumBlocks, false,
    false, cache_hint::cached, cache_hint::cached> (payload);
```

The X<sup>e</sup> GPU memory system provides efficient support for access to various address spaces. Due to differences in address mode, size restriction, and other message encoding discrepancies, the compiler needs to generate different types of messages for different address spaces. In general, the compiler tries to infer the address space statically in order to determine which message type should be generated for a specific memory operation. However, there are cases where it’s not always possible to derive the address space at compile time, for example when a generic pointer is used in control flow or function call. In such case, the compiler will fall back to generate branchy code, which essentially performs dynamic checks at runtime to determine the address space and then executes the right path. This increases the code size and may result in substantial degradation in performance. To prevent this problem, ESIMD programmers can add explicit address space cast to help the compiler make the right code generation choice. The following code shows how to add an address space cast in ESIMD function:

```txt
1: simd<float, 16> test(float *A, simd<float, 16> b, int i)
    SYCL_ESIMD_FUNCTION {
2:     simd<float, 16> a;
3:     global_ptr<float, access::decorated::yes> ptr =
        sycl::address_space_cast<access::address_space::global_space,
        access::decorated::yes, float>(A);
4:     a.copy_from(ptr + i);
5:     return a + b;
6: }
```

At line 1, the function parameter A is declared as a generic pointer. The actual address space depends on the calling context and may not be determined at compile time. Line 3 adds the address space cast to indicate that the data pointed to by A is located in the global address space, so that the compiler will be able to generate global memory access message based on this information.

For a complete list of memory APIs available in ESIMD, please refer to:

DPC++ Runtime: Memory access API. (intel.github.io)
