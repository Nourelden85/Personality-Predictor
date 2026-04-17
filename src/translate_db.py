import json
import os
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='ar')
base_path = os.path.dirname(os.path.abspath(__file__))
input_json = os.path.join(base_path, "..", "data", "metadata", "mbti_data_en.json")
output_json = os.path.join(base_path, "..", "data", "metadata", "mbti_data_ar.json")
os.makedirs(os.path.dirname(output_json), exist_ok=True)

def translate_text(text):
    if not text or len(text) < 2: return text
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Error translating: {text[:20]}... -> {e}")
        return text

with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

translated_data = {"mbti_database": {}}

for mbti_type, info in data['mbti_database'].items():
    print(f"Translating {mbti_type}...")
    
    new_info = {
        "title": translate_text(info['title']),
        "ratio": info['ratio'],
        "description": translate_text(info['description']),
        "famous_people": []
    }
    
    for celeb in info['famous_people']:
        translated_celeb = {
            "name": translate_text(celeb['name']),
            "image_path": celeb['image_path'],
            "bio": translate_text(celeb['bio'])
        }
        new_info['famous_people'].append(translated_celeb)
        
    translated_data['mbti_database'][mbti_type] = new_info

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=2)

print("✅ Done! mbti_data_ar.json has been created.")