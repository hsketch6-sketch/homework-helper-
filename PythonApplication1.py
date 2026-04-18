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

# --- 📱 사이드바 ---
with st.sidebar:
    st.title("👨‍💻 개발자 정보")
    st.success("중1 개발자가 만든 프로젝트입니다!(바이브코딩)")
    
    st.divider()
    
    # 🍬 간식 후원 섹션 (실명 노출 없는 기프티콘 방식)
    st.subheader("🍬 개발자에게 간식 쏘기")
    st.write("실명 노출 없이 **익명**으로 응원하실 수 있습니다. 제 코딩 작업이 마음에 드셨다면 기프티콘으로 마음을 전해주세요!")
    
    # [중요] 본인의 카카오톡 오픈채팅 링크를 아래에 넣으세요!
    kakao_open_chat = "https://open.kakao.com/o/sPpbP0qi"
    
    st.link_button("🎁 익명 기프티콘 후원하기", kakao_open_chat, help="카카오톡 오픈채팅(익명)으로 연결됩니다.")
    st.caption("편의점, 카페 등 작은 간식도 큰 힘이 됩니다! 🚀")
    
    st.divider()
    st.write("📢 친구들에게 공유하기")
    # 배포 후 실제 주소가 생기면 아래를 수정하세요.
    st.code("https://2wdbuutbgcqtwhqxhktk4z.streamlit.app/") 
    
    st.caption("© 2024 중1 개발자 프로젝트")

# --- 🏠 메인 화면 ---
st.title("🔐 비밀 메세지 제작소")
st.write("부모님이나 선생님께 들키기 싫은 대화, '인강 링크'로 위장해서 보내세요!")

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
            
            # 실제 인강 사이트 주소처럼 위장
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

# 📥 복호화 탭
with tab2:
    received = st.text_area("🔓 받은 문장을 통째로 붙여넣으세요")
    
    if st.button("진짜 내용 보기"):
        try:
            # 암호화된 토큰(gAAAA로 시작하는 부분)만 추출
            match = re.search(r'gAAAA[A-Za-z0-9\-_=]+', received)
            
            if match:
                token = match.group()
                decrypted = cipher.decrypt(token.encode()).decode()
                
                st.success("🔓 해독 완료!")
                st.info(f"🔎 숨겨진 내용: {decrypted}")
            else:
                st.error("암호를 찾을 수 없습니다. 문장 전체를 복사했는지 확인하세요!")
        
        except Exception:
            st.error("❌ 해독 실패! '암호 키'가 다르거나 메세지가 복사 중에 잘렸을 수 있습니다.")

# --- 💡 푸터 ---
st.divider()

# --- 📊 방문자 통계 (텍스트 버전) ---
st.divider()

# 방문자 수를 기록할 텍스트 파일이나 DB가 없으므로, 
# 가장 확실하게 숫자를 보려면 Streamlit Cloud의 'Analytics'를 확인하는 게 정확합니다.
# 대신 앱 화면에는 방문자에게 안내 문구를 남겨주세요.

st.write("📊 **방문자 통계 안내**")
st.caption("실시간 누적 방문자 수는 개발자 대시보드에서 집계 중입니다.")

# 위에서 시도한 이미지 배지가 계속 깨진다면 아래 코드로 대체해서 
# 아예 '분석 페이지'로 연결되는 버튼을 만드는 것도 방법입니다.
if st.button("📈 내 방문자 통계 확인하기 (개발자용)"):
    st.info("Streamlit Cloud 로그인 후 [Analytics] 탭을 확인하세요!")

st.divider()
st.caption("비밀 메세지 제작소 - 중1 개발자의 코딩 실험실")

