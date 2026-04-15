import joblib
import json
import os
import numpy as np
import pandas as pd
from nicegui import ui
from functools import lru_cache
import math

# -----------------------------
# STATE
# -----------------------------
answers = {}
current_page = 0
page_size = 8
language = {'value': 'English'}

# -----------------------------
# LOAD RESOURCES
# -----------------------------
@lru_cache(maxsize=1)
def load_resources():
    base_path = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(base_path, "models")

    models = {
        'IE': joblib.load(os.path.join(models_path, "Is_Extrovert_model.pkl")),
        'SN': joblib.load(os.path.join(models_path, "Is_Sensor_model.pkl")),
        'TF': joblib.load(os.path.join(models_path, "Is_Thinker_model.pkl")),
        'JP': joblib.load(os.path.join(models_path, "Is_Judger_model.pkl"))
    }

    with open(
        os.path.join(base_path, "data", "metadata", "mbti_data.json"),
        "r",
        encoding="utf-8"
    ) as f:
        mbti_db = json.load(f)

    X_train = pd.read_csv(
        os.path.join(base_path, "data", "processed", "x_train.csv"),
        encoding="latin1"
    )

    questions = X_train.columns.tolist()

    return models, mbti_db, questions


models, mbti_db, questions = load_resources()

# -----------------------------
# HELPERS
# -----------------------------
def get_bio(person):
    if language['value'] == "Arabic":
        return person.get("bio_ar", person["bio_en"])
    return person["bio_en"]

def get_desc(data):
    if language['value'] == "Arabic":
        return data.get("description_ar", data.get("description_en", ""))
    return data.get("description_en", "")

# -----------------------------
# PREDICT
# -----------------------------
def predict_mbti():
    user_input = [answers.get(q, 0) for q in questions]

    IE = models['IE'].predict([user_input])[0]
    SN = models['SN'].predict([user_input])[0]
    TF = models['TF'].predict([user_input])[0]
    JP = models['JP'].predict([user_input])[0]

    return f"{'E' if IE else 'I'}{'N' if SN else 'S'}{'T' if TF else 'F'}{'J' if JP else 'P'}"

# -----------------------------
# NAVIGATION
# -----------------------------
welcome_page = ui.column()
quiz_page = ui.column().set_visibility(False)
result_page = ui.column().set_visibility(False)

# -----------------------------
# WELCOME PAGE
# -----------------------------
with welcome_page:
    ui.label("Welcome to MBTI Predictor").classes("text-2xl font-bold")

    lang_radio = ui.radio(["English", "Arabic"], value="English")

    def start():
        global current_page, answers
        current_page = 0
        answers = {}

        language['value'] = lang_radio.value

        welcome_page.set_visibility(False)
        quiz_page.set_visibility(True)

        render_questions()

    ui.button("Start", on_click=start)

# -----------------------------
# QUIZ LOGIC
# -----------------------------
def get_current_questions():
    start = current_page * page_size
    end = start + page_size
    return questions[start:end]

def render_questions():
    quiz_page.clear()

    with quiz_page:

        ui.label("Answer the questions").classes("text-xl")

        total_pages = math.ceil(len(questions) / page_size)
        progress = (current_page + 1) / total_pages

        ui.linear_progress(value=progress)

        ui.label(f"Page {current_page + 1} / {total_pages}")

        for q in get_current_questions():

            with ui.card().classes("w-full p-3"):
                ui.label(q)

                ui.slider(
                    min=-3,
                    max=3,
                    step=1,
                    value=0,
                    on_change=lambda e, q=q: answers.update({q: e.value})
                )

        def next_page():
            global current_page

            if (current_page + 1) * page_size >= len(questions):
                show_result()
            else:
                current_page += 1
                render_questions()

        ui.button("Next", on_click=next_page)

# -----------------------------
# RESULT PAGE
# -----------------------------
def show_result():
    quiz_page.set_visibility(False)
    result_page.set_visibility(True)

    mbti = predict_mbti()
    data = mbti_db[mbti]

    with result_page:
        ui.label(f"Your MBTI Type: {mbti}").classes("text-2xl font-bold")
        ui.label(data["title"])

        ui.label(get_desc(data))

        ui.separator()
        ui.label("Famous People:")

        for person in data["famous_people"]:
            with ui.card().classes("w-full"):
                ui.label(person["name"])
                ui.label(get_bio(person))

# -----------------------------
# RUN APP
# -----------------------------
ui.run(title="MBTI Predictor")