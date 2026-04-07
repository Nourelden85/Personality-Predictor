import pandas as pd
from sklearn.feature_selection import mutual_info_classif

df = pd.read_csv("../data/raw/16P.csv" , encoding="latin1")
unwanted_cols = ["Response Id"]

X_raw = df.drop(columns=unwanted_cols)

personalities_df = pd.DataFrame({
    "Is_Extrovert": df["Personality"].map(lambda x: 1 if x[0] == 'E' else 0),
    "Is_Sensor": df["Personality"].map(lambda x: 1 if x[1] == 'S' else 0),
    "Is_Thinker": df["Personality"].map(lambda x: 1 if x[2] == 'T' else 0),
    "Is_Judger": df["Personality"].map(lambda x: 1 if x[3] == 'J' else 0)
})

print("Calculating feature importance (Mutual Information)... This may take a minute.")
traits = personalities_df.columns
mi_results = pd.DataFrame(index=X_raw.columns)

for trait in traits:
    scores = mutual_info_classif(X_raw, personalities_df[trait], discrete_features=False, random_state=42)
    mi_results[trait] = scores

mi_results["Average_Score"] = mi_results.mean(axis=1)
top_40_list = mi_results.sort_values(by="Average_Score", ascending=False).head(40).index.tolist()

final_df = pd.concat([X_raw[top_40_list + ["Personality"]], personalities_df], axis=1)

final_df.to_csv("cleaned_personality_data_top40.csv", index=False)

print("\nDone! ✅")
print(f"Original columns: {df.shape[1]}")
print(f"Cleaned Questions: {len(top_40_list)}")
print("Saved to: 'cleaned_personality_data_top40.csv'")