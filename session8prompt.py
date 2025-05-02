# Cell 1: Imports
import numpy as np
import matplotlib.pyplot as plt

# Cell 2: Create x array
x = np.linspace(0, 1, 100)

# Cell 3: Define sine and cosine functions
def my_sin(x):
    return np.sin(x)

def my_cos(x):
    return np.cos(x)

# Cell 4: Plot both in subplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(x, my_sin(x), color='blue')
axes[0].set_title("sin(x)")
axes[0].set_xlabel("x")
axes[0].set_ylabel("sin(x)")

axes[1].plot(x, my_cos(x), color='green')
axes[1].set_title("cos(x)")
axes[1].set_xlabel("x")
axes[1].set_ylabel("cos(x)")

plt.tight_layout()
plt.savefig("session8_sin_cos.pdf")
plt.show()
