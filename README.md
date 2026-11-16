# Python Libraries Implemented in C

COMP 211 Checkoff 3, by [Your Name]

## Topic

Python is easy to write but slow for heavy number crunching. Libraries like NumPy get
C-level speed by doing the heavy work in compiled C code. I explored how that works, how
Python can call C functions directly, and how much faster it actually is.

## What I explored

1. **Why use C extensions?** A Python int is a heap object (reference count, type pointer,
   value) while a C int is just 4 bytes. A Python loop pays that overhead per element.
2. **How NumPy works:** A NumPy array is one contiguous block of typed values, like a C
   array from `malloc`. `arr.sum()` runs a compiled C loop, so Python makes a single call.
3. **Calling C from Python:** I wrote a C function and called it with `ctypes`.
4. **Compiling C for Python:** I built a shared library with `gcc -shared -fPIC`.
5. **Performance comparison:** I benchmarked summing 10 million integers four ways.

## Results

Fill these in with your own numbers from `bench.py` (best of 5 runs):

| Method | Time (ms) |
|---|---|
| Python loop | [__] |
| Python `sum()` | [__] |
| NumPy `sum` | [__] |
| C via ctypes | [__] |
| C via ctypes + list conversion | [__] |

## Most interesting discoveries

- [Write 2-3 things that surprised you, in your own words]

## How to run the code

Requires Python 3, a C compiler (`gcc` or `clang`), and NumPy.

```bash
pip install -r requirements.txt
cd code
gcc -O2 -shared -fPIC -o libsum.so sum.c      # on Mac: libsum.dylib, on Windows: libsum.dll
python bench.py
```

## Repository contents

- `code/sum.c` - C function that sums an int array
- `code/bench.py` - loads the C library with ctypes and runs the benchmark
- `slides/` - presentation slides
- `resources/resources.md` - references I used
