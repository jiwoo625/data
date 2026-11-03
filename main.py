from pathlib import Path
import json

import pandas as pd
import streamlit as st


        with RECORD_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)
        return {
            "meanings": saved.get("meanings", {}),
            "source": saved.get("source", ""),
        }
    except (json.JSONDecodeError, OSError):
        st.warning("기존 기록 파일을 읽지 못했습니다. 새 기록으로 시작합니다.")
        return {"meanings": {}, "source": ""}


def save_notes(meanings, source):
    """입력한 설명과 출처를 UTF-8 JSON 파일로 저장합니다."""
    RECORD_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "meanings": meanings,
        "source": source,
    }
    with RECORD_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


# ---------------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL, encoding="utf-8")


try:
    df = load_data()
except Exception as error:
    st.error("데이터를 불러오지 못했습니다. 인터넷 연결과 데이터 주소를 확인해 주세요.")
    st.exception(error)
    st.stop()

required_columns = [
    "id", "gender", "age", "hypertension", "heart_disease",
    "ever_married", "work_type", "Residence_type",
    "avg_glucose_level", "bmi", "smoking_status", "stroke",
]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    st.error(f"데이터에 필요한 열이 없습니다: {', '.join(missing_columns)}")
    st.stop()

notes = load_notes()


# ---------------------------------------------------------
# 화면
# ---------------------------------------------------------
st.title(f"🧠 {APP_TITLE}")
st.write(
    "이 실습실은 뇌졸중 관련 데이터를 살펴보고 각 열의 의미를 정리하는 공간입니다. "
    "먼저 데이터의 전체 규모와 열 구성을 확인한 뒤, 교재를 참고해 우리말 뜻과 출처를 기록해 보세요."
)
st.caption("※ 이 앱은 데이터 탐색 학습용이며, 개인의 건강 상태나 뇌졸중 발생 가능성을 진단·예측하지 않습니다.")

total_people = len(df)
column_count = len(df.columns)
stroke_count = int((df["stroke"] == 1).sum())
stroke_ratio = (stroke_count / total_people * 100) if total_people else 0.0

metric_cols = st.columns(4)
metric_cols[0].metric("전체 사람 수", f"{total_people:,}명")
metric_cols[1].metric("열 개수", f"{column_count:,}개")
metric_cols[2].metric("stroke가 1인 사람 수", f"{stroke_count:,}명")
metric_cols[3].metric("stroke가 1인 비율", f"{stroke_ratio:.2f}%")

st.divider()
st.subheader("1. 데이터 열 살펴보기")
st.write("‘우리말 뜻’ 칸을 교재를 참고해 직접 채워 보세요. 입력한 내용은 아래 저장 버튼을 눌러 보관할 수 있습니다.")

meanings_saved = notes.get("meanings", {})
column_rows = []
for column in df.columns:
    if pd.api.types.is_numeric_dtype(df[column]):
        kind = f"수치형 ({df[column].nunique(dropna=True):,}종류)"
    else:
        kind = f"범주형 ({df[column].nunique(dropna=True):,}종류)"

    column_rows.append({
        "열 이름": column,
        "우리말 뜻": meanings_saved.get(column, ""),
        "값의 종류": kind,
        "빈 값 개수": int(df[column].isna().sum()),
    })

columns_df = pd.DataFrame(column_rows)
edited_columns = st.data_editor(
    columns_df,
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    disabled=["열 이름", "값의 종류", "빈 값 개수"],
    column_config={
        "열 이름": st.column_config.TextColumn("열 이름"),
        "우리말 뜻": st.column_config.TextColumn(
            "우리말 뜻",
            help="교재를 참고해 각 열의 뜻을 직접 입력하세요.",
            width="large",
        ),
        "값의 종류": st.column_config.TextColumn("값의 종류"),
        "빈 값 개수": st.column_config.NumberColumn("빈 값 개수", format="%d"),
    },
    key="column_meanings_editor",
)

st.divider()
st.subheader("2. 데이터 미리보기")
st.write("원본 데이터의 처음 다섯 줄입니다. 값은 별도로 가공하지 않고 그대로 표시합니다.")
st.dataframe(df.head(5), hide_index=True, use_container_width=True)

st.divider()
st.subheader("3. 데이터 출처 기록")
source_text = st.text_area(
    "데이터 출처",
    value=notes.get("source", ""),
    placeholder="교재에 안내된 데이터 출처를 여기에 입력하세요.",
    height=100,
)

if st.button("우리말 뜻과 출처 저장", type="primary", use_container_width=True):
    updated_meanings = {
        row["열 이름"]: str(row["우리말 뜻"])
        for _, row in edited_columns.iterrows()
