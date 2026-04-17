UI_TEXTS = {
    "English": {
        "dir": "ltr",
        "title": "MBTI Personality Predictor",
        "question_of": "Question {} of {}",
        "start": "Start Test 🚀",
        "next": "Next Page ➡️",
        "previous": "Previous Page ⬅️",
        "finish": "Finish & Analyze 🏁",
        "choices": ["Strongly Disagree", "Disagree", "Slightly Disagree", "Neutral", "Slightly Agree", "Agree", "Strongly Agree"],
        "restart": "Restart 🔄",
        "lang_key": "en",
        "description": "Discover your MBTI personality type and see which famous personalities share your traits!",
        "famous_people": "Famous People with Similar Personality Type",
        "your_type": "Your Personality Type",
        "population": "Population:",
        "traits_title": "Traits Analysis",
        "traits_map": {
            "E": "Extroverted", "I": "Introverted",
            "S": "Sensing", "N": "Intuitive",
            "T": "Thinking", "F": "Feeling",
            "J": "Judging", "P": "Prospecting"
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
        "choices": ["أعارض بشدة", "أعارض", "أعارض قليلاً", "محايد", "أوافق قليلاً", "أوافق", "أوافق بشدة"],
        "restart": "إعادة الاختبار 🔄",
        "lang_key": "ar",
        "description": "اكتشف نوع شخصيتك MBTI وشاهد أي الشخصيات الشهيرة تشترك في صفاتك!",
        "famous_people": "الشخصيات الشهيرة ذات نمط الشخصية المشابه",
        "your_type": "نوع شخصيتك هو",
        "population": "نسبة الانتشار:",
        "traits_title": "تحليل السمات",
        "traits_map": {
            "E": "منفتح", "I": "متحفظ",
            "S": "حسي", "N": "حدسي",
            "T": "عقلاني", "F": "عاطفي",
            "J": "حازم", "P": "مرن"
        }
    }
}

def ar_num(n, lang):
    if lang == "English": return str(n)
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
