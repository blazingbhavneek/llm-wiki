# CUDA Feature Set Compiler Targets

CUDA compilers support three distinct sets of compute features, each with specific compiler target suffixes and compatibility characteristics [CUDA_C_Programming_Guide:L19461-L19484].

## Baseline Feature Set

The Baseline Feature Set consists of the predominant compute features introduced with the intent to be available for subsequent compute architectures [CUDA_C_Programming_Guide:L19461-L19484].

*   **Compiler Target Suffix:** None (e.g., `compute_100`)
*   **Compatibility:** Compatible with all devices of the specified compute capability and later [CUDA_C_Programming_Guide:L19461-L19484].
*   **Feature Scope:** This target does not allow the use of architecture-specific features [CUDA_C_Programming_Guide:L19461-L19484].

## Architecture-Specific Feature Set

The Architecture-Specific Feature Set is a small, highly specialized set of features introduced to accelerate specialized operations. These features are not guaranteed to be available or might change significantly on subsequent compute architectures [CUDA_C_Programming_Guide:L19461-L19484].

*   **Compiler Target Suffix:** `a` (e.g., `compute_100a`, `compute_120a`) [CUDA_C_Programming_Guide:L19461-L19484].
*   **Introduction:** Introduced with Compute Capability 9.0 devices [CUDA_C_Programming_Guide:L19461-L19484].
*   **Compatibility:** Compatible only with devices of the specific compute capability for which the target was designed [CUDA_C_Programming_Guide:L19461-L19484].
*   **Feature Scope:** Allows use of the complete set of architecture-specific features for that device [CUDA_C_Programming_Guide:L19461-L19484].
*   **Hierarchy:** The architecture-specific feature set is a superset of the family-specific feature set [CUDA_C_Programming_Guide:L19461-L19484].

## Family-Specific Feature Set

Some architecture-specific features are common to GPUs of more than one compute capability. These features are summarized in the respective "Compute Capability #.#" subsections [CUDA_C_Programming_Guide:L19461-L19484]. With a few exceptions, later generation devices with the same major compute capability are in the same family [CUDA_C_Programming_Guide:L19461-L19484].

*   **Compiler Target Suffix:** `f` (e.g., `compute_100f`, `compute_120f`) [CUDA_C_Programming_Guide:L19461-L19484].
*   **Introduction:** Introduced with Compute Capability 10.0 devices [CUDA_C_Programming_Guide:L19461-L19484].
*   **Compatibility:** Compatible only with devices that are part of the specific GPU family [CUDA_C_Programming_Guide:L19461-L19484].
*   **Feature Scope:** Allows the compiler to generate code using the common subset of architecture-specific features shared by all members of that GPU family [CUDA_C_Programming_Guide:L19461-L19484].
*   **Hierarchy:** The family-specific feature set is a superset of the baseline feature set [CUDA_C_Programming_Guide:L19461-L19484].

## Compatibility and Examples

The following examples illustrate the differences between the three targets for Compute Capability 10.0:

1.  **Baseline (`compute_100`):** Does not allow use of architecture-specific features. Compatible with all devices of compute capability 10.0 and later [CUDA_C_Programming_Guide:L19461-L19484].
2.  **Family-Specific (`compute_100f`):** Allows use of the subset of architecture-specific features common across the GPU family. Compatible with devices of Compute Capability 10.0 and Compute Capability 10.3 [CUDA_C_Programming_Guide:L19461-L19484]. The features available in `compute_100f` form a superset of the features available in `compute_100` [CUDA_C_Programming_Guide:L19461-L19484].
3.  **Architecture-Specific (`compute_100a`):** Allows use of the complete set of architecture-specific features in Compute Capability 10.0 devices. Compatible only with devices of Compute Capability 10.0 [CUDA_C_Programming_Guide:L19461-L19484]. The features available in `compute_100a` form a superset of the features available in `compute_100f` [CUDA_C_Programming_Guide:L19461-L19484].

### Family-Specific Compatibility Table

Table 25 indicates the compatibility of family-specific targets with device compute capability, including exceptions [CUDA_C_Programming_Guide:L19461-L19484].

| Compilation Target | Compatible with Compute Capability |
| :--- | :--- |
| `compute_100f` | 10.0, 10.3 |
| `compute_103f` | 10.3 |
| `compute_110f` | 11.0 |
| `compute_120f` | 12.0, 12.1 |
| `compute_121f` | 12.1 |

*Note: The table above reflects the content of Table 25 from the source documentation [CUDA_C_Programming_Guide:L19461-L19484].*

## References

*   [CUDA_C_Programming_Guide:L19461-L19484] CUDA C++ Programming Guide, Section 20.1.3. Feature Set Compiler Targets. Includes Table 25 (Family-Specific Compatibility) and Table 26 (Baseline Feature Set availability).
