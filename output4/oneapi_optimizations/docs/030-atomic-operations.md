
Atomics allow multiple work-items for any cross work-item communication via memory. SYCL atomics are similar to C++ atomics and make the access to resources protected by atomics guaranteed to be executed as a single unit. The following factors affect the performance and legality of atomic operations

• Data types

• Local vs global address space

• Host, shared and device allocated USM

## Data Types in Atomic Operations

The following kernel shows the implementation of a reduction operation in SYCL where every work-item is updating a global accumulator atomically. The input data type of this addition and the vector on which this reduction operation is being applied is an integer. The performance of this kernel is reasonable compared to other techniques used for reduction, such as blocking.

```rust
q.submit([&](auto &h) {
    sycl::accessor buf_acc(buf, h, sycl::read_only);
    sycl::accessor sum_acc(sum_buf, h, sycl::write_only, sycl::no_init);

    h.parallel_for(data_size, [=](auto index) {
        size_t glob_id = index[0];
        auto v = sycl::atomic_ref<int, sycl::memory_order::relaxed,
                             sycl::memory_scope::device,
                             sycl::access::address_space::global_space>(
            sum_acc[0]);
        v.fetch_add(buf_acc[glob_id]);
    });
});
```

If the data type of the vector is a float or a double as shown in the kernel below, the performance on certain accelerators is impaired due to lack of hardware support for float or double atomics. The following two kernels demonstrate how the time to execute an atomic add can vary drastically based on whether native atomics are supported.

```cpp
//
int VectorInt(sycl::queue &q, int iter) {
  VectorAllocator<int> alloc;
  AlignedVector<int> a(array_size, alloc);
  AlignedVector<int> b(array_size, alloc);

  InitializeArray<int>(a);
  InitializeArray<int>(b);
  sycl::range num_items{a.size()};
  sycl::buffer a_buf(a);
  sycl::buffer b_buf(b);
  auto start = std::chrono::steady_clock::now();
  for (int i = 0; i < iter; i++) {
    q.submit([&](sycl::handler &h) {
      // InpuGt accessors
      sycl::accessor a_acc(a_buf, h, sycl::read_write);
      sycl::accessor b_acc(a_buf, h, sycl::read_only);

      h.parallel_for(num_items, [=](auto i) {
        auto v = sycl::atomic_ref<int, sycl::memory_order::relaxed,
                                    sycl::memory_scope::device,
                                    sycl::access::address_space::global_space>(
          a_acc[0]);
        v += b_acc[i];
      });
    });
```

```cpp
}
q.wait();
auto end = std::chrono::steady_clock::now();
std::cout << "Vector int completed on device - took " << (end - start).count()
        << " u-secs\n";
return ((end - start).count());
}
```

When using atomics, care must be taken to ensure that there is support in the hardware and that they can be executed efficiently. In Gen9 and Intel Iris X<sup>e</sup> integrated graphics, there is no support for atomics on float or double data types and the performance of VectorDouble will be very poor.

```cpp
//
int VectorDouble(sycl::queue &q, int iter) {
  VectorAllocator<double> alloc;
  AlignedVector<double> a(array_size, alloc);
  AlignedVector<double> b(array_size, alloc);

  InitializeArray<double>(a);
  InitializeArray<double>(b);
  sycl::range num_items{a.size()};
  sycl::buffer a_buf(a);
  sycl::buffer b_buf(b);

  auto start = std::chrono::steady_clock::now();
  for (int i = 0; i < iter; i++) {
    q.submit([&](sycl::handler &h) {
      // InpuGt accessors
      sycl::accessor a_acc(a_buf, h, sycl::read_write);
      sycl::accessor b_acc(a_buf, h, sycl::read_only);

      h.parallel_for(num_items, [=](auto i) {
        auto v = sycl::atomic_ref<double, sycl::memory_order::relaxed,
                               sycl::memory_scope::device,
                               sycl::access::address_space::global_space>(
          a_acc[0]);
        v += b_acc[i];
      });
    });
  }
  q.wait();
  auto end = std::chrono::steady_clock::now();
  std::cout << "Vector Double completed on device - took "
              << (end - start).count() << " u-secs\n";
  return ((end - start).count());
}
```

