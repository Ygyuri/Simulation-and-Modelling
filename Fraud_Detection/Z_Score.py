import numpy as np
import time

# Function to detect abnormal transactions using Z-score
def detect_abnormal_transactions(data, threshold=3):
    mean_value = np.mean(data)
    std_value = np.std(data)

    # Calculate Z-scores for each transaction amount
    z_scores = (data - mean_value) / std_value

    # Identify abnormal transactions based on the threshold
    abnormal_indices = np.where(np.abs(z_scores) > threshold)[0]
    abnormal_transactions = data[abnormal_indices]

    return abnormal_transactions, abnormal_indices, z_scores

# Set the threshold for abnormal transactions (higher threshold = fewer anomalies)
z_score_threshold = 3

# Transaction amounts from the generated data
transaction_amounts = np.array([519.140709, 378.983755, 565.684989, 252.792059, 318.919943])

# Detect abnormal transactions and get Z-scores
start_time = time.time()
abnormal_transactions, abnormal_indices, z_scores = detect_abnormal_transactions(transaction_amounts, threshold=z_score_threshold)
end_time = time.time()

# Calculate the detection times for each abnormal transaction
detection_times = [f"Transaction {i+1} detected in {z_scores[i]:.6f} seconds." for i in abnormal_indices]

# Print the results
if len(abnormal_transactions) > 0:
    print("Abnormal transactions detected:")
    for amount, detection_time in zip(abnormal_transactions, detection_times):
        print(f"Transaction amount: {amount:.2f}, {detection_time}")
else:
    print("No abnormal transactions detected.")

# Print the total detection time
total_detection_time = end_time - start_time
print(f"Total detection time: {total_detection_time:.6f} seconds.")

