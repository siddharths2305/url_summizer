# 🔗 LangChain Summarizer — Web & YouTube Content Summarization

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM%20API-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Summarize any web article or YouTube video with a single link — powered by LangChain, Groq, and LLaMA 3.3 70B.**

</div>

---

## ✨ Overview

**LangChain Summarizer** is a lightweight Streamlit app that turns any URL — a blog post, news article, or YouTube video — into a clean, digestible bullet-point summary. It auto-detects the content source, extracts the raw text (via `UnstructuredURLLoader` for web pages or the YouTube Transcript API for videos), and feeds it to **Groq's LLaMA 3.3 70B** through a LangChain pipeline.

The UI renders the result with a smooth animated "typing" effect for a polished, ChatGPT-like feel.

---

## 🖼️ How It Works

The app follows a simple, linear pipeline from input to summary:

1. **Input validation** — The user provides a Groq API key and a URL. The app checks that both fields are filled and that the URL is well-formed before proceeding.
2. **Source detection** — The app checks whether the URL points to a YouTube video (`youtube.com` / `youtu.be`) or a regular web page.
3. **Content extraction**:
   - **YouTube URLs**: The video ID is extracted from the link, and the transcript is fetched using the YouTube Transcript API.
   - **Web page URLs**: The page is loaded and parsed into plain text using `UnstructuredURLLoader`, with a custom browser User-Agent to avoid basic blocking.
4. **Prompt construction** — Based on the selected summary size (Short, Medium, or Detailed), a tailored prompt is built instructing the model on bullet count and depth.
5. **LLM summarization** — The prompt is passed through a LangChain chain (`PromptTemplate → ChatGroq → StrOutputParser`) using Groq's `llama-3.3-70b-versatile` model.
6. **Formatting & display** — The raw model output is normalized into clean bullet points and revealed in the UI with a typewriter-style animation.

| Stage | Component Used | Purpose |
|---|---|---|
| Input Validation | `validators.url()` | Confirms the URL is properly formatted before any processing begins |
| Source Detection | URL parsing (`urlparse`) | Determines whether to use the YouTube path or the web-scraping path |
| YouTube Extraction | `YouTubeTranscriptApi` | Fetches the video's transcript text directly, no audio/video download required |
| Web Extraction | `UnstructuredURLLoader` | Loads and parses HTML content into clean text |
| Prompt Building | `build_prompt()` | Generates a size-specific instruction prompt (3, 5, or 8–10 bullets) |
| Summarization | `ChatGroq` (LLaMA 3.3 70B) | Generates the actual summary via Groq's inference API |
| Output Parsing | `StrOutputParser` | Extracts plain text from the LLM's structured response |
| Display Formatting | `format_summary_for_display()` | Converts raw text into consistent Markdown bullet points |
| Animated Rendering | `display_summary_with_typing()` | Streams the summary into the UI character-by-character |

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🌐 **Universal URL Support** | Summarizes both regular web pages and YouTube videos |
| 🎚️ **Adjustable Summary Length** | Choose between **Short**, **Medium**, or **Detailed** summaries |
| ⚡ **Blazing Fast Inference** | Powered by Groq's LPU-accelerated **LLaMA 3.3 70B** model |
| 🎬 **YouTube Transcript Extraction** | Pulls transcripts directly — no audio download needed |
| ✅ **URL Validation** | Ensures a valid, well-formed URL before processing |
| ⌨️ **Typing Animation UI** | Summary is revealed with a smooth typewriter effect |
| 🔒 **Secure API Key Input** | Groq API key is entered as a masked password field |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Interactive web UI
- **[LangChain](https://www.langchain.com/)** — Prompt orchestration & chaining
- **[Groq](https://groq.com/)** — Ultra-fast LLM inference (`langchain-groq`)
- **[Unstructured](https://unstructured.io/)** — Web page content extraction (`langchain-community`)
- **[youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)** — YouTube transcript fetching
- **[validators](https://pypi.org/project/validators/)** — URL validation

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/langchain-summarizer.git
cd langchain-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>📋 Sample <code>requirements.txt</code></summary>

```txt
streamlit
validators
langchain
langchain-groq
langchain-community
unstructured
youtube-transcript-api
```

</details>

### 4. Get your Groq API Key

Sign up at [console.groq.com](https://console.groq.com/) and generate a free API key.

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then in the browser:

1. Enter your **Groq API Key** in the sidebar.
2. Paste a **web article or YouTube URL** into the input box.
3. Select your preferred **summary size** — Short, Medium, or Detailed.
4. Click **"Summarize the Content from URL"** and watch the summary appear.

---

## 🧩 Project Structure

```
langchain-summarizer/
├── app.py               # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Configuration Notes

- Summary style is controlled via the `build_prompt()` function, which dynamically adjusts bullet count and depth based on the selected size.
- The app gracefully handles YouTube-specific errors: `TranscriptsDisabled`, `VideoUnavailable`, and `NoTranscriptFound`.
- Web page scraping uses a custom `User-Agent` header to reduce the chance of being blocked by target sites.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ using **LangChain** + **Groq** 

</div>
