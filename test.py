print("This is a test")
print("Attention this is a test!!!!!!!!!!!!!!!!")
print("Version Control Test 0.1")
# IT project 1
# Bit and Bytes or Bits N bytes
print("H")


def primes(n: int):
    """Return a list of the first n primes."""
    sieve = [True] * n

    res = []

    for i in range(2, n):
        if sieve[i]:
            res.append(i)
            for j in range(i * i, n, i):
                sieve[j] = False

    return res


xs = primes(100)
print(xs)
import pandas as pd
import numpy as np

# Create a DataFrame with 1000 rows and 5 columns of random numbers
data = pd.DataFrame(np.random.randn(1000, 4), columns=list('ABCD'))

# Save the DataFrame to a CSV file
data.to_csv('your_data.csv', index=False)