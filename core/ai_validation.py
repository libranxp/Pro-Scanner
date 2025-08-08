# core/ai_validation.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_reason(ticker, data):
    prompt = f"""
    Ticker: {ticker}
    Price: {data['price']}
    Volume Spike: {data['volume']}
    Catalyst: {data['catalyst']}
    Sentiment: {data['sentiment']}
    Technicals: {data['technicals']}

    Based on this, explain why this ticker is moving.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        reason = response['choices'][0]['message']['content'].strip()
        return reason
    except Exception as e:
        return f"AI validation failed: {str(e)}"
