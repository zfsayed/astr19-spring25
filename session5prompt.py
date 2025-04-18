# session5promt.py

import numpy as np

def main():
    x_vals = np.linspace(0, 2, 1000)
    for x in x_vals:
        print(f"x: {x:.3f}, sin(x): {np.sin(x):.3f}")

main()
