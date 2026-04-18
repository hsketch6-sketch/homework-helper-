import streamlit as st
import random
from cryptography.fernet import Fernet
import base64
import hashlib

# 페이지 설정
st.set_page_config(page_title="암호 메세지 제작")

# 🔑 비밀번호 → Fernet 키 변환 함수
def make_key(password: str):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)
# 친구들만 아는 우리만의 암호 (0515 대신 원하는 비번 넣으세요)
if st.sidebar.text_input("🔑 우리끼리 비밀번호", type="password") != "jihyun77^^":
    st.warning("비밀번호를 입력해야 사용할 수 있어!")
    st.stop()

st.title("암호 메세지 제작")
st.write("""프라이버시 메시지 생성기
         사용법:
         원하는 비밀번호(해독의 핵심!) 을 넣고
         가릴 글자를 칩니다.
         이후 링크와 함께 친구에게 보내주세요!""")
st.write("비밀번호를 망각하시면 개발자도 모릅니다. 잘 기억하거나 어디에 보관해두세요.")

# 🔐 비밀번호 입력
password = st.text_input("🔑 비밀번호를 입력하세요", type="password")

if not password:
    st.warning("비밀번호를 먼저 입력하세요!")
    st.stop()

# 키 생성
MY_KEY = make_key(password)
cipher = Fernet(MY_KEY)

# 탭 UI
tab1, tab2 = st.tabs(["메시지 만들기", "메시지 해독하기"])

# 📤 암호화 탭
with tab1:
    msg = st.text_input("🤫 숨길 내용을 입력하세요 (예: 피방 고?)")
    
    if st.button("공부 톡으로 변환"):
        if not msg:
            st.warning("내용을 입력하세요!")
        else:
            encrypted = cipher.encrypt(msg.encode()).decode()
            
            themes = [
                f"오늘 숙제 있었냐? [Ref: {encrypted}]",
                f"시간표가 뭐더라 내일? (ID: {encrypted})",
                f"야 같이 공부나 좀 하자 {{Code: {encrypted}}}"
            ]
            
            result = random.choice(themes)
            st.success("아래 문장을 복사해서 보내세요!")
            st.code(result)

# 📥 복호화 탭
with tab2:
    received = st.text_area("🔓 받은 문장을 통째로 붙여넣으세요")
    
    if st.button("진짜 내용 보기"):
        try:
            if "[Ref: " in received:
                start, end = "[Ref: ", "]"
            elif "(ID: " in received:
                start, end = "(ID: ", ")"
            elif "{Code: " in received:
                start, end = "{Code: ", "}"
            else:
                raise ValueError("형식 오류")

            token = received.split(start)[1].split(end)[0].strip()
            decrypted = cipher.decrypt(token.encode()).decode()
            
            st.info(f"진짜 내용: {decrypted}")
        
        except Exception:
            st.error("해독 실패! 비밀번호가 틀리거나 형식이 잘못되었습니다.")
