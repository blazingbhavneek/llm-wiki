## Configuring GPU Device

To extract the best end-to-end performance from applications, you may sometimes need to modify device settings at a system level. Depending on whether sudo access is required, a system administrator may need to apply these settings.

## GPU Drivers or Plug-ins (Optional)

You can develop oneAPI applications using C++ and SYCL\* that run on Intel, AMD\*, or NVIDIA\* GPUs.

To develop and run applications for specific GPUs, you must first install the corresponding drivers or plug-ins:

• To use an Intel GPU, install the latest Intel GPU drivers.

• To use an AMD GPU (Linux only):

• Read the oneAPI for AMD GPUs Guide from Codeplay.

• Download oneAPI for AMD GPUs.

• To use an NVIDIA GPU (Linux and Windows):

• Read the oneAPI for NVIDIA® GPUs Guide from Codeplay.

• Download oneAPI for NVIDIA® GPUs GPUs.

## Performance Impact of Pinning GPU Frequency

When applications use GPUs for large portions of their computations, we recommend that you pin the GPU at an optimal frequency. Some examples of these applications are High-Performance Computing workloads, which have computationally intensive portions in their algorithms offloaded to the device.

For applications that are memory bound, with kernels running for a very short time but spend more time in data exchanges, the effects of pinning the GPU to a higher frequency might be less pronounced or even detrimental.

The maximum fused GPU frequency, which is the theoretical hardware maximum frequency, can be obtained using sysfs handles, for example:

```txt
for (( i=1; i<$num_cards; i++ ))
do
    for (( j=0; j<$num_tiles; j++ ))
    do
        cat /sys/class/drm/card$i/gt/gt$j/rps_RP0_freq_mhz;
    done
done
```

You can also obtain the current maximum software frequency, which you can dynamically modify with rps\_max\_freq\_mhz:

```shell
for (( i=1; i<\$num_cards; i++ ))
do
    for (( j=0; j<\$num_tiles; j++ ))
    do
        cat /sys/class/drm/card\$i/gt/gt\$j/rps_max_freq_mhz;
    done
done
```

The default policy in the Linux\* kernel mode driver (i915) for server platforms is to set the frequency request range where: rps\_min\_freq\_mhz = rps\_max\_freq\_mhz = rps\_boost\_freq\_mhz = rps\_RP0\_freq\_mhz

You can set the frequency using sysfs handles provided by the DRM Linux kernel driver:

```shell
for (( i=1; i<\$num_cards; i++ ))
do
  for (( j=0; j<\$num_tiles; j++ ))
  do
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_min_freq_mhz;
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_max_freq_mhz;
    echo \$desired_freq > /sys/class/drm/card\$i/gt/gt\$j/rps_boost_freq_mhz;
  done
done
```

Notes regarding frequency pinning:

• Firmware is final arbiter on granted frequency.

• Some throttling may occur for thermal/power budget reasons.

• Once the frequency is pinned to a fixed value, there is no dynamic scaling. For server platforms, the current i915 policy pins frequency to rps\_max\_freq\_mhz at boot time.

## Switching Intel<sup>®</sup> X<sup>e</sup> Link On/Off

Intel<sup>®</sup> X<sup>e</sup> Link is a high-speed connectivity fabric hardware that provides accelerated data transfer capabilities for scale-up and scale-out operations. These are typically used for inter-GPU and inter-node data transfer operations for HPC applications deployed at cluster scale. However, for applications that do not use these capabilities, it could be beneficial to turn off the power to this resource to allow for lower frequency throttling on the GPU compute engines.

The following examples describe how to turn off power to Intel<sup>®</sup> X<sup>e</sup> Link:

```shell
modprobe -r iaf;
for i in {0..\$num_cards}; do
  cat /sys/class/drm/card$i/iaf_power_enable;
done;

for i in {0..\$num_cards}; do
  echo 0 > /sys/class/drm/card$i/iaf_power_enable;
```

```shell
done;

for i in {0..\$numcards}; do
  cat /sys/class/drm/card$i/iaf_power_enable;
done
```

\$num\_cards can be obtained by listing the /sys/class/drm/ directory and noting how many card\* subdirectories exist.

## Time Slice Considerations

The performance of workloads can vary depending on the amount of time slice given to each context. To control the time slice duration, you can use a parameter to allow fine-tuning of the time slice at a per-engine level. The released driver default is set to five ms. If a workload needs a higher time slice, configure the parameter accordingly. The following example sets the time slice to 50 ms on all engines and devices:

```txt
for i in /sys/class/drm/card*/engine/*/timeslice_duration_ms; do
    echo 50 >\$i;
done;
```

You must initiate this process any time the driver loads since the echo is not persistent across reboots. You can use udev scripts to run the process automatically.
