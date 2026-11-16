# Python Libraries Implemented in C

COMP 211 Checkoff 3 by Samanvi Ayyagari

## Topic
Python is easy to write but slow in tight loops. Libraries like NumPy get C speed by running compiled C code. I explored how that works, how to compile C into a shared library, and how to call it from Python with `ctypes`. Code was developed with AI assistance and then run, debugged, and modified by me.

## What I explored
1. **Why use C extensions?** A C array holds numbers directly. A Python list holds pointers to int objects on the heap (about 28 bytes each), so a Python loop pays overhead per number.
2. **How NumPy works:** one contiguous typed block of memory, and `arr.sum()` is a single call into a compiled C loop.
3. **Compiling C for Python:** `gcc -O2 -shared -fPIC` builds a shared library. `ctypes.CDLL` loads it (`dlopen`) and finds functions by name (`dlsym`).
4. **Calling C from Python:** `argtypes`/`restype` describe the C prototype. NumPy arrays pass a pointer to the same memory, so nothing is copied.
5. **Performance comparison:** summing 10 million integers.

## Results (one run on my Mac)
| Method | Time | vs Python loop |
|---|---|---|
| Python loop | 645.8 ms | 1x |
| NumPy sum | 4.5 ms | ~145x faster |
| My C via ctypes | 2.3 ms | ~277x faster |

All three totals matched (49,999,995,000,000). NumPy and my C are in the same league.
`bench_repeat.py` gives a fairer best-of-5 measurement.

## Results (best of 5 runs on my Mac, 10 million integers)
| Method | Time | vs Python loop |
|---|---|---|
| Python loop | 263.3 ms | 1x |
| Python sum() | 46.9 ms | ~6x faster |
| NumPy sum | 2.0 ms | ~130x faster |
| C via ctypes | 1.7 ms | ~153x faster |
| C + list conversion | 950.9 ms | ~3.6x slower |

## Interesting discoveries
- **Silent wrong answer:** mixing `int *` and `long long *` gave a plausible but wrong sum and no error, because ctypes can't see my C code.
- **Compile after saving:** I compiled before saving `sum_int.c`, got an empty library (`nm`: "no symbols"), and Python said "symbol not found".
- My C function was slightly faster than NumPy’s sum (1.7 ms vs. 2.0 ms, best of 5), but they’re basically comparable. That makes sense, because NumPy is also running a compiled C loop. The difference is probably that NumPy’s version is general purpose and mine only handles one data type.

## How to run
Requires Python 3, a C compiler, and NumPy.
```bash
pip3 install -r requirements.txt
cd code
gcc -O2 -shared -fPIC -o libsum_int.dylib sum_int.c   # Linux: libsum_int.so, Windows: libsum_int.dll
python3 call_sum_int.py
python3 bench_repeat.py    
```

## Contents
- `code/sum_int.c` - C sum functions
- `code/call_sum_int.py` - main benchmark
- `code/bench_repeat.py` - best-of-5 timing and list-conversion cost
- `slides/` - presentation slides
- `resources/resources.md` - references
