# 실제 배포를 하기위해 파일을 GitHub 로 업로드 할거니. 별도의 폴더 [ streamlit_deploy ] 안에서 작업 후 Git Repository 를 만든 후 업로드.

# open ai api 는 유료만 가능하여.
# 부득이. google ai studio 의 genai api 사용

#1. GEN AI 응답을 위한 라이브러리 사용 및 생성AI객체 생성 -------------------
from google import genai
client= genai.Client(api_key='AIzaSyDoOloJkE0woHr4aMt0qzs1ty0SEg9X0bs')

# 응답 제어를 위한 하이퍼파라미터 설정.
from google.genai import types
config=types.GenerateContentConfig(
    max_output_tokens=10000,
    response_mime_type='text/plain',
    #system_instruction='넌 만물박사야. 넌 최대 100글자안에 어린이도 이해할 수 있게 뭐든지 설명해.'
    #system_instruction='넌 아주 섹시한 여자야. 뭐든지 아주 저속하고 아햐게 말해.'
    #system_instruction='넌 모든 대답을 언제나 개조식으로 해.'
    system_instruction='넌 불량한 고등학생이야. 비속어를 아주 많이쓰고 뭐든 100글자 안에 말해.'
)

# '질문'을 파라미터로 받아 GEN AI 로 응답한 글씨를 리턴 해주는 기능 함수
def get_ai_response(question):
    response= client._models.generate_content(
        #model="gemini-3-flash-preview",
        model="gemini-2.5-flash",
        contents=question,
        config=config
    )
    return response.text # response 응답객체(dict) 에는 여러정보가 있음. 그중 응답글씨만..
# -------------------------------------------------------------------

#2. 채팅 UI 만들기
import streamlit as st

#0. 페이지 기본 설정 -- 브라우저의 탭영역에 표시되는 내용.
st.set_page_config(
    page_title="AI 불량봇",
    page_icon="./logo/logo_chatbot.png"   
)

#1. HEADER 영역
# 헤더 레이아웃 (이미지 + 제목 가로 배치)
col1, col2 = st.columns([1.2, 4.8])

with col1:
    st.image(
        "./logo/logo_chatbot.png",  # 챗봇 이미지 파일 경로 (같은 폴더에 위치)
        width=200,
    )

with col2:
    #HTML 로 만들어보기
    st.markdown(
        """
        <h1 style='margin-bottom:0;'>AI 불량봇</h1>
        <p style='color:gray; margin-top:0;'>이 챗봇은 모든 답변을 불량 고등학생처럼 합니다. 상처받지 마세요.</p>
        """,
        unsafe_allow_html=True
    )

# 구분선
st.markdown("---") 


#a. messages 라는 이름의 변수가 session_state 에 존재하는지 부터 확인하고 없다면 첫 문장 저장
if "messages" not in st.session_state:
    st.session_state.messages= [
        {'role':'assistant', 'content':'무엇이든 물어보세요.'},
    ]

#b. session_state 에 저장된 "messages" 의 메세지들을 채팅UI로 그리기 [처음시작할때는 위 1개의 메세지만 있지만 아래에서 input으로 생성된 메세지들이 저장되어 많아짐.]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


#c. 사용자 채팅메세지를 입력받아 session_state 에 저장하기
question= st.chat_input('질문을 입력하세요.') # 줄바꿈은 shift+enter
if question:
    # Markdown에서 줄바꿈은 공백 2개 + \n
    question= question.replace('\n','  \n')
    st.session_state.messages.append({'role':'user','content':question}) 
    st.chat_message('user').write(question)

    #응답 - AI 응답 요구기능 함수 호출....... 스피너 적용
    with st.spinner('AI가 응답 중입니다... 잠시만 기다려주세요'):
        response= get_ai_response(question)
        st.session_state.messages.append({'role':'assistant','content':response})
        st.chat_message('assistant').write(response)


# Streamlit 배포하기

# Streamlit Community Cloud 배포
# GitHub에 프로젝트 업로드
# Streamlit Cloud 접속
# New app 버튼 클릭 후 GitHub 저장소 선택
# 자동으로 배포됨 (무료 배포 가능)

# 배포한 웹앱을 컴퓨터에 앱을 설치하는 것도 가능함. [브라우저의 주소줄에 설치항목이 있음.]  -- 아래 위치에 설치됨.
# C:\Users\Admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome 앱 



# !! google.genai 라이브러리가 서버에 설치되어 있지 않아서 에러 !!

# Streamlit Cloud는 requirements.txt에 적힌 것만 설치합니다.

#프로젝트 루트에 requirements.txt 만들고 ------------------
# streamlit
# google-genai
#-------------------------------------------------------

# 이미 있다면 반드시 google-genai가 있는지 확인.
# 그리고 GitHub에 push → Streamlit Cloud 재배포.


#[수행과제]
# 본인만의 챗봇 만들기!!!!!