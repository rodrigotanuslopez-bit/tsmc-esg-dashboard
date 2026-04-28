"""
TSMC ESG Dashboard - Main Page
Executive overview for board directors covering company profile, materiality
matrix, and the Net-Zero 2050 trajectory.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.styling import apply_global_styling, COLORS, PILLAR_COLORS
from utils.data_loader import (
    load_kpi_long,
    load_net_zero,
    load_materiality,
    get_kpi,
    yoy_change,
    format_value,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TSMC ESG Dashboard | Director View",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styling()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align:center; padding: 0.5rem 0 1rem 0;">
            <h2 style="color: white; margin-bottom: 0;">TSMC</h2>
            <p style="color: #cccccc; font-size: 0.85rem; margin-top: 0.25rem;">
                ESG Director Dashboard
            </p>
        </div>
        <hr style="border-color: rgba(255,255,255,0.2);">
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Navigation")
    st.markdown(
        """
        - **Overview** _(current)_
        - **Environmental**
        - **Social**
        - **Governance**
        - **Financial**
        """
    )
    st.markdown("---")
    st.caption("Reporting period: FY2020 - FY2024")
    st.caption("Source: TSMC Sustainability Report 2024")
    st.caption("Assurance: DNV Business Assurance Co., Ltd.")

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="tsmc-hero">
        <h1 style="margin: 0; font-size: 2.4rem;">
            Taiwan Semiconductor Manufacturing Company
        </h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0; opacity: 0.95;">
            ESG Performance &amp; Net-Zero Strategy | Board Decision Support
        </p>
        <p style="font-size: 0.95rem; margin-top: 0.75rem; opacity: 0.85;">
            World's largest dedicated semiconductor foundry &middot; Hsinchu, Taiwan &middot;
            83,825 employees &middot; FY2024 Revenue $88.3B
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Company profile
# ---------------------------------------------------------------------------
st.markdown("## Company Profile")

profile_col1, profile_col2 = st.columns([2, 1])

with profile_col1:
    st.markdown(
        """
        <div class="panel">
        <p style="font-size: 1.0rem; line-height: 1.6;">
        TSMC is the world's largest contract semiconductor manufacturer, powering AI,
        smartphone, and automotive innovation while pursuing <b>Net-Zero by 2050</b> and
        <b>RE100 by 2040</b>. The 2024 reporting year shows the central tension in the
        ESG narrative: absolute emissions continue to grow as new fabs ramp up in Arizona,
        Kumamoto, and Dresden, while renewable energy adoption hit a record 14.1%.
        </p>
        <p style="font-size: 1.0rem; line-height: 1.6;">
        <b>Reporting frameworks:</b> GRI Universal Standards 2021 (primary disclosure),
        TCFD &amp; TNFD (climate and nature risk), SASB Semiconductor Index, and WEF IBC
        Stakeholder Capitalism Metrics.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with profile_col2:
    st.markdown(
        f"""
        <div class="panel">
        <h4 style="color: {COLORS['tsmc_navy']}; margin-top: 0;">ESG Ratings &amp; Recognition</h4>
        <ul style="line-height: 1.8;">
            <li><b>MSCI ESG:</b> AAA</li>
            <li><b>DJSI World:</b> 25 consecutive years</li>
            <li><b>CDP:</b> B- (Climate &amp; Water)</li>
            <li><b>ISS ESG:</b> Prime</li>
            <li><b>Assurance:</b> DNV (third-party)</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Executive KPI snapshot
# ---------------------------------------------------------------------------
st.markdown("## Executive KPI Snapshot — FY2024")

# Compute headline values
revenue = yoy_change("Annual Revenue")
scope1 = yoy_change("Scope 1 GHG Emissions")
scope2 = yoy_change("Scope 2 GHG Emissions (Market-Based)")
scope3 = yoy_change("Scope 3 GHG Emissions (Total)")
total_ghg_2024 = (scope1["current"] or 0) + (scope2["current"] or 0) + (scope3["current"] or 0)
total_ghg_2023 = (
    get_kpi("Scope 1 GHG Emissions", 2023)
    + get_kpi("Scope 2 GHG Emissions (Market-Based)", 2023)
    + get_kpi("Scope 3 GHG Emissions (Total)", 2023)
)
total_ghg_delta = total_ghg_2024 - total_ghg_2023
total_ghg_delta_pct = (total_ghg_delta / total_ghg_2023) * 100

renewable = yoy_change("Renewable Energy Percentage")
trir = yoy_change("Total Recordable Incident Rate (TRIR)")
turnover = yoy_change("Voluntary Employee Turnover Rate")
women_board = yoy_change("Women on Board")

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        "Annual Revenue",
        f"${revenue['current']/1000:.2f}B",
        f"{revenue['delta_pct']:+.1f}% YoY",
    )
with k2:
    st.metric(
        "Total GHG (Scope 1+2+3)",
        f"{total_ghg_2024/1_000_000:.1f}M tCO2e",
        f"{total_ghg_delta_pct:+.1f}% YoY",
        delta_color="inverse",
    )
with k3:
    st.metric(
        "Renewable Energy",
        f"{renewable['current']:.1f}%",
        f"{renewable['delta_pct']:+.1f}% YoY",
    )
with k4:
    st.metric(
        "Safety (TRIR)",
        f"{trir['current']:.3f}",
        f"{trir['delta_pct']:+.1f}% YoY",
        delta_color="inverse",
    )

k5, k6, k7, k8 = st.columns(4)
with k5:
    st.metric(
        "Voluntary Turnover",
        f"{turnover['current']:.1f}%",
        f"{turnover['delta_pct']:+.1f}% YoY",
        delta_color="inverse",
    )
with k6:
    st.metric(
        "Women on Board",
        f"{women_board['current']:.0f}%",
        f"{women_board['delta']:+.0f} pp YoY",
    )
with k7:
    employees = yoy_change("Total Number of Employees")
    st.metric(
        "Total Employees",
        f"{employees['current']:,.0f}",
        f"{employees['delta_pct']:+.1f}% YoY",
    )
with k8:
    rd = yoy_change("R&D Expenditure")
    st.metric(
        "R&D Spend",
        f"${rd['current']/1000:.2f}B",
        f"{rd['delta_pct']:+.1f}% YoY",
    )

# ---------------------------------------------------------------------------
# Double Materiality Matrix
# ---------------------------------------------------------------------------
st.markdown("## Double Materiality Matrix")
st.markdown(
    """
    Aligned with **ESRS** and **GRI** double-materiality requirements via TSMC's
    *Dynamic and Double Materiality (TDDM) Protocol*.
    The horizontal axis captures **Impact on Operations** (financial materiality);
    the vertical axis captures **Impact on Sustainability** (impact materiality).
    Bubble size reflects **stakeholder concern**.
    """
)

mat_df = load_materiality()
pillar_full = {"E": "Environmental", "S": "Social", "G": "Governance"}
mat_df["PillarName"] = mat_df["Pillar"].map(pillar_full)

fig_mat = px.scatter(
    mat_df,
    x="Impact_Operations",
    y="Impact_Sustainability",
    size="Stakeholder_Concern",
    color="PillarName",
    text="Topic",
    size_max=55,
    color_discrete_map={
        "Environmental": COLORS["env_green"],
        "Social": COLORS["social_blue"],
        "Governance": COLORS["gov_gold"],
    },
    hover_data={
        "Topic": True,
        "PillarName": True,
        "Impact_Operations": ":.1f",
        "Impact_Sustainability": ":.1f",
        "Stakeholder_Concern": ":.1f",
    },
)

fig_mat.update_traces(
    textposition="top center",
    textfont=dict(size=10, color=COLORS["tsmc_charcoal"]),
    marker=dict(line=dict(width=1.5, color="white"), opacity=0.85),
)

fig_mat.update_layout(
    height=600,
    xaxis=dict(
        title="<b>Impact on Operations</b> (financial materiality)",
        range=[0, 10],
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
        zeroline=False,
    ),
    yaxis=dict(
        title="<b>Impact on Sustainability</b> (impact materiality)",
        range=[0, 10],
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
        zeroline=False,
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(
        title="ESG Pillar",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
    margin=dict(l=20, r=20, t=20, b=20),
)

# Add quadrant lines and labels
fig_mat.add_hline(y=5, line_dash="dash", line_color="rgba(0,0,0,0.25)", line_width=1)
fig_mat.add_vline(x=5, line_dash="dash", line_color="rgba(0,0,0,0.25)", line_width=1)
fig_mat.add_annotation(
    x=7.5, y=9.5,
    text="<b>Quadrant I — Highest Priority</b>",
    showarrow=False,
    font=dict(size=11, color=COLORS["tsmc_red"]),
    bgcolor="rgba(255,255,255,0.7)",
)

st.plotly_chart(fig_mat, use_container_width=True)

# Quadrant I summary
q1 = mat_df[(mat_df["Impact_Operations"] >= 5) & (mat_df["Impact_Sustainability"] >= 5)]
q1 = q1.sort_values("Stakeholder_Concern", ascending=False)
st.markdown(
    f"""
    <div class="panel">
    <h4 style="color: {COLORS['tsmc_red']}; margin-top: 0;">Quadrant I — Director Action Items</h4>
    <p>The {len(q1)} topics in Quadrant I represent the highest-priority drivers of
    sustainability, with elevated impact on both operations and external sustainability
    outcomes. These should anchor board ESG agendas and capital allocation decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.dataframe(
    q1[["Topic", "PillarName", "Impact_Operations", "Impact_Sustainability", "Stakeholder_Concern"]]
    .rename(columns={"PillarName": "Pillar"})
    .reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------------------------
# Net-Zero Trajectory
# ---------------------------------------------------------------------------
st.markdown("## Net-Zero 2050 Trajectory")
st.markdown(
    """
    TSMC's committed pathway to **Net-Zero emissions by 2050**, with the interim
    2030 target of returning to 2020 emission levels. The chart overlays historical
    Scope 1+2 emissions against the forward commitment line.
    """
)

# Build combined trajectory data
nz = load_net_zero()
hist_years = [2020, 2021, 2022, 2023, 2024]
hist_emissions = [
    get_kpi("Scope 1 GHG Emissions", y) + get_kpi("Scope 2 GHG Emissions (Market-Based)", y)
    for y in hist_years
]

fig_nz = go.Figure()

# Historical actuals
fig_nz.add_trace(
    go.Scatter(
        x=hist_years,
        y=hist_emissions,
        mode="lines+markers",
        name="Historical Scope 1+2 (actual)",
        line=dict(color=COLORS["tsmc_red"], width=4),
        marker=dict(size=10, line=dict(width=2, color="white")),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} tCO2e<extra></extra>",
    )
)

# Net-Zero commitment line (2025-2050)
fig_nz.add_trace(
    go.Scatter(
        x=nz["Year"],
        y=nz["Net_Zero_Commitment_tCO2e"],
        mode="lines",
        name="Net-Zero commitment pathway",
        line=dict(color=COLORS["env_green"], width=3, dash="dash"),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} tCO2e<extra></extra>",
    )
)

