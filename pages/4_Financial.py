"""
TSMC ESG Dashboard - Financial Page
Director-level financial performance and ESG-linked capital allocation.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.styling import apply_global_styling, COLORS, page_header
from utils.data_loader import load_kpi_long, yoy_change, get_kpi

st.set_page_config(
    page_title="Financial | TSMC ESG",
    page_icon="◆",
    layout="wide",
)
apply_global_styling()

page_header(
    "Financial Performance",
    "Revenue, profitability, and capital allocation in the context of ESG strategy",
    pillar="F",
)

df_long = load_kpi_long()
fin = df_long[df_long["Pillar"] == "Financial"].copy()

# ---------------------------------------------------------------------------
# Headline financial KPIs
# ---------------------------------------------------------------------------
st.markdown("### Headline Financial KPIs (FY2024)")

revenue = yoy_change("Annual Revenue")
ebitda = yoy_change("EBITDA Margin")
capex = yoy_change("Capital Expenditure")
rd = yoy_change("R&D Expenditure")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Annual Revenue",
              f"${revenue['current']/1000:.2f}B",
              f"{revenue['delta_pct']:+.1f}% YoY")
with c2:
    st.metric("EBITDA Margin",
              f"{ebitda['current']:.0f}%",
              f"{ebitda['delta'] :+.0f} pp YoY")
with c3:
    st.metric("Capital Expenditure",
              f"${capex['current']/1000:.2f}B",
              f"{capex['delta_pct']:+.1f}% YoY")
with c4:
    st.metric("R&D Spend",
              f"${rd['current']/1000:.2f}B",
              f"{rd['delta_pct']:+.1f}% YoY")

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Revenue & Profitability", "Capital Allocation", "ESG ↔ Financial Linkage"])

# ---------------- REVENUE ----------------
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Annual Revenue ($M)")
        rev_df = fin[fin["KPI"] == "Annual Revenue"]
        fig_rev = px.bar(rev_df, x="Year", y="Value",
                         text=[f"${int(v):,}M" for v in rev_df["Value"]],
                         labels={"Value": "Revenue ($M)"})
        fig_rev.update_traces(marker_color=COLORS["fin_teal"], textposition="outside")
        fig_rev.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_b:
        st.markdown("#### EBITDA Margin (%)")
        eb_df = fin[fin["KPI"] == "EBITDA Margin"]
        fig_eb = go.Figure()
        fig_eb.add_trace(go.Scatter(
            x=eb_df["Year"], y=eb_df["Value"],
            mode="lines+markers+text",
            text=[f"{v:.0f}%" for v in eb_df["Value"]],
            textposition="top center",
            line=dict(color=COLORS["fin_teal"], width=4),
            marker=dict(size=14, line=dict(width=2, color="white")),
            fill="tozeroy", fillcolor="rgba(0, 105, 92, 0.15)",
        ))
        fig_eb.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="EBITDA Margin (%)", range=[0, 80],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_eb, use_container_width=True)

    st.success(
        "**Director note:** FY2024 revenue rose 27.4% to $88.3B, driven by AI accelerator demand "
        "(N3, N5 nodes). EBITDA margin recovered to 69%, matching the 2022 peak. Strong "
        "profitability provides the cash flow runway needed to fund decarbonisation capex."
    )

# ---------------- CAPITAL ALLOCATION ----------------
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Capital Expenditure vs R&D Spend")
        ca_df = fin[fin["KPI"].isin(["Capital Expenditure", "R&D Expenditure"])].copy()
        ca_df["KPI_short"] = ca_df["KPI"].str.replace(" Expenditure", "", regex=False)

        fig_ca = px.bar(
            ca_df, x="Year", y="Value", color="KPI_short", barmode="group",
            labels={"Value": "Spend ($M)", "KPI_short": "Type"},
            color_discrete_map={
                "Capital": COLORS["fin_teal"],
                "R&D": COLORS["tsmc_red"],
            }
        )
        fig_ca.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_ca, use_container_width=True)

    with col_b:
        st.markdown("#### CapEx as % of Revenue")
        capex_pct = []
        years = [2020, 2021, 2022, 2023, 2024]
        for y in years:
            cx = get_kpi("Capital Expenditure", y)
            rv = get_kpi("Annual Revenue", y)
            capex_pct.append((cx / rv) * 100)

        fig_pct = go.Figure()
        fig_pct.add_trace(go.Scatter(
            x=years, y=capex_pct,
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in capex_pct],
            textposition="top center",
            line=dict(color=COLORS["fin_teal"], width=4),
            marker=dict(size=12),
        ))
        fig_pct.update_layout(
            height=420, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="CapEx / Revenue (%)", range=[0, 60],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_pct, use_container_width=True)

    st.info(
        "**Director note:** CapEx fell from 47.9% of revenue in 2022 to 33.7% in 2024 as the "
        "post-pandemic build cycle moderated. R&D spend continues to climb (+6.6% YoY to $6.2B), "
        "underwriting next-generation node leadership (N2, A16)."
    )

# ---------------- ESG-FINANCIAL LINKAGE ----------------
with tab3:
    st.markdown("#### Revenue per tCO2e (Carbon Productivity)")
    years = [2020, 2021, 2022, 2023, 2024]
    intensity_inv = []
    for y in years:
        s1 = get_kpi("Scope 1 GHG Emissions", y)
        s2 = get_kpi("Scope 2 GHG Emissions (Market-Based)", y)
        rev = get_kpi("Annual Revenue", y)
        intensity_inv.append((rev * 1_000_000) / (s1 + s2))  # $ per tCO2e

    fig_ci = go.Figure()
    fig_ci.add_trace(go.Bar(
        x=years, y=intensity_inv,
        text=[f"${v:,.0f}" for v in intensity_inv],
        textposition="outside",
        marker_color=COLORS["env_green"],
    ))
    fig_ci.update_layout(
        height=400, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(title="Revenue ($) per tCO2e (Scope 1+2)",
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        xaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_ci, use_container_width=True)

    st.markdown("#### Revenue Growth vs Total GHG Growth (Indexed to 2020 = 100)")
    rev_idx, ghg_idx = [], []
    rev_2020 = get_kpi("Annual Revenue", 2020)
    ghg_2020 = (get_kpi("Scope 1 GHG Emissions", 2020)
                + get_kpi("Scope 2 GHG Emissions (Market-Based)", 2020)
                + get_kpi("Scope 3 GHG Emissions (Total)", 2020))
    for y in years:
        rev_y = get_kpi("Annual Revenue", y)
        ghg_y = (get_kpi("Scope 1 GHG Emissions", y)
                 + get_kpi("Scope 2 GHG Emissions (Market-Based)", y)
                 + get_kpi("Scope 3 GHG Emissions (Total)", y))
        rev_idx.append((rev_y / rev_2020) * 100)
        ghg_idx.append((ghg_y / ghg_2020) * 100)

    fig_dec = go.Figure()
    fig_dec.add_trace(go.Scatter(
        x=years, y=rev_idx, mode="lines+markers", name="Revenue (indexed)",
        line=dict(color=COLORS["fin_teal"], width=4), marker=dict(size=10),
    ))
    fig_dec.add_trace(go.Scatter(
        x=years, y=ghg_idx, mode="lines+markers", name="Total GHG (indexed)",
        line=dict(color=COLORS["tsmc_red"], width=4), marker=dict(size=10),
    ))
    fig_dec.update_layout(
        height=400, plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(title="Index (2020 = 100)",
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_dec, use_container_width=True)

    rev_growth = rev_idx[-1] - 100
    ghg_growth = ghg_idx[-1] - 100
    st.warning(
        f"**Decoupling status:** Revenue has grown {rev_growth:.0f}% since 2020 while total GHG "
        f"emissions grew {ghg_growth:.0f}%. Carbon productivity (revenue per tCO2e) is "
        f"improving, but absolute decoupling has not yet been achieved — a key director-level "
        f"concern for the 2030 milestone."
    )
