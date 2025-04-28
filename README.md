# 📰 AI-Powered Tech News Generator

This is a **Flask**-based web app that lets users **search for a tech topic** and then **generates a professional AI-written article** based on real-time related news from Google and NewsAPI.

---

## 🚀 Features

- 🔍 Search any tech-related topic
- 🧠 Auto-fetch real news links using Google Custom Search API and NewsAPI
- 🤖 Generate a full professional article using AI (Llama Vision Free model)
- 🛡️ Secure API key handling with `.env`
- 🎨 Clean, professional, responsive UI

---

## 📂 Project Structure

```bash
├── app.py            # Main Flask server
├── templates/
│   ├── home.html      # Search input page
│   └── article.html   # Generated article output page
├── static/
│   └── styles.css     # Styles for the website
├── .env              # API keys (not uploaded to GitHub)
├── .gitignore        # Ignore .env and Python cache
├── README.md         # This file
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-news-generator.git
cd ai-news-generator
```

### 2. Install dependencies

```bash
Flask
requests
beautifulsoup4
python-dotenv
```

---

### 3. Create a `.env` file

In the root of your project, create a `.env` file and add your API keys:

```env
LLM_API_TYPE=together
LLM_MODEL=meta-llama/Llama-Vision-Free
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=https://api.together.xyz/v1
LLM_TEMPERATURE=0

GOOGLE_API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_search_engine_id

NEWS_API_KEY=your_newsapi_key
```

**Important**: Never upload your `.env` to GitHub!

---

### 4. Run the Flask app

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` to start using the app locally.

---

## 🧩 APIs Used

- [Together AI (Meta Llama-Vision)](https://www.together.ai/)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [NewsAPI](https://newsapi.org/)

---

## ✨ To Do

- [ ] Add pagination for more related articles
- [ ] Improve article styling
- [ ] Add loading spinners while fetching data
- [ ] Deploy online (Render, Railway, etc.)

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

- GitHub: [Charbel Nohra](https://github.com/CharbelNohra)
- Email: charbelnohra113@gmail.com