# Connect 2024 actual to 2025 commitment
fig_nz.add_trace(
    go.Scatter(
        x=[2024, 2025],
        y=[hist_emissions[-1], nz["Net_Zero_Commitment_tCO2e"].iloc[0]],
        mode="lines",
        line=dict(color=COLORS["tsmc_charcoal"], width=2, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    )
)

# 2030 milestone marker
val_2030 = nz[nz["Year"] == 2030]["Net_Zero_Commitment_tCO2e"].iloc[0]
fig_nz.add_trace(
    go.Scatter(
        x=[2030],
        y=[val_2030],
        mode="markers+text",
        marker=dict(size=18, color=COLORS["gov_gold"], symbol="star",
                    line=dict(width=2, color="white")),
        text=["2030 milestone"],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["gov_gold"]),
        showlegend=False,
        hovertemplate="<b>2030 Target</b><br>%{y:,.0f} tCO2e<extra></extra>",
    )
)

# 2050 net-zero marker
val_2050 = nz[nz["Year"] == 2050]["Net_Zero_Commitment_tCO2e"].iloc[0]
fig_nz.add_trace(
    go.Scatter(
        x=[2050],
        y=[val_2050],
        mode="markers+text",
        marker=dict(size=18, color=COLORS["env_green"], symbol="star",
                    line=dict(width=2, color="white")),
        text=["Net-Zero 2050"],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["env_green"]),
        showlegend=False,
        hovertemplate="<b>Net-Zero 2050</b><br>%{y:,.0f} tCO2e<extra></extra>",
    )
)

