import streamlit as st

st.set_page_config(page_title="치료", page_icon="💊")

st.markdown("<h2>💊 당뇨 치료 가이드</h2>", unsafe_allow_html=True)
st.markdown("<p>정기적인 관리와 치료를 통해 합병증을 예방하고 건강을 지킬 수 있어요.</p>", unsafe_allow_html=True)

def treatment_card(title, emoji, description, color):
    st.markdown(f"""
        <div style='background-color: {color}; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='margin-bottom:10px;'>{emoji} <strong>{title}</strong></h4>
            <p style='margin: 0;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

with st.expander("💊 당뇨 약물 설명"):
    treatment_card(
        "메트포르민",
        "💊",
        "제2형 당뇨의 1차 치료제로 가장 널리 사용됩니다. 간에서 포도당 생성을 억제하고, 인슐린 감수성을 높이며, 체중 증가나 저혈당 위험이 적습니다.",
        "#f3e5f5"
    )

    treatment_card(
        "글리메피리드 / 글리클라지드 / 글리벤클라미드",
        "💊",
        "이들은 '설폰요소제' 계열로, 췌장에서 인슐린 분비를 촉진합니다. 혈당을 빠르게 낮출 수 있지만 저혈당 위험이 존재하며 체중 증가도 동반될 수 있습니다.",
        "#f3e5f5"
    )

    treatment_card(
        "DPP-4 억제제",
        "💊",
        "인크레틴 호르몬을 분해하는 효소(DPP-4)를 억제해 인슐린 분비를 증가시키고 글루카곤을 억제합니다. 저혈당 위험이 낮고 체중에 영향이 적습니다.",
        "#f3e5f5"
    )

    treatment_card(
        "SGLT-2 억제제",
        "💊",
        "신장을 통해 포도당을 소변으로 배출시켜 혈당을 낮춥니다. 체중 감소, 혈압 감소, 심장·신장 보호 효과도 보고되고 있어 최근 많이 사용됩니다.",
        "#f3e5f5"
    )

    treatment_card(
        "GLP-1 유사체",
        "💉",
        "인크레틴(GLP-1) 유사 호르몬을 모방해 인슐린 분비를 촉진하고 식욕을 억제하며 체중 감량에 효과적입니다. 주사제로 사용되며 위 배출 지연 작용도 있습니다.",
        "#f3e5f5"
    )

    treatment_card(
        "인슐린",
        "🩸",
        "제1형 당뇨는 필수, 제2형 당뇨에서도 약물만으로 조절이 어려운 경우 사용됩니다. 식사 전 또는 장기 지속형으로 투여되며, 지속적인 혈당 모니터링이 필요합니다.",
        "#f3e5f5"
    )


with st.expander("📉 혈당 모니터링"):
    treatment_card(
        "정기적인 혈당 체크",
        "📉",
        """
        자가 혈당 측정기를 통해 공복 및 식후 혈당을 확인하고, 이상 수치를 빠르게 조정할 수 있도록 도와줍니다.

        🔎 **정상 건강 지표 참고 범위**  
        - **공복 혈당**: 70 ~ 99 mg/dL  
        - **당화혈색소 (HbA1c)**: 4.0 ~ 5.6%  
        - **혈압 (수축기 / 이완기)**: 90~119 / 60~79 mmHg  

        위 수치를 초과하거나 지속적으로 변동이 큰 경우, 반드시 전문가와 상담이 필요합니다.
        """,
        "#e3f2fd"
    )

with st.expander("🏃 생활습관 개선"):
    treatment_card(
        "건강한 일상 습관",
        "🏃",
        """
        운동, 체중 감량, 금연, 스트레스 관리 등은 약물만큼이나 중요한 요소예요. 특히,

        ✔ **운동**은 주 150분 이상 유산소 운동 + 근력운동 병행  
        ✔ **식사**는 혈당지수(GI)가 낮은 식품 위주, 일정한 식사 시간 유지  
        ✔ **체중 감량**은 전체 체중의 5~10%만 줄여도 혈당 개선에 큰 효과  
        ✔ **수면 부족과 스트레스**는 혈당 급등을 유발하므로 반드시 관리 필요

        🧘 생활 전반의 **균형 있는 루틴**이 혈당 안정에 직접적인 영향을 줍니다!
        """,
        "#e8f5e9"
    )

