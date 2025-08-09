from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_sentiment(keyword):
    try:
        # Replace with actual Twitter API logic
        mark_provider_status("twitter_sentiment", "online")
        return {"keyword": keyword, "sentiment_score": 0.7}
    except Exception as e:
        mark_provider_status("twitter_sentiment", "error")
        log(f"❌ Twitter sentiment fetch failed: {e}")
        raise
