import streamlit as st

st.set_page_config(
    page_title="Build-a-Bacterium",
    page_icon="🦠",
    layout="wide"
)

# -----------------------------
# Helper logic
# -----------------------------
def determine_metabolism(oxygen, electron_acceptor):
    """
    Decide whether the cell uses aerobic respiration,
    anaerobic respiration, or fermentation.
    """
    if oxygen == "Present":
        return "Aerobic Respiration"
    if oxygen == "Absent" and electron_acceptor != "None":
        return "Anaerobic Respiration"
    return "Fermentation"


def carbon_source_notes(carbon_source):
    """
    Give short notes based on the chosen carbon source.
    """
    if carbon_source == "Glucose":
        return (
            "Glucose enters central metabolism easily and can be processed through glycolysis. "
            "From there, the cell may continue into fermentation or respiration depending on conditions."
        )
    if carbon_source == "Complex carbohydrate":
        return (
            "Complex carbohydrates must be broken down first. This can slow energy access compared with glucose, "
            "but the products still feed into central metabolic pathways."
        )
    return (
        "Mixed nutrients provide flexibility. Different molecules can enter central pathways such as glycolysis, "
        "the pentose phosphate pathway, or the TCA cycle."
    )


def compute_results(metabolism, carbon_source, nutrient_level, environment):
    """
    Return a dictionary of outputs for the dashboard.
    This is intentionally simplified for learning value.
    """
    # Base values
    if metabolism == "Fermentation":
        atp_score = 2
        atp_label = "Low"
        growth_score = 35
        byproducts = ["Organic acids", "Alcohols", "CO₂ (sometimes)"]
        pathway = "Glucose → Glycolysis → Fermentation → ATP"
        explanation = (
            "Fermentation makes ATP directly from an energy-rich intermediate "
            "by substrate-level phosphorylation. It is simple and fast, but wasteful."
        )
        location = "Mostly in the cytoplasm"
        key_feature = "NADH is recycled by passing electrons back to an internal organic molecule."
        examples = "Examples include lactic acid, mixed acid, and alcohol fermentation."

    elif metabolism == "Aerobic Respiration":
        atp_score = 9
        atp_label = "High"
        growth_score = 85
        byproducts = ["CO₂", "H₂O"]
        pathway = "Glucose → Glycolysis → TCA Cycle → ETS/ETC → ATP"
        explanation = (
            "Aerobic respiration uses an electron transport system in the membrane. "
            "Electrons flow to oxygen, and the released energy helps generate a proton motive force for ATP synthesis."
        )
        location = "Cytoplasm + cell membrane electron transport system"
        key_feature = "Oxygen is the terminal electron acceptor."
        examples = "Often the most energy-efficient option when oxygen is available."

    else:  # Anaerobic Respiration
        atp_score = 6
        atp_label = "Medium"
        growth_score = 65
        pathway = "Glucose → Glycolysis → TCA Cycle / ETS → ATP"
        explanation = (
            "Anaerobic respiration still uses an electron transport system, but oxygen is replaced "
            "by another terminal electron acceptor such as nitrate or sulfate."
        )
        location = "Cytoplasm + cell membrane electron transport system"
        key_feature = "Respiration does not always require oxygen."
        examples = "This often occurs in environments like wetland soil or the gut."

        if environment["electron_acceptor"] == "Nitrate (NO₃⁻)":
            byproducts = ["Possible nitrogen compounds", "CO₂"]
        elif environment["electron_acceptor"] == "Sulfate (SO₄²⁻)":
            byproducts = ["Possible sulfur compounds (for example H₂S)", "CO₂"]
        elif environment["electron_acceptor"] == "TMAO":
            byproducts = ["Trimethylamine-related products", "CO₂"]
        else:
            byproducts = ["Reduced inorganic products", "CO₂"]

    # Carbon source adjustment
    carbon_note = carbon_source_notes(carbon_source)
    if carbon_source == "Complex carbohydrate":
        growth_score -= 10
    elif carbon_source == "Mixed nutrients":
        growth_score += 5

    # Nutrient adjustment
    if nutrient_level == "Low":
        growth_score -= 20
    elif nutrient_level == "Medium":
        growth_score += 0
    else:  # High
        growth_score += 10

    # Keep within range
    growth_score = max(5, min(growth_score, 100))

    # Survival feedback
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


