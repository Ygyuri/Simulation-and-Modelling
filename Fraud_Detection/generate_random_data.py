import random
import pandas as pd

def generate_random_data(num_samples):
    # Initialize lists to store generated data
    transaction_amounts = []
    transaction_times = []

    # Generate random data for num_samples
    for _ in range(num_samples):
        # Generate random transaction amount between 1 and 1000 (you can adjust the range as needed)
        transaction_amounts.append(random.uniform(1, 1000))

        # Generate random transaction time (assuming the dataset is for one day, 24 hours format)
        transaction_times.append(random.randint(0, 23))

    # Create a DataFrame to store the data
    data = pd.DataFrame({'TransactionAmount': transaction_amounts, 'TransactionTime': transaction_times})

    return data

# Generate 1000 random data samples
num_samples = 1000
random_data = generate_random_data(num_samples)

# Display the first few rows of the generated data
print(random_data.head())

