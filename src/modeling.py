import pandas as pd
import joblib
from sklearn.svm import SVC
import os

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "..", "data", "processed")
model_path = os.path.join(base_path, "..", "models")

X_train = pd.read_csv(os.path.join(data_path, "x_train.csv"))
y_train = pd.read_csv(os.path.join(data_path, "y_train.csv"))

def train_models(X_train, y_train):
    models = {}
    for trait in y_train.columns:
        svm_classifier = SVC(random_state=42)
        svm_classifier.fit(X_train, y_train[trait])
        models[trait] = svm_classifier
    return models

def save_models(models, directory=os.path.join(model_path, "")):
    for trait, model in models.items():
        joblib.dump(model, f"{directory}{trait}_model.pkl")

if __name__ == "__main__":
    print("Training models...")
    trained_models = train_models(X_train, y_train)
    print("Saving models...")
    save_models(trained_models)
    print("All models trained and saved successfully!")