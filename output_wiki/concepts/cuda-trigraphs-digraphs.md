# Trigraphs and Digraphs in CUDA

## Overview

CUDA C++ enforces specific restrictions regarding the use of trigraphs and digraphs, which are legacy C language features for representing special characters. These restrictions are defined in the CUDA C++ Programming Guide under the section on language features.

## Support Status

### Trigraphs
Trigraphs are sequences of three characters that represent a single character (e.g., `??=` for `#`). CUDA does not support trigraphs on any platform. Attempting to use trigraphs in CUDA code will result in compilation errors or undefined behavior, as the compiler does not process them.

### Digraphs
Digraphs are two-character sequences that represent certain punctuation characters (e.g., `<:` for `[`). The support for digraphs depends on the operating system:

- **Windows**: Digraphs are **not supported** on Windows platforms. Using digraphs in CUDA code on Windows will likely cause syntax errors.
- **Other Platforms**: The documentation explicitly states that digraphs are not supported on Windows, implying that support may vary or be limited on other platforms, but the primary restriction highlighted is for Windows.

## Recommendations

Developers should avoid using trigraphs and digraphs in CUDA code to ensure compatibility and prevent compilation issues. Standard ASCII characters and Unicode escapes should be used instead for representing special characters.

## References

- CUDA C++ Programming Guide, Section 18.5.13: Trigraphs and Digraphs [CUDA_C_Programming_Guide:L17402-L17405]
