from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Mood Chat", page_icon="🎭", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: #0d0d0d;
    color: #f0ede6;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 760px; padding: 2rem 1.5rem 6rem; }

.chat-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem; font-weight: 800;
    letter-spacing: -1px; color: #f0ede6; margin-bottom: 0.1rem;
}
.chat-subtitle {
    font-size: 0.72rem; color: #555;
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 2rem;
}

.mode-card {
    border: 1px solid #2a2a2a; border-radius: 14px;
    padding: 1.2rem 0.9rem; text-align: center;
    background: #141414; margin-bottom: 0.5rem;
}
.mode-emoji { font-size: 2.2rem; }
.mode-label { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; margin-top: 0.4rem; letter-spacing: 1px; }

.msg-row { display: flex; gap: 12px; margin-bottom: 1.2rem; align-items: flex-start; }
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0; border: 1px solid #2a2a2a;
}
.avatar.bot  { background: #1a1a1a; }
.avatar.user { background: var(--accent, #c8ff00); color: #0d0d0d; }

.bubble {
    max-width: 78%; padding: 0.75rem 1.1rem;
    border-radius: 14px; font-size: 0.88rem;
    line-height: 1.65; word-break: break-word;
}
.bubble.bot {
    background: #1a1a1a; border: 1px solid #272727;
    border-top-left-radius: 4px; color: #ddd;
}
.bubble.user {
    background: var(--accent, #c8ff00); color: #0d0d0d;
    border-top-right-radius: 4px; font-weight: 700;
}

.stTextInput > div > div > input {
    background: #141414 !important; border: 1px solid #2a2a2a !important;
    border-radius: 10px !important; color: #f0ede6 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important; padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus { border-color: #888 !important; }
.stTextInput > div > div > input::placeholder { color: #444 !important; }

.stButton > button {
    background: var(--accent, #c8ff00) !important; color: #0d0d0d !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    font-size: 0.85rem !important; border: none !important;
    border-radius: 10px !important; padding: 0.75rem 1.6rem !important;
    width: 100%; transition: opacity 0.15s;
}
.stButton > button:hover { opacity: 0.85 !important; }
hr { border-color: #1e1e1e; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Mode definitions ──────────────────────────────────────────────────────────
MODES = {
    1: {
        "label": "ANGRY",
        "emoji": "😡",
        "accent": "#ff3b30",
        "system": "you are an angry AI agent. you respond aggressively and impatiently",
    },
    2: {
        "label": "FUNNY",
        "emoji": "🤡",
        "accent": "#c8ff00",
        "system": "you are a very funny AI agent. you respond with humor and jokes",
    },
    3: {
        "label": "SAD",
        "emoji": "😢",
        "accent": "#5e9bff",
        "system": "you are very sad AI agent. you respond accordingly",
    },
}

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")

model = get_model()

# ── Session state ─────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-title">🎭 AI Mood Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">powered by mistral · langchain</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — Mode selection
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode is None:

    st.markdown("### Choose your AI mode")
    col1, col2, col3 = st.columns(3)

    for col, key in zip([col1, col2, col3], [1, 2, 3]):
        m = MODES[key]
        with col:
            st.markdown(f"""
            <div class="mode-card">
                <div class="mode-emoji">{m['emoji']}</div>
                <div class="mode-label" style="color:{m['accent']};">{m['label']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {m['label'].capitalize()}", key=f"btn{key}", use_container_width=True):
                st.session_state.mode = key
                st.session_state.messages = [SystemMessage(content=m["system"])]
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — Chat
# ═══════════════════════════════════════════════════════════════════════════════
else:
    m = MODES[st.session_state.mode]

    # Inject accent colour
    st.markdown(f"<style>:root {{ --accent: {m['accent']}; }}</style>", unsafe_allow_html=True)

    # Mode badge + reset
    badge_col, reset_col = st.columns([5, 1])
    with badge_col:
        st.markdown(
            f"<span style='font-size:0.8rem;color:{m['accent']};letter-spacing:2px;"
            f"text-transform:uppercase;font-weight:700;'>{m['emoji']} {m['label']} MODE</span>",
            unsafe_allow_html=True,
        )
    with reset_col:
        if st.button("↩ Reset", use_container_width=True):
            st.session_state.mode = None
            st.session_state.messages = []
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Render conversation ───────────────────────────────────────────────────
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user">🧑</div>
                <div class="bubble user">{msg.content}</div>
            </div>""", unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"""
            <div class="msg-row bot">
                <div class="avatar bot">{m['emoji']}</div>
                <div class="bubble bot">{msg.content}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Input row ─────────────────────────────────────────────────────────────
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            label="",
            placeholder="Type your message…",
            label_visibility="collapsed",
            key=f"user_input_{st.session_state.input_counter}",
        )
    with col2:
        send = st.button("Send", use_container_width=True)

    if send and user_input.strip():
        prompt = user_input.strip()
        st.session_state.messages.append(HumanMessage(content=prompt))

        with st.spinner("Thinking…"):
            response = model.invoke(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content=response.content))
        st.session_state.input_counter += 1  # forces input box to re-render empty
        st.rerun()