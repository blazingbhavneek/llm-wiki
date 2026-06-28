## Troubleshooting SLM Errors

A PI\_ERROR\_OUT\_OF\_RESOURCES error may occur when a kernel uses more shared local memory than the amount available on the hardware. When this occurs, you will see an error message similar to this:

```txt
$ ./myapp
:
terminate called after throwing an instance of 'sycl::_V1::runtime_error'
what(): Native API failed. Native API returns: -5
(PI_ERROR_OUT_OF_RESOURCES) -5 (PI_ERROR_OUT_OF_RESOURCES)
Aborted (core dumped)
$
```

To see how much memory was being requested and the actual hardware limit, set debug keys:

```typescript
export PrintDebugMessages=1
export NEOReadDebugKeys=1
```

This will change the output to:

```txt
$ ./myapp
:
Size of SLM (656384) larger than available (131072)
terminate called after throwing an instance of 'sycl::_V1::runtime_error'
what(): Native API failed. Native API returns: -5
(PI_ERROR_OUT_OF_RESOURCES) -5 (PI_ERROR_OUT_OF_RESOURCES)
Aborted (core dumped)
$
```
