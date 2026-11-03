from pathlib import Path
import json

import pandas as pd
import streamlit as st


APP_TITLE = "뇌졸중 예측 실습실"
DATA_URL = "https://raw.githubusercontent.com/jiwoo625/data/refs/heads/main/stroke.csv"

BASE_DIR = Path(__file__).resolve().parent
RECORD_DIR = BASE_DIR / "내_기록"
RECORD_FILE = RECORD_DIR / "설명_및_출처.json"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
)


def load_notes():
    """JSON 파일에서 저장된 설명과 출처를 읽습니다."""
    if not RECORD_FILE.exists():
        return {"meanings": {}, "source": ""}

    try:
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)

        return {
            "meanings": saved.get("meanings", {}),
            "source": saved.get("source", ""),
        }
    except (json.JSONDecodeError, OSError):
        st.warning("기존 기록 파일을 읽지 못했습니다. 빈 기록으로 시작합니다.")
        return {"meanings": {}, "source": ""}


def save_notes(meanings, source):
    """설명과 출처를 JSON 파일로 저장합니다."""
    RECORD_DIR.mkdir(parents=True, exist_ok=True)

    saved_data = {
        "meanings": meanings,
        "source": source,
    }

    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(saved_data, file, ensure_ascii=False, indent=2)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL, encoding="utf-8")


try:
    df = load_data()
except Exception as error:
    st.error("CSV 데이터를 불러오지 못했습니다. 데이터 주소와 인터넷 연결을 확인하세요.")
    st.exception(error)
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

missing_columns = [name for name in required_columns if name not in df.columns]

if missing_columns:
    st.error(f"CSV 파일에 필요한 열이 없습니다: {', '.join(missing_columns)}")
    st.stop()


notes = load_notes()


# 제목과 데이터 소개
st.title(f"🧠 {APP_TITLE}")
st.write(
    "이 실습실에서는 뇌졸중 관련 데이터를 살펴보고 각 열의 의미를 정리합니다. "
    "교재를 참고해 우리말 뜻과 데이터 출처를 직접 입력해 보세요."
