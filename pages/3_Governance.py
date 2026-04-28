"""
TSMC ESG Dashboard - Governance Page
Director-level deep-dive on board composition, ethics, and ESG ratings.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.styling import apply_global_styling, COLORS, page_header
from utils.data_loader import load_kpi_long, yoy_change

st.set_page_config(
    page_title="Governance | TSMC ESG",
    page_icon="◆",
    layout="wide",
)
apply_global_styling()

page_header(
    "Governance Performance",
    "Board composition, ethics, and ESG oversight structures",
    pillar="G",
)

df_long = load_kpi_long()
gov = df_long[df_long["Pillar"] == "G"].copy()

# ---------------------------------------------------------------------------
# Headline governance KPIs
# ---------------------------------------------------------------------------
st.markdown("### Headline Governance KPIs (FY2024)")

board_size = yoy_change("Total Board Size")
board_indep = yoy_change("Board Independence")
women_board = yoy_change("Women on Board")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Board Size", f"{board_size['current']:.0f}",
              "Stable", delta_color="off")
with c2:
    st.metric("Board Independence",
              f"{board_indep['current']:.0f}%",
              f"{board_indep['delta']:+.0f} pp YoY")
with c3:
    st.metric("Women on Board",
              f"{women_board['current']:.0f}%",
              f"{women_board['delta']:+.0f} pp YoY")
with c4:
    st.metric("ESG-Linked Exec Pay", "Yes",
              "Maintained", delta_color="off")

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Board Composition", "Ethics & Oversight", "ESG Ratings"])

# ---------------- BOARD ----------------
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Board Independence Trend")
        b_df = gov[gov["KPI"] == "Board Independence"]
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(
            x=b_df["Year"], y=b_df["Value"],
            mode="lines+markers+text",
            text=[f"{v:.0f}%" for v in b_df["Value"]],
            textposition="top center",
            line=dict(color=COLORS["gov_gold"], width=4),
            marker=dict(size=14, line=dict(width=2, color="white")),
            fill="tozeroy", fillcolor="rgba(184, 134, 11, 0.15)",
        ))
        fig_b.add_hline(y=50, line_dash="dot", line_color=COLORS["tsmc_charcoal"],
                        annotation_text="Majority threshold (50%)",
                        annotation_position="bottom right")
        fig_b.update_layout(
            height=400, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Independence (%)", range=[0, 100],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_b, use_container_width=True)

    with col_b:
        st.markdown("#### Women on Board")
        w_df = gov[gov["KPI"] == "Women on Board"]
        fig_w = go.Figure()
        fig_w.add_trace(go.Bar(
            x=w_df["Year"], y=w_df["Value"],
            text=[f"{v:.0f}%" for v in w_df["Value"]],
            textposition="outside",
            marker_color=[
                COLORS["gov_gold"] if y < 2024 else COLORS["tsmc_red"]
                for y in w_df["Year"]
            ],
        ))
        fig_w.update_layout(
            height=400, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Women on Board (%)", range=[0, 30],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_w, use_container_width=True)

    st.success(
        "**Governance progress:** 2024 marked a step-change in board diversity — independence rose "
        "from 60% to 70% and women on board doubled from 10% to 20%. These changes align TSMC with "
        "leading global governance benchmarks and emerging Taiwan corporate-governance disclosure rules."
    )

# ---------------- ETHICS ----------------
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Governance & Oversight Structure")
        st.markdown(
            f"""
            <div class="panel">
            <table style="width: 100%; line-height: 1.9;">
                <tr><td><b>ESG Steering Committee</b></td><td>Chaired at C.C. Wei (Chairman level)</td></tr>
                <tr><td><b>ESG Committee</b></td><td>Operational oversight</td></tr>
                <tr><td><b>Audit Committee</b></td><td>100% independent directors</td></tr>
                <tr><td><b>Compensation Committee</b></td><td>ESG-linked exec pay</td></tr>
                <tr><td><b>Risk Management Committee</b></td><td>Climate &amp; cyber risk</td></tr>
                <tr><td><b>Third-Party Assurance</b></td><td>DNV Business Assurance</td></tr>
            </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown("#### Supplier Governance")
        st.markdown(
            f"""
            <div class="panel">
            <h5 style="color: {COLORS['gov_gold']}; margin-top: 0;">Supplier ESG Performance</h5>
            <p>100% of <b>Tier 1 suppliers</b> completed sustainability self-assessment questionnaires (SAQ).</p>
            <p>100% of <b>significant suppliers</b> received Responsible Business Alliance (RBA) audits.</p>
            <p>90% of high-energy suppliers verified for Scope 3 reporting.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "**Director note:** TSMC's three-tier ESG governance — Board → Steering Committee → "
        "Operating Committee — is widely viewed as best-in-class in semiconductor industry. "
        "Executive compensation is explicitly linked to ESG performance targets, satisfying "
        "TCFD governance disclosures and emerging EU CSRD requirements."
    )

# ---------------- ESG RATINGS ----------------
with tab3:
    st.markdown("#### External ESG Ratings & Recognition")

    ratings = [
        {"Rater": "MSCI ESG", "Score": "AAA", "Note": "Top tier (highest)"},
        {"Rater": "DJSI World Index", "Score": "Included", "Note": "25 consecutive years"},
        {"Rater": "CDP Climate", "Score": "B-", "Note": "Management level"},
        {"Rater": "CDP Water", "Score": "B-", "Note": "Management level"},
        {"Rater": "ISS ESG Corporate Rating", "Score": "Prime", "Note": "Above industry threshold"},
        {"Rater": "FTSE4Good Index", "Score": "Included", "Note": "Constituent"},
        {"Rater": "Sustainalytics", "Score": "Low Risk", "Note": "ESG Risk Rating"},
        {"Rater": "DNV Assurance", "Score": "Reasonable Assurance", "Note": "E/S data third-party verified"},
    ]
    import pandas as pd
    rdf = pd.DataFrame(ratings)
    st.dataframe(rdf, use_container_width=True, hide_index=True)

    st.markdown("#### Rating Summary Visualisation")
    rating_score_map = {
        "MSCI ESG (AAA = 7)": 7,
        "ISS ESG Prime": 6,
        "Sustainalytics Low Risk": 6,
        "DJSI World": 6,
        "CDP Climate (B-)": 4,
        "CDP Water (B-)": 4,
    }
    fig_r = go.Figure()
    fig_r.add_trace(go.Bar(
        x=list(rating_score_map.keys()),
        y=list(rating_score_map.values()),
        marker_color=[
            COLORS["env_green"] if v >= 6 else COLORS["gov_gold"] if v >= 4 else COLORS["tsmc_red"]
            for v in rating_score_map.values()
        ],
        text=list(rating_score_map.values()),
        textposition="outside",
    ))
    fig_r.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(title="Indicative Tier (higher = stronger)", range=[0, 8],
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        xaxis=dict(showgrid=False, tickangle=-15),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_r, use_container_width=True)

    st.warning(
        "**Improvement opportunity:** While MSCI rates TSMC AAA, CDP Climate and Water "
        "scores remain at B- (Management level). Reaching A- (Leadership) requires deeper "
        "Scope 3 supplier engagement disclosure and forward-looking scenario analysis."
    )
