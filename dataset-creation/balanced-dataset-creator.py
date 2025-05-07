import pandas as pd
import numpy as np

# Load the original imbalanced dataset
df = pd.read_csv("../datasets/train_test_network.csv")

# Drop rows with missing labels or IPs
df = df.dropna(subset=["src_ip", "dst_ip", "label"])

# Ensure labels are integers
df["label"] = df["label"].astype(int)

# Separate by class
normal_df = df[df["label"] == 0]
attack_df = df[df["label"] == 1]

# Undersample the attack class to match the normal class
num_normals = len(normal_df)
attack_sampled = attack_df.sample(n=num_normals, random_state=42)

# Combine and shuffle
balanced_df = pd.concat([normal_df, attack_sampled], ignore_index=True)
balanced_df = balanced_df.sample(frac=1.0, random_state=42).reset_index(drop=True)

# Write to CSV
balanced_df.to_csv("../datasets/balanced_train_test_network.csv", index=False)

print(f"Saved balanced dataset with {len(balanced_df)} rows to '../datasets/balanced_train_test_network.csv'")