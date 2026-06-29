# Unified Memory Performance Hints

Performance hints are APIs available for all Unified Memory types, including CUDA Managed Memory and, on systems with full CUDA Unified Memory support, System-Allocated Memory [CUDA_C_Programming_Guide:L21193-L21201]. These hints enable applications to provide CUDA with more information than it may otherwise have, allowing for better performance-related decisions [CUDA_C_Programming_Guide:L21193-L21201].

## Characteristics

*   **Non-Semantic Impact**: These APIs are strictly hints; they do not impact the semantics of applications, only their performance [CUDA_C_Programming_Guide:L21193-L21201].
*   **Reversibility**: Hints can be added or removed anywhere in an application without impacting its results [CUDA_C_Programming_Guide:L21193-L21201].

## Usage Guidelines

Applications should only utilize these hints if they demonstrably improve performance [CUDA_C_Programming_Guide:L21193-L21201].

## Data Prefetching

One category of performance hints involves data prefetching [CUDA_C_Programming_Guide:L21193-L21201].
