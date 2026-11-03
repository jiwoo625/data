from pathlib import Path
import json

import pandas as pd
import streamlit as st


APP_TITLE = "뇌졸중 예측 실습실"
DATA_URL = "https://raw.githubusercontent.com/jiwoo625/data/refs/heads/main/stroke.csv"

BASE_DIR = Path(__file__).resolve().parent
RECORD_DIR = BASE_DIR / "내_기록"
RECORD_FILE = RECORD_DIR / "설명_및_출처.json"

st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")


def load_notes():
    if not RECORD_FILE.exists():
        return {"meanings": {}, "source": ""}

    try:
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            "meanings": data.get("meanings", {}),
            "source": data.get("source", ""),
        }
    except (OSError, json.JSONDecodeError):
        return {"meanings": {}, "source": ""}


def save_notes(meanings, source):
    RECORD_DIR.mkdir(parents=True, exist_ok=True)
    data = {"meanings": meanings, "source": source}
    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL, encoding="utf-8")


st.title("🧠 " + APP_TITLE)
st.write("뇌졸중 관련 데이터를 살펴보고 각 열의 의미를 정리하는 학습용 앱입니다.")
st.info("이 앱은 학습용 데이터 탐색 도구이며, 개인의 건강 상태를 진단하거나 뇌졸중 위험을 판정하지 않습니다.")

try:
    df = load_data()
except Exception as error:
    st.error("데이터를 불러오지 못했습니다. 인터넷 연결과 데이터 주소를 확인하세요.")
    st.code(str(error))
    st.stop()

required_columns = [
    "id",
    "gender",
    "age",
    "hypertension",
    "heart_disease",
    "ever_married",
    "work_type",
    "Residence_type",
    "avg_glucose_level",
    "bmi",
    "smoking_status",
    "stroke",
]

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error("필요한 열이 데이터에 없습니다: " + ", ".join(missing_columns))
    st.stop()

notes = load_notes()

total_people = len(df)
column_count = len(df.columns)
stroke_count = int((df["stroke"] == 1).sum())
stroke_ratio = (stroke_count / total_people * 100) if total_people > 0 else 0

card1, card2, card3, card4 = st.columns(4)
card1.metric("전체 사람 수", f"{total_people:,}명")
card2.metric("열 개수", f"{column_count:,}개")
card3.metric("stroke가 1인 사람 수", f"{stroke_count:,}명")
card4.metric("stroke가 1인 비율", f"{stroke_ratio:.2f}%")

st.divider()
st.subheader("1. 데이터 열 살펴보기")
st.write("각 열의 우리말 뜻을 교재를 참고해 입력하세요.")

meaning_rows = []
saved_meanings = notes.get("meanings", {})

for col in df.columns:
