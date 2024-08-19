import os
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(
    page_title="사회과 수업 도우미",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto",
)

# 더 세련된 Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            font-family: 'Noto Sans KR', sans-serif;
        }
        h1 {
            color: #1e3a8a;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .instructions {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .instructions h3 {
            color: #2563eb;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .section {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1e40af;
        }
        .stTextArea>div>div>textarea {
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }
        .stSelectbox>div>div>select {
            border-radius: 5px;
            border: 1px solid #e5e7eb;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 앱 제목
st.markdown("<h1>질문이 있는 사회과 수업 도우미 📚</h1>", unsafe_allow_html=True)

# 사용 설명서
st.markdown("""
<div class="instructions">
    <h3>사용 설명서 ✏️</h3>
    <ul>
        <li><strong>성취기준 입력하기</strong>: 수업의 성취기준을 간단하게 입력해주세요.</li>
        <li><strong>학년 선택</strong>: 해당 수업의 대상 학년을 선택해주세요.</li>
        <li><strong>수업모형 선택하기</strong>: 원하는 수업모형을 선택해주세요.</li>
        <li>모든 정보를 입력한 후 <strong>'생성하기'</strong> 버튼을 클릭하면, AI가 수업 지도안을 생성합니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 사용자 입력
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    topic_keyword = st.text_area("성취기준 입력하기", height=100, placeholder="성취기준을 간단하게 입력하여 주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    grade_options = ["초등학교 3학년", "초등학교 4학년", "초등학교 5학년", "초등학교 6학년", "중학교 1학년", "중학교 2학년", "중학교 3학년"]
    grade_keyword = st.selectbox("학년을 선택하세요", grade_options)

    subject_options = ["개념 학습", "탐구학습", "문제 해결 학습", "의사 결정 학습", "논쟁문제학습", "STAD 교수·학습"]
    subject_keyword = st.selectbox("수업모형 선택하기", subject_options)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button('생성하기', key='generate_button'):
    with st.spinner('생성 중입니다...'):
        # 키워드 결합
        keywords_combined = f"성취기준: {topic_keyword}, 학년: {grade_keyword}, 수업모형: {subject_keyword}"
        
        # OpenAI API 요청
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": keywords_combined,
                },
                {
                    "role": "system",
                    "content": 
                        "당신은 수업지도안을 전문적으로 작성하는 20년차 교사입니다. 입력 받은 성취기준, 학년, 수업모형을 바탕으로 수업지도안을 5000자 이내로 작성해주세요 "
                        "1. 개념학습을 선택하였다면 문제 제기, 속성 제시, 속성 및 사례 검토, 가설 검증, 개념 분석 5단계로 작성해야 한다."
                        "2. 탐구학습은 준비하기, 가설세우기, 가설 검증하기, 정리하기 4단계로 작성해야 한다. "
                        "3. 문제 해결 학습은 문제 확인, 문제 발생 원인 파악, 문제 해결 방안 탐색, 문제 해결 방안 결정, 문제 해결 방안 실천 5단계로 작성해야 한다."
                        "4. 의사 결정 학습 문제 정의, 대안 나열, 선택 기준 작성, 대안 평가, 의사 결정 5단계로 작성해야 한다."
                        "5. 논쟁문제학습은 문제 제기, 개념의 명확화, 사실의 경험적 확인, 가치 갈등의 해결, 대안 모색 및 결론 5단계로 작성해야 한다. "
                        "6. 협동 학습은 소집단(원모둠) 구성, 전문가 집단 학습, 소집단(원모둠), 전체 학습지 작성 및 정답지 확인 4단계로 작성해야 한다." 
                        "7. 모든 수업은 학생들이 좋아하는 다양한 놀이와 게임, 퀴즈, 학생 활동이 중심이 되는 수업이 각 수업의 각 단계마다 들어가야 한다."
                        "8. 모든 수업의 각 단계마다 다양한 사례와 예시 자료를 통해서 학생들이 흥미와 관심을 가지도록 해야 한다."
                        "9. 수업의 각 단계마다 필요한 수업 자료 및 유의점도 함께 제시하면 된다."
                        "10.수업의 단계마다 교사의 활동과 학생의 활동이 구분되어서 제시되어야 한다. 교사는 질문이나 자료를 제시하는 역할을 학생은 조사, 탐구, 토의, 자료 분석의 역할을 하도록 각 단계마다 지도안을 작성해야한다."
                        "11.수업의 단계마다 핵심질문도 함께 제시하면 좋을 것 같아."
                        "12.입력된 학년의 수준에 맞게 지도안을 작성하면 좋겠어."
                        "13.수업의 단계에는 목표를 제시하면 안된다. 그리고 각 수업의 단계가 성취 기준을 달성하도록 유기적으로 연결되어야 한다."
                }          
            ],
            model="gpt-4o",
        )

        # 생성된 내용 추출
        result = chat_completion.choices[0].message.content

        # 결과 표시
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### 생성된 수업 지도안")
        st.write(result)
        st.markdown("</div>", unsafe_allow_html=True)