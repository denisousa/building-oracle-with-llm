import pandas as pd
import math

df = pd.read_csv("clones.csv")
mini_clones_df = pd.DataFrame()

for classification in df['classification'].unique():
    class_df = df[df['classification'] == classification]
    sample_size = math.ceil(0.10 * len(class_df)) # 5% population
    sample_df = class_df.sample(n=sample_size)
    mini_clones_df = pd.concat([mini_clones_df, sample_df])

mini_clones_df.to_csv("mini_clones.csv", index=False)
print("mini_clones.csv has been created successfully.")

class_counts = df['classification'].value_counts()
with open("class_counts.txt", "w") as f:
    for classification, count in class_counts.items():
        f.write(f"Classification: {classification} - Count: {count}\n")


