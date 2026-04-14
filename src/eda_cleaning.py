import pandas as pd
import numpy as np
import os
from sklearn.feature_selection import mutual_info_classif

base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "..", "data", "raw", "16P.csv")

try:
    df = pd.read_csv(file_path, encoding="latin1")
    print("File loaded successfully!")
except FileNotFoundError:
    print(f"Path error: {file_path}")
    exit()

personalities_df = pd.DataFrame({
    "Is_Extrovert": df["Personality"].str[0].map({'E': 1, 'I': 0}),
    "Is_Sensor":    df["Personality"].str[1].map({'S': 1, 'N': 0}),
    "Is_Thinker":   df["Personality"].str[2].map({'T': 1, 'F': 0}),
    "Is_Judger":    df["Personality"].str[3].map({'J': 1, 'P': 0})
})


X_for_mi = df.select_dtypes(include=[np.number])
X_for_mi = X_for_mi.drop(columns=["Response Id"])

print("Calculating importance for 50 questions... please wait.")
mi_results = pd.DataFrame(index=X_for_mi.columns)

for trait in personalities_df.columns:
    scores = mutual_info_classif(X_for_mi, personalities_df[trait], discrete_features=False, random_state=42)
    mi_results[trait] = scores

mi_results['Average_Score'] = mi_results.mean(axis=1)
top_50_questions = mi_results.sort_values(by='Average_Score', ascending=False).head(50).index.tolist()


final_df = pd.concat([
    df[['Personality']],
    df[top_50_questions],
    personalities_df
], axis=1)

output_path = os.path.join(base_path, "..", "data", "cleaned", "cleaned_top50.csv")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

final_df.to_csv(output_path, index=False)

print(f"\nDone!")
print(f"Final file contains: 1 (Personality) + 50 (Questions) + 4 (Binary Traits) = {final_df.shape[1]} columns.")
print(f"Saved to: {output_path}")