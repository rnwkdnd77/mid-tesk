import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# ✅ 한글 폰트 설정
font_path = "./fonts/NanumGothic-Regular.ttf"
nanum_font = font_manager.FontProperties(fname=font_path)

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 앱 기본 설정
st.set_page_config(layout="wide")
st.title("기출 분석")

# 이미지 경로 설정
image_folder = './imgs'  # 이미지가 저장된 폴더 경로

# CSV 데이터 불러오기
df = pd.read_csv('./data/final-exam-data.csv')

# 좌측, 우측 레이아웃
left_col, right_col = st.columns(2)

# --- 좌측: 1~18번 버튼을 클릭하면 해당 이미지를 표시 ---
with left_col:
    st.header("1학기 기말고사")
    
    # 문제 번호 선택 (1~18번)
    image_num = st.selectbox("문제를 선택하세요", range(1, 19), index=0)
    
    # 선택된 번호에 해당하는 이미지 경로 설정 및 표시
    image_path = os.path.join(image_folder, f"{image_num}.png")
    if os.path.exists(image_path):
        st.image(image_path, caption=f"문제 {image_num}", use_container_width=True)
    else:
        st.warning(f"문제 {image_num} 이미지가 존재하지 않습니다.")

# --- 우측: 차트 보기 버튼 및 해당 데이터 표시 ---
with right_col:
    st.header("정답률")

    # 차트 보기 버튼
    if st.button("차트 보기"):
        # 해당 문제 번호에 대한 데이터 (이미지 번호에 맞는 데이터)
        row_data = df.iloc[image_num - 1, :].astype(float)

        # 차트 그리기
        labels = df.columns.astype(str)  # 문제 번호 (CSV 열 제목)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(labels, row_data, color='skyblue')

        ax.set_ylim(0, 100)
        ax.set_ylabel("정답률 (%)", fontproperties=nanum_font)
        ax.set_title(f"{image_num}번 문항 정답률", fontproperties=nanum_font)
        ax.set_xticklabels(labels, fontproperties=nanum_font)

        # 축 레이블 폰트도 설정
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(nanum_font)

        st.pyplot(fig)
