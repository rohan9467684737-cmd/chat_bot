# 🎭 AI Mood Chat

A conversational AI chatbot with 3 personality modes, built with **LangChain**, **Mistral AI**, and **Streamlit**.

[![Streamlit App](https://chatbot-rmz64ksvt6bd4hzhc9ctfg.streamlit.app/)

---

## 🤖 Modes

| Mode | Personality |
|------|-------------|
| 😡 Angry | Responds aggressively and impatiently |
| 🤡 Funny | Responds with humor and jokes |
| 😢 Sad | Responds in a melancholic tone |

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/rohan9467684737-cmd/chat_bot.git
cd chat_bot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the root folder:
```
MISTRAL_API_KEY=your_api_key_here
```

**4. Run the app**
```bash
streamlit run uichatbot_streamlit.py
```

---

## 🛠️ Tech Stack

- [LangChain](https://www.langchain.com/) — LLM framework
- [Mistral AI](https://mistral.ai/) — `mistral-small-2506` model
- [Streamlit](https://streamlit.io/) — UI framework
- [python-dotenv](https://pypi.org/project/python-dotenv/) — API key management

---

## 📁 Project Structure

```
chat_bot/
├── uichatbot_streamlit.py   # Main Streamlit app
├── requirements.txt         # Dependencies
├── .env                     # API key (not pushed to GitHub)
└── README.md
```

---

## ⚠️ Important

Never share your `.env` file. Your `MISTRAL_API_KEY` should stay private.
