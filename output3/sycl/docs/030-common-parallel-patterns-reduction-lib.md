
Many of these patterns can be expressed directly using builtin functionality of SYCL or vendor-provided libraries written in SYCL. Leveraging these functions and libraries is the best way to balance performance, portability, and productivity in real large-scale software engineering projects.

## The SYCL Reduction Library

Rather than require that each of us maintain our own library of portable and highly performant reduction kernels, SYCL provides a convenient abstraction for describing variables with reduction semantics. This abstraction simplifies the expression of reduction kernels and makes the fact that a reduction is being performed explicit, allowing implementations to select between different reduction algorithms for different combinations of device, data type, and reduction operation.

The kernel in Figure 14-8 shows an example of using the reduction library. Note that the kernel body doesn’t contain any reference to reductions—all we must specify is that the kernel contains a reduction which combines instances of the sum variable using the plus functor. This provides enough information for an implementation to automatically generate an optimized reduction sequence.

```javascript
h.parallel_for(
    range<1>{N}, reduction(sum, plus<>()),
    [=](id<1> i, auto& sum) { sum += data[i]; });
```

Figure 14-8. Reduction expressed as a data-parallel kernel using the reduction library

The result of a reduction is not guaranteed to be written back to the original variable until the kernel has completed. Apart from this restriction, accessing the result of a reduction behaves identically to accessing any other variable in SYCL: accessing a reduction result stored in a buffer requires the creation of an appropriate device or host accessor, and accessing a reduction result stored in a USM allocation may require explicit synchronization and/or memory movement.

One important way in which the SYCL reduction library differs from reduction abstractions found in other languages is that it restricts our access to the reduction variable during kernel execution—we cannot inspect the intermediate values of a reduction variable, and we are forbidden from updating the reduction variable using anything other than the specified combination function. These restrictions prevent us from making mistakes that would be hard to debug (e.g., adding to a reduction variable while trying to compute the maximum) and ensure that reductions can be implemented efficiently on a wide variety of different devices.

## The reduction Class

The reduction class is the interface we use to describe the reductions present in a kernel. The only way to construct a reduction object is to use one of the functions shown in Figure 14-9. Note that there are three families of reduction function (for buffers, USM pointers and spans), each with two overloads (with and without an identity variable).

## Chapter 14 Common Parallel Patterns

```cpp
template <typename BufferT, typename BinaryOperation>
unspecified reduction(BufferT variable, handler& h,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename BufferT, typename BinaryOperation>
unspecified reduction(BufferT variable, handler& h,
                       const BufferT::value_type& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename BinaryOperation>
unspecified reduction(T* variable, BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename BinaryOperation>
unspecified reduction(T* variable, const T& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename Extent,
       typename BinaryOperation>
unspecified reduction(span<T, Extent> variables,
                       BinaryOperation combiner,
                       const property_list& properties = {});

template <typename T, typename Extent,
       typename BinaryOperation>
unspecified reduction(span<T, Extent> variables,
                       const T& identity,
                       BinaryOperation combiner,
                       const property_list& properties = {});
```

## Figure 14-9. Function prototypes of the reduction function

If a reduction is initialized using a buffer or a USM pointer, the reduction is a scalar reduction, operating on the first object in an array. If a reduction is initialized using a span, the reduction is an array reduction. Each component of an array reduction is independent—we can think of an array reduction operating on an array of size N as equivalent to N scalar reductions with the same data type and operator.

The simplest overloads of the function allow us to specify the reduction variable and the operator used to combine the contributions from each work-item. The second set of overloads allow us to provide an optional identity value associated with the reduction operator—this is an optimization for user-defined reductions, which we will revisit later.

Note that the return type of the reduction function is unspecified, and the reduction class itself is completely implementation-defined. Although this may appear slightly unusual for a C++ class, it permits an implementation to use different classes (or a single class with any number of template arguments) to represent different reduction algorithms. Future versions of SYCL may decide to revisit this design in order to enable us to explicitly request specific reduction algorithms in specific execution contexts (most likely, via the property\_list argument).

