import streamlit as st
import asyncio
import os
import sys
from agent.auto_ppt_agent import run_agent

st.set_page_config(
    page_title="Auto PPT Agent",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
<style>

/* background */
.stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 100%);
}

/* main card */
.main-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,180,216,0.2);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

/* header */
.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00b4d8, #90e0ef);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero-sub {
    text-align: center;
    color: #adb5bd;
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
}

/* chip buttons */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin: 1rem 0 1.5rem 0;
}
.chip {
    background: rgba(0,180,216,0.15);
    border: 1px solid rgba(0,180,216,0.4);
    color: #90e0ef;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    background: rgba(0,180,216,0.35);
}

/* textarea */
.stTextArea textarea {
    background: rgba(255,255,255,0.07) !important;
    color: #03045e !important;   /* force visible text */
    border: 1px solid rgba(0,180,216,0.3) !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    caret-color: #03045e !important;  /* cursor visible */
}

/* generate button */
.stButton > button {
    background: linear-gradient(90deg, #00b4d8, #0077b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.2em !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}

/* download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, #00b4d8, #0077b6) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    height: 3em !important;
}

/* progress stepper */
.stepper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07);
}
.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    flex: 1;
}
.step-icon {
    font-size: 1.4rem;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
}
.step-icon.done {
    border-color: #00b4d8;
    background: rgba(0,180,216,0.15);
}
.step-icon.active {
    border-color: #90e0ef;
    background: rgba(144,224,239,0.2);
    animation: pulse 1.2s infinite;
}
.step-label {
    font-size: 0.72rem;
    color: #adb5bd;
    text-align: center;
}
.step-label.done { color: #00b4d8; }
.step-label.active { color: #90e0ef; }
.step-divider {
    height: 2px;
    flex: 0.3;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    margin-bottom: 20px;
}
.step-divider.done { background: #00b4d8; }

@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(0,180,216,0.5); }
    70%  { box-shadow: 0 0 0 8px rgba(0,180,216,0); }
    100% { box-shadow: 0 0 0 0 rgba(0,180,216,0); }
}

/* log box */
.log-box {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 1rem;
    font-family: monospace;
    font-size: 0.82rem;
    color: #90e0ef;
    max-height: 220px;
    overflow-y: auto;
    margin-top: 1rem;
}

/* success box */
.success-box {
    background: rgba(0,180,216,0.1);
    border: 1px solid rgba(0,180,216,0.4);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.success-box h3 {
    color: #00b4d8;
    margin: 0 0 0.5rem 0;
}
.success-box p {
    color: #adb5bd;
    font-size: 0.9rem;
    margin: 0;
}

/* footer */
.footer {
    text-align: center;
    color: #495057;
    font-size: 0.85rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)


# ── EXAMPLE PROMPTS ──────────────────────────────────────────
EXAMPLE_PROMPTS = [
    "Deep Learning vs Machine Learning",
    "Blockchain Technology and Its Applications",
    "Cloud Computing Architecture",
    "Cybersecurity Threats and Prevention",
    "Operating System Concepts",
    "Evolution of Artificial Intelligence",
]

# ── STEPPER HELPER ───────────────────────────────────────────
STEPS = [
    ("🧠", "Planning"),
    ("🔍", "Searching"),
    ("📄", "Creating"),
    ("🖼️", "Slides"),
    ("💾", "Saving"),
]

def render_stepper(active: int):
    """Render progress stepper. active = index of current step (0-based)."""
    parts = []
    for i, (icon, label) in enumerate(STEPS):
        if i < active:
            icon_cls  = "done"
            label_cls = "done"
            disp      = "✅"
        elif i == active:
            icon_cls  = "active"
            label_cls = "active"
            disp      = icon
        else:
            icon_cls  = ""
            label_cls = ""
            disp      = icon

        parts.append(f"""
        <div class="step">
            <div class="step-icon {icon_cls}">{disp}</div>
            <div class="step-label {label_cls}">{label}</div>
        </div>
        """)

        if i < len(STEPS) - 1:
            div_cls = "done" if i < active else ""
            parts.append(f'<div class="step-divider {div_cls}"></div>')

    html = f'<div class="stepper">{"".join(parts)}</div>'
    return html


# ── HEADER ───────────────────────────────────────────────────
st.markdown('<div class="hero-title">✨ Auto PPT Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Turn your idea into a presentation in seconds</div>',
    unsafe_allow_html=True
)

# ── MAIN CARD ────────────────────────────────────────────────
#st.markdown('<div class="main-card">', unsafe_allow_html=True)



# Clicking a chip fills the box via session state
if "prompt_value" not in st.session_state:
    st.session_state.prompt_value = ""

cols = st.columns(len(EXAMPLE_PROMPTS))
for i, ep in enumerate(EXAMPLE_PROMPTS):
    with cols[i % len(EXAMPLE_PROMPTS)]:
        pass

# Hidden buttons for chips (one per chip)
st.markdown("<div style='display:flex; gap:8px; flex-wrap:wrap; margin-bottom:0.5rem;'>", unsafe_allow_html=True)
chip_cols = st.columns(3)
for i, ep in enumerate(EXAMPLE_PROMPTS):
    with chip_cols[i % 3]:
        if st.button(ep, key=f"chip_{i}", use_container_width=True):
           st.session_state.prompt_value = ep
# Text area
prompt = st.text_area(
    "Enter your topic",
    value=st.session_state.prompt_value,
    placeholder="e.g. Create a 5-slide presentation on Artificial Intelligence",
    height=110,
    label_visibility="collapsed",
)

generate = st.button("Generate Presentation", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── GENERATION SECTION ───────────────────────────────────────
if generate:
    if not prompt.strip():
        st.warning("Please enter a topic first.")
    else:
        stepper_box = st.empty()
        log_box     = st.empty()
        logs        = []
        current_step = [0]

        # Map log keywords → stepper step index
        STEP_KEYWORDS = {
            "plan":   0,
            "search": 1,
            "create": 2,
            "slide":  3,
            "saving": 4,
            "save":   4,
            "done":   5,
        }

        class LogCapture:
            def write(self, msg):
                if msg.strip():
                    logs.append(msg.strip())
                    # Advance stepper based on log content
                    lower = msg.lower()
                    for kw, idx in STEP_KEYWORDS.items():
                        if kw in lower and idx >= current_step[0]:
                            current_step[0] = idx
                            break
                    stepper_box.markdown(
                        render_stepper(current_step[0]),
                        unsafe_allow_html=True
                    )
                    log_html = (
                        '<div class="log-box">'
                        + "<br>".join(logs[-14:])
                        + "</div>"
                    )
                    log_box.markdown(log_html, unsafe_allow_html=True)

            def flush(self):
                pass

        stepper_box.markdown(render_stepper(0), unsafe_allow_html=True)

        old_stdout = sys.stdout
        sys.stdout = LogCapture()

        try:
            asyncio.run(run_agent(prompt))
            sys.stdout = old_stdout
            current_step[0] = 5
            stepper_box.markdown(render_stepper(5), unsafe_allow_html=True)

            output_path = "output.pptx"
            if os.path.exists(output_path):
                log_box.empty()
                st.markdown("""
                <div class="success-box">
                    <h3> Presentation Ready!</h3>
                    <p>Your presentation has been generated successfully.</p>
                </div>
                """, unsafe_allow_html=True)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Presentation",
                        data=f,
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
            else:
                st.error("File not found. Something went wrong.")

        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Agent failed: {e}")


# ── FOOTER ───────────────────────────────────────────────────
st.markdown(
    '<div class="footer">Built with Groq · LangChain · MCP · python-pptx</div>',
    unsafe_allow_html=True
)