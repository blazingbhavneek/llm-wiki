# Add Devices to Multicast Objects

Devices can be added to a Multicast Team using the `cuMulticastAddDevice` function. This function takes the multicast handle and the device identifier as arguments.

```javascript
cuMulticastAddDevice(&mcHandle, device);
```

This step needs to be completed on all processes controlling devices that should participate in a Multicast Team before memory on any device is bound to the Multicast Object [CUDA_C_Programming_Guide:L15316-L15325].
