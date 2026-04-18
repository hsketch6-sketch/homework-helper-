import streamlit as st
import random
from cryptography.fernet import Fernet
import base64
import hashlib
import re

# 페이지 설정
st.set_page_config(page_title="비밀 메세지 제작소", page_icon="🔐")

# --- 🔑 함수 정의 ---
def make_key(password: str):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# --- 📱 사이드바 (후원 및 홍보) ---
with st.sidebar:
    st.title("👨‍💻 개발자 정보")
    st.info("중1 개발자가 만든 '비밀 메세지' 변환기입니다!")
    
    st.subheader("🍬 간식 후원하기")
    st.write("실명 노출 없이 안전하게 응원하실 수 있습니다!")
    
    safe_link = "https://open.kakao.com/o/srNPC0qi" 
    st.link_button("🎁 익명으로 응원 보내기", safe_link)
    
    st.divider()
    st.write("📢 친구들에게 공유하기")
    # 실제 주소로 업데이트
    st.code("https://streamlit.app")
    
    st.caption("© 2024 중1 개발자 프로젝트")

# --- 🏠 메인 화면 ---
st.title("🔐 비밀 메세지 제작소")
st.write("부모님이나 선생님께 들키기 싫은 대화, '공부 톡'으로 위장해서 보내세요!")

st.warning("⚠️ 비밀번호를 잊어버리면 개발자도 절대 복구해줄 수 없습니다!")

# 🔐 비밀번호 입력 (해독 키)
password = st.text_input("🔑 우리만의 암호 키를 입력하세요", type="password", help="메세지를 잠그고 풀 때 필요한 단어입니다.")

if not password:
    st.info("💡 먼저 암호 키를 설정해야 메세지를 만들 수 있습니다.")
    st.stop()

# 키 생성
MY_KEY = make_key(password)
cipher = Fernet(MY_KEY)

# 탭 UI
tab1, tab2 = st.tabs(["📤 메세지 숨기기", "📥 메세지 풀기"])

# 📤 암호화 탭
with tab1:
    msg = st.text_input("🤫 숨길 내용을 입력하세요 (예: 오늘 피방 ㄱ?)")
    
    if st.button("위장 메세지 생성"):
        if not msg:
            st.warning("내용을 입력하세요!")
        else:
            encrypted = cipher.encrypt(msg.encode()).decode()
            
            # 💡 암호를 더 링크처럼 보이게 '?id=' 또는 '/view/' 등을 추가
            themes = [
                f"EBS 강의자료 확인: https://ebs.edu{encrypted}",
                f"수학 오답노트 PDF: https://class-edu.net{encrypted}",
                f"학원 단어장 배포: https://voca-study.app{encrypted}",
                f"수행평가 공지사항: https://school.info{encrypted}",
                f"영어 듣기평가 자료: https://edu-audio.com{encrypted}"
            ]
            
            result = random.choice(themes)
            st.success("✅ 위장 성공! 아래 문장을 복사해서 보내세요.")
            st.code(result)
            st.caption("팁: 받은 친구도 이 사이트에서 동일한 '암호 키'를 입력해야 풀 수 있어요.")

# 📥 복호화 탭
with tab2:
    received = st.text_area("🔓 받은 문장을 통째로 붙여넣으세요")
    
    if st.button("진짜 내용 보기"):
        try:
            # 💡 정규표현식을 사용해 문장 속에 숨겨진 '암호 덩어리'만 쏙 뽑아냅니다.
            # Fernet 암호문은 보통 대문자, 소문자, 숫자, +, /, -가 섞인 긴 문자열입니다.
            match = re.search(r'[A-Za-z0-9+/=_-]{30,}', received)
            
            if match:
                token = match.group()
                decrypted = cipher.decrypt(token.encode()).decode()
                st.balloons() 
                st.info(f"🔎 숨겨진 내용: {decrypted}")
            else:
                st.error("문장에서 암호를 찾을 수 없습니다. 문장 전체를 정확히 입력했나요?")
        
        except Exception:
            st.error("❌ 해독 실패! '암호 키'가 틀리거나 메세지가 복사 중에 잘렸을 수 있습니다.")

# --- 💡 푸터(Footer) ---
st.divider()
st.caption("© 2024 중1 개발자 프로젝트. All rights reserved.")
