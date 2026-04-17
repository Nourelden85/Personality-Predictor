import os
import joblib
import json
import numpy as np
from nicegui import app, ui
from i18n import UI_TEXTS, ar_num

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
QUESTIONS_PATH = os.path.join(DATA_DIR, "metadata", "questions.json")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")

app.add_static_files('/assets/images', IMAGES_DIR)
ui.add_head_html("""
<style>
*{
    transition:
        background-color 0.35s ease,
        color 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease;
}
</style>
""")

def load_resources():
    traits = ['Is_Extrovert', 'Is_Sensor', 'Is_Thinker', 'Is_Judger']
    loaded_models = {}
    for trait in traits:
        path = os.path.join(MODELS_PATH, f"{trait}_model.pkl")
        if os.path.exists(path):
            loaded_models[trait] = joblib.load(path)
    
    ordered_questions = []
    if os.path.exists(QUESTIONS_PATH):
        try:
            with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
                questions_dict = json.load(f)
            sorted_keys = sorted(questions_dict.keys(), key=lambda x: int(x))
            ordered_questions = [questions_dict[k] for k in sorted_keys]
        except Exception as e:
            print(e)
    return loaded_models, ordered_questions

models, questions_list = load_resources()

def load_mbti_db(lang):
    file_name = "mbti_data_ar.json" if lang == "العربية" else "mbti_data_en.json"
    path = os.path.join(DATA_DIR, "metadata", file_name)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)["mbti_database"]
    except Exception as e:
        print(e)
        return {}
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
        self.mbti_db = load_mbti_db(self.lang)

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

        res_proba = {
            'IE': models['Is_Extrovert'].predict_proba(user_input)[0],
            'SN': models['Is_Sensor'].predict_proba(user_input)[0],
            'TF': models['Is_Thinker'].predict_proba(user_input)[0],
            'JP': models['Is_Judger'].predict_proba(user_input)[0]
        }
        state.result_type = (('E' if res['IE'] == 1 else 'I') + ('S' if res['SN'] == 1 else 'N') + 
                             ('T' if res['TF'] == 1 else 'F') + ('J' if res['JP'] == 1 else 'P'))
        for key in res_proba.keys():
            state.percentages[key] = round(res_proba[key][1] * 100)
        state.finished = True 
    except Exception as e:
        ui.notify(str(e), color='red')
        print(e)
    render_ui_content.refresh()

def restart():
    state.test_started = False
    state.finished = False
    state.current_idx = 0
    state.answers = [0] * len(questions_list)
    state.result_type = ""
    state.percentages = {}
    render_ui_content.refresh()