fig_nz.update_layout(
    height=520,
    xaxis=dict(
        title="<b>Year</b>",
        tickmode="linear",
        dtick=5,
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
    ),
    yaxis=dict(
        title="<b>Scope 1+2 Emissions (tCO2e)</b>",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
        rangemode="tozero",
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=40, b=20),
)

st.plotly_chart(fig_nz, use_container_width=True)

# Net-zero milestones panels
nz_col1, nz_col2, nz_col3, nz_col4 = st.columns(4)
with nz_col1:
    st.metric("2024 Scope 1+2", f"{hist_emissions[-1]/1_000_000:.2f}M tCO2e")
with nz_col2:
    delta_to_2025 = (
        (nz["Net_Zero_Commitment_tCO2e"].iloc[0] - hist_emissions[-1]) / hist_emissions[-1] * 100
    )
    st.metric("2025 Commitment", f"{nz['Net_Zero_Commitment_tCO2e'].iloc[0]/1_000_000:.2f}M tCO2e",
              f"{delta_to_2025:+.1f}% vs 2024", delta_color="inverse")
with nz_col3:
    delta_to_2030 = ((val_2030 - hist_emissions[-1]) / hist_emissions[-1]) * 100
    st.metric("2030 Milestone", f"{val_2030/1_000_000:.2f}M tCO2e",
              f"{delta_to_2030:+.1f}% vs 2024", delta_color="inverse")
