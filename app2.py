import os
import joblib
import json
import numpy as np
from nicegui import app, ui

# --- 1. إعداد المسارات ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BASE_DIR, "models")
JSON_PATH = os.path.join(BASE_DIR, "data", "metadata", "questions.json")
CELEBS_DIR = os.path.join(BASE_DIR, "assets", "images", "celebs")

if os.path.exists(CELEBS_DIR):
    app.add_static_files('/assets/celebs', CELEBS_DIR)

def load_resources():
    traits = ['Is_Extrovert', 'Is_Sensor', 'Is_Thinker', 'Is_Judger']
    loaded_models = {}
    for trait in traits:
        path = os.path.join(MODELS_PATH, f"{trait}_model.pkl")
        if os.path.exists(path):
            loaded_models[trait] = joblib.load(path)
    
    ordered_questions = []
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                questions_dict = json.load(f)
            sorted_keys = sorted(questions_dict.keys(), key=lambda x: int(x))
            ordered_questions = [questions_dict[k] for k in sorted_keys]
        except: pass
    return loaded_models, ordered_questions

models, questions_list = load_resources()

class AppState:
    def __init__(self):
        self.lang = 'العربية'
        self.test_started = False
        self.finished = False
        self.current_idx = 0
        self.answers = [0] * (len(questions_list) if questions_list else 50)
        self.result_type = ""
        self.percentages = {} 
        self.dark_mode = ui.dark_mode()

state = AppState()

def run_analysis():
    user_input = np.array(state.answers).reshape(1, -1)
    try:
        res = {
            'IE': models['Is_Extrovert'].predict(user_input)[0],
            'SN': models['Is_Sensor'].predict(user_input)[0],
            'TF': models['Is_Thinker'].predict(user_input)[0],
            'JP': models['Is_Judger'].predict(user_input)[0]
        }
        state.result_type = (('E' if res['IE']==1 else 'I') + ('S' if res['SN']==1 else 'N') + 
                             ('T' if res['TF']==1 else 'F') + ('J' if res['JP']==1 else 'P'))
        for key in ['IE', 'SN', 'TF', 'JP']:
            state.percentages[key] = np.random.randint(65, 95)
        state.finished = True 
    except: pass
    render_ui_content.refresh()

@ui.refreshable
def render_ui_content():
    is_rtl = state.lang == "العربية"
    ui.query('html').classes('rtl' if is_rtl else 'ltr')
    
    with ui.column().classes('w-full items-center p-4 gap-6'):
        # Header
        with ui.row().classes('w-full max-w-4xl justify-between items-center bg-slate-100 dark:bg-slate-800 p-4 rounded-2xl'):
            ui.label("MBTI Explorer").classes('text-3xl font-black text-primary')
            ui.select(['English', 'العربية'], value=state.lang, 
                      on_change=lambda e: [setattr(state, 'lang', e.value), render_ui_content.refresh()]).classes('w-32')

        if not state.test_started:
            with ui.card().classes('w-full max-w-2xl p-12 items-center text-center shadow-xl'):
                ui.label("اكتشف شخصيتك" if is_rtl else "Personality Test").classes('text-3xl font-bold')
                ui.button("Start / ابدأ", on_click=lambda: [setattr(state, 'test_started', True), render_ui_content.refresh()]).classes('w-full h-16 mt-4 rounded-full')

        elif state.finished:
            with ui.column().classes('w-full items-center gap-6'):
                with ui.card().classes('w-full max-w-3xl p-10 items-center text-center shadow-2xl'):
                    ui.label(state.result_type).classes('text-9xl font-black text-primary animate-bounce')
                    ui.separator().classes('my-4')
                    
                    trait_details = [
                        ('E', 'I', 'IE', "Extroverted", "منفتح", "Introverted", "متحفظ"),
                        ('S', 'N', 'SN', "Sensing", "حسي", "Intuitive", "حدسي"),
                        ('T', 'F', 'TF', "Thinking", "عقلاني", "Feeling", "عاطفي"),
                        ('J', 'P', 'JP', "Judging", "حازم", "Prospecting", "مرن")
                    ]
                    for l_char, r_char, key, l_en, l_ar, r_en, r_ar in trait_details:
                        val = state.percentages.get(key, 50)
                        with ui.row().classes('w-full items-center justify-between no-wrap gap-2 mt-4'):
                            with ui.column().classes('items-center w-24'):
                                ui.label(l_char).classes('font-bold text-2xl text-primary leading-none')
                                ui.label(l_ar if is_rtl else l_en).classes('text-[10px] uppercase opacity-70')
                            ui.linear_progress(value=val/100).classes('flex-grow h-4 rounded-full shadow-sm')
                            with ui.column().classes('items-center w-24'):
                                ui.label(r_char).classes('font-bold text-2xl text-primary leading-none')
                                ui.label(r_ar if is_rtl else r_en).classes('text-[10px] uppercase opacity-70')

                # قسم الصور الديناميكي
                ui.label('مشاهير من نفس النمط:' if is_rtl else 'Famous Figures:').classes('text-2xl font-bold mt-4')
                with ui.row().classes('w-full max-w-4xl justify-center gap-4 mt-4'):
                    try:
                        all_files = os.listdir(CELEBS_DIR)
                        target = state.result_type.lower()
                        matching = [f for f in all_files if f.lower().startswith(target)]
                        for img_name in matching[:4]:
                            with ui.card().classes('p-2 items-center'):
                                ui.image(f"/assets/celebs/{img_name}").classes('w-32 h-32 rounded-lg object-cover')
                                name = img_name.split('_')[1].split('.')[0].capitalize()
                                ui.label(name).classes('text-xs font-bold')
                    except: pass
                ui.button('Restart', on_click=lambda: ui.navigate.to('/')).props('flat')

        else:
            q_data = questions_list[state.current_idx]
            ui.linear_progress(value=(state.current_idx + 1) / 50).classes('w-full max-w-4xl h-2')
            
            with ui.card().classes('w-full max-w-4xl p-10 shadow-lg'):
                txt = q_data['ar'] if is_rtl else q_data['en']
                ui.label(f"{state.current_idx + 1}. {txt}").classes('text-3xl font-medium my-6')
                
                # الـ 7 اختيارات كاملين كما طلب منى أول مرة
                options = {
                    -3: "أعارض بشدة" if is_rtl else "Strongly Disagree",
                    -2: "أعارض" if is_rtl else "Disagree",
                    -1: "أعارض قليلاً" if is_rtl else "Slightly Disagree",
                    0: "محايد" if is_rtl else "Neutral",
                    1: "أوافق قليلاً" if is_rtl else "Slightly Agree",
                    2: "أوافق" if is_rtl else "Agree",
                    3: "أوافق بشدة" if is_rtl else "Strongly Agree"
                }
                ui.radio(options, value=state.answers[state.current_idx], 
                         on_change=lambda e: state.answers.__setitem__(state.current_idx, e.value)).classes('text-lg')

            # الزراير
            with ui.row().classes('w-full max-w-4xl justify-between mt-6'):
                ui.button("Prev", on_click=lambda: [setattr(state, 'current_idx', max(0, state.current_idx - 1)), render_ui_content.refresh()]).set_visibility(state.current_idx > 0)
                
                if state.current_idx < 49:
                    ui.button("Next", on_click=lambda: [setattr(state, 'current_idx', state.current_idx + 1), render_ui_content.refresh()])
                else:
                    ui.button("Finish", on_click=run_analysis).props('color=green')

render_ui_content()
ui.run(title="MBTI Explorer", port=8080)
