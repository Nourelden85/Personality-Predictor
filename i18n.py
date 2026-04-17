UI_TEXTS = {
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
        "traits_title": "Traits Analysis",
        "traits_map": {
            "E": "Extroverted", "I": "Introverted",
            "S": "Sensing", "N": "Intuitive",
            "T": "Thinking", "F": "Feeling",
            "J": "Judging", "P": "Prospecting"
        }
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
