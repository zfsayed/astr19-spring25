# Cell 1: Imports
import numpy as np
import matplotlib.pyplot as plt

# Cell 2: Generate Beta-distributed random numbers and plot histogram
# Parameters a=2, b=5 skew the distribution toward 0
beta_random = np.random.beta(a=2, b=5, size=1000)

plt.hist(beta_random, bins=100, color='orange', edgecolor='black')
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram of Beta(2,5) Distributed Random Numbers")
plt.grid(True)
plt.savefig("session10_beta_hist.pdf")
plt.show()
