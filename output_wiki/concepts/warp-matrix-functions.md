# Warp Matrix Functions (nvcuda::wmma)

C++ warp matrix operations leverage Tensor Cores to accelerate matrix problems of the form D=A*B+C [CUDA_C_Programming_Guide:L8851-L8851]. These operations are supported on mixed-precision floating point data for devices of compute capability 7.0 or higher [CUDA_C_Programming_Guide:L8851-L8851]. This requires co-operation from all threads in a warp [CUDA_C_Programming_Guide:L8851-L8851]. In addition, these operations are allowed in conditional code only if the condition evaluates identically across the entire warp, otherwise the code execution is likely to hang [CUDA_C_Programming_Guide:L8851-L8851].

All following functions and types are defined in the namespace `nvcuda::wmma` [CUDA_C_Programming_Guide:L8855-L8855]. Sub-byte operations are considered preview, i.e. the data structures and APIs for them are subject to change and may not be compatible with future releases [CUDA_C_Programming_Guide:L8855-L8855]. This extra functionality is defined in the `nvcuda::wmma::experimental` namespace [CUDA_C_Programming_Guide:L8855-L8855].

## Core API

The primary types and functions for warp matrix operations include:

*   **`fragment`**: A template class representing a matrix fragment.
    ```cpp
    template<typename Use, int m, int n, int k, typename T, typename Layout=void> class fragment;
    ```
*   **`load_matrix_sync`**: Loads a matrix from memory into a fragment.
    ```cpp
    void load_matrix_sync(fragment<...> &a, const T* mptr, unsigned ldm);
    void load_matrix_sync(fragment<...> &a, const T* mptr, unsigned ldm, layout_t layout);
    ```
*   **`store_matrix_sync`**: Stores a fragment back to memory.
    ```cpp
    void store_matrix_sync(T* mptr, const fragment<...> &a, unsigned ldm, layout_t layout);
    ```
*   **`fill_fragment`**: Fills a fragment with a constant value.
    ```cpp
    void fill_fragment(fragment<...> &a, const T& v);
    ```
*   **`mma_sync`**: Performs the matrix multiply-accumulate operation.
    ```cpp
    void mma_sync(fragment<...> &d, const fragment<...> &a, const fragment<...> &b, const fragment<...> &c, bool satf=false);
    ```

## Numerical Properties

If `satf` (saturate to finite value) mode is true in `mma_sync`, the following additional numerical properties apply for the destination accumulator [CUDA_C_Programming_Guide:L8902-L8903]:

*   If an element result is -Infinity, the corresponding accumulator will contain -MAX_NORM [CUDA_C_Programming_Guide:L8906-L8906].

## Sub-byte Precision (Experimental)

Sub-byte operations are available in the `nvcuda::wmma::experimental` namespace [CUDA_C_Programming_Guide:L8855-L8855]. The following precision types are defined:

```cpp
namespace experimental {
    namespace precision {
        struct u4; // 4-bit unsigned
        struct s4; // 4-bit signed
        struct b1; // 1-bit
    }
}
```

For 4 bit precision, the APIs available remain the same, but you must specify `experimental::precision::u4` or `experimental::precision::s4` as the fragment data type [CUDA_C_Programming_Guide:L8977-L8977]. Since the elements of the fragment are packed together, `num_storage_elements` will be smaller than `num_elements` for that fragment [CUDA_C_Programming_Guide:L8977-L8977]. The `num_elements` variable for a sub-byte fragment, hence returns the number of elements of sub-byte type `element_type<T>` [CUDA_C_Programming_Guide:L8977-L8977]. This is true for single bit precision as well, in which case, the mapping from `element_type<T>` to `storage_element_type<T>` is as follows [CUDA_C_Programming_Guide:L8977-L8977]:

*   `experimental::precision::u4` -> unsigned (8 elements in 1 storage element)
*   `experimental::precision::s4` -> int (8 elements in 1 storage element)
*   `experimental::precision::b1` -> unsigned (32 elements in 1 storage element)
*   `T` -> T //all other types

### Bitwise Matrix Multiply Accumulate (BMMA)

The experimental namespace also defines enums for bitwise operations:

```cpp
enum bmmaBitOp {
    bmmaBitOpXOR = 1, // compute_75 minimum
    bmmaBitOpAND = 2  // compute_80 minimum
};
enum bmmaAccumulateOp { bmmaAccumulateOpPOPC = 1 };
```

## Alternate Floating Point Support

Alternate floating point support includes double precision operations:

| Matrix A | Matrix B | Accumulator | Matrix Size (m-n-k) |
| :--- | :--- | :--- | :--- |
| double | double | double | 8x8x4 |

[CUDA_C_Programming_Guide:L9048-L9048]

## See Also

*   Tensor Cores
*   Mixed Precision Training
*   CUDA C++ Programming Guide Section 10.24
