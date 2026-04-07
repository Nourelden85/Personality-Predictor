import pandas as pd
from sklearn.model_selection import train_test_split
import os

base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "..", "data", "cleaned", "cleaned_top40.csv")

df = pd.read_csv(file_path)

personalities = ["Is_Extrovert", "Is_Sensor", "Is_Thinker", "Is_Judger"]

X = df.drop(["Personality"] + personalities, axis=1)
y = df[personalities]


x_train , x_test , y_train , y_test = train_test_split(X , y , test_size = 0.2 , random_state = 42)


save_path = os.path.join(base_path, "..", "data", "processed")

x_train.to_csv(os.path.join(save_path, "x_train.csv"), index=False)
x_test.to_csv(os.path.join(save_path, "x_test.csv"), index=False)
y_train.to_csv(os.path.join(save_path, "y_train.csv"), index=False)
y_test.to_csv(os.path.join(save_path, "y_test.csv"), index=False)

print("✅ Train/Test sets saved successfully!")