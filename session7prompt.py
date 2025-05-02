# Cell 1: Imports
import numpy as np
import matplotlib.pyplot as plt

# Cell 2: Create x array
x = np.linspace(0, 1, 100)

# Cell 3: Define the exponential function
def my_exp(x):
    return np.exp(x)

# Cell 4: Compute y and plot
y = my_exp(x)

plt.plot(x, y)
plt.xlabel("Time [milliseconds]")
plt.ylabel("Awesomeness")
plt.title("Exponential Growth of Awesomeness")
plt.grid(True)
plt.savefig("session7_exp_plot.pdf")
plt.show()
