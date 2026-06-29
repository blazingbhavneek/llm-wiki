# 18.5.3. Qualifiers

Part of [Cuda C Programming Guide Reference](README.md). Source lines L16640-L17266.

- [Device Memory Space Specifiers](../../../concepts/device-memory-space-specifiers.md) — Restrictions on using __device__, __shared__, __managed__, and __constant__ specifiers on class members, parameters, and variable declarations, including rules for empty constructors/destructors and extern linkage in different compilation modes.
- [__managed__ Memory Space Specifier](../../../concepts/managed-memory-space.md) — The __managed__ memory space specifier allows variables to be accessed by both host and device code, subjecting them to specific restrictions regarding constancy, references, initialization contexts, and multi-GPU allocation.
- [Volatile Qualifier](../../../concepts/volatile-qualifier.md) — In CUDA C++, the volatile keyword is supported for ISO C++ compatibility but is unsuitable for inter-thread synchronization or MMIO because it does not guarantee atomicity, memory ordering, or deterministic instruction counts.
- [Pointers](../../../concepts/pointers.md) — Rules regarding pointer dereferencing across host/device boundaries and usage of addresses obtained from __device__, __shared__, or __constant__ variables.
- [Operators](../../../concepts/operators.md) — Restrictions on assignment and address operators for __constant__, __shared__, and built-in variables.
- [Run Time Type Information (RTTI)](../../../concepts/rtti.md) — Run Time Type Information (RTTI) features such as typeid, std::type_info, and dynamic_cast are supported in host code but are not available in device code within CUDA.
- [Exception Handling](../../../concepts/exception-handling.md) — Exception handling is supported in host code but not in device code, and exception specifications are not supported for __global__ functions.
- [Standard Library](../../../concepts/standard-library.md) — Standard libraries are only supported in host code, but not in device code, unless specified otherwise.
- [Namespace Reservations](../../../concepts/namespace-reservations.md) — It is undefined behavior to add declarations or definitions to the cuda::, nv::, or cooperative_groups:: namespaces or any namespaces nested within them.
- [External Linkage](../../../concepts/external-linkage.md) — Rules for calling functions declared with extern qualifier from device code, requiring definition in the same compilation unit.
- [Implicitly-declared and non-virtual explicitly-defaulted functions](../../../concepts/implicit-functions.md) — Rules for determining execution space specifiers (__host__, __device__) for implicitly-declared or explicitly-defaulted functions based on callers and overridden virtual functions.
- [Function Parameters](../../../concepts/function-parameters.md) — Restrictions on __global__ function parameters regarding size limits, varargs, and pass-by-reference, along with ODR-use requirements for separate compilation.
- [__global__ Function Argument Processing](../../../concepts/global-function-argument-processing.md) — Details on how arguments are passed to __global__ functions, including memcpy vs copy constructor, and destructor timing issues due to asynchronous execution.
- [Toolkit and Driver Compatibility](../../../concepts/toolkit-driver-compatibility.md) — CUDA 12.1 Toolkit and r530 driver or higher are required to support kernel parameters larger than 4KB.
- [Link Compatibility across Toolkit Revisions](../../../concepts/link-compatibility.md) — When linking device objects, if at least one object contains a kernel with a parameter larger than 4KB, all objects must be recompiled with the 12.1 toolkit or higher to avoid linker errors.
- [Static Variables within Function](../../../concepts/static-variables.md) — Rules governing the declaration, memory space specifiers, and initialization restrictions for static variables declared within function scope in CUDA.
- [Function Pointers](../../../concepts/function-pointers.md) — Restrictions on taking the address of __global__ or __device__ functions and using them across host/device boundaries.
- [Function Recursion](../../../concepts/function-recursion.md) — __global__ functions in CUDA do not support recursion.
- [Friend Functions](../../../concepts/friend-functions.md) — Restrictions on defining __global__ functions or function templates in friend declarations.
