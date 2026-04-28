"""
TSMC ESG Dashboard - Social Page
Director-level deep-dive on workforce, diversity, safety, and human capital.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.styling import apply_global_styling, COLORS, page_header
from utils.data_loader import load_kpi_long, yoy_change

st.set_page_config(
    page_title="Social | TSMC ESG",
    page_icon="◆",
    layout="wide",
)
apply_global_styling()

page_header(
    "Social Performance",
    "Workforce, diversity, safety, and human capital KPIs",
    pillar="S",
)

df_long = load_kpi_long()
soc = df_long[df_long["Pillar"] == "S"].copy()

# ---------------------------------------------------------------------------
# Headline social KPIs
# ---------------------------------------------------------------------------
st.markdown("### Headline Social KPIs (FY2024)")

emp = yoy_change("Total Number of Employees")
women_wf = yoy_change("Women in Total Workforce")
women_sm = yoy_change("Women in Senior Management")
trir = yoy_change("Total Recordable Incident Rate (TRIR)")
turnover = yoy_change("Voluntary Employee Turnover Rate")
training = yoy_change("Average Training Hours per Employee")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Employees",
              f"{emp['current']:,.0f}",
              f"{emp['delta_pct']:+.1f}% YoY")
with c2:
    st.metric("Women in Workforce",
              f"{women_wf['current']:.1f}%",
              f"{women_wf['delta'] :+.1f} pp YoY")
with c3:
    st.metric("Women in Senior Mgmt",
              f"{women_sm['current']:.1f}%",
              f"{women_sm['delta'] :+.1f} pp YoY")

c4, c5, c6 = st.columns(3)
with c4:
    st.metric("Recordable Incident Rate",
              f"{trir['current']:.3f}",
              f"{trir['delta_pct']:+.1f}% YoY",
              delta_color="inverse",
              help="Incidents per 1,000 employees")
with c5:
    st.metric("Voluntary Turnover",
              f"{turnover['current']:.1f}%",
              f"{turnover['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c6:
    st.metric("Training Hours / Employee",
              f"{training['current']:.1f}",
              f"{training['delta_pct']:+.1f}% YoY")

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Workforce", "Diversity & Inclusion", "Safety", "Training & Development"]
)

# ---------------- WORKFORCE ----------------
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Headcount Growth")
        e_df = soc[soc["KPI"] == "Total Number of Employees"]
        fig_e = px.bar(e_df, x="Year", y="Value",
                       text=[f"{int(v):,}" for v in e_df["Value"]],
                       labels={"Value": "Total Employees"})
        fig_e.update_traces(marker_color=COLORS["social_blue"], textposition="outside")
        fig_e.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_e, use_container_width=True)

    with col_b:
        st.markdown("#### Voluntary Turnover Rate")
        t_df = soc[soc["KPI"] == "Voluntary Employee Turnover Rate"]
        fig_t = px.line(t_df, x="Year", y="Value", markers=True,
                        labels={"Value": "Turnover (%)"})
        fig_t.update_traces(line=dict(color=COLORS["social_blue"], width=4),
                             marker=dict(size=12))
        fig_t.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_t, use_container_width=True)

    st.success(
        "**Director note:** Headcount grew 9.6% in 2024 to support fab expansion in Arizona, "
        "Kumamoto, and Dresden. Voluntary turnover fell to 3.4% — best in 5 years and well "
        "below industry benchmarks — signalling strong retention during a competitive talent market."
    )

# ---------------- DIVERSITY ----------------
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Women in Workforce vs Senior Management")
        d_df = soc[soc["KPI"].isin(["Women in Total Workforce", "Women in Senior Management"])].copy()
        d_df["KPI_short"] = d_df["KPI"].str.replace("Women in ", "", regex=False)

        fig_d = px.line(d_df, x="Year", y="Value", color="KPI_short", markers=True,
                        labels={"Value": "Women (%)", "KPI_short": ""},
                        color_discrete_map={
                            "Total Workforce": COLORS["social_blue"],
                            "Senior Management": COLORS["tsmc_red"],
                        })
        fig_d.update_traces(line=dict(width=3), marker=dict(size=10))
        fig_d.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)", rangemode="tozero"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_d, use_container_width=True)

    with col_b:
        st.markdown("#### 2024 Diversity Snapshot")
        women_wf_val = yoy_change("Women in Total Workforce")["current"]
        women_sm_val = yoy_change("Women in Senior Management")["current"]

        fig_pie = go.Figure(go.Bar(
            x=["Workforce", "Senior Mgmt"],
            y=[women_wf_val, women_sm_val],
            marker_color=[COLORS["social_blue"], COLORS["tsmc_red"]],
            text=[f"{v:.1f}%" for v in [women_wf_val, women_sm_val]],
            textposition="outside",
        ))
        fig_pie.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Women (%)", range=[0, 50],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.warning(
        "**Director attention required:** Women in workforce has declined steadily from 37.1% (2020) "
        "to 33.7% (2024). Women in senior management partially recovered to 11.4% in 2024 after "
        "dropping to 5.9% in 2023 — but the 2023 dip is not explained in disclosures and remains "
        "a governance concern under emerging CSRD and SEC human capital rules."
    )

# ---------------- SAFETY ----------------
with tab3:
    st.markdown("#### Total Recordable Incident Rate (TRIR)")
    s_df = soc[soc["KPI"] == "Total Recordable Incident Rate (TRIR)"]

    fig_s = go.Figure()
    fig_s.add_trace(go.Scatter(
        x=s_df["Year"], y=s_df["Value"],
        mode="lines+markers+text",
        text=[f"{v:.3f}" for v in s_df["Value"]],
        textposition="top center",
        line=dict(color=COLORS["social_blue"], width=4),
        marker=dict(size=14, color=COLORS["social_blue"], line=dict(width=2, color="white")),
        fill="tozeroy", fillcolor="rgba(21, 101, 192, 0.15)",
    ))
    fig_s.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(title="TRIR (per 1,000 employees)",
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)", rangemode="tozero"),
        xaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_s, use_container_width=True)

    st.success(
        "**Industry-leading performance:** TRIR fell from 0.311 (2020) to 0.133 (2024) — a 57% "
        "reduction over five years. This is well below semiconductor peer benchmarks and "
        "demonstrates structural improvement in process safety and behavioural training programs."
    )

# ---------------- TRAINING ----------------
with tab4:
    st.markdown("#### Average Training Hours per Employee")
    tr_df = soc[soc["KPI"] == "Average Training Hours per Employee"]

    fig_tr = px.bar(tr_df, x="Year", y="Value",
                    text=[f"{v:.1f}" for v in tr_df["Value"]],
                    labels={"Value": "Hours per Employee"})
    fig_tr.update_traces(marker_color=COLORS["social_blue"], textposition="outside")
    fig_tr.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_tr, use_container_width=True)

    st.info(
        "**Director note:** Training hours have grown from 16.3 hrs (2020) to 100.5 hrs (2024) — "
        "a 6.2x increase reflecting heavy investment in process node R&D upskilling, advanced "
        "packaging training, and overseas fab onboarding."
    )
