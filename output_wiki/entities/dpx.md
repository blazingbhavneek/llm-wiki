# DPX (Dynamic Programming eXtensions)

DPX is a set of hardware-accelerated functions (compute capability 9+) for min/max, fused add/min/max, and optional ReLU operations on 16/32-bit signed/unsigned integers. Widely used in dynamic programming algorithms like Smith-Waterman, Needleman-Wunsch, and Floyd-Warshall.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L9083-L9151

Citation: [CUDA_C_Programming_Guide:L9083-L9151]

````text
## 10.25. DPX

DPX is a set of functions that enable finding min and max values, as well as fused addition and min/max, for up to three 16 and 32-bit signed or unsigned integer parameters, with optional ReLU (clamping to zero):

three parameters: \_\_vimax3\_s32, \_\_vimax3\_s16x2, \_\_vimax3\_u32, \_\_vimax3\_u16x2, \_\_vimin3\_s32, \_\_vimin3\_s16x2, \_\_vimin3\_u32, \_\_vimin3\_u16x2

two parameters, with ReLU: \_\_vimax\_s32\_relu, \_\_vimax\_s16x2\_relu, \_\_vimin\_s32\_relu, \_\_vimin\_s16x2\_relu

▶ three parameters, with ReLU: \_\_vimax3\_s32\_relu, \_\_vimax3\_s16x2\_relu, \_\_vimin3\_s32\_relu, \_\_vimin3\_s16x2\_relu

two parameters, also returning which parameter was smaller/larger: \_\_vibmax\_s32, \_\_vibmax\_u32, \_\_vibmin\_s32, \_\_vibmin\_u32, \_\_vibmax\_s16x2, \_\_vibmax\_u16x2, \_\_vibmin\_s16x2, \_\_vibmin\_u16x2

three parameters, comparing (first + second) with the third: \_\_viaddmax\_s32, \_\_viaddmax\_s16x2, \_\_viaddmax\_u32, \_\_viaddmax\_u16x2, \_\_viaddmin\_s32, \_\_viaddmin\_s16x2, \_\_viaddmin\_u32, \_\_viaddmin\_u16x2

▶ three parameters, with ReLU, comparing (first + second) with the third and a zero: \_\_viaddmax\_s32\_relu, \_\_viaddmax\_s16x2\_relu, \_\_viaddmin\_s32\_relu, \_\_viaddmin\_s16x2\_relu

These instructions are hardware-accelerated on devices with compute capability 9 and higher, and software emulation on older devices.

Full API can be found in CUDA Math API documentation.

DPX is exceptionally useful when implementing dynamic programming algorithms, such as Smith-Waterman or Needleman–Wunsch in genomics and Floyd-Warshall in route optimization.

## 10.25.1. Examples

Max value of three signed 32-bit integers, with ReLU

```c
const int a = -15;
const int b = 8;
const int c = 5;
int max_value_0 = __vimax3_s32_relu(a, b, c); // max(-15, 8, 5, 0) = 8
const int d = -2;
const int e = -4;
int max_value_1 = __vimax3_s32_relu(a, d, e); // max(-15, -2, -4, 0) = 0
```

Min value of the sum of two 32-bit signed integers, another 32-bit signed integer and a zero (ReLU)

```c
const int a = -5;
const int b = 6;
const int c = -2;
int max_value_0 = __viaddmax_s32_relu(a, b, c); // max(-5 + 6, -2, 0) = max(1, -2, 0)
    ← = 1
const int d = 4;
int max_value_1 = __viaddmax_s32_relu(a, d, c); // max(-5 + 4, -2, 0) = max(-1, -2, 0)
    ← = 0
```

Min value of two unsigned 32-bit integers and determining which value is smaller

```txt
const unsigned int a = 9;
const unsigned int b = 6;
bool smaller_value;
unsigned int min_value = __vibmin_u32(a, b, &smaller_value); // min_value is 6,
    ←smaller_value is true
```

Max values of three pairs of unsigned 16-bit integers

```txt
const unsigned a = 0x00050002;
const unsigned b = 0x00070004;
const unsigned c = 0x00020006;
unsigned int max_value = __vimax3_u16x2(a, b, c); // max(5, 7, 2) and max(2, 4, 6), so
    max_value is 0x00070006
```
````
