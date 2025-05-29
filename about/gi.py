import streamlit as st
import pandas as pd
from openai import OpenAI

st.markdown("""
<h2>🗂️ GI지수</h2>
<p style="color:#555; margin-bottom:18px;">
음식의 GI지수를 검색하세요.<br>
최근 공복 혈당 수치에 따른 알맞은 GI 음식을 알려드려요.
</p>
""", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

csv_path = "data/gi_data.csv"
df_gi = pd.read_csv(csv_path)
# — 검색 UI —
st.markdown("#### 🖱️ GI지수 검색")
search = st.text_input("음식명 검색")
filtered = df_gi[df_gi["음식명"].str.contains(search, case=False)] if search else df_gi

if search.strip():
    if not filtered.empty:
        # 데이터가 있으면 표 출력
        df_display = filtered.copy()
        df_display = df_display[["음식명", "GI지수", "분류"]].astype({"GI지수": str})
        st.dataframe(df_display.to_dict(orient="records"), use_container_width=True)
    else:
        # 없으면 AI에게 간단히 물어보기
        st.warning(f"'{search}'에 대한 GI지수 정보가 없습니다.")
        
        if st.button("🤖 AI에게 GI지수 물어보기"):
            try:
                with st.spinner("AI가 조회 중..."):
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    resp = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system",
                             "content": (
                                 "당신은 GI지수 전문 지식이 있는 어시스턴트입니다. "
                                 "대답은 최대한 짧고 간단하게, '음식명의 GI지수는 XX입니다.' "
                                 "포맷으로만 작성해 주세요."
                             )},
                            {"role": "user",
                             "content": f"다음 음식의 GI지수를 알려주세요: {search}"}
                        ]
                    )
                    answer = resp.choices[0].message.content.strip()
                st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
                st.markdown(f"**🤖 AI의 간단 답변:** {answer}")
                st.success("정확한 정보를 알고 싶다면 챗봇에게 질문해주세요!")
            except Exception as e:
                st.error(f"⚠️ AI 호출 중 오류가 발생했습니다: {e}")
else:
    df_display = filtered.copy()
    df_display = df_display[["음식명", "GI지수", "분류"]].astype({"GI지수": str})
    st.dataframe(df_display.to_dict(orient="records"), use_container_width=True)

st.markdown("---")

# — 이하 공복혈당 입력 및 추천 식단 (기존 코드 그대로) —
st.markdown("#### 📋 최근 공복혈당 입력")
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
fasting_glucose = st.number_input("공복혈당 입력", min_value=60, max_value=400, value=100)

def glucose_status(val):
    if val < 100:
        return "정상"
    elif val <= 125:
        return "경계(전당뇨)"
    else:
        return "높음(당뇨범위)"

status = glucose_status(fasting_glucose)

if status == "정상":
    st.success("🥗 정상범위 입니다. 꾸준히 저GI 음식을 드시고 계시네요!")
elif status == "경계(전당뇨)":
    st.warning("⚠️ 경계범위 입니다. 저GI 음식과 단백질, 채소를 함께 드시는게 좋아요.")
else:
    st.error("❗ 위험범위 입니다. 꼭 저GI 음식 위주로 드세요.")
st.markdown("---")
st.info("🤖 더 자세한 식단 추천은 챗봇에게 질문하세요!")