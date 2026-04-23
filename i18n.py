UI_TEXTS = {
    "English": {
        "dir": "ltr",
        "title": "MBTI Personality Predictor",
        "question_of": "Question {} of {}",
        "start": "Start Test 🚀",
        "next": "Next Page ➡️",
        "previous": "Previous Page ⬅️",
        "finish": "Finish & Analyze 🏁",
        "skip": "Skip to Result",
        "choices": ["Strongly Disagree", "Disagree", "Slightly Disagree", "Neutral", "Slightly Agree", "Agree", "Strongly Agree"],
        "restart": "Restart 🔄",
        "lang_key": "en",
        "description": "Discover your MBTI personality type and see which famous personalities share your traits!",
        "famous_people": "Famous People with Similar Personality Type",
        "population": "Population:",
        "traits_title": "Traits Analysis",
        "traits_map": {
            "E": "Extroverted", "I": "Introverted",
            "S": "Sensing", "N": "Intuitive",
            "T": "Thinking", "F": "Feeling",
            "J": "Judging", "P": "Prospecting"
        },
        "about_test": "What is this test?",
        "about_test_desc": "This test is based on the Myers-Briggs Type Indicator (MBTI), categorizing personalities into 16 distinct types. It helps you better understand yourself, your strengths, and how you interact with the world.",
        "test_tips": "💡 Tip: Answer honestly, and remember there are no right or wrong answers!",
        "comparison_title": "Understanding the 4 Pillars",
        "traits_info": {
        "EI": {
            "left": {"title": "Introvert (I)", "desc": "Focused on the inner world, recharges through solitude and reflection."},
            "right": {"title": "Extravert (E)", "desc": "Focused on the outer world, energized by social interaction and action."}
        },
        "SN": {
            "left": {"title": "Sensor (S)", "desc": "Focuses on physical reality, facts, and what is happening in the present."},
            "right": {"title": "Intuitive (N)", "desc": "Focuses on possibilities, meanings, and the 'big picture' for the future."}
        },
        "TF": {
            "left": {"title": "Thinker (T)", "desc": "Makes decisions based on logic, objective truth, and consistency."},
            "right": {"title": "Feeler (F)", "desc": "Makes decisions based on personal values and the people involved."}
        },
        "JP": {
            "left": {"title": "Judger (J)", "desc": "Prefers order, structure, and having things settled and planned."},
            "right": {"title": "Perceiver (P)", "desc": "Prefers flexibility, spontaneity, and keeping options open."}
        }
    }
    },
    "العربية": {
        "dir": "rtl",
        "title": "محلل الشخصية MBTI",
        "question_of": "السؤال {} من {}",
        "start": "ابدأ الاختبار 🚀",
        "next": "الصفحة التالية ⬅️",
        "previous": "الصفحة السابقة ➡️",
        "finish": "إنهاء وتحليل 🏁",
        "skip": "تخطي وتحليل",
        "choices": ["أعارض بشدة", "أعارض", "أعارض قليلاً", "محايد", "أوافق قليلاً", "أوافق", "أوافق بشدة"],
        "restart": "إعادة الاختبار 🔄",
        "lang_key": "ar",
        "description": "اكتشف نوع شخصيتك MBTI وشاهد أي الشخصيات الشهيرة تشترك في صفاتك!",
        "famous_people": "الشخصيات الشهيرة ذات نمط الشخصية المشابه",
        "population": "نسبة الانتشار:",
        "traits_title": "تحليل السمات",
        "traits_map": {
            "E": "منفتح", "I": "متحفظ",
            "S": "حسي", "N": "حدسي",
            "T": "عقلاني", "F": "عاطفي",
            "J": "حازم", "P": "مرن"
        },
        "about_test": "ما هو هذا الاختبار؟",
        "about_test_desc": "هذا الاختبار مبني على مؤشر مايرز-بريجز (MBTI)، الذي يصنف الشخصيات إلى 16 نوعًا مميزًا. يساعدك على فهم نفسك بشكل أفضل، نقاط قوتك، وكيفية تفاعلك مع العالم.",
        "test_tips": "💡 نصيحة: أجب بصدق وعفوية، وتذكر أنه لا توجد إجابة صحيحة وأخرى خاطئة!",
        "comparison_title": "فهم المحاور الأربعة",
        "traits_info": {
            "EI": {
                "left": {"title": "انطوائي (I)", "desc": "يركز على عالمه الداخلي، يستعيد طاقته بالهدوء."},
                "right": {"title": "انبساطي (E)", "desc": "يركز على العالم الخارجي، يستمد طاقته من التفاعل."}
            },
            "SN": {
                "left": {"title": "حسي (S)", "desc": "يركز على الحقائق، التفاصيل، والواقع الملموس."},
                "right": {"title": "حدسي (N)", "desc": "يركز على الأنماط، الاحتمالات، والأفكار المجردة."}
            },
            "TF": {
                "left": {"title": "منطقي (T)", "desc": "يتخذ قراراته بناءً على المنطق والتحليل الموضوعي."},
                "right": {"title": "عاطفي (F)", "desc": "يتخذ قراراته بناءً على القيم والمشاعر والعلاقات."}
            },
            "JP": {
                "left": {"title": "حازم (J)", "desc": "يفضل النظام، الجدولة، وحسم الأمور مبكراً."},
                "right": {"title": "مرن (P)", "desc": "يفضل العفوية، إبقاء الخيارات مفتوحة، والتكيف."}
            }
        }
    }
}

def ar_num(n, lang):
    if lang == "English": return str(n)
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
