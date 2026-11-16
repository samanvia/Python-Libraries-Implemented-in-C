import ctypes
import time
import numpy as np

# --- Load the C library and declare the signature ---
lib = ctypes.CDLL("./libsum_int.dylib")
lib.sum_int64.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_int]
lib.sum_int64.restype = ctypes.c_longlong

# --- Set up the data once (setup is NOT part of what we time) ---
n = 10_000_000
big = np.arange(n, dtype=np.int64)
big_list = big.tolist()                      # plain Python list of ints
ptr = big.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong))


# --- 1. Pure Python loop ---
start = time.perf_counter()
total = 0
for x in big_list:
    total += x
py_time = time.perf_counter() - start
print("Python loop:      ", total, f"{py_time:.4f} s")

# --- 2. NumPy ---
start = time.perf_counter()
total = big.sum(dtype=np.int64)
np_time = time.perf_counter() - start
print("NumPy sum:        ", total, f"{np_time:.4f} s")

# --- 3. Our C function via ctypes ---
start = time.perf_counter()
total = lib.sum_int64(ptr, n)
c_time = time.perf_counter() - start
print("C via ctypes:     ", total, f"{c_time:.4f} s")

# --- Comparison ---
print()
print(f"NumPy is {py_time / np_time:.0f}x faster than the Python loop")
print(f"C     is {py_time / c_time:.0f}x faster than the Python loop")