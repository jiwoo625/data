
뇌졸중 예측 앱 작성
에서 이어짐
main.py

수정한 main.py 파일입니다.

main.py

문법 검사 통과
main.py 다운로드

requirements.txt 포함 ZIP 다운로드

기존 GitHub의 data/main.py 내용을 전부 지우고 새 파일의 내용으로 교체한 뒤 저장해 주세요.


main.py
코드
https://raw.githubusercontent.com/jiwoo625/data/refs/heads/main/stroke.csv
보내주신 주소의 CSV 파일을 확인했습니다. 이 주소를 main.py에서 데이터 불러오기 주소로 사용하면 됩니다.

DATA_URL = "https://raw.githubusercontent.com/jiwoo625/data/refs/heads/main/stroke.csv"

확인된 내용:

열 개수: 12개

데이터에 bmi 결측값이 포함되어 있습니다.

CSV 형식이며 UTF-8로 읽도록 설정할 수 있습니다.

기존에 드린 main.py에는 이 주소가 이미 반영되어 있습니다. 따라서 데이터 주소를 따로 수정할 필요는 없습니다.

"뇌졸중 예측 실습실" 스트림릿 앱을 main.py 파일 하나로 만들어 줘.
화면 맨 위에 앱 제목과 어울리는 아이콘을 넣고, 브라우저 탭에도 그 제목이 표시되게 해 줘.
데이터: https://raw.githubusercontent.com/jiwoo625/data/refs/heads/main/stroke.csv
이 파일의 열 이름은 id, gender, age, hypertension, heart_disease, ever_married,
work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke이고,
인코딩은 UTF-8이야. bmi 열에는 빈 값이 있어.
첫 화면은 이 데이터가 무엇인지 소개하는 화면이야.
맨 위에 전체 사람 수, 열 개수, stroke가 1인 사람 수, 그 비율을 큰 숫자 카드 네 개로 보여 줘.
그 아래에 열 이름·우리말 뜻·값의 종류·빈 값 개수를 담은 표를 보여 줘.
우리말 뜻 칸은 비워 두고, 내가 교재를 보고 직접 채워 넣을 수 있게 만들어 줘.
표 아래에 데이터를 처음 다섯 줄만 그대로 보여 줘.
맨 아래에 데이터 출처를 적는 자리를 만들어 줘. 내가 적을 글은 교재에 있어.
우리말 뜻과 출처 칸에 적은 내용은 내_기록 폴더에 json 파일로 저장해서, 새로고침해도 다시 불러오게 해 줘.
사용할 수 있는 라이브러리는 streamlit, pandas, plotly, scikit-learn 네 가지뿐이야.
그림을 그린다면 plotly로만 그려 줘.
requirements.txt도 꼭 같이 만들어 줘. 그 네 가지를 버전 숫자 없이 이름만 적어 줘.

…

요청하신 **「뇌졸중 예측 실습실」**을 main.py와 requirements.txt로 만들었습니다.

Python 문법 검사 통과
파일 다운로드
전체 파일 ZIP

완성
main.py + requirements.txt 다운로드

개별 파일

main.py

requirements.txt

구현된 기능
🧠 앱 제목과 브라우저 탭 아이콘

전체 사람 수, 열 개수, stroke=1 인원과 비율을 큰 카드 4개로 표시

열 이름, 우리말 뜻, 값의 종류, 빈 값 개수 표

우리말 뜻을 직접 입력하고 수정

원본 데이터 처음 5행 표시

데이터 출처 입력 칸

내_기록/설명_및_출처.json에 입력 내용 저장 및 불러오기

사용 방법: ZIP 압축을 풀고 GitHub 저장소의 data/main.py와 requirements.txt를 각각 교체한 다음 Commit changes를 눌러 주세요.

참고로 Streamlit Cloud에서는 로컬 JSON 파일이 재배포나 서버 변경 후에도 영구 보존된다고 보장할 수는 없습니다.


main.py
코드

requirements.txt
문서



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
    """저장된 우리말 뜻과 출처를 불러옵니다."""
    if not RECORD_FILE.exists():
        return {"meanings": {}, "source": ""}

    try:
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)

        return {
            "meanings": saved.get("meanings", {}),
            "source": saved.get("source", ""),
        }
    except (OSError, json.JSONDecodeError):
        st.warning("기존 기록 파일을 읽지 못해 빈 내용으로 시작합니다.")
        return {"meanings": {}, "source": ""}


def save_notes(meanings, source):
    """우리말 뜻과 출처를 JSON 파일로 저장합니다."""
    RECORD_DIR.mkdir(parents=True, exist_ok=True)
    saved = {
        "meanings": meanings,
        "source": source,
    }

    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(saved, file, ensure_ascii=False, indent=2)


@st.cache_data
def load_data():
    """GitHub CSV를 UTF-8 인코딩으로 읽습니다."""
    return pd.read_csv(DATA_URL, encoding="utf-8")


st.title("🧠 뇌졸중 예측 실습실")
st.write(
    "뇌졸중 관련 데이터의 전체 규모와 열 구성을 살펴보는 학습용 앱입니다. "
    "교재를 참고해 각 열의 우리말 뜻과 데이터 출처를 직접 기록해 보세요."
)
st.info(
    "이 앱은 데이터 탐색을 위한 학습용 도구입니다. "
    "개인의 건강 상태를 진단하거나 뇌졸중 발생 가능성을 판단하지 않습니다."
)

try:
    df = load_data()
except Exception as error:
    st.error("CSV 데이터를 불러오지 못했습니다. 인터넷 연결과 데이터 주소를 확인하세요.")
    st.code(str(error))
    st.stop()

expected_columns = [
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

missing_columns = [name for name in expected_columns if name not in df.columns]
if missing_columns:
    st.error("CSV 파일에서 다음 열을 찾을 수 없습니다: " + ", ".join(missing_columns))
    st.stop()

notes = load_notes()

