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
    
    # 1. تجهيز المدخلات
    user_input = np.array(st.session_state.all_answers).reshape(1, -1)
    results = {}
    probs = {}

    traits_info = {
        'IE': ('Introvert', 'Extrovert'),
        'SN': ('Intuitive', 'Sensing'),
        'TF': ('Feeling', 'Thinking'),
        'JP': ('Perceiving', 'Judger')
    }

    # 2. حساب التوقعات والنسب
    for key, (label0, label1) in traits_info.items():
        model = models[key]
        prediction = model.predict(user_input)[0]
        results[key] = label1 if prediction == 1 else label0
        probs[key] = model.predict_proba(user_input)[0][1]

    # 3. تكوين كود الـ MBTI
    mbti_type = (
        f"{'E' if results['IE']=='Extrovert' else 'I'}"
        f"{'S' if results['SN']=='Sensing' else 'N'}"
        f"{'T' if results['TF']=='Thinking' else 'F'}"
        f"{'J' if results['JP']=='Judger' else 'P'}"
    )
    
    st.header(f"Your Personality Type: {mbti_type}")

    # 4. عرض الـ Progress Bars
    st.write("### Personality Traits Breakdown")
    for key, (label0, label1) in traits_info.items():
        score = probs[key]
        percentage = score * 100
        st.write(f"**{label0} vs {label1}**")
        st.progress(score)
        col_left, col_right = st.columns(2)
        with col_left:
            st.caption(f"{label0}: {100 - percentage:.1f}%")
        with col_right:
            st.caption(f"{label1}: {percentage:.1f}%")
        st.write("")

    st.divider()
    
    # 5. عرض تفاصيل الشخصية والمشاهير (داخل شرط التأكد من وجود النوع)
    if mbti_type in mbti_db['mbti_database']:
        info = mbti_db['mbti_database'][mbti_type]
        st.subheader(info['title'])
        st.info(info['description'])
        
        st.write("### Famous People with Similar Personality Types:")
        cols = st.columns(2)
        for idx, celeb in enumerate(info['famous_people']):
            with cols[idx % 2]:
                raw_path = celeb['image_path'].lstrip("/") # تنظيف المسار
                base_path = os.path.dirname(os.path.abspath(__file__))
                full_image_path = os.path.join(base_path, raw_path)

                if os.path.exists(full_image_path):
                    st.image(full_image_path, use_container_width=True) # التعديل الجديد لـ streamlit
                else:
                    st.warning(f"Image not found: {celeb['name']}")
                
                st.write(f"**{celeb['name']}**")
                st.caption(celeb['bio'])
    else:
        st.error(f"Personality type {mbti_type} data is missing from the database.")

    # 6. زر إعادة الاختبار
    if st.button("Restart Test 🔄"):
        st.session_state.page = 0
        st.session_state.all_answers = [0] * len(questions)
        for key in list(st.session_state.keys()):
            if key.startswith("q_") or key == "balloons_done":
                del st.session_state[key]
        st.rerun()