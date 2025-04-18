# session6promt.py

import numpy as np

def sin_x(x):
    return np.sin(x)

def cos_x(x):
    return np.cos(x)
x_vals = np.linspace(0, 2, 1000)
sin_vals = sin_x(x_vals)
cos_vals = cos_x(x_vals)
for i in range(10):
    print(f"x: {x_vals[i]:.3f}, sin(x): {sin_vals[i]:.3f}, cos(x): {cos_vals[i]:.3f}")
