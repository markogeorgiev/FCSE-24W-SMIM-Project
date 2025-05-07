import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Output directory
save_dir = "../Project-Images/balanced-imbalanced-comparison/"
os.makedirs(save_dir, exist_ok=True)


# Load datasets
df_bal = pd.read_csv("../datasets/balanced_train_test_network.csv")
df_unbal = pd.read_csv("../datasets/train_test_network.csv")

# Settings
max_unique = 10
ignore_value = "-"
plot_palette = {"Balanced": "#1f77b4", "Unbalanced": "#ff7f0e"}

columns_to_check = df_bal.columns.intersection(df_unbal.columns)

for col in columns_to_check:
    if df_bal[col].dtype not in ["object", "category"] and df_bal[col].nunique() > max_unique:
        continue

    bal_values = df_bal[col].dropna()
    unbal_values = df_unbal[col].dropna()
    bal_values = bal_values[bal_values != ignore_value]
    unbal_values = unbal_values[unbal_values != ignore_value]

    if unbal_values.nunique() > max_unique:
        top_vals = unbal_values.value_counts().head(max_unique).index
        bal_values = bal_values[bal_values.isin(top_vals)]
        unbal_values = unbal_values[unbal_values.isin(top_vals)]

    bal_counts = bal_values.value_counts()
    unbal_counts = unbal_values.value_counts()

    all_values = sorted(set(bal_counts.index).union(unbal_counts.index))
    bal_counts = bal_counts.reindex(all_values, fill_value=0)
    unbal_counts = unbal_counts.reindex(all_values, fill_value=0)

    plot_df = pd.DataFrame({
        "Value": all_values * 2,
        "Count": list(bal_counts.values) + list(unbal_counts.values),
        "Dataset": ["Balanced"] * len(all_values) + ["Unbalanced"] * len(all_values)
    })

    plt.figure(figsize=(12, 6))
    sns.barplot(data=plot_df, x="Value", y="Count", hue="Dataset", palette=plot_palette)

    bar_width = 0.4  # adjust spacing between bars
    group_offset = {"Balanced": -bar_width / 2, "Unbalanced": bar_width / 2}

    for i, row in plot_df.iterrows():
        x_pos = all_values.index(row["Value"]) + group_offset[row["Dataset"]]
        y_pos = row["Count"]
        label_text = f"{int(row['Count'])}"
        plt.text(
            x=x_pos,
            y=y_pos / 2,  # middle of the bar
            s=label_text,
            ha='center',
            va='center',
            fontsize=8,
            rotation=0,
            color="white" if y_pos > 0 else "black"
        )

    plt.title(f"Value Counts for '{col}' (Balanced vs. Unbalanced)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filename = f"{col.replace('/', '_')}.png"
    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"Saved plot for '{col}' to {save_path}")
