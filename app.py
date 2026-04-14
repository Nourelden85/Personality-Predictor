import streamlit as st
import joblib
import json
import os
import numpy as np
import pandas as pd
import math

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
    
    with open(os.path.join(base_path, "data", "metadata", "questions.json"), "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    q_ids = list(questions.keys())
    q_en_list = [questions[q_id]['en'] for q_id in q_ids]

    return models, mbti_db, questions, q_ids, q_en_list

def ar_num(n):
    if st.session_state.lang == "English": return str(n)
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))

models, mbti_db, questions, q_ids, q_en_list = load_resources()

if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

ui_text = {
    "English": {
        "title": "MBTI Personality Predictor",
        "choose": "Choose your answer:",
        "start": "Start Test 🚀",
        "next": "Next Page ➡️",
        "previous": "Previous Page ⬅️",
        "finish": "Finish & Analyze 🏁",
        "result": "Your Personality Type:",
        "choices": ["Strongly Disagree", "Disagree", "Slightly Disagree", "Neutral", "Slightly Agree", "Agree", "Strongly Agree"],
        "restart": "Restart 🔄",
        "lang_key": "en",
        "description": "Discover your MBTI personality type and see which famous personalities share your traits!",
        "famous_people": "Famous People with Similar Personality Type:",
        "complete": "You have completed the questions! Analyzing your results...",
        "your_type": "Your Personality Type",
        "traits_title": "Traits Analysis"
    },
    "العربية": {
        "title": "محلل الشخصية MBTI",
        "choose": "اختر إجابتك:",
        "start": "ابدأ الاختبار 🚀",
        "next": "الصفحة التالية ⬅️",
        "previous": "الصفحة السابقة ➡️",
        "finish": "إنهاء وتحليل 🏁",
        "result": "نمط شخصيتك هو:",
        "choices": ["أعارض بشدة", "أعارض", "أعارض قليلاً", "محايد", "أوافق قليلاً", "أوافق", "أوافق بشدة"],
        "restart": "إعادة الاختبار 🔄",
        "lang_key": "ar",
        "description": "اكتشف نوع شخصيتك MBTI وشاهد أي الشخصيات الشهيرة تشترك في صفاتك!",
        "famous_people": "الشخصيات الشهيرة ذات نمط الشخصية المشابه:",
        "complete": "لقد أكملت الأسئلة! جاري تحليل نتائجك...",
        "your_type": "نوع شخصيتك هو",
        "traits_title": "تحليل السمات"
    }
}

