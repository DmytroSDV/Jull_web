import subprocess
import os
import json


def run_articles_scrape_spider():
    script_path = os.path.join(
        os.path.dirname(__file__), "..", "spiders", "articles_scrape.py"
    )
    print(script_path)
    result = subprocess.run(["py", script_path], capture_output=True, text=True)

    json_data = json.dumps(result.stdout, ensure_ascii=False, indent=4)
    return json_data


run_articles_scrape_spider()
