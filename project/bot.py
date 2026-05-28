import time
import schedule
from gnews import GNews
from google import genai
from telegram import Bot

# 설정
API_KEY = "AIzaSyAgquQyJVSYLiaQlOMvU7S-Y2KJGF2gQCs"
BOT_TOKEN = "8314970219:AAHPIqtMSO0e8radW9CGX7XEVHdf0JADpS0"
CHAT_ID = "8964465056"


client = genai.Client(api_key=API_KEY)
bot = Bot(token=BOT_TOKEN)

def get_top_news():
    google_news = GNews(language='ko', country='KR', max_results=5)
    news_list = google_news.get_top_news()
    
    result_text = "📰 [오늘의 핵심 뉴스 5가지]\n\n"
    
    for i, article in enumerate(news_list[:5], 1):
        title = article['title']
        # 기사 내용을 간단히 3줄 요약 요청
        prompt = f"다음 뉴스를 3줄로 요약해줘: {title}"
        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
        
        result_text += f"{i}. {title}\n{response.text.strip()}\n\n"
    
    bot.send_message(chat_id=CHAT_ID, text=result_text)

# 매일 아침 8시 실행
schedule.every().day.at("08:00").do(get_top_news)

print("뉴스 비서가 가동되었습니다. 매일 아침 8시에 5가지 뉴스를 배달합니다.")

while True:
    schedule.run_pending()
    time.sleep(60)