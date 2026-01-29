# AI 챗봇 만들기 참고 블로그 [ https://dongdongfather.tistory.com/287 ]

import streamlit as st

#1) st.chat_message() : Streamlit 채팅 UI 전용 컴포넌트

with st.chat_message("user"):  # 'human' 과 완전 같음.
    st.write("안녕하세요")

with st.chat_message("assistant"): # 'ai' 과 완전 같음.
    st.write("반갑습니다!")

# role 에 없는 명칭을 사용하면 첫글자 표시   
with st.chat_message('bot'): # icon이 'B'
    st.write("this is ai")

with st.chat_message('sam'): # icon이 'S'
    st.write("this is sam")

with st.chat_message('son'): # icon이 'S' -- 구별안됨
    st.write("this is son")
 
with st.chat_message('홍길동'): # icon이 '홍'
    st.write("나는 홍길동이야.")
    st.write('반가워요.') # 여러줄 가능
    st.button('눌러주세요') # 다른 요소도 가능

st.chat_message('ai').write('한줄로 써도 됩니다.')
st.divider()
# ####################################################################################

#2) 채팅처럼 대화하는 형태가 되려면 각각의 메세지를 리스트로 가지고 있어야함.
# 단, 메세지 데이터는 {역할:'', 내용:''} 구조로 만들어야 함.
messages= [
    {'role':'assistant', 'content':'무엇을 도와드릴까요?'},
    {'role':'user', 'content':'대한민국의 수도는?'},
    {'role':'assistant', 'content':'대한민국의 수도는 **서울**입니다.'}, # 마크다운 인식함.
    {'role':'user', 'content':'오. 고마워~'},
]

for msg in messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        #st.write(msg['content']) # 이것도 일부 마크다운 됨.
# ##########################################################################


#3) 사용자의 질문 받기  st.chat_input() --- 특이하게 알아서 화면의 가장 하단에 배치됨. 스크롤 해보면 알 수 있음.
# question= st.chat_input('질문을 입력하세요.')
# if question:
#     messages.append({'role':'user','content':question})
#     st.chat_message('user').write(question)
#     # ai 응답 글씨...[실습용으로 아무글씨나]
#     response= f"{question}에 대해 알고싶군요.\n어쩌고 저쩌고...." # \n 은 무시됨. 마크다운으로 해석..
#     response= f"{question}에 대해 알고싶군요.  \n어쩌고 저쩌고...." # Markdown에서 줄바꿈은 공백 2개 + \n
#     messages.append({'role':'assistant','content':response})
#     st.chat_message('assistant').write(response)

# 하지만.. 이렇게 작성하면.. streamlit 의 랜러딩 방식에 따라... 새로운 메세지가 입력될때마다 처음부터 다시 실행되어.
# messages 에 append()로 추가한 마지막 입력 메세지들은 사라지고 새로운 메세지만 보임..

# 채팅은 기존 메세지를 잘 저장하고 있어야 겠죠.
# 웹의 기록저장에 사용되었던 session(연결) 개념을 활용한 저장기능이 streamlit에 제공됨.
# #################################################################################
st.divider()

#4) st.session_state 라는 특별한 속성(객체)를 이용하여 기존 대화내용 저장하기 

#a. messages 라는 이름의 변수가 session_state 에 존재하는지 부터 확인하고 없다면 첫 문장 저장
if "messages" not in st.session_state:
    st.session_state.messages= [
        {'role':'assistant', 'content':'무엇이든 물어보세요.'},
    ]

#b. session_state 에 저장된 "messages" 의 메세지들을 채팅UI로 그리기 [처음시작할때는 위 1개의 메세지만 있지만 아래에서 input으로 생성된 메세지들이 저장되어 많아짐.]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


#c. 사용자 채팅메세지를 입력받아 session_state 에 저장하기 [[단!! 위에서 이미 st.chat_input 이 있기에 화면 아래에 2개의 입력요소가 생김] -- 데이터를 받는 처리코드가 들어가면 에러남. 그러니 위 3)예제 주석. ]
question= st.chat_input('질문을 입력하세요.') # 줄바꿈은 shift+enter
if question:
    # Markdown에서 줄바꿈은 공백 2개 + \n
    question= question.replace('\n','  \n')
    st.session_state.messages.append({'role':'user','content':question}) 
    st.chat_message('user').write(question)

    #응답 - 원래는 ai에게 응답하도록....
    response= f"{question}에 대해 알고싶군요.  \n어쩌고 저쩌고...." # \n 은 무시됨. 마크다운으로 해석..# Markdown에서 줄바꿈은 공백 2개 + \n
    st.session_state.messages.append({'role':'assistant','content':response})
    st.chat_message('assistant').write(response)




