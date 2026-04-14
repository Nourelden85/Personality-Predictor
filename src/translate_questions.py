import pandas as pd
import json
import os
import time
from deep_translator import GoogleTranslator

def translate_and_generate_metadata():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_path, "..", "data", "processed", "x_train.csv")
    
    output_json = os.path.join(base_path, "..", "data", "metadata", "questions.json")

    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    if not os.path.exists(input_file):
        print(f"Error: File not found at {input_file}")
        return

    df = pd.read_csv(input_file)
    english_questions = df.columns.tolist()

    translator = GoogleTranslator(source='en', target='ar')
    metadata = {}

    for i, q_en in enumerate(english_questions):


        q_ar = translator.translate(q_en.strip())
        
        q_id = str(i + 1)

        metadata[q_id] = {
            "en": q_en,
            "ar": q_ar
        }
        time.sleep(0.2) 

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print(f"JSON file saved to: {output_json}")

if __name__ == "__main__":
    translate_and_generate_metadata()