from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# API Configuration
LLM_CONFIG = {
    "api_type": "together",
    "model": "meta-llama/Llama-Vision-Free",
    "api_key": "tgp_v1_jh9oJN_Ksmc6MrhB-mDGdgd8cODmiQJUcuit_7E1NX4",
    "base_url": "https://api.together.xyz/v1",
    "temperature": 0
}

GOOGLE_API_KEY = "AIzaSyA7q7jdzTc_9cQaneG9AIxOALwZC_UTohE"
SEARCH_ENGINE_ID = "f676707b4878b417f"
NEWS_API_KEY = "0bb5c94b7a7b4f5c928f2201276fb1c0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def is_valid_url(url):
    return re.match(r"^https?://", url) is not None

def fetch_article(url):
    if not is_valid_url(url):
        return None, None, None
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Untitled Article"
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")[:5]
                     if p.get_text(strip=True)]
        summary = " ".join(paragraphs) if paragraphs else "No summary available."
        keywords = title.lower().split()[:3]

        return title, summary, keywords
    except requests.RequestException:
        return None, None, None

def google_search_news(keywords):
    if not keywords:
        return []
    try:
        query = "+".join(keywords) + "+technology+news"
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        results = response.json().get("items", [])
        return [item["link"] for item in results[:3]]
    except requests.RequestException:
        return []

def fetch_newsapi_articles():
    try:
        news_url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(news_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [article["url"] for article in articles[:3]]
    except requests.RequestException:
        return []

def generate_ai_article(title, summary, similar_news):
    if not title or not summary:
        return "Unable to generate an article due to missing title or summary."

    prompt = f"""
    Write a tech news article about: {title}.
    Summary: {summary}
    Related news: {', '.join(similar_news)}
    The article should be engaging and professional.
    """

    headers = {"Authorization": f"Bearer {LLM_CONFIG['api_key']}", "Content-Type": "application/json"}
    payload = {
        "model": LLM_CONFIG["model"],
        "messages": [{"role": "system", "content": prompt}],
        "temperature": LLM_CONFIG["temperature"],
        "max_tokens": 1000
    }

    try:
        response = requests.post(f"{LLM_CONFIG['base_url']}/chat/completions", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if choices and "message" in choices[0] and "content" in choices[0]["message"]:
            return choices[0]["message"]["content"].strip()
        else:
            return "Did not generate content."
    except requests.RequestException:
        return "Failed to generate an article."

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if not topic:
            return render_template("home.html", error="Please enter a topic.")

        similar_news = google_search_news([topic]) or fetch_newsapi_articles()

        if similar_news:
            article_url = similar_news[0]
            title, summary, keywords = fetch_article(article_url)

            if title:
                content = generate_ai_article(title, summary, similar_news)
                return render_template("article.html", title=title, content=content, links=similar_news)
            else:
                return render_template("home.html", error="Failed to fetch the article.")
        else:
            return render_template("home.html", error="No related news found.")

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)