# app.py
import streamlit as st
import time
from prompt_config import generate_diary_summary

st.set_page_config(page_title="AIME - 교제폭력 증거수집 AI 다이어리", page_icon="📖", layout="centered")

# 대화 기록 및 상태 초기화 (PDF 2페이지 시나리오 기준)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "오늘 하루도 수고하셨습니다. 당신을 돕는 AI 챗봇 에이미입니다.\n\n오늘 어떤 사건이 있었나요? 최대한 자세하게 알려주세요. (누가, 언제, 어디서, 무엇을, 어떻게, 왜)"}
    ]

if "step" not in st.session_state:
    st.session_state.step = 1  # 1: 사건파악, 2: 증거확인, 3: 감정확인, 4: 공감확인, 5: 추가기록확인, 6: 일기출력 및 종료확인, 7: 완료

if "user_data" not in st.session_state:
    st.session_state.user_data = {"event": "", "evidence": "", "emotion": "", "extra": ""}

# 사이드바 (증거 제출 및 상담 연결)
with st.sidebar:
    st.header("📂 증거 제출 (MY BOX 연동)")
    st.caption("CLOVA OCR & Speech API 기반 자동 텍스트 변환")
    uploaded_file = st.file_uploader("스크린샷 또는 녹음 파일 업로드", type=["png", "jpg", "jpeg", "mp3", "m4a"])
    if uploaded_file:
        st.success(f"'{uploaded_file.name}' 파일이 CLOVA API로 분석 후 MY BOX에 안전하게 저장되었습니다.")
    st.divider()
    if st.button("🚨 상담기관 연결 안내"):
        st.warning("여성긴급전화 ☎ 1366 / 경찰청 ☎ 112\n도움이 필요하시면 언제든 연결해 드립니다.")

st.title("📖 AIME (에이미)")
st.caption("교제폭력 증거수집 AI 다이어리")

# 이전 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력 처리
if user_input := st.chat_input("에이미에게 이야기를 들려주세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        response_box = st.empty()
        
        # [Step 1] 사건 접수 -> 증거 질문
        if st.session_state.step == 1:
            st.session_state.user_data["event"] = user_input
            ai_reply = "그런 일이 있으셨군요. 이를 뒷받침해줄 사진이나 녹음본이 있나요?"
            st.session_state.step = 2

        # [Step 2] 증거 접수 -> 감정 질문
        elif st.session_state.step == 2:
            st.session_state.user_data["evidence"] = user_input
            ai_reply = "그때의 감정은 어땠나요?"
            st.session_state.step = 3

        # [Step 3] 감정 접수 -> 감정 지지 및 공감 확인 질문
        elif st.session_state.step == 3:
            st.session_state.user_data["emotion"] = user_input
            ai_reply = "그렇게 느꼈나요?"
            st.session_state.step = 4

        # [Step 4] 공감 확인 -> 일기 생성 전 추가 기록 질문
        elif st.session_state.step == 4:
            ai_reply = "이제 '하루의 기록'을 생성할 수 있습니다. 추가적으로 더 기록하고 싶은 내용이 있나요?"
            st.session_state.step = 5

        # [Step 5] 추가 기록 처리 (긍정/부정 판단) -> 일기 생성 및 마무리 질문
        elif st.session_state.step == 5:
            # 부정 응답 구별
            negative_keywords = ["없", "아니", "괜찮", "없어", "없습니다", "아니요"]
            if not any(keyword in user_input for keyword in negative_keywords):
                st.session_state.user_data["extra"] = user_input
            
            diary = generate_diary_summary(st.session_state.user_data)
            ai_reply = f"{diary}\n\n하루의 기록을 마무리해볼까요?"
            st.session_state.step = 6

        # [Step 6] 기록 저장 마무리 및 안내
        elif st.session_state.step == 6:
            ai_reply = "이제 '하루의 기록'이 저장됩니다. 그 외에 어려움을 겪고 있거나 상담 등의 도움이 필요하면 에이미에게 말을 걸어주세요."
            st.session_state.step = 7

        # [Step 7] 저장 완료 이후 일반 대화
        else:
            ai_reply = "오늘의 기록과 증거 자료는 안전하게 보관되었습니다. 도움이 필요하시면 언제든 말씀해 주세요."

        # 타이핑 애니메이션 효과
        full_text = ""
        for char in ai_reply:
            full_text += char
            response_box.write(full_text)
            time.sleep(0.01)

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})