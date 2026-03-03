# PyPyj

PyPyj is a lightweight extension layer for **Pyjinn** that re‑implements selected Python built‑in functions which are currently not supported natively by Pyjinn.

The goal of this project is to improve Python compatibility while staying fully within Pyjinn constraints and using standard Java classes under the hood.

PyPyj is designed to be imported as a regular `.py` module inside Pyjinn scripts.

---

## Purpose

Pyjinn provides a Python‑like environment running on the JVM, but several built‑in Python functions are marked as unsupported in the official documentation.

PyPyj fills part of that gap by providing compatible implementations of some of those missing built‑ins, prioritizing:

- Behavioral similarity to CPython
- Minimal complexity
- No external dependencies
- JVM compatibility

---

## Installation

Simply place `pypyj.py` in the same directory as your Pyjinn scripts and import it:

```python
from pypyj import *
```

---

## Implemented Functions

Below is the list of functions currently implemented by PyPyj.

---

### `open()`

Text file implementation compatible with common Python usage.

Supported modes:

- `"r"`
- `"w"`
- `"a"`
- `"r+"`
- `"w+"`
- `"a+"`

Supported methods:

- `read()`
- `read(size)`
- `readline()`
- `readlines()`
- `write()`
- `seek()`
- `tell()`
- `close()`

Notes:

- Text mode only. (for now)
- Default encoding is UTF‑8 (configurable if specified).
- No `with` statement support (Pyjinn limitation).
- Error handling raises exceptions.

---

### `pow(x, y, mod=None)`

Implements Python’s built‑in `pow` including the 3‑argument modular form.

Notes:

- Modular exponentiation is supported.
- Behavior matches Python for positive integer inputs.
- Negative exponent with modulus raises an exception.
- Floating‑point edge cases may not exactly match CPython.

---

### `bin(x)`

Returns the binary representation of an integer as a string.

Example:

```python
bin(10)  # "0b1010"
```

Notes:

- Supports negative integers.
- Only integer input is supported.

---

### `oct(x)`

Returns the octal representation of an integer as a string.

Example:

```python
oct(8)  # "0o10"
```

Notes:

- Supports negative integers.
- Only integer input is supported.

---

### `all(iterable)`

Returns `True` if all elements of the iterable are truthy.

Notes:

- Follows standard Python truthiness rules for common types.
- Custom object truth evaluation may differ if Pyjinn handles them differently.

---

### `any(iterable)`

Returns `True` if any element of the iterable is truthy.

Notes:

- Behavior mirrors Python for standard types.

---

### `reversed(sequence)`

Returns a reversed version of a sequence.

Supported types:

- `list`
- `str`

Notes:

- Returns a new reversed object.
- Unlike CPython, this does not return an iterator; it returns a fully materialized reversed result.

---

### `sorted(iterable, reverse=False)`

Returns a new sorted list.

Supported features:

- Basic sorting
- `reverse=True`

Notes:

- Does not support `key` parameter (at this stage).
- Sorting relies on natural ordering.
- Custom comparator functions are not supported.

---

## Design Philosophy

PyPyj aims to:

- Stay minimal
- Keep behavior predictable
- Remain easy to extend

Future functions may be added as long as they can be implemented cleanly using standard Java classes without breaking Pyjinn compatibility.

---

## Limitations

Because Pyjinn is not full CPython, some behaviors may differ slightly, particularly in:

- Numeric edge cases
- Type coercion
- Object introspection
- Iterator protocol

Whenever a function deviates from CPython semantics, that deviation is explicitly documented.

---

## Contributing

Contributions are welcome.

When contributing:

1. Ensure the function you are implementing is not already supported natively by Pyjinn.
2. Maintain behavior as close as reasonably possible to CPython.
3. Clearly document any deviation from Python’s original semantics.
4. Keep implementations minimal and avoid unnecessary abstraction.
5. Add test coverage for new functionality.

Before opening a pull request:

- Verify compatibility with the current Pyjinn documentation.
- Run existing tests.
- Include new tests if you add new functionality.

Feature suggestions should prioritize built‑ins that:

- Are marked as unsupported in Pyjinn
- Can be implemented cleanly using standard Java classes
- Do not require unsupported Python features (e.g., advanced introspection)

---

## License and Attribution

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

This project is intended as an open compatibility layer for the Pyjinn ecosystem. \
You are free to modify and extend it according to your needs.