@ui.refreshable
def render_ui_content():
    texts = UI_TEXTS[state.lang]
    mbti_db = state.mbti_db
    ui.timer(0.01, lambda: ui.run_javascript(f"document.documentElement.dir = '{texts['dir']}'"), once=True)
    ui.query('html').classes(replace=texts['dir'])
    with ui.column().classes('w-full items-center p-4 gap-6'):
        with ui.row().classes('w-full max-w-4xl justify-between items-center bg-slate-100 dark:bg-slate-800 p-4 rounded-2xl'):
            ui.label(texts['title']).classes('text-3xl font-black text-primary')

            ui.select(['English', 'العربية'], value=state.lang, on_change=lambda e: [setattr(state, 'lang', e.value), setattr(state, 'mbti_db', load_mbti_db(e.value)), render_ui_content.refresh()]).classes('w-32')

            ui.button(icon='light_mode' if state.dark_mode.value else 'dark_mode', 
                          on_click=lambda: [state.dark_mode.toggle(), render_ui_content.refresh()]).props('round flat glossy')

        if not state.test_started:
            with ui.card().classes('w-full max-w-2xl p-12 items-center text-center shadow-xl'):
                ui.label(texts["title"]).classes('text-3xl font-bold')
                ui.button(texts["start"], on_click=lambda: [setattr(state, 'test_started', True), render_ui_content.refresh()]).classes('w-full h-16 mt-4 rounded-full')

        elif state.finished:
            with ui.column().classes('w-full items-center gap-6'):
                with ui.card().classes('w-full max-w-3xl p-10 items-center text-center shadow-2xl'):
                    ui.label(state.result_type).classes('text-9xl font-black text-primary animate-pulse')
                    ui.separator().classes('my-4')
                    ui.label(texts['traits_title']).classes('text-2xl font-black mt-8 text-blue-600')

                trait_pairs = [('E', 'I', 'IE'), ('S', 'N', 'SN'), ('T', 'F', 'TF'), ('J', 'P', 'JP')]
                with ui.grid(columns=1).classes('w-full max-w-2xl gap-6 mt-4'):
                    for l_char, r_char, key in trait_pairs:
                        val = state.percentages.get(key, 50)
                        
                        is_left = state.result_type[trait_pairs.index((l_char, r_char, key))] == l_char
                        
                        if not is_left:
                            val = 100 - val
                        left_name = texts['traits_map'][l_char]
                        right_name = texts['traits_map'][r_char]
                        
                        with ui.row().classes('w-full items-center justify-between no-wrap gap-4 mt-2'):
                            with ui.column().classes('items-center w-24'):
                                ui.label(l_char).classes(f'text-2xl font-black leading-none {"text-blue-600" if is_left else "opacity-30"}')
                                ui.label(left_name).classes('text-[10px] uppercase font-bold opacity-70')

                            with ui.row().classes('flex-grow bg-slate-100 dark:bg-slate-800 h-3 rounded-full overflow-hidden relative shadow-inner'):
                                if texts['dir'] == 'rtl':
                                    side = "right: 0" if is_left else "left: 0"
                                else:
                                    side = "left: 0" if is_left else "right: 0"
                                
                                color = "bg-blue-500" if is_left else "bg-indigo-500"
                                ui.row().style(f'width: {val}%; position: absolute; {side}; transition: width 1s ease-in-out') \
                                        .classes(f'h-full {color} shadow-md shadow-blue-500/50')

                            with ui.column().classes('items-center w-24'):
                                ui.label(r_char).classes(f'text-2xl font-black leading-none {"text-blue-600" if not is_left else "opacity-30"}')
                                ui.label(right_name).classes('text-[10px] uppercase font-bold opacity-70')
                personality = mbti_db.get(state.result_type, {})
                ui.label(personality.get("title","")).classes("text-3xl font-bold")
                ui.label(personality.get("description","")).classes("text-center opacity-80 max-w-2xl")
                ui.label(f'{texts["population"]} {personality.get("ratio","")}')
                ui.label(texts["famous_people"]).classes('text-2xl font-bold mt-8')

                famous_people = personality.get("famous_people", [])
                with ui.row().classes('w-full max-w-5xl flex flex-wrap justify-center gap-6 mt-4'):
                    for person in famous_people:
                        with ui.card().classes('w-full sm:w-[48%] p-4 rounded-2xl shadow-xl flex flex-col'):
                            ui.image(person["image_path"]).classes('w-full object-cover rounded-xl')
                            ui.label(person["name"]).classes('text-lg font-bold mt-3')
                            ui.label(person["bio"]).classes('text-sm opacity-80 mt-2')
                ui.button(texts["restart"], on_click=restart).props('flat')

        else:
            q_data = questions_list[state.current_idx]
            progress = (state.current_idx + 1) / len(questions_list)
            
            with ui.column().classes('w-full max-w-4xl items-center gap-6 mt-10'):
                ui.label(texts['question_of'].format(ar_num(state.current_idx + 1, state.lang), ar_num(len(questions_list), state.lang))).classes('font-bold opacity-60')
                ui.linear_progress(value=progress, show_value=False).classes('w-full h-3 rounded-full shadow-sm')

                with ui.card().classes('w-full max-w-4xl p-10 shadow-lg'):
                    txt = q_data[texts["lang_key"]]
                    ui.label(f"{ar_num(state.current_idx + 1, state.lang)}. {txt}").classes('text-3xl font-medium my-6')
                    option_values = [-3, -2, -1, 0, 1, 2, 3]

                    options = {
                        value: text
                        for value, text in zip(option_values, texts["choices"])
                    }
                    ui.radio(options, value=state.answers[state.current_idx], 
                            on_change=lambda e: state.answers.__setitem__(state.current_idx, e.value)).classes('text-lg gap-3')

            with ui.row().classes('w-full max-w-4xl justify-between mt-6'):
                ui.button(texts["previous"], on_click=lambda: [setattr(state, 'current_idx', max(0, state.current_idx - 1)), render_ui_content.refresh()]).set_visibility(state.current_idx > 0)
                
                if state.current_idx < (len(questions_list) - 1):
                    ui.button(texts["next"], on_click=lambda: [setattr(state, 'current_idx', state.current_idx + 1), render_ui_content.refresh()])
                else:
                    ui.button(texts["finish"], on_click=run_analysis).props('color=green')

render_ui_content()
ui.run(port=8080, title="MBTI Explorer", favicon="🚀")
