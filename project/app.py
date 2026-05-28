import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from gnews import GNews
from google import genai

# 환경변수 로드
load_dotenv("my_keys.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Insight Bridge", layout="wide")
st.title("💡 나의 깨달음 노트: 뉴스 브릿지")

if st.button("오늘의 핵심 뉴스 5선 불러오기"):
    google_news = GNews(language='ko', country='KR', max_results=5)
    news_list = google_news.get_top_news()
    
    for i, article in enumerate(news_list[:5], 1):
        # 3줄 요약
        response = client.models.generate_content(
            model='gemini-3.5-flash', 
            contents=f"이 뉴스를 3줄 요약해줘: {article['title']}"
        )
        
        # UI 구성
        st.subheader(f"{i}. {article['title']}")
        st.markdown(response.text)
        
        # 님의 생각을 기록하는 입력창 (깨달음 노트)
        with st.form(key=f"form_{i}"):
            thought = st.text_input("이 뉴스에 대한 나의 깨달음 기록:")
            if st.form_submit_button("저장하기"):
                df = pd.DataFrame([{"날짜": datetime.now(), "제목": article['title'], "깨달음": thought}])
                df.to_csv("my_insights.csv", mode='a', header=not os.path.exists("my_insights.csv"), index=False, encoding='utf-8-sig')
                st.success("노트에 저장되었습니다!")
        st.divider()