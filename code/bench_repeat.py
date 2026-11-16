import ctypes
import sys
import timeit
from pathlib import Path

import numpy as np

ext = {"darwin": ".dylib", "win32": ".dll"}.get(sys.platform, ".so")
lib = ctypes.CDLL(str(Path(__file__).parent / f"libsum_int{ext}"))
lib.sum_int64.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_int]
lib.sum_int64.restype = ctypes.c_longlong

n = 10_000_000
big = np.arange(n, dtype=np.int64)
py_list = big.tolist()
ptr = big.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))


def loop():
    total = 0
    for x in py_list:
        total += x
    return total


tests = {
    "Python loop": loop,
    "Python sum()": lambda: sum(py_list),
    "NumPy sum": lambda: big.sum(),
    "C via ctypes (NumPy memory)": lambda: lib.sum_int64(ptr, n),
}
for name, f in tests.items():
    best = min(timeit.repeat(f, number=1, repeat=5))
    print(f"{name:32s} {best * 1000:9.2f} ms (best of 5)")


def with_conversion():  # copies the whole list into a C array first
    arr = (ctypes.c_longlong * n)(*py_list)
    return lib.sum_int64(arr, n)


t = timeit.timeit(with_conversion, number=1)
print(f"{'C + list conversion':32s} {t * 1000:9.2f} ms (1 run)")
