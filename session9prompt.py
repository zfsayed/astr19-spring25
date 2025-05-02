# Cell 1: Imports
import numpy as np
import matplotlib.pyplot as plt

# Cell 2: Generate random numbers and plot histogram
random_nums = np.random.uniform(0, 1, 1000)

plt.hist(random_nums, bins=100, color='purple', edgecolor='black')
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram of Uniform[0,1] Random Numbers")
plt.grid(True)
plt.savefig("session9_uniform_hist.pdf")
plt.show()