def draw_progress_bar(label, value, color):
    """
    Render a simple HTML progress bar.
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 0.3rem; font-weight: 600;">{label}</div>
        <div style="background-color: #eaeaea; border-radius: 10px; height: 20px; width: 100%; margin-bottom: 0.8rem;">
            <div style="background-color: {color}; width: {value}%; height: 20px; border-radius: 10px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def preset_environment(choice):
    """
    Provide real-world presets.
    """
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


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #444444;
        margin-bottom: 1.2rem;
    }
    .section-card {
        background-color: #f8f9fb;
        border: 1px solid #e6e9ef;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }
    .big-metric {
        font-size: 2rem;
        font-weight: 800;
    }
    .small-label {
        color: #555;
        font-size: 0.95rem;
    }
    .pathway-box {
        background-color: #ffffff;
        border-left: 6px solid #4c78a8;
        padding: 0.9rem;
        border-radius: 10px;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .footer-note {
        font-size: 0.9rem;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🦠 Build-a-Bacterium: Metabolic Survival Simulator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Choose environmental conditions and see how your microbe makes ATP, grows, and survives.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Top controls
# -----------------------------
with st.expander("How to use this simulator", expanded=False):
    st.write(
        """
        1. Choose the environment conditions on the left.
        2. Watch the middle panel update with the metabolic pathway used.
        3. Check the right panel for ATP yield, growth, and byproducts.
        4. Try the preset environments to compare how microbes survive in different habitats.
        """
    )

preset = st.selectbox(
    "Optional real-world preset",
    ["Custom", "Human gut", "Wetland soil", "Surface ocean"]
)

preset_values = preset_environment(preset) if preset != "Custom" else None

# -----------------------------
# Main layout
# -----------------------------
left, middle, right = st.columns([1.05, 1.25, 1.1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Environment Controls")

    oxygen = st.radio(
        "🫁 Oxygen level",
        ["Present", "Absent"],
        index=0 if preset_values is None else ["Present", "Absent"].index(preset_values["oxygen"])
    )

    electron_options = ["O₂ (oxygen)", "Nitrate (NO₃⁻)", "Sulfate (SO₄²⁻)", "TMAO", "None"]
    electron_acceptor = st.selectbox(
        "⚡ Terminal electron acceptor",
        electron_options,
        index=0 if preset_values is None else electron_options.index(preset_values["electron_acceptor"])
    )

    carbon_options = ["Glucose", "Complex carbohydrate", "Mixed nutrients"]
    carbon_source = st.selectbox(
        "🍞 Carbon source",
        carbon_options,
        index=0 if preset_values is None else carbon_options.index(preset_values["carbon_source"])
    )

    nutrient_options = ["Low", "Medium", "High"]
    nutrient_level = st.select_slider(
        "🔋 Nutrient level",
        options=nutrient_options,
        value="Medium" if preset_values is None else preset_values["nutrient_level"]
    )

    if oxygen == "Present" and electron_acceptor != "O₂ (oxygen)":
        st.info("Because oxygen is present, this simulator will treat the bacterium as using aerobic respiration.")

    if oxygen == "Absent" and electron_acceptor == "O₂ (oxygen)":
        st.warning("Oxygen cannot be used as the terminal electron acceptor if oxygen is absent. Consider choosing another acceptor or 'None'.")

    st.markdown('</div>', unsafe_allow_html=True)

# Normalize inconsistent oxygen/acceptor combinations for learning logic
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

with middle:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("What Your Bacterium Does")

    if metabolism == "Aerobic Respiration":
        st.success("Selected pathway: Aerobic Respiration")
    elif metabolism == "Anaerobic Respiration":
        st.warning("Selected pathway: Anaerobic Respiration")
    else:
        st.error("Selected pathway: Fermentation")

    st.markdown(f'<div class="pathway-box"><strong>{results["pathway"]}</strong></div>', unsafe_allow_html=True)

    st.markdown("**What this means**")
    st.write(results["explanation"])

    st.markdown("**Key feature**")
    st.write(results["key_feature"])

    st.markdown("**Where it happens**")
    st.write(results["location"])

    st.markdown("**Carbon source note**")
    st.write(results["carbon_note"])

    st.markdown("**Microbiology takeaway**")
    st.write(results["examples"])

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Results Dashboard")

    st.markdown(f'<div class="big-metric">{results["atp_label"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-label">ATP yield</div>', unsafe_allow_html=True)

    draw_progress_bar("ATP efficiency", results["atp_score"] * 10, "#4c78a8")
    draw_progress_bar("Estimated growth", results["growth_score"], "#54a24b")

    st.markdown("**🧪 Byproducts**")
    for item in results["byproducts"]:
        st.write(f"- {item}")

    st.markdown("**📣 Survival feedback**")
    st.write(results["survival"])

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Comparison / self-check section
# -----------------------------
st.markdown("---")
st.subheader("Compare the major strategies")

compare_cols = st.columns(3)

comparison_data = {
    "Fermentation": {
        "ATP": "Low",
        "Oxygen required?": "No",
        "Electron transport system?": "No",
        "Terminal electron acceptor": "Internal organic molecule",
        "Main ATP method": "Substrate-level phosphorylation",
        "General idea": "Fast and simple, but wasteful"
    },
    "Aerobic Respiration": {
        "ATP": "High",
        "Oxygen required?": "Yes in this simulator",
        "Electron transport system?": "Yes",
        "Terminal electron acceptor": "O₂",
        "Main ATP method": "Proton motive force / oxidative phosphorylation",
        "General idea": "Efficient and strong growth"
    },
    "Anaerobic Respiration": {
        "ATP": "Medium",
        "Oxygen required?": "No",
        "Electron transport system?": "Yes",
        "Terminal electron acceptor": "Nitrate, sulfate, TMAO, etc.",
        "Main ATP method": "Proton motive force / oxidative phosphorylation",
        "General idea": "Flexible in low-oxygen environments"
    }
}

for i, strategy in enumerate(comparison_data):
    with compare_cols[i]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### {strategy}")
        for k, v in comparison_data[strategy].items():
            st.write(f"**{k}:** {v}")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Challenge mode
# -----------------------------
st.markdown("---")
st.subheader("Challenge Mode")

challenge = st.radio(
    "Which condition should produce the fastest growth in this simulator?",
    [
        "No oxygen + no electron acceptor + low nutrients",
        "Oxygen present + glucose + high nutrients",
        "No oxygen + sulfate + low nutrients",
        "No oxygen + none + medium nutrients"
    ],
    index=None
)

if challenge is not None:
    if challenge == "Oxygen present + glucose + high nutrients":
        st.success("Correct! In this simulator, aerobic respiration with abundant nutrients gives the highest ATP yield and fastest growth.")
    else:
        st.info("Not quite. The best answer is oxygen present + glucose + high nutrients, because aerobic respiration is modeled as the most energy-efficient option here.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    """
    <div class="footer-note">
    Educational note: This simulator is intentionally simplified for learning. Real microbes are far more diverse,
    and many species use specialized pathways, alternative electron donors, and different metabolic strategies depending on their ecology.
    </div>
    """,
    unsafe_allow_html=True
)
