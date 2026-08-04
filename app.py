import re
import time
import validators
import streamlit as st
from urllib.parse import parse_qs, urlparse
from langchain_groq import ChatGroq
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter

st.set_page_config(page_title="LangChain : Summarizer from links", page_icon=":robot:")
st.title("LangChain : Summarizer from links")
st.subheader("This app summarizes content from links using LangChain and Groq API.")

with st.sidebar:
    st.markdown("## Made by SID")
    st.markdown("This app allows you to summarize content from links using LangChain and Groq API. You can input a link, and the app will fetch the content and provide a summary.")
    st.markdown("## Instructions mandate")
    st.markdown("1. Enter a valid URL in the input box.")
    st.markdown("2. Choose the preferred summary size.")
    st.markdown("3. Click on the 'Summarize' button.")
    st.markdown("4. The summary will be displayed below.")
    groq_api_key = st.text_input("Enter your Groq API Key ", type="password")

summary_size = st.selectbox(
    "Select summary size",
    ["Short", "Medium", "Detailed"],
    index=1,
)

generic_url = st.text_input("Enter a valid URL to summarize", label_visibility="collapsed")


def extract_youtube_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc in {"www.youtube.com", "youtube.com", "m.youtube.com"}:
        return parse_qs(parsed.query).get("v", [""])[0]
    if parsed.netloc in {"youtu.be", "www.youtu.be"}:
        return parsed.path.lstrip("/")
    return ""


def extract_text_from_url(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        video_id = extract_youtube_video_id(url)
        if not video_id:
            raise ValueError("Could not extract a YouTube video ID from the provided URL.")
        try:
            api = YouTubeTranscriptApi()
            if hasattr(api, "get_transcript"):
                transcript = api.get_transcript(video_id, languages=["en"])
            else:
                transcript = api.fetch(video_id, languages=["en"])
            return TextFormatter().format_transcript(transcript)
        except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound) as exc:
            raise ValueError(f"No transcript is available for this YouTube video: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Unable to fetch the YouTube transcript: {exc}") from exc

    loader = UnstructuredURLLoader(
        urls=[url],
        ssl_verify=False,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        },
    )
    docs = loader.load()
    return "\n\n".join(doc.page_content for doc in docs if getattr(doc, "page_content", None))


def build_prompt(text: str) -> str:
    if summary_size == "Short":
        return f"""
Provide a very short summary in 3 bullet points of the following content.
Keep each bullet extremely concise.
Content:{text}
"""
    if summary_size == "Detailed":
        return f"""
Provide a detailed summary in 8-10 bullet points of the following content.
Make each bullet informative and slightly descriptive.
Content:{text}
"""
    return f"""
Provide a concise summary in 5 bullet points of the following content.
Keep each bullet short and easy to read.
Content:{text}
"""

prompt = PromptTemplate(template="{text}", input_variables=["text"])


def format_summary_for_display(summary: str) -> str:
    cleaned = summary.strip()
    if not cleaned:
        return ""

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    if any(line.startswith(("- ", "• ")) for line in lines):
        return "\n".join(line if line.startswith(("- ", "• ")) else f"- {line}" for line in lines)

    parts = [part.strip() for part in re.split(r"(?<=[.?!])\s+", cleaned) if part.strip()]
    if len(parts) > 1:
        return "\n".join(f"- {part}" for part in parts)
    return f"- {cleaned}"


def display_summary_with_typing(summary: str) -> None:
    styled_summary = format_summary_for_display(summary)
    placeholder = st.empty()
    rendered = ""
    for char in styled_summary:
        rendered += char
        placeholder.markdown(
            f"<div style='padding: 24px 28px; margin-top: 12px; background-color: #ffffff; color: #111827; border-left: 5px solid #4f46e5; border-radius: 10px; line-height: 1.7; white-space: pre-wrap; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>"
            f"{rendered.replace(chr(10), '<br>')}"
            f"</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.01)


if st.button("Summarize the Content from URL"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. Make sure to include the protocol (http:// or https://).")
    else:
        try:
            with st.spinner("Waiting..."):
                text = extract_text_from_url(generic_url)
                if not text.strip():
                    st.warning("No readable content was found from the provided URL.")
                    st.stop()

                llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key)
                prompt_text = build_prompt(text)
                chain = prompt | llm | StrOutputParser()
                summary = chain.invoke({"text": prompt_text})

                st.subheader("Summary")
                display_summary_with_typing(summary)
        except Exception as e:
            st.exception(f"Exception:{e}")
