import streamlit as st

st.set_page_config(
    page_title="Build-a-Bacterium",
    page_icon="🦠",
    layout="wide"
)
import streamlit as st

st.markdown("""
    <style>
    /* Target the selectbox input component */
    div[data-baseweb="select"] > div {
        background-color: #f0f2f6; /* Change to your desired color */
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

option = st.selectbox('Select an option', ['Option 1', 'Option 2'])
st.markdown("""
    <style>
    div[role="listbox"] ul {
        background-color: #f0f2f6; /* Background of the dropdown list */
    }
    div[role="listbox"] li {
        color: black; /* Color of the text in the list */
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Helper logic
# -----------------------------
def determine_metabolism(oxygen, electron_acceptor):
    if oxygen == "Present":
        return "Aerobic Respiration"
    if oxygen == "Absent" and electron_acceptor != "None":
        return "Anaerobic Respiration"
    return "Fermentation"


def carbon_source_notes(carbon_source):
    if carbon_source == "Glucose":
        return "Glucose enters central metabolism quickly and can move into glycolysis first."
    if carbon_source == "Complex carbohydrate":
        return "Complex carbohydrates must be broken down before their components can enter central metabolism."
    return "Mixed nutrients give the microbe flexibility because different molecules can feed into different pathways."


def compute_results(metabolism, carbon_source, nutrient_level, environment):
    if metabolism == "Fermentation":
        atp_score = 2
        atp_label = "Low"
        growth_score = 35
        byproducts = ["Organic acids", "Alcohols", "CO₂ (sometimes)"]
        pathway = "Glucose → Glycolysis → Fermentation → ATP"
        explanation = (
            "Fermentation produces ATP by substrate-level phosphorylation. "
            "It is simple and fast, but it leaves a lot of energy in the end products."
        )
        location = "Mostly in the cytoplasm"
        key_feature = "NADH is recycled by transferring electrons back to an internal organic molecule."
        examples = "Common fermentation products include lactate, ethanol, acids, and gas."

    elif metabolism == "Aerobic Respiration":
        atp_score = 9
        atp_label = "High"
        growth_score = 85
        byproducts = ["CO₂", "H₂O"]
        pathway = "Glucose → Glycolysis → TCA Cycle → Electron Transport System → ATP"
        explanation = (
            "Aerobic respiration uses an electron transport system in the membrane. "
            "Electrons move to oxygen, creating a proton motive force that powers ATP synthesis."
        )
        location = "Cytoplasm + membrane electron transport system"
        key_feature = "Oxygen is the terminal electron acceptor."
        examples = "This is modeled as the most energy-efficient pathway in the simulator."

    else:
        atp_score = 6
        atp_label = "Medium"
        growth_score = 65
        pathway = "Glucose → Glycolysis → TCA Cycle / Electron Transport System → ATP"
        explanation = (
            "Anaerobic respiration still uses an electron transport system, but oxygen is replaced "
            "by another terminal electron acceptor such as nitrate or sulfate."
        )
        location = "Cytoplasm + membrane electron transport system"
        key_feature = "Respiration does not always require oxygen."
        examples = "This strategy is useful in places like sediments, wetland soils, and low-oxygen habitats."

        if environment["electron_acceptor"] == "Nitrate (NO₃⁻)":
            byproducts = ["Reduced nitrogen compounds", "CO₂"]
        elif environment["electron_acceptor"] == "Sulfate (SO₄²⁻)":
            byproducts = ["Reduced sulfur compounds (for example H₂S)", "CO₂"]
        elif environment["electron_acceptor"] == "TMAO":
            byproducts = ["Trimethylamine-related products", "CO₂"]
        else:
            byproducts = ["Reduced inorganic products", "CO₂"]

    carbon_note = carbon_source_notes(carbon_source)

    if carbon_source == "Complex carbohydrate":
        growth_score -= 10
    elif carbon_source == "Mixed nutrients":
        growth_score += 5

    if nutrient_level == "Low":
        growth_score -= 20
    elif nutrient_level == "High":
        growth_score += 10

    growth_score = max(5, min(growth_score, 100))

    if growth_score >= 80:
        survival = "🟢 Optimal conditions: rapid growth and efficient energy production."
    elif growth_score >= 50:
        survival = "🟡 Survivable conditions: the bacterium can grow, but not at maximum efficiency."
    else:
        survival = "🔴 Stress conditions: growth is limited and energy is scarce."

    return {
        "atp_score": atp_score,
        "atp_label": atp_label,
        "growth_score": growth_score,
        "byproducts": byproducts,
        "pathway": pathway,
        "explanation": explanation,
        "location": location,
        "key_feature": key_feature,
        "examples": examples,
        "carbon_note": carbon_note,
        "survival": survival
    }


def preset_environment(choice):
    if choice == "Human gut":
        return {
            "oxygen": "Absent",
            "electron_acceptor": "None",
            "carbon_source": "Mixed nutrients",
            "nutrient_level": "High"
        }
    if choice == "Wetland soil":
        return {
            "oxygen": "Absent",
            "electron_acceptor": "Nitrate (NO₃⁻)",
            "carbon_source": "Complex carbohydrate",
            "nutrient_level": "Medium"
        }
    if choice == "Surface ocean":
        return {
            "oxygen": "Present",
            "electron_acceptor": "O₂ (oxygen)",
            "carbon_source": "Glucose",
            "nutrient_level": "Medium"
        }
    return {
        "oxygen": "Present",
        "electron_acceptor": "O₂ (oxygen)",
        "carbon_source": "Glucose",
        "nutrient_level": "High"
    }


def colored_tag(text, bg, color):
    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:0.35rem 0.75rem;
            border-radius:999px;
            background:{bg};
            color:{color};
            font-weight:700;
            font-size:0.95rem;
            margin-bottom:0.8rem;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def custom_meter(label, value, fill_color, text_color="#183153"):
    st.markdown(
        f"""
        <div style="margin-bottom:0.35rem; font-weight:700; color:{text_color};">{label}</div>
        <div style="
            width:100%;
            height:10px;
            background:#e7edf7;
            border-radius:999px;
            overflow:hidden;
            margin-bottom:0.9rem;
            border:1px solid #d7e1f0;">
            <div style="
                width:{max(0, min(value, 100))}%;
                height:100%;
                background:{fill_color};
                border-radius:999px;">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stat_card(title, value):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">{title}</div>
            <div class="stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


comparison_data = {
    "Fermentation": {
        "ATP yield": "Low",
        "Needs oxygen?": "No",
        "Uses ETS?": "No",
        "Terminal acceptor": "Internal organic molecule",
        "ATP method": "Substrate-level phosphorylation",
        "Summary": "Simple, fast, and wasteful"
    },
    "Aerobic Respiration": {
        "ATP yield": "High",
        "Needs oxygen?": "Yes",
        "Uses ETS?": "Yes",
        "Terminal acceptor": "O₂",
        "ATP method": "Proton motive force / oxidative phosphorylation",
        "Summary": "Most efficient in this simulator"
    },
    "Anaerobic Respiration": {
        "ATP yield": "Medium",
        "Needs oxygen?": "No",
        "Uses ETS?": "Yes",
        "Terminal acceptor": "Nitrate, sulfate, TMAO, etc.",
        "ATP method": "Proton motive force / oxidative phosphorylation",
        "Summary": "Flexible in low-oxygen environments"
    }
}

challenge_bank = [
    {
        "question": "Which condition should produce the fastest growth in this simulator?",
        "choices": [
            "No oxygen + no electron acceptor + low nutrients",
            "Oxygen present + glucose + high nutrients",
            "No oxygen + sulfate + low nutrients",
            "No oxygen + none + medium nutrients"
        ],
        "answer": "Oxygen present + glucose + high nutrients",
        "explanation": "Aerobic respiration with abundant nutrients is modeled as the most energy-efficient condition."
    },
    {
        "question": "Which setup is most likely to lead to fermentation?",
        "choices": [
            "Oxygen absent + no external electron acceptor",
            "Oxygen present + glucose",
            "Oxygen absent + nitrate available",
            "Oxygen present + sulfate available"
        ],
        "answer": "Oxygen absent + no external electron acceptor",
        "explanation": "Fermentation happens here because there is no usable external terminal electron acceptor."
    },
    {
        "question": "Which pathway in this simulator uses a proton motive force?",
        "choices": [
            "Fermentation only",
            "Aerobic respiration only",
            "Aerobic and anaerobic respiration",
            "None of them"
        ],
        "answer": "Aerobic and anaerobic respiration",
        "explanation": "Both forms of respiration use an electron transport system and proton motive force."
    },
]

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
        color: #1a1a1a;
    }

    p, span, label, li {
        color: #1a1a1a !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #183153 !important;
    }

    .hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 55%, #f59e0b 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 24px;
        margin-bottom: 1.0rem;
        box-shadow: 0 10px 30px rgba(29, 78, 216, 0.18);
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: white !important;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.97;
        color: white !important;
    }

    .card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(220,230,245,0.95);
        padding: 1.15rem;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(40, 60, 100, 0.08);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        color: #183153 !important;
    }

    .pathway-box {
        background: linear-gradient(135deg, #f5f9ff 0%, #ecf3ff 100%);
        border: 1px solid #dce8ff;
        border-left: 7px solid #2563eb;
        padding: 1rem;
        border-radius: 16px;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 0.5rem 0 0.9rem 0;
        color: #15325b !important;
    }

    .mini-card {
        background: #ffffff;
        border: 1px solid #e7edf7;
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 6px 18px rgba(20, 40, 70, 0.05);
        height: 100%;
    }

    .footer-note {
        font-size: 0.9rem;
        color: #526173 !important;
        background: rgba(255,255,255,0.88);
        border: 1px solid #e3ebf7;
        padding: 1rem;
        border-radius: 16px;
    }

    .comparison-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #183153 !important;
        margin-bottom: 0.6rem;
    }

    .stat-card {
        background: rgba(255,255,255,0.98);
        border: 1px solid #dfe8f5;
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 6px 18px rgba(20, 40, 70, 0.06);
        margin-bottom: 0.5rem;
        min-height: 108px;
    }

    .stat-title {
        font-size: 1rem;
        font-weight: 700;
        color: #44566c !important;
        margin-bottom: 0.45rem;
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #122b57 !important;
        line-height: 1.1;
        word-break: break-word;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7fbff 0%, #edf4ff 100%);
    }

    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    button[data-baseweb="tab"] {
        color: #183153 !important;
        font-weight: 700 !important;
    }

    /* Dropdowns / selectboxes */
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #d6e0ee !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    div[data-baseweb="select"] span {
        color: #1a1a1a !important;
    }

    div[data-baseweb="select"] input {
        color: #1a1a1a !important;
    }

    div[data-baseweb="select"] svg {
        fill: #1a1a1a !important;
    }

    div[role="listbox"] {
        background: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #d6e0ee !important;
    }

    div[role="option"] {
        background: #ffffff !important;
        color: #1a1a1a !important;
    }

    div[role="option"]:hover {
        background: #fff7ed !important;
        color: #1a1a1a !important;
    }
/* REMOVE STREAMLIT TOP BLACK BAR */
header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}
/* Pull app up after removing header */
.block-container {
    padding-top: 1rem !important;
}
    /* Radio options: blue outline / white center, orange on hover */
    div[role="radiogroup"] label {
        background: #ffffff !important;
        border: 2px solid #60a5fa !important;
        padding: 0.35rem 0.6rem;
        border-radius: 14px;
        margin-bottom: 0.45rem;
        transition: all 0.2s ease;
    }

    div[role="radiogroup"] label:hover {
        border-color: #f59e0b !important;
        background: #fffaf0 !important;
    }

    div[role="radiogroup"] label p {
        color: #1a1a1a !important;
        font-weight: 500;
    }

    /* Button styling */
    .stButton > button {
        background: #ffffff !important;
        color: #1d4ed8 !important;
        border: 2px solid #60a5fa !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 0.45rem 1rem !important;
        box-shadow: 0 3px 8px rgba(29, 78, 216, 0.10);
    }

    .stButton > button:hover {
        background: #fffaf0 !important;
        color: #b45309 !important;
        border-color: #f59e0b !important;
    }

    .stButton > button:active {
        background: #fff7ed !important;
        color: #b45309 !important;
        border-color: #f59e0b !important;
    }

    /* Remove extra vertical spacing that creates blank oval-looking gaps */
    div.block-container {
        padding-top: 1rem !important;
    }

    .element-container:has([data-testid="stMetric"]) {
        display: none !important;
    }

    [data-testid="metric-container"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🦠 Build-a-Bacterium: Metabolic Survival Simulator</div>
        <div class="hero-subtitle">
            Adjust the environment and watch how a bacterium changes its strategy for making ATP, growing, and surviving.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.markdown("## ⚙️ Environment Controls")

preset = st.sidebar.selectbox(
    "Real-world preset",
    ["Custom", "Human gut", "Wetland soil", "Surface ocean"],
    index=0
)

preset_values = preset_environment(preset) if preset != "Custom" else None

oxygen = st.sidebar.selectbox(
    "🫁 Oxygen level",
    ["Present", "Absent"],
    index=0 if preset_values is None else ["Present", "Absent"].index(preset_values["oxygen"])
)

electron_options = ["O₂ (oxygen)", "Nitrate (NO₃⁻)", "Sulfate (SO₄²⁻)", "TMAO", "None"]
electron_acceptor = st.sidebar.selectbox(
    "⚡ Terminal electron acceptor",
    electron_options,
    index=0 if preset_values is None else electron_options.index(preset_values["electron_acceptor"])
)

carbon_options = ["Glucose", "Complex carbohydrate", "Mixed nutrients"]
carbon_source = st.sidebar.selectbox(
    "🍞 Carbon source",
    carbon_options,
    index=0 if preset_values is None else carbon_options.index(preset_values["carbon_source"])
)

nutrient_options = ["Low", "Medium", "High"]
nutrient_level = st.sidebar.select_slider(
    "🔋 Nutrient level",
    options=nutrient_options,
    value="Medium" if preset_values is None else preset_values["nutrient_level"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: Try switching between oxygen present, anaerobic acceptors, and no acceptor to compare aerobic respiration, anaerobic respiration, and fermentation."
)

if oxygen == "Present" and electron_acceptor != "O₂ (oxygen)":
    st.sidebar.warning("Oxygen is present, so the simulator will treat this as aerobic respiration.")

if oxygen == "Absent" and electron_acceptor == "O₂ (oxygen)":
    st.sidebar.warning("If oxygen is absent, oxygen cannot serve as the terminal electron acceptor.")

# -----------------------------
# Normalize logic
# -----------------------------
effective_acceptor = electron_acceptor
if oxygen == "Present":
    effective_acceptor = "O₂ (oxygen)"
elif oxygen == "Absent" and electron_acceptor == "O₂ (oxygen)":
    effective_acceptor = "None"

environment = {
    "oxygen": oxygen,
    "electron_acceptor": effective_acceptor,
    "carbon_source": carbon_source,
    "nutrient_level": nutrient_level
}

metabolism = determine_metabolism(oxygen, effective_acceptor)
results = compute_results(metabolism, carbon_source, nutrient_level, environment)

# -----------------------------
# Top stat cards
# -----------------------------
m1, m2, m3 = st.columns(3)
with m1:
    stat_card("Pathway", metabolism)
with m2:
    stat_card("ATP Yield", results["atp_label"])
with m3:
    stat_card("Estimated Growth", f'{results["growth_score"]}%')

# -----------------------------
# Main content
# -----------------------------
left, middle, right = st.columns([1.05, 1.2, 1.0])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧪 Current Environment</div>', unsafe_allow_html=True)
    st.write(f"**Oxygen:** {oxygen}")
    st.write(f"**Electron acceptor:** {effective_acceptor}")
    st.write(f"**Carbon source:** {carbon_source}")
    st.write(f"**Nutrient level:** {nutrient_level}")

    st.markdown("#### Quick interpretation")
    if metabolism == "Aerobic Respiration":
        colored_tag("Aerobic mode", "#d8ecff", "#124a8a")
        st.write("This bacterium can use oxygen as the terminal electron acceptor.")
    elif metabolism == "Anaerobic Respiration":
        colored_tag("Anaerobic mode", "#fff2d6", "#8a5a00")
        st.write("This bacterium is respiring without oxygen by using an alternative acceptor.")
    else:
        colored_tag("Fermentation mode", "#ffe0e0", "#8a1c1c")
        st.write("This bacterium has no usable external electron acceptor, so it ferments.")
    st.markdown('</div>', unsafe_allow_html=True)

with middle:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔬 What Your Bacterium Does</div>', unsafe_allow_html=True)

    if metabolism == "Aerobic Respiration":
        colored_tag("Selected pathway: Aerobic Respiration", "#d8ecff", "#124a8a")
    elif metabolism == "Anaerobic Respiration":
        colored_tag("Selected pathway: Anaerobic Respiration", "#fff2d6", "#8a5a00")
    else:
        colored_tag("Selected pathway: Fermentation", "#ffe0e0", "#8a1c1c")

    st.markdown(f'<div class="pathway-box">{results["pathway"]}</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["How it works", "Key feature", "Where it happens"])
    with tab1:
        st.write(results["explanation"])
        st.write(f"**Carbon source note:** {results['carbon_note']}")
    with tab2:
        st.write(results["key_feature"])
        st.write(results["examples"])
    with tab3:
        st.write(results["location"])

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Results Dashboard</div>', unsafe_allow_html=True)

    custom_meter("ATP efficiency", results["atp_score"] * 10, "linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%)")
    custom_meter("Growth potential", results["growth_score"], "linear-gradient(90deg, #10b981 0%, #34d399 100%)")

    st.markdown("#### 🧪 Byproducts")
    for item in results["byproducts"]:
        st.write(f"• {item}")

    st.markdown("#### 📣 Survival Feedback")
    st.write(results["survival"])
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Interactive comparison section
# -----------------------------
st.markdown("## Compare the Major Strategies")

compare_left, compare_right = st.columns(2)
with compare_left:
    strategy_a = st.selectbox("Choose strategy A", list(comparison_data.keys()), index=0)
with compare_right:
    strategy_b = st.selectbox("Choose strategy B", list(comparison_data.keys()), index=1)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="mini-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-title">{strategy_a}</div>', unsafe_allow_html=True)
    for k, v in comparison_data[strategy_a].items():
        st.write(f"**{k}:** {v}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="mini-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="comparison-title">{strategy_b}</div>', unsafe_allow_html=True)
    for k, v in comparison_data[strategy_b].items():
        st.write(f"**{k}:** {v}")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Challenge mode
# -----------------------------
st.markdown("## 🎯 Challenge Mode")

if "challenge_index" not in st.session_state:
    st.session_state.challenge_index = 0

challenge = challenge_bank[st.session_state.challenge_index]

st.write(f"**{challenge['question']}**")
answer = st.radio(
    "Choose your answer:",
    challenge["choices"],
    index=None,
    key=f"challenge_{st.session_state.challenge_index}"
)

if answer is not None:
    if answer == challenge["answer"]:
        st.success(f"Correct! {challenge['explanation']}")
    else:
        st.error(f"Not quite. {challenge['explanation']}")

if st.button("Load New Challenge"):
    st.session_state.challenge_index = (st.session_state.challenge_index + 1) % len(challenge_bank)
    st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    """
    <div class="footer-note">
        This simulator is intentionally simplified for teaching. Real microbes are much more diverse and may use
        specialized pathways, different electron donors, or unique ecological strategies depending on their environment.
    </div>
    """,
    unsafe_allow_html=True
)