language = ui_text[st.session_state.lang]
if st.session_state.lang == "العربية":
    st.markdown("""
        <style>
        /* قلب التطبيق بالكامل */
        .stApp { direction: rtl; text-align: right; }
        [data-testid="stVerticalBlock"] > div { direction: rtl; text-align: right; }
        
        /* عكس اتجاه شريط التقدم (Progress Bar) */
        div[data-testid="stProgress"] > div > div > div > div {
            flex-direction: row-reverse !important;
        }
        /* في بعض إصدارات ستريم ليت نستخدم الـ scale لعكس الشريط */
        div[data-testid="stProgress"] div[role="progressbar"] > div {
            transform: scaleX(-1);
            transform-origin: center;
        }

        /* تعديل الراديو بوتون ليكون النص يمين الدائرة */
        [data-testid="stRadio"] label { 
            flex-direction: row-reverse !important; 
            text-align: right !important; 
            justify-content: flex-end !important; 
            width: 100%; 
        }
        
        /* محاذاة العناوين والنصوص */
        h1, h2, h3, h4, p, span, label { text-align: right !important; direction: rtl !important; }
        
        /* تعديل القوائم المنسدلة */
        div[data-baseweb="select"] { direction: rtl; }
        </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 0
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'all_answers' not in st.session_state:
    st.session_state.all_answers = [0] * len(q_ids)

st.title(language['title'])
col_title, col_lang = st.columns([3, 1])

with col_lang:
    lang_options = ["English", "العربية"]
    current_idx = lang_options.index(st.session_state.lang)
    
    selected_lang = st.selectbox(
        "🌐 Language", 
        options=lang_options, 
        index=current_idx,
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
language = ui_text[st.session_state.lang]




if not st.session_state.test_started:
    st.markdown(f"### {'Welcome!' if st.session_state.lang == 'English' else 'مرحباً بك!'}")
    st.write(language['description'])
    if st.button(language['start'], use_container_width=True):
        st.session_state.test_started = True
        st.rerun()

else:
    QUESTIONS_PER_PAGE = 5
    total_pages = math.ceil((len(q_ids) / QUESTIONS_PER_PAGE))
    if st.session_state.page < total_pages:
        progress_value = (st.session_state.page + 1) / total_pages
        st.progress(progress_value)
        st.subheader(f"{'Page' if st.session_state.lang == 'English' else 'صفحة'} {ar_num(st.session_state.page + 1)} / {ar_num(total_pages)}")

        start_idx = st.session_state.page * QUESTIONS_PER_PAGE
        end_idx = start_idx + QUESTIONS_PER_PAGE
        with st.form(key=f"page_{st.session_state.page}"):
            page_answers = []
            current_page_ids = q_ids[start_idx:end_idx]
            for i, qid in enumerate(current_page_ids):
                real_idx = start_idx + i + 1

                lang_key = language['lang_key']
                q_text = questions[qid][lang_key]
                
                st.write(f"**{ar_num(real_idx)}. {q_text}**")
                
                ans = st.radio(language['choose'],
                                options=[-3, -2, -1, 0, 1, 2, 3],
                                index=3,
                                format_func=lambda x: language['choices'][x + 3],
                                horizontal=False,
                                key=f"q_{qid}")
                page_answers.append(ans)
                st.divider()
            button_label = language['finish'] if st.session_state.page == total_pages - 1 else language['next']
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
        st.success(language['complete'])
        
        user_input = np.array(st.session_state.all_answers).reshape(1, -1)
        res_IE = models['IE'].predict(user_input)[0]
        res_SN = models['SN'].predict(user_input)[0]
        res_TF = models['TF'].predict(user_input)[0]
        res_JP = models['JP'].predict(user_input)[0]

        res_IE_proba = models['IE'].predict_proba(user_input)[0]
        res_SN_proba = models['SN'].predict_proba(user_input)[0]
        res_TF_proba = models['TF'].predict_proba(user_input)[0]
        res_JP_proba = models['JP'].predict_proba(user_input)[0]

        res_IE = 'E' if res_IE == 1 else 'I'
        res_SN = 'S' if res_SN == 1 else 'N'
        res_TF = 'T' if res_TF == 1 else 'F'
        res_JP = 'J' if res_JP == 1 else 'P'

        mbti_type = f"{res_IE}{res_SN}{res_TF}{res_JP}"
        st.header(f"{language['your_type']}: {mbti_type}")
        
        info = mbti_db['mbti_database'][mbti_type]
        st.subheader(info['title'])
        st.info(info['description'])
        
        st.divider()
        st.write(f"### {language['traits_title']}")
        
        res_probs = [
            (res_IE, models['IE'].predict_proba(user_input)[0]),
            (res_SN, models['SN'].predict_proba(user_input)[0]),
            (res_TF, models['TF'].predict_proba(user_input)[0]),
            (res_JP, models['JP'].predict_proba(user_input)[0])
        ]

        trait_names = {
            "E": {"English": "Extroverted", "العربية": "منفتح"}, "I": {"English": "Introverted", "العربية": "متحفظ"},
            "S": {"English": "Sensing", "العربية": "حسي"}, "N": {"English": "Intuitive", "العربية": "حدسي"},
            "T": {"English": "Thinking", "العربية": "عقلاني"}, "F": {"English": "Feeling", "العربية": "عاطفي"},
            "J": {"English": "Judging", "العربية": "حازم"}, "P": {"English": "Prospecting", "العربية": "مرن"}
        }

        for trait_char, proba in res_probs:
            score = proba[1] if trait_char in ['E', 'S', 'T', 'J'] else proba[0]
            display_name = trait_names[trait_char][st.session_state.lang]
            col_lbl, col_br = st.columns([1, 3])
            with col_lbl: st.write(f"**{display_name}**")
            with col_br:
                st.progress(float(score))
                st.caption(ar_num(f"{int(score * 100)}%"))
        st.write(f"### {language['famous_people']}")
        
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

        if st.button(language['restart'], use_container_width=True):
            st.session_state.page = 0
            st.session_state.all_answers = [0] * len(questions)
            for key in list(st.session_state.keys()):
                if key.startswith("q_") or key == "balloons_done" or key == "test_started":
                    del st.session_state[key]
            st.rerun()