with nz_col4:
    st.metric("2050 Net-Zero", f"{val_2050/1_000_000:.2f}M tCO2e",
              "Final commitment", delta_color="off")

# ---------------------------------------------------------------------------
# Director's strategic narrative
# ---------------------------------------------------------------------------
st.markdown("## Strategic Context for Directors")

narrative_cols = st.columns(3)
with narrative_cols[0]:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['env_green']};">
            <h4 style="color: {COLORS['env_green']}; margin-top: 0;">Where TSMC Leads</h4>
            <ul style="line-height: 1.7;">
                <li>Worker safety: TRIR 0.133 (best in 5 years)</li>
                <li>F-GHG abatement: 96% reduction rate</li>
                <li>Supplier ESG audits: 100% completion</li>
                <li>Training intensity: 100.5 hrs/employee</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with narrative_cols[1]:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['warning']};">
            <h4 style="color: {COLORS['warning']}; margin-top: 0;">Where TSMC Lags</h4>
            <ul style="line-height: 1.7;">
                <li>Absolute Scope 1+2 emissions up 8% YoY</li>
                <li>Unit GHG intensity missed target by 19%</li>
                <li>Renewable energy at 14.1% vs RE60 by 2030</li>
                <li>Women in workforce trending down (33.7%)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with narrative_cols[2]:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['tsmc_red']};">
            <h4 style="color: {COLORS['tsmc_red']}; margin-top: 0;">Board-Level Decisions</h4>
            <ul style="line-height: 1.7;">
                <li>Mandate 30% renewables for new fabs</li>
                <li>Accelerate Taiwan offshore wind PPAs</li>
                <li>Disclose fab-level GHG and water data</li>
                <li>Quantify climate physical risk in capex</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "Use the sidebar to drill into Environmental, Social, Governance, and Financial detail pages. "
    "Each section provides multi-year trends, target progress, and director-level commentary."
)
