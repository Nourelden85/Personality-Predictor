import pandas as pd
import joblib
from sklearn.svm import SVC
import os

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "..", "data", "processed")
model_path = os.path.join(base_path, "..", "models")

# تأكدي من وجود الفولدر
if not os.path.exists(model_path):
    os.makedirs(model_path)

X_train = pd.read_csv(os.path.join(data_path, "x_train.csv"))
y_train = pd.read_csv(os.path.join(data_path, "y_train.csv"))

def train_models(X_train, y_train):
    models = {}
    for trait in y_train.columns:
        print(f"Training model for: {trait}")
        # التعديل الأهم: إضافة probability=True
        svm_classifier = SVC(kernel='linear', probability=True, random_state=42)
        svm_classifier.fit(X_train, y_train[trait])
        models[trait] = svm_classifier
    return models

def save_models(models, directory):
    # خريطة لربط اسم العمود في الـ CSV باسم الملف اللي الـ Streamlit كود مستنيه
    filename_map = {
        'Is_Extrovert': 'Is_Extrovert_model.pkl',
        'Is_Sensing': 'Is_Sensor_model.pkl',
        'Is_Thinker': 'Is_Thinker_model.pkl',
        'Is_Judger': 'Is_Judger_model.pkl'
    }
    
    for trait, model in models.items():
        # لو اسم العمود موجود في الخريطة استخدمي الاسم الجديد، لو مش موجود استخدمي اسم العمود نفسه
        filename = filename_map.get(trait, f"{trait}_model.pkl")
        save_full_path = os.path.join(directory, filename)
        joblib.dump(model, save_full_path)
        print(f"Saved: {save_full_path}")

if __name__ == "__main__":
    print("Training models with probability enabled...")
    trained_models = train_models(X_train, y_train)
    print("Saving models...")
    save_models(trained_models, model_path)
    print("All models trained and saved successfully!")