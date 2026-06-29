# DPX (Data Parallel eXtensions)

DPX (Data Parallel eXtensions) is a set of functions that enable finding min and max values, as well as fused addition and min/max, for up to three 16 and 32-bit signed or unsigned integer parameters, with optional ReLU (clamping to zero) [CUDA_C_Programming_Guide:L9083-L9094]. These instructions are hardware-accelerated on devices with compute capability 9 and higher, and software emulation is provided on older devices [CUDA_C_Programming_Guide:L9095-L9097].

DPX is exceptionally useful when implementing dynamic programming algorithms, such as Smith-Waterman or Needleman–Wunsch in genomics and Floyd-Warshall in route optimization [CUDA_C_Programming_Guide:L9098-L9101].

## Function Categories

The DPX API provides several categories of functions based on the number of parameters and the operations performed [CUDA_C_Programming_Guide:L9083-L9094]:

### Three Parameters
Functions that operate on three parameters to find the maximum or minimum value:
- `__vimax3_s32`, `__vimax3_s16x2`, `__vimax3_u32`, `__vimax3_u16x2`
- `__vimin3_s32`, `__vimin3_s16x2`, `__vimin3_u32`, `__vimin3_u16x2`

### Three Parameters with ReLU
Functions that compute the max or min of three parameters and clamp the result to zero (ReLU):
- `__vimax3_s32_relu`, `__vimax3_s16x2_relu`, `__vimin3_s32_relu`, `__vimin3_s16x2_relu`

### Two Parameters with ReLU
Functions that compute the max or min of two parameters and clamp the result to zero:
- `__vimax_s32_relu`, `__vimax_s16x2_relu`, `__vimin_s32_relu`, `__vimin_s16x2_relu`

### Two Parameters with Index
Functions that return the min or max value and indicate which parameter was smaller or larger:
- `__vibmax_s32`, `__vibmax_u32`, `__vibmin_s32`, `__vibmin_u32`
- `__vibmax_s16x2`, `__vibmax_u16x2`, `__vibmin_s16x2`, `__vibmin_u16x2`

### Fused Addition and Max/Min
Functions that compare the sum of the first two parameters with the third parameter:
- `__viaddmax_s32`, `__viaddmax_s16x2`, `__viaddmax_u32`, `__viaddmax_u16x2`
- `__viaddmin_s32`, `__viaddmin_s16x2`, `__viaddmin_u32`, `__viaddmin_u16x2`

### Fused Addition, Max/Min, and ReLU
Functions that compare the sum of the first two parameters with the third parameter and clamp the result to zero:
- `__viaddmax_s32_relu`, `__viaddmax_s16x2_relu`, `__viaddmin_s32_relu`, `__viaddmin_s16x2_relu`

## Examples

### Max Value with ReLU
The following example demonstrates finding the maximum value of three signed 32-bit integers with ReLU clamping:

```c
const int a = -15;
const int b = 8;
const int c = 5;
int max_value_0 = __vimax3_s32_relu(a, b, c); // max(-15, 8, 5, 0) = 8

const int d = -2;
const int e = -4;
int max_value_1 = __vimax3_s32_relu(a, d, e); // max(-15, -2, -4, 0) = 0
```

### Fused Addition and Max with ReLU
This example computes the min value of the sum of two 32-bit signed integers, another 32-bit signed integer, and zero (ReLU):

```c
const int a = -5;
const int b = 6;
const int c = -2;
int max_value_0 = __viaddmax_s32_relu(a, b, c); // max(-5 + 6, -2, 0) = max(1, -2, 0) = 1

const int d = 4;
int max_value_1 = __viaddmax_s32_relu(a, d, c); // max(-5 + 4, -2, 0) = max(-1, -2, 0) = 0
```

### Min Value with Index
This example finds the minimum value of two unsigned 32-bit integers and determines which value is smaller:

```c
const unsigned int a = 9;
const unsigned int b = 6;
bool smaller_value;
unsigned int min_value = __vibmin_u32(a, b, &smaller_value); // min_value is 6, smaller_value is true
```

### Max Value of Packed 16-bit Integers
This example computes the max values of three pairs of unsigned 16-bit integers:

```c
const unsigned a = 0x00050002;
const unsigned b = 0x00070004;
const unsigned c = 0x00020006;
unsigned int max_value = __vimax3_u16x2(a, b, c); // max(5, 7, 2) and max(2, 4, 6), so max_value is 0x00070006
```

## See Also

- CUDA Math API documentation
