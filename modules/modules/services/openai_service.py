from openai import OpenAI
from modules.services.ai_prompt import build_prompt
from modules.analyzers.ai_analysis import analyze_sentiment, analyze_full

client = OpenAI()

async def run_sentiment(ticker: str, indicators: dict, news_data: list, horizon: str):
    prompt = build_prompt(ticker, indicators, news_data, horizon)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return analyze_sentiment(response.choices[0].message["content"])

async def run_full_analysis(ticker: str, indicators: dict, news_data: list, horizon: str):
    prompt = build_prompt(ticker, indicators, news_data, horizon)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return analyze_full(response.choices[0].message["content"])
