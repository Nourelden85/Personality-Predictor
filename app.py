import streamlit as st
import joblib
import json
import os
import numpy as np
import pandas as pd

st.set_page_config(page_title="MBTI Explorer", page_icon="🧠", layout="centered")

@st.cache_resource
def load_resources():
    base_path = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(base_path, "models")
    
    models = {
        'IE': joblib.load(os.path.join(models_path, "Is_Extrovert_model.pkl")),
        'SN': joblib.load(os.path.join(models_path, "Is_Sensor_model.pkl")),
        'TF': joblib.load(os.path.join(models_path, "Is_Thinker_model.pkl")),
        'JP': joblib.load(os.path.join(models_path, "Is_Judger_model.pkl"))
    }
    
    with open(os.path.join(base_path, "data", "metadata", "mbti_data.json"), "r", encoding="utf-8") as f:
        mbti_db = json.load(f)
    
    X_train = pd.read_csv(os.path.join(base_path, "data", "processed", "x_train.csv"), encoding="latin1")
    questions_list = X_train.columns.tolist()

    return models, mbti_db, questions_list

models, mbti_db, questions = load_resources()


QUESTIONS_PER_PAGE = 5
total_pages = (len(questions) // QUESTIONS_PER_PAGE)

if 'page' not in st.session_state:
    st.session_state.page = 0
if 'all_answers' not in st.session_state:
    st.session_state.all_answers = [0] * len(questions)

st.title("MBTI Personality Test 🧠")
st.write("Explore your personality type and discover famous personalities who share your traits!")

progress_value = st.session_state.page / total_pages
st.progress(progress_value)

if st.session_state.page < total_pages:
    st.subheader(f"Page {st.session_state.page + 1} of {total_pages}")

    start_idx = st.session_state.page * QUESTIONS_PER_PAGE
    end_idx = start_idx + QUESTIONS_PER_PAGE
    with st.form(key=f"page_{st.session_state.page}"):
        page_answers = []
        for idx in range(start_idx, min(end_idx, len(questions))):
            st.write(f"**{idx + 1}. {questions[idx]}**")
            ans = st.radio("Choose your answer:", options=[-3, -2, -1, 0, 1, 2, 3], index=3, horizontal=True, key=f"q_{idx}")
            page_answers.append(ans)
            st.divider()
        button_label = "Finish 🏁" if st.session_state.page == total_pages - 1 else "Next Page ➡️"
        sumbit_button = st.form_submit_button(label=button_label)
        if sumbit_button:
            for idx, val in enumerate(page_answers):
                st.session_state.all_answers[start_idx + idx] = val

            st.session_state.page += 1
            st.rerun()

else:
    if 'balloons_done' not in st.session_state:
        st.balloons()
        st.session_state.balloons_done = True
    st.success("You have completed the questions! Analyzing your results...")
    
    user_input = np.array(st.session_state.all_answers).reshape(1, -1)
    res_IE = models['IE'].predict(user_input)[0]
    res_SN = models['SN'].predict(user_input)[0]
    res_TF = models['TF'].predict(user_input)[0]
    res_JP = models['JP'].predict(user_input)[0]

    if res_IE == 1:
        res_IE = 'E'
    else:
        res_IE = 'I'

    if res_SN == 1:
        res_SN = 'S'
    else:
        res_SN = 'N'

    if res_TF == 1:
        res_TF = 'T'
    else:
        res_TF = 'F'

    if res_JP == 1:
        res_JP = 'J'
    else:
        res_JP = 'P'

    mbti_type = f"{res_IE}{res_SN}{res_TF}{res_JP}"
    st.header(f"Your Personality Type: {mbti_type}")
    
    info = mbti_db['mbti_database'][mbti_type]
    st.subheader(info['title'])
    st.info(info['description'])
    
    st.divider()
    st.write("### Famous People with Similar Personality Types:")
    
    cols = st.columns(2)
    for idx, celeb in enumerate(info['famous_people']):
        with cols[idx % 2]:
            raw_path = celeb['image_path']
            if raw_path.startswith("/"):
                raw_path = raw_path[1:]
            base_path = os.path.dirname(os.path.abspath(__file__))
            full_image_path = os.path.join(base_path, raw_path)

            if os.path.exists(full_image_path):
                st.image(full_image_path, width="stretch")
            else:
                st.warning(f"Image not found: {celeb['name']}")
                st.write(f"Check path: {full_image_path}")
                
            st.write(f"**{celeb['name']}**")
            st.caption(celeb['bio'])

    if st.button("Restart Test 🔄"):
        st.session_state.page = 0
        st.session_state.all_answers = [0] * len(questions)
        for key in list(st.session_state.keys()):
            if key.startswith("q_") or key == "balloons_done":
                del st.session_state[key]
        st.rerun()
