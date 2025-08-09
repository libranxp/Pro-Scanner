import requests
import os
from apis.provider_registry import mark_provider_status
from utils.logger import log

def fetch_social_volume(slug):
    try:
        url = f"https://api.santiment.net/graphql"
        headers = {"Authorization": f"Apikey {os.getenv('SANTIMENT_KEY')}"}
        query = {
            "query": """
            {
              getMetric(metric: "social_volume_total") {
                timeseriesData(
                  slug: "%s"
                  from: "utc_now-1d"
                  to: "utc_now"
                  interval: "1h"
                ) {
                  datetime
                  value
                }
              }
            }
            """ % slug
        }
        res = requests.post(url, json=query, headers=headers)
        res.raise_for_status()
        mark_provider_status("santiment", "online")
        return res.json()
    except Exception as e:
        mark_provider_status("santiment", "error")
        log(f"❌ Santiment fetch failed for {slug}: {e}")
        raise
