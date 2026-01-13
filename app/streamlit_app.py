import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------- Page config ----------
st.set_page_config(
    page_title="FoodSense",
    layout="wide",
    page_icon="🥗",
)

# ---------- Paths & data ----------
DATA_FILE = r"data\foodsense_meals_symptoms.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(
        columns=["date", "food", "portion", "meal_time", "sleep_quality", "symptom"]
    )

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

# ---------- CSS ----------
st.markdown(
    """
<style>
    .main {
        max-width: 1300px;
        margin: 0 auto;
        padding-top: 0.25rem;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }

    /* Header */
    .fs-header {
        padding: 1rem 1.5rem;
        border-radius: 14px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.35);
        text-align: center;
    }
    .fs-header-inner {
        max-width: 480px;
        margin: 0 auto;
    }
    .fs-header-title {
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
    }
    .fs-header-subtitle {
        font-size: 0.9rem;
        opacity: 0.95;
        margin: 0;
    }

    /* Cards */
    .fs-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 0.9rem 1rem 0.8rem 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 6px rgba(15, 23, 42, 0.06);
        margin-bottom: 0.75rem;
    }
    .fs-card-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Insight cards */
    .fs-insight-card {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border-radius: 10px;
        padding: 0.8rem 0.9rem;
        border-left: 4px solid #667eea;
        margin: 0.4rem 0 0.6rem 0;
    }
    .fs-insight-label {
        font-size: 0.75rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.1rem;
    }
    .fs-insight-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4338ca;
        margin: 0.1rem 0 0 0;
    }

    /* Empty state */
    .fs-empty {
        text-align: center;
        color: #6b7280;
        padding: 1.5rem 0 1.2rem 0;
    }

    /* Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border-radius: 8px;
        border: none;
        padding: 0.55rem 1rem;
        font-size: 0.95rem;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(79, 70, 229, 0.35);
        transition: all 0.15s ease-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(79, 70, 229, 0.45);
    }

    /* Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px !important;
        border: 1.5px solid #e5e7eb !important;
        padding: 0.45rem 0.6rem !important;
        font-size: 0.9rem !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
<div class="fs-header">
  <div class="fs-header-inner">
    <p class="fs-header-title">. </p>
    <p class="fs-header-subtitle">
        🥗 FoodSense - Log your meals and track how  you feel.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Layout: inputs (left) | insights (right) ----------
left, right = st.columns([1.1, 1])

with left:
    # --- Food details ---
    st.markdown('<div class="fs-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="fs-card-title">🍽️ Food details</div>',
        unsafe_allow_html=True,
    )

    food = st.text_input(
        "What did you eat?",
        placeholder="e.g. Grilled chicken sandwich with cheese",
    )

    col_portion, col_time = st.columns(2)
    with col_portion:
        portion = st.selectbox("Portion size", ["Small", "Medium", "Large"])
    with col_time:
        meal_time = st.selectbox("Meal time", ["Morning", "Afternoon", "Evening"])

    st.caption("Tip: Be specific. Chips + dip behaves differently from baked potatoes.")

    st.markdown("</div>", unsafe_allow_html=True)

    # --- How you feel + button (same card to save height) ---
    st.markdown('<div class="fs-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="fs-card-title">💤 How are you feeling?</div>',
        unsafe_allow_html=True,
    )

    sleep = st.slider("Sleep quality last night", 1, 5, 3)
    col_energy, col_symptom = st.columns([1, 1.4])

    with col_energy:
        energy = st.radio(
            "Energy after this meal",
            ["Low", "OK", "High"],
            index=1,
            horizontal=True,
        )

    with col_symptom:
        symptom = st.selectbox(
            "Symptoms after the meal?",
            ["No", "Bloating", "Gas", "Nausea", "Loose motion"],
        )

    st.caption(
        "You only need a few days of consistent logging for useful patterns to appear."
    )

    # Map numeric sleep to label for storage
    sleep_map = {1: "Very poor", 2: "Poor", 3: "OK", 4: "Good", 5: "Great"}
    sleep_label = sleep_map.get(sleep, "OK")

    # Button inside same card
    log_clicked = st.button("Log meal", type="primary", use_container_width=True)

    if log_clicked:
        if not food or not food.strip():
            st.error("Food name is required to log a meal.")
        else:
            new_row = {
                "date": date.today(),
                "food": food.lower().strip(),
                "portion": portion,
                "meal_time": meal_time,
                "sleep_quality": sleep_label,
                "symptom": symptom,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Meal logged. Updating your insights…")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="fs-card">', unsafe_allow_html=True)

    have_food = bool(food and food.strip())
    normalized_food = food.lower().strip() if have_food else ""

    if have_food and normalized_food in df["food"].values:
        st.markdown(
            '<div class="fs-card-title">💡 Your insights</div>',
            unsafe_allow_html=True,
        )

        df_food = df[df["food"] == normalized_food].copy()
        df_food["symptom_flag"] = df_food["symptom"].apply(lambda x: 0 if x == "No" else 1)

        total = len(df_food)
        symptom_rate = round(df_food["symptom_flag"].mean() * 100, 1)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f"""
                <div class="fs-insight-card">
                    <div class="fs-insight-label">Times eaten</div>
                    <p class="fs-insight-value">{total}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_b:
            st.markdown(
                f"""
                <div class="fs-insight-card">
                    <div class="fs-insight-label">Symptom rate</div>
                    <p class="fs-insight-value">{symptom_rate}%</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Portion insight
        portion_stats = (
            df_food.groupby("portion")["symptom_flag"]
            .mean()
            .reset_index()
        )

        if len(portion_stats) > 1:
            best = portion_stats.sort_values("symptom_flag").iloc[0]
            worst = portion_stats.sort_values("symptom_flag").iloc[-1]

            if worst["symptom_flag"] - best["symptom_flag"] >= 0.3:
                st.warning(
                    f"⚠️ More symptoms with **{worst['portion']}** portions.\n\n"
                    f"💡 Try **{best['portion']}** portions instead."
                )
            else:
                st.info(
                    "ℹ️ Portion size does not seem to change symptoms much.\n\n"
                    "Patterns are more likely tied to the food itself."
                )
        else:
            st.info(
                "ℹ️ Log a few more meals with different portion sizes "
                "to unlock portion insights."
            )

    else:
        st.markdown(
            '<div class="fs-card-title">💡 Insights</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="fs-empty">
                <div style="font-size: 1.6rem; margin-bottom: 0.2rem;">📊</div>
                <p style="margin: 0.2rem 0 0.15rem 0;">
                    Type a food above and log a meal to see your history and patterns.
                </p>
                <p style="font-size: 0.8rem; margin: 0.1rem 0 0 0; color: #9ca3af;">
                    Insights get smarter as you build your personal food journal.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    """
<div style="text-align:center; padding: 0.5rem 0 0.25rem 0; color:#6b7280; font-size:0.8rem;">
    🌱 MVP: Insights will get more accurate as you log more meals over time.
</div>
""",
    unsafe_allow_html=True,
)
