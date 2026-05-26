import json
import streamlit as st

st.set_page_config(
    page_title="MemoryLens",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #faf9f7;
    color: #0d0d0d;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 3.5rem 2rem 4rem 2rem; max-width: 700px; }

.ml-title {
    font-family: 'Lora', serif;
    font-size: 2.4rem;
    font-weight: 500;
    color: #0d0d0d;
    margin-bottom: 0.2rem;
}
.ml-sub {
    font-size: 1rem;
    color: #7a7975;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

div[data-testid="stTextInput"] label { display: none !important; }
div[data-testid="stTextInput"] input {
    background: #fff !important;
    border: 1px solid #e2e0db !important;
    border-radius: 6px !important;
    color: #0d0d0d !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.15s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #b8a99a !important;
    box-shadow: 0 0 0 3px rgba(184,169,154,0.12) !important;
    outline: none !important;
}

hr { border: none; border-top: 1px solid #ebe9e4; margin: 1.4rem 0; }

.ml-count {
    font-size: 0.92rem;
    color: #7a7975;
    margin-bottom: 0.6rem;
    font-weight: 400;
}

.ml-card {
    display: flex;
    gap: 1.4rem;
    padding: 1.1rem 0;
    border-bottom: 1px solid #f0ede8;
}
.ml-card:last-child { border-bottom: none; }

.ml-time {
    flex-shrink: 0;
    width: 3.8rem;
    text-align: right;
    padding-top: 0.15rem;
}
.ml-time-start {
    font-size: 0.95rem;
    font-weight: 500;
    color: #7a6e65;
}
.ml-time-end {
    font-size: 0.85rem;
    color: #a09d98;
    margin-top: 0.1rem;
}

.ml-bar {
    width: 1px;
    background: #e8e5e0;
    flex-shrink: 0;
}

.ml-body { flex: 1; }
.ml-text {
    font-size: 1.15rem;
    color: #111111;
    font-weight: 400;
    line-height: 1.55;
    margin-bottom: 0.45rem;
}
.ml-meta {
    display: flex;
    gap: 1.2rem;
}
.ml-tag {
    font-size: 0.92rem;
    color: #8a8883;
    font-weight: 300;
}
.ml-tag span { color: #4a4945; }

.ml-empty {
    font-size: 1rem;
    color: #999;
    text-align: center;
    padding: 3rem 0;
}
</style>
""", unsafe_allow_html=True)


MEMORY_FILE = "outputs/memory_timeline.json"

with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)


st.markdown('<div class="ml-title">MemoryLens</div>', unsafe_allow_html=True)
st.markdown('<div class="ml-sub">multimodal memory retrieval</div>', unsafe_allow_html=True)

query = st.text_input("search", placeholder="search by word, person, speaker…").lower().strip()

st.markdown("<hr>", unsafe_allow_html=True)

results = [
    e for e in memory
    if not query or query in " ".join([
        e.get("text", ""),
        e.get("person", ""),
        e.get("speaker", ""),
        " ".join(e.get("visible", []))
    ]).lower()
]

if query:
    count = len(results)
    st.markdown(
        f'<div class="ml-count">{count} result{"s" if count != 1 else ""}</div>',
        unsafe_allow_html=True
    )

if query and not results:
    st.markdown('<div class="ml-empty">nothing found</div>', unsafe_allow_html=True)

cards_html = ""
for e in results:
    visible_str = ", ".join(e.get("visible", [])) or "—"
    cards_html += f"""
    <div class="ml-card">
        <div class="ml-time">
            <div class="ml-time-start">{e.get('start')}s</div>
            <div class="ml-time-end">{e.get('end')}s</div>
        </div>
        <div class="ml-bar"></div>
        <div class="ml-body">
            <div class="ml-text">{e.get('text', '')}</div>
            <div class="ml-meta">
                <div class="ml-tag">speaker&nbsp;<span>{e.get('speaker', '—')}</span></div>
                <div class="ml-tag">visible&nbsp;<span>{visible_str}</span></div>
            </div>
        </div>
    </div>
    """

if cards_html:
    st.markdown(cards_html, unsafe_allow_html=True)