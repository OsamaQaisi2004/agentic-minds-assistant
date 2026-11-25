# Agentic Minds Assistant

A bilingual Streamlit chatbot prototype for the Agentic Minds student technology team. It uses an OpenRouter API model and keeps conversation history in the current Streamlit session.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

4. Copy .env.example to .env and add your own OpenRouter API key.
5. Start the app:

~~~bash
streamlit run app.py
~~~

The main app needs an OpenRouter API key. The optional Falcon example needs a Hugging Face token. Put keys only in your local .env; never commit it.

## Files

- app.py — main bilingual Agentic Minds chatbot.
- examples/falcon_demo.py — separate Hugging Face Hub example.
- examples/simple_chatbot.py — small Streamlit chatbot example.

Each app reads its token from environment variables. This repository does not contain API keys.
