"""
TSMC ESG Dashboard - Environmental Page
Director-level deep-dive on climate, energy, water, and waste KPIs.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.styling import apply_global_styling, COLORS, page_header
from utils.data_loader import (
    load_kpi_long,
    load_net_zero,
    get_kpi,
    yoy_change,
    YEARS,
)

st.set_page_config(
    page_title="Environmental | TSMC ESG",
    page_icon="◆",
    layout="wide",
)
apply_global_styling()

page_header(
    "Environmental Performance",
    "Climate, energy, water, and circular-economy KPIs aligned with SASB & TCFD",
    pillar="E",
)

df_long = load_kpi_long()
env = df_long[df_long["Pillar"] == "E"].copy()

# ---------------------------------------------------------------------------
# Headline environmental KPIs
# ---------------------------------------------------------------------------
st.markdown("### Headline Environmental KPIs (FY2024)")

s1 = yoy_change("Scope 1 GHG Emissions")
s2 = yoy_change("Scope 2 GHG Emissions (Market-Based)")
s3 = yoy_change("Scope 3 GHG Emissions (Total)")
ren = yoy_change("Renewable Energy Percentage")
energy = yoy_change("Total Energy Consumption")
water = yoy_change("Total Water Withdrawal")
waste = yoy_change("Total Waste Generated")
intensity = yoy_change("Carbon Intensity (per $M Revenue)")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Scope 1 Emissions",
              f"{s1['current']/1_000_000:.2f}M tCO2e",
              f"{s1['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c2:
    st.metric("Scope 2 (Market-Based)",
              f"{s2['current']/1_000_000:.2f}M tCO2e",
              f"{s2['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c3:
    st.metric("Scope 3 Emissions",
              f"{s3['current']/1_000_000:.2f}M tCO2e",
              f"{s3['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c4:
    st.metric("Carbon Intensity",
              f"{intensity['current']:.1f}",
              f"{intensity['delta_pct']:+.1f}% YoY",
              delta_color="inverse",
              help="tCO2e per $M revenue")

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.metric("Renewable Energy",
              f"{ren['current']:.1f}%",
              f"{ren['delta'] :+.1f} pp YoY")
with c6:
    st.metric("Total Energy",
              f"{energy['current']:,.0f} GWh",
              f"{energy['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c7:
    st.metric("Water Withdrawal",
              f"{water['current']:.1f}M MT",
              f"{water['delta_pct']:+.1f}% YoY",
              delta_color="inverse")
with c8:
    st.metric("Total Waste",
              f"{waste['current']/1000:.0f}K MT",
              f"{waste['delta_pct']:+.1f}% YoY",
              delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs by environmental subdomain
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Carbon & Climate", "Energy", "Water", "Waste", "Net-Zero Trajectory"]
)

# ---------------- CARBON ----------------
with tab1:
    st.markdown("#### Greenhouse Gas Emissions by Scope")

    scopes = ["Scope 1 GHG Emissions",
              "Scope 2 GHG Emissions (Market-Based)",
              "Scope 3 GHG Emissions (Total)"]
    scope_df = env[env["KPI"].isin(scopes)].copy()
    scope_df["KPI_short"] = scope_df["KPI"].str.replace(" GHG Emissions", "", regex=False) \
                                            .str.replace(" (Market-Based)", "", regex=False) \
                                            .str.replace(" (Total)", "", regex=False)

    fig = px.bar(
        scope_df,
        x="Year",
        y="Value",
        color="KPI_short",
        barmode="stack",
        color_discrete_map={
            "Scope 1": COLORS["tsmc_red"],
            "Scope 2": COLORS["env_green"],
            "Scope 3": COLORS["social_blue"],
        },
        labels={"Value": "Emissions (tCO2e)", "KPI_short": "Scope"},
    )
    fig.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Carbon Intensity Trend")
        ci = env[env["KPI"] == "Carbon Intensity (per $M Revenue)"]
        fig_ci = px.line(ci, x="Year", y="Value", markers=True,
                         labels={"Value": "tCO2e per $M revenue"})
        fig_ci.update_traces(line=dict(color=COLORS["env_green"], width=4),
                              marker=dict(size=10))
        fig_ci.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                             xaxis=dict(showgrid=False),
                             yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
                             margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_ci, use_container_width=True)

    with col_b:
        st.markdown("#### Scope 2 Market vs Location Based")
        s2_df = env[env["KPI"].str.startswith("Scope 2")]
        s2_df = s2_df.assign(KPI_short=s2_df["KPI"].str.replace("Scope 2 GHG Emissions ", "", regex=False))
        fig_s2 = px.line(s2_df, x="Year", y="Value", color="KPI_short", markers=True,
                         labels={"Value": "Emissions (tCO2e)", "KPI_short": "Method"},
                         color_discrete_map={
                             "(Market-Based)": COLORS["env_green"],
                             "(Location-Based)": COLORS["tsmc_charcoal"],
                         })
        fig_s2.update_traces(line=dict(width=3), marker=dict(size=8))
        fig_s2.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                             xaxis=dict(showgrid=False),
                             yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
                             margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_s2, use_container_width=True)

    st.info(
        "**Director note:** While carbon intensity per $M revenue improved 14.8% YoY "
        "(from 170.05 to 144.82), absolute emissions rose 7.6% as new fabs ramped up. "
        "Per-unit gains are masking continued growth in the absolute footprint."
    )

# ---------------- ENERGY ----------------
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Total Energy Consumption (GWh)")
        e_df = env[env["KPI"] == "Total Energy Consumption"]
        fig_e = px.bar(e_df, x="Year", y="Value",
                       labels={"Value": "Energy (GWh)"})
        fig_e.update_traces(marker_color=COLORS["env_green"])
        fig_e.update_layout(height=380, plot_bgcolor="white", paper_bgcolor="white",
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
                            margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_e, use_container_width=True)

    with col_b:
        st.markdown("#### Renewable Energy % vs Targets")
        r_df = env[env["KPI"] == "Renewable Energy Percentage"].copy()

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(
            x=r_df["Year"], y=r_df["Value"],
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in r_df["Value"]],
            textposition="top center",
            line=dict(color=COLORS["env_green"], width=4),
            marker=dict(size=12, line=dict(width=2, color="white")),
            name="Actual",
        ))
        fig_r.add_hline(y=60, line_dash="dash", line_color=COLORS["gov_gold"],
                        annotation_text="RE60 by 2030 target",
                        annotation_position="bottom right")
        fig_r.add_hline(y=100, line_dash="dash", line_color=COLORS["tsmc_red"],
                        annotation_text="RE100 by 2040 target",
                        annotation_position="bottom right")
        fig_r.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(title="Renewable %", range=[0, 105],
                       showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_r, use_container_width=True)

    st.warning(
        "**Gap to target:** Renewable energy reached 14.1% in 2024. To meet the **RE60 by 2030** "
        "interim target requires roughly 7.7 percentage points of growth per year — versus the "
        "2.9 pp gain achieved in 2024."
    )

# ---------------- WATER ----------------
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Total Water Withdrawal (Million MT)")
        w_df = env[env["KPI"] == "Total Water Withdrawal"]
        fig_w = px.area(w_df, x="Year", y="Value",
                        labels={"Value": "Water Withdrawal (Million MT)"})
        fig_w.update_traces(line=dict(color=COLORS["social_blue"], width=3),
                            fillcolor="rgba(21, 101, 192, 0.2)")
        fig_w.update_layout(height=380, plot_bgcolor="white", paper_bgcolor="white",
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
                            margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_w, use_container_width=True)

    with col_b:
        st.markdown("#### Water Recycled / Reused (%)")
        wr_df = env[env["KPI"] == "Water Recycled / Reused"]
        fig_wr = px.line(wr_df, x="Year", y="Value", markers=True,
                         labels={"Value": "Recycling Rate (%)"})
        fig_wr.update_traces(line=dict(color=COLORS["env_green"], width=4),
                              marker=dict(size=12))
        fig_wr.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[80, 95], showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_wr, use_container_width=True)

    st.info(
        "**Director note:** Water withdrawal grew 13.4% YoY in 2024, reflecting higher production. "
        "Recycling rate dipped from 90.3% to 88.1%, missing the unit water target by 14.3%. "
        "Water risk in Taiwan fab locations is a director-level concern."
    )

# ---------------- WASTE ----------------
with tab4:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Total vs Hazardous Waste (MT)")
        wt = env[env["KPI"].isin(["Total Waste Generated", "Hazardous Waste Generated"])].copy()
        wt["KPI_short"] = wt["KPI"].str.replace(" Generated", "", regex=False)
        fig_wt = px.bar(wt, x="Year", y="Value", color="KPI_short", barmode="group",
                        labels={"Value": "Waste (MT)", "KPI_short": "Type"},
                        color_discrete_map={
                            "Total Waste": COLORS["env_green"],
                            "Hazardous Waste": COLORS["tsmc_red"],
                        })
        fig_wt.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_wt, use_container_width=True)

    with col_b:
        st.markdown("#### Waste Diversion Rate (% not to landfill)")
        d_df = env[env["KPI"] == "Waste Diversion Rate (not to landfill)"]
        fig_d = px.line(d_df, x="Year", y="Value", markers=True,
                        labels={"Value": "Diversion Rate (%)"})
        fig_d.update_traces(line=dict(color=COLORS["env_green"], width=4),
                             marker=dict(size=12))
        fig_d.update_layout(
            height=380, plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(range=[90, 100], showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
            xaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_d, use_container_width=True)

    st.success(
        "**Strength:** Waste diversion improved to 97% in 2024. Circular-economy initiatives "
        "are translating into demonstrable performance even as absolute waste grows with capacity."
    )

# ---------------- NET-ZERO (Three Scenarios) ----------------
with tab5:
    st.markdown("#### Detailed Net-Zero 2050 Scenario Analysis")
    st.markdown(
        "Compares total emissions (Scope 1 + Scope 2 Market + Scope 3) across three "
        "forward-looking scenarios from 2019 through 2050."
    )

    nz = load_net_zero()

    fig = go.Figure()

    # Scenario 1: BAU
    fig.add_trace(go.Scatter(
        x=nz["Year"], y=nz["BAU"],
        mode="lines+markers", name="Scenario 1: Business as Usual",
        line=dict(color=COLORS["tsmc_red"], width=3),
        marker=dict(size=6),
        fill="tozeroy", fillcolor="rgba(200, 16, 46, 0.08)",
        hovertemplate="<b>BAU - %{x}</b><br>%{y:,.0f} tCO2e<extra></extra>",
    ))

    # Scenario 2: Net Zero linear
    fig.add_trace(go.Scatter(
        x=nz["Year"], y=nz["NetZero"],
        mode="lines+markers", name="Scenario 2: Net Zero (linear)",
        line=dict(color=COLORS["social_blue"], width=3, dash="dash"),
        marker=dict(size=6),
        hovertemplate="<b>Net Zero - %{x}</b><br>%{y:,.0f} tCO2e<extra></extra>",
    ))

    # Scenario 3: Proposed Actions
    fig.add_trace(go.Scatter(
        x=nz["Year"], y=nz["ProposedActions"],
        mode="lines+markers", name="Scenario 3: Proposed Actions",
        line=dict(color=COLORS["env_green"], width=4),
        marker=dict(size=7),
        hovertemplate="<b>Proposed - %{x}</b><br>%{y:,.0f} tCO2e<extra></extra>",
    ))

    fig.add_vline(x=2024, line_dash="dot", line_color="rgba(0,0,0,0.3)",
                  annotation_text="Historical / Forecast", annotation_position="top")

    # Milestone stars on Proposed Actions
    val_2030 = nz[nz["Year"] == 2030]["ProposedActions"].iloc[0]
    val_2040 = nz[nz["Year"] == 2040]["ProposedActions"].iloc[0]
    fig.add_trace(go.Scatter(
        x=[2030, 2040, 2050], y=[val_2030, val_2040, 0],
        mode="markers+text",
        marker=dict(size=20, color=[COLORS["gov_gold"], COLORS["social_blue"], COLORS["env_green"]],
                    symbol="star", line=dict(width=2, color="white")),
        text=["2030<br>back to 2020", "2040<br>RE100", "2050<br>Net-Zero"],
        textposition="top center", textfont=dict(size=10),
        showlegend=False,
    ))

    fig.update_layout(
        height=560, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="<b>Year</b>", tickmode="linear", dtick=5,
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(title="<b>Total Emissions S1+S2+S3 (tCO2e)</b>",
                   showgrid=True, gridcolor="rgba(0,0,0,0.06)", rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Milestones table — comparing scenarios at key years
    st.markdown("#### Scenario Comparison at Key Milestones (tCO2e)")
    milestones = nz[nz["Year"].isin([2024, 2030, 2035, 2040, 2045, 2050])].copy()
    milestones["BAU"] = milestones["BAU"].apply(lambda v: f"{v:,.0f}")
    milestones["NetZero"] = milestones["NetZero"].apply(lambda v: f"{v:,.0f}")
    milestones["ProposedActions"] = milestones["ProposedActions"].apply(lambda v: f"{v:,.0f}")
    milestones = milestones.rename(columns={
        "BAU": "Scenario 1: BAU",
        "NetZero": "Scenario 2: Net Zero",
        "ProposedActions": "Scenario 3: Proposed",
    })
    st.dataframe(milestones, use_container_width=True, hide_index=True)

    st.info(
        "**Recommendation:** Scenario 3 (Proposed Actions) aligns with TSMC's published "
        "commitment of returning to 2020 emission levels by 2030 and reaching net-zero by 2050. "
        "It is the only scenario that combines aggressive near-term reductions with a credible "
        "long-term glide path, satisfying SBTi 1.5°C alignment criteria."
    )