## The reducer Class

An instance of the reducer class encapsulates a reduction variable, exposing a limited interface ensuring that we cannot update the reduction variable in any way that an implementation could consider to be unsafe. A simplified definition of the reducer class is shown in Figure 14-10. Like the reduction class, the precise definition of the reducer class is implementation-defined—a reducer’s type will depend on how the reduction is being performed, and it is important to know this at compile time in order to maximize performance. However, the functions and operators that allow us to update the reduction variable are well defined and are guaranteed to be supported by any SYCL implementation.

## Chapter 14 Common Parallel Patterns

```cpp
template <typename T, typename BinaryOperation,
         /* implementation-defined */>
class reducer {
  // Combine partial result with reducer's value
  void combine(const T& partial);
};

// Other operators are available for standard binary
// operations
template <typename T>
auto& operator+=(reducer<T, plus::<T>>&, const T&);
```

## Figure 14-10. Simplified definition of the reducer class

Specifically, every reducer provides a combine() function which combines the partial result (from a single work-item) with the value of the reduction variable. How this combine function behaves is implementation-defined but is not something that we need to worry about when writing a kernel. A reducer is also required to make other operators available depending on the reduction operator; for example, the += operator is defined for plus reductions. These additional operators are provided only as a programmer convenience and to improve readability; where they are available, these operators have identical behavior to calling combine() directly.

When working with array reductions, the reducer provides an additional subscript operator (i.e., operator[]), allowing access to individual elements of the array. Rather than returning a reference directly to an element of the array, this operator returns another reducer object, which exposes the same combine() function and shorthand operators as the reducers associated with a scalar reduction. Figure 14-11 shows a simple example of a kernel using an array reduction to compute a histogram, where the subscript operator is used to access only the histogram bin that is updated by the work-item.

```txt
h.parallel_for(
    range{N},
    reduction(span<int, 16>(histogram, 16), plus<>()),
    [=](id<1> i, auto& histogram) {
        histogram[i % B]++;
    });
```

Figure 14-11. An example kernel using an array reduction to compute a histogram

## User-Defined Reductions

Several common reduction algorithms (e.g., a tree reduction) do not see each work-item directly update a single shared variable, but instead accumulate some partial result in a private variable that will be combined at some point in the future. Such private variables introduce a problem: how should the implementation initialize them? Initializing variables to the first contribution from each work-item has potential performance ramifications, since additional logic is required to detect and handle uninitialized variables. Initializing variables to the identity of the reduction operator instead avoids the performance penalty but is only possible when the identity is known.

SYCL implementations can only automatically determine the correct identity value to use when a reduction is operating on simple arithmetic types and the reduction operator is one of several standard function objects (e.g., plus). For user-defined reductions (i.e., those operating on user-defined types and/or using user-defined function objects), we may be able to improve performance by specifying the identity value directly.

Support for user-defined reductions is limited to trivially copyable types and combination functions with no side effects, but this is enough to enable many real-life use cases. For example, the code in Figure 14-12 demonstrates the usage of a user-defined reduction to compute both the minimum element in a vector and its location.

## Chapter 14 Common Parallel Patterns

```cpp
template <typename T, typename I>
using minloc = minimum<std::pair<T, I>>;

int main() {
  constexpr size_t N = 16;

  queue q;
  float* data = malloc_shared<float>(N, q);
  std::pair<float, int>* res =
    malloc_shared<std::pair<float, int>>(1, q);
  std::generate(data, data + N, std::mt19937{});

  std::pair<float, int> identity = {
    std::numeric_limits<float>::max(),
    std::numeric_limits<int>::min()};
  *res = identity;

  auto red =
    sycl::reduction(res, identity, minloc<float, int>());
  q.submit([&](handler& h) {
    h.parallel_for(
      range<1>{N}, red, [=](id<1> i, auto& res) {
        std::pair<float, int> partial = {data[i], i};
        res.combine(partial);
      });
    }).wait();

  std::cout << "minimum value = " << res->first << " at "
              << res->second << "\n";
  ...
```