By analyzing these kernels using VTune Profiler, we can measure the impact of native atomic support. You can see that the VectorInt kernel is much faster than VectorDouble and VectorFloat.

VTune Dynamic Instruction

<table><tr><td colspan="5">Grouping: Source Computing Task / Function / Call Stack</td><td></td></tr><tr><td rowspan="2">Source Computing Task (GPU) / Function / Call Stack</td><td colspan="3">Computing Task</td><td>Data Tra...</td><td></td></tr><tr><td>Total Time ▼</td><td>Average Time</td><td>Instance Count</td><td>Size</td><td>Co</td></tr><tr><td>VectorDouble(cl::sycl::queue</td><td>741.734ms</td><td>74.173ms</td><td>10</td><td>0 B</td><td>66,783,2</td></tr><tr><td>VectorFloat(cl::sycl::queue&amp;</td><td>685.505ms</td><td>68.551ms</td><td>10</td><td>0 B</td><td>64,047,8</td></tr><tr><td>VectorInt(cl::sycl::queue&amp;, in</td><td>0.427ms</td><td>0.021ms</td><td>20</td><td>0 B</td><td></td></tr><tr><td>clEnqueueReadBuffer</td><td>0.076ms</td><td>0.019ms</td><td>4</td><td>640 KB</td><td></td></tr></table>

VTune<sup>TM</sup> Profiler dynamic instruction analysis allows us to see the instruction counts vary dramatically when there is no support for native atomics.

Here is the assembly code for our VectorInt kernel.

## VTune Atomic Integer

<table><tr><td>Addr... ▲</td><td>So...</td><td>Assembly</td><td></td></tr><tr><td>0</td><td></td><td>Block 1:</td><td></td></tr><tr><td>0</td><td>53</td><td>(W) mov (8|M0) r3.0&lt;1&gt;:ud r0.0&lt;1;1,0&gt;:ud</td><td></td></tr><tr><td>0x10</td><td>53</td><td>(W) or (1|M0) cr0.0&lt;1&gt;:ud cr0.0&lt;0;1,0&gt;:ud 0x4C0:uw {Swi</td><td></td></tr><tr><td>0x20</td><td></td><td>(W) mul (1|M0) r10.0&lt;1&gt;:d r11.0&lt;0;1,0&gt;:d r3.1&lt;0;1,0&gt;:d</td><td></td></tr><tr><td>0x28</td><td></td><td>(W) mov (16|M0) r11.0&lt;1&gt;:d 0:w</td><td></td></tr><tr><td>0x38</td><td></td><td>(W) shl (1|M0) r10.2&lt;1&gt;:d r9.6&lt;0;1,0&gt;:d 2:w</td><td></td></tr><tr><td>0x48</td><td></td><td>(W) mov (16|M16) r4.0&lt;1&gt;:d 0:w</td><td></td></tr><tr><td>0x58</td><td></td><td>(W) shl (1|M0) r10.1&lt;1&gt;:d r9.0&lt;0;1,0&gt;:d 2:w</td><td></td></tr><tr><td>0x68</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r10.0&lt;0;1,0&gt;:d r1.0&lt;16;16,1&gt;:uw</td><td></td></tr><tr><td>0x78</td><td></td><td>add (16|M16) r4.0&lt;1&gt;:d r10.0&lt;0;1,0&gt;:d r2.0&lt;16;16,1&gt;:uw</td><td></td></tr><tr><td>0x88</td><td></td><td>(W) add (1|M0) r10.0&lt;1&gt;:d r10.2&lt;0;1,0&gt;:d r10.5&lt;0;1,0&gt;:d</td><td></td></tr><tr><td>0x98</td><td></td><td>(W) mov (8|M0) r112.0&lt;1&gt;:ud r3.0&lt;8;8,1&gt;:ud {Compacted}</td><td></td></tr><tr><td>0xa0</td><td></td><td>(W) add (1|M0) r14.0&lt;1&gt;:d r10.1&lt;0;1,0&gt;:d r10.4&lt;0;1,0&gt;:d</td><td></td></tr><tr><td>0xb0</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r8.0&lt;8;8,1&gt;:d r7.0&lt;0;1,0&gt;:d {Comp</td><td></td></tr><tr><td>0xb8</td><td></td><td>add (16|M16) r4.0&lt;1&gt;:d r4.0&lt;8;8,1&gt;:d r7.0&lt;0;1,0&gt;:d</td><td></td></tr><tr><td>0xc8</td><td></td><td>shl (16|M0) r8.0&lt;1&gt;:d r8.0&lt;8;8,1&gt;:d 2:w</td><td></td></tr><tr><td>0xd8</td><td></td><td>shl (16|M16) r4.0&lt;1&gt;:d r4.0&lt;8;8,1&gt;:d 2:w</td><td></td></tr><tr><td>0xe8</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r10.0&lt;0;1,0&gt;:d r8.0&lt;8;8,1&gt;:d {Comp</td><td></td></tr><tr><td>0xf0</td><td></td><td>add (16|M16) r4.0&lt;1&gt;:d r10.0&lt;0;1,0&gt;:d r4.0&lt;8;8,1&gt;:d</td><td></td></tr><tr><td>0x100</td><td></td><td>send (16|M0) r6:w r8 0xC 0x04205E01 [Data Cache Data Po</td><td></td></tr><tr><td>0x110</td><td></td><td>send (16|M16) r4:w r4 0xC 0x04205E01 [Data Cache Data Po</td><td></td></tr><tr><td>0x120</td><td></td><td>mov (16|M0) r11.0&lt;1&gt;:d r6.0&lt;8;8,1&gt;:d {Compacted}</td><td></td></tr><tr><td>0x128</td><td></td><td>(W) add (16|M0) r4.0&lt;1&gt;:d r11.0&lt;8;8,1&gt;:d r4.0&lt;8;8,1&gt;:d</td><td></td></tr><tr><td>0x130</td><td></td><td>(W) add (8|M0) r2.0&lt;1&gt;:d r4.0&lt;8;8,1&gt;:d r5.0&lt;8;8,1&gt;:d {C</td><td></td></tr><tr><td>0x138</td><td></td><td>(W) add (4|M0) r2.0&lt;1&gt;:d r2.0&lt;4;4,1&gt;:d r2.4&lt;4;4,1&gt;:d {C</td><td></td></tr><tr><td>0x140</td><td></td><td>(W) add (2|M0) r2.0&lt;1&gt;:d r2.0&lt;2;2,1&gt;:d r2.2&lt;2;2,1&gt;:d</td><td></td></tr><tr><td>0x150</td><td></td><td>(W) add (1|M0) r2.0&lt;1&gt;:d r2.0&lt;0;1,0&gt;:d r2.1&lt;0;1,0&gt;:d {C</td><td></td></tr><tr><td>0x158</td><td></td><td>(W) sends (1|M0) null:ud r14 r2 0x4C 0x02009700 [Data C</td><td></td></tr><tr><td>0x168</td><td></td><td>(W) send (8|M0) null r112 0x27 0x02000010 {EOT} [Thread</td><td></td></tr></table>

Compared to the assembly code for VectorDouble, there are 33 million more GPU instructions required when we execute our VectorDouble kernel. VTune Atomic Double

<table><tr><td>Addr... ▲</td><td>Sour...</td><td>Assembly</td><td></td><td>GPU</td></tr><tr><td>0x50</td><td></td><td>(W) shl (1|M0) r6.0&lt;1&gt;:q r6.0&lt;0;1,0&gt;:q 3:w</td><td></td><td></td></tr><tr><td>0x60</td><td></td><td>mov (8|M8) r16.0&lt;1&gt;:q 0:w</td><td></td><td></td></tr><tr><td>0x70</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r8.0&lt;0;1,0&gt;:d r1.0&lt;16;16,1&gt;:uw</td><td></td><td></td></tr><tr><td>0x80</td><td></td><td>(W) add (1|M0) r6.2&lt;1&gt;:d r6.2&lt;0;1,0&gt;:d r7.4&lt;0;1,0&gt;:d</td><td></td><td></td></tr><tr><td>0x90</td><td></td><td>(W) add (1|M0) r26.0&lt;1&gt;:q r6.0&lt;0;1,0&gt;:q r5.0&lt;0;1,0&gt;:q</td><td></td><td></td></tr><tr><td>0xa0</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r8.0&lt;8;8,1&gt;:d r4.0&lt;0;1,0&gt;:d {Comp</td><td></td><td></td></tr><tr><td>0xa8</td><td></td><td>mov (8|M0) r10.0&lt;1&gt;:uq r26.0&lt;0;1,0&gt;:uq</td><td></td><td></td></tr><tr><td>0xb8</td><td></td><td>mov (8|M8) r12.0&lt;1&gt;:uq r26.0&lt;0;1,0&gt;:uq</td><td></td><td></td></tr><tr><td>0xc8</td><td></td><td>shl (16|M0) r8.0&lt;1&gt;:d r8.0&lt;8;8,1&gt;:d 3:w</td><td></td><td></td></tr><tr><td>0xd8</td><td></td><td>add (16|M0) r8.0&lt;1&gt;:d r6.2&lt;0;1,0&gt;:d r8.0&lt;8;8,1&gt;:d {Comp</td><td></td><td></td></tr><tr><td>0xe0</td><td></td><td>send (16|M0) r4:w r8 0xC 0x04405C01 [Data Cache Data Pc</td><td></td><td></td></tr><tr><td>0xf0</td><td></td><td>sends (8|M0) r8:ug r10 r14 0x8C 0x0424B2FF [Data Cache</td><td></td><td></td></tr><tr><td>0x100</td><td></td><td>sends (8|M8) r10:ug r12 r16 0x8C 0x0424B2FF [Data Cache</td><td></td><td></td></tr><tr><td>0x110</td><td></td><td>mov (8|M0) r23.0&lt;2&gt;:d r4.0&lt;8;8,1&gt;:d</td><td></td><td></td></tr><tr><td>0x120</td><td></td><td>mov (8|M8) r21.0&lt;2&gt;:d r5.0&lt;8;8,1&gt;:d</td><td></td><td></td></tr><tr><td>0x130</td><td></td><td>mov (8|M0) r23.1&lt;2&gt;:d r6.0&lt;8;8,1&gt;:d</td><td></td><td></td></tr><tr><td>0x140</td><td></td><td>mov (8|M8) r21.1&lt;2&gt;:d r7.0&lt;8;8,1&gt;:d</td><td></td><td></td></tr><tr><td>0x150</td><td></td><td>mov (8|M0) r19.0&lt;1&gt;:ug r8.0&lt;4;4,1&gt;:ug</td><td></td><td></td></tr><tr><td>0x160</td><td></td><td>mov (8|M8) r17.0&lt;1&gt;:ug r10.0&lt;4;4,1&gt;:ug</td><td></td><td></td></tr><tr><td>0x170</td><td></td><td>Block 2:</td><td></td><td></td></tr><tr><td>0x170</td><td></td><td>add (8|M0) r11.0&lt;1&gt;:df r23.0&lt;4;4,1&gt;:df r19.0&lt;4;4,1&gt;</td><td></td><td></td></tr><tr><td>0x180</td><td></td><td>mov (8|M0) r5.0&lt;1&gt;:ug r26.0&lt;0;1,0&gt;:ug</td><td></td><td></td></tr><tr><td>0x190</td><td></td><td>mov (8|M0) r9.0&lt;1&gt;:q r19.0&lt;4;4,1&gt;:q</td><td></td><td></td></tr><tr><td>0x1a0</td><td></td><td>add (8|M8) r15.0&lt;1&gt;:df r21.0&lt;4;4,1&gt;:df r17.0&lt;4;4,1&gt;</td><td></td><td></td></tr><tr><td>0x1b0</td><td></td><td>mov (8|M8) r7.0&lt;1&gt;:ug r26.0&lt;0;1,0&gt;:ug</td><td></td><td></td></tr><tr><td>0x1c0</td><td></td><td>mov (8|M8) r13.0&lt;1&gt;:q r17.0&lt;4;4,1&gt;:q</td><td></td><td></td></tr><tr><td>0x1d0</td><td></td><td>sends (8|M0) r3:ug r5 r9 0x10C 0x0424BEFF [Data Cac</td><td></td><td></td></tr><tr><td>0x1e0</td><td></td><td>sends (8|M8) r5:ug r7 r13 0x10C 0x0424BEFF [Data Ca</td><td></td><td></td></tr><tr><td>0x1f0</td><td></td><td>mov (8|M0) r7.0&lt;1&gt;:ug r3.0&lt;4;4,1&gt;:ug</td><td></td><td></td></tr><tr><td>0x200</td><td></td><td>mov (8|M8) r3.0&lt;1&gt;:ug r5.0&lt;4;4,1&gt;:ug</td><td></td><td></td></tr><tr><td>0x210</td><td></td><td>cmp (8|M0) (eq)f0.0 null&lt;1&gt;:q r7.0&lt;4;4,1&gt;:q r19.0&lt;4</td><td></td><td></td></tr><tr><td>0x220</td><td></td><td>cmp (8|M8) (eq)f0.0 null&lt;1&gt;:q r3.0&lt;4;4,1&gt;:q r17.0&lt;4</td><td></td><td></td></tr><tr><td>0x230</td><td></td><td>(f0.0) break (16|M0) bb_4 bb_4</td><td></td><td></td></tr><tr><td>0x240</td><td></td><td>Block 3:</td><td></td><td></td></tr><tr><td>0x240</td><td></td><td>mov (8|M0) r19.0&lt;1&gt;:q r7.0&lt;4;4,1&gt;:q</td><td></td><td></td></tr><tr><td>0x250</td><td></td><td>mov (8|M8) r17.0&lt;1&gt;:q r3.0&lt;4;4,1&gt;:q</td><td></td><td></td></tr><tr><td>0x260</td><td></td><td>Block 4:</td><td></td><td></td></tr><tr><td>0x260</td><td></td><td>while (16|M0) bb_2</td><td></td><td></td></tr><tr><td>0x270</td><td></td><td>Block 5:</td><td></td><td></td></tr><tr><td>0x270</td><td></td><td>(W) mov (8|M0) r112.0&lt;1&gt;:ud r2.0&lt;8;8,1&gt;:ud {Compacted}</td><td></td><td></td></tr><tr><td>0x278</td><td></td><td>(W) s VTune Profiler session timed out. All open results were closed and a new se</td><td></td><td></td></tr></table>

The Intel<sup>®</sup> Advisor tool has a recommendation pane that provides insights on how to improve the performance of GPU kernels.

Advisor Recommendation Pane

![](images/5d0a44c1510313b17c4d7dd3e6dc09deaa7f591a632f9a6899e02febb2a71253.jpg)

One of the recommendations that Intel<sup>®</sup> Advisor provides is “Inefficient atomics present”. When atomics are not natively supported in hardware, they are emulated. This can be detected and Intel<sup>®</sup> Advisor gives advice on possible solutions.

Advisor Inefficient Atomics

![](images/1801d9770c9d0137115f2912c155f59f21e6e70e0c85b3de3bcaab4b460b0522.jpg)
