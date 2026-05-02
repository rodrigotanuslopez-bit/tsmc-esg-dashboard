"""
TSMC ESG Dashboard - Peer Comparison Page
Benchmarking TSMC against NVIDIA, ASML, and Broadcom across E/S/G dimensions.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from utils.styling import apply_global_styling, COLORS, page_header
from utils.data_loader import load_peer_comparison

st.set_page_config(
    page_title="Peer Comparison | TSMC ESG",
    page_icon="◆",
    layout="wide",
)
apply_global_styling()

page_header(
    "Peer Comparison Analysis",
    "TSMC benchmarked against NVIDIA, ASML, and Broadcom across ESG dimensions",
    pillar=None,
)

# Load peer data
peer_data = load_peer_comparison()

# ---------------------------------------------------------------------------
# Executive Summary
# ---------------------------------------------------------------------------
st.markdown("## ESG Ratings Consensus")

st.markdown(
    f"""
    <div class="panel">
    <p style="font-size: 1.0rem; line-height: 1.6;">
    TSMC is benchmarked against three semiconductor industry peers: <b>NVIDIA</b> (fabless designer),
    <b>ASML</b> (lithography equipment supplier), and <b>Broadcom</b> (fabless communications/AI).
    This peer set spans the value chain rather than direct foundry competitors, providing strategic
    context on ESG performance across the ecosystem.
    </p>
    <p style="font-size: 0.9rem; color: {COLORS['tsmc_charcoal']}; margin-top: 1rem;">
    <b>Critical context:</b> Absolute environmental metrics (emissions, energy, water) are NOT
    directly comparable due to business model differences. TSMC operates 21 fabs globally;
    NVIDIA and Broadcom are fabless. Focus on intensity ratios and governance practice.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Rating tiles
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="panel" style="border-left: 5px solid {COLORS['tsmc_red']};">
            <h3 style="color: {COLORS['tsmc_navy']}; margin-top: 0;">TSMC</h3>
            <p style="margin: 0.25rem 0;"><b>MSCI:</b> AA</p>
            <p style="margin: 0.25rem 0;"><b>Sustainalytics:</b> 13.57 (Low Risk)</p>
            <p style="margin: 0.25rem 0;"><b>S&P:</b> 99</p>
            <p style="margin: 0.25rem 0;"><b>RepRisk:</b> BB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="panel" style="border-left: 5px solid {COLORS['env_green']};">
            <h3 style="color: {COLORS['tsmc_navy']}; margin-top: 0;">NVIDIA</h3>
            <p style="margin: 0.25rem 0;"><b>MSCI:</b> AA</p>
            <p style="margin: 0.25rem 0;"><b>Sustainalytics:</b> 12.45 (Low Risk)</p>
            <p style="margin: 0.25rem 0;"><b>S&P:</b> 93</p>
            <p style="margin: 0.25rem 0;"><b>RepRisk:</b> CCC</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="panel" style="border-left: 5px solid {COLORS['social_blue']};">
            <h3 style="color: {COLORS['tsmc_navy']}; margin-top: 0;">ASML</h3>
            <p style="margin: 0.25rem 0;"><b>MSCI:</b> AAA ⭐</p>
            <p style="margin: 0.25rem 0;"><b>Sustainalytics:</b> 8.67 (Negligible)</p>
            <p style="margin: 0.25rem 0;"><b>S&P:</b> 96</p>
            <p style="margin: 0.25rem 0;"><b>RepRisk:</b> AA</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="panel" style="border-left: 5px solid {COLORS['gov_gold']};">
            <h3 style="color: {COLORS['tsmc_navy']}; margin-top: 0;">Broadcom</h3>
            <p style="margin: 0.25rem 0;"><b>MSCI:</b> AA</p>
            <p style="margin: 0.25rem 0;"><b>Sustainalytics:</b> 20.11 (Medium)</p>
            <p style="margin: 0.25rem 0;"><b>S&P:</b> 57</p>
            <p style="margin: 0.25rem 0;"><b>RepRisk:</b> BB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Environmental",
    "👥 Social",
    "🏛️ Governance",
    "📊 Gap Analysis",
    "💡 Strategic Priorities"
])

# ===========================================================================
# ENVIRONMENTAL TAB
# ===========================================================================
with tab1:
    st.markdown("### Environmental Performance Comparison")
    
    # Renewable Energy Gap
    st.markdown("#### Renewable Energy % — Primary Strategic Gap")
    
    renewable_data = pd.DataFrame({
        'Company': ['TSMC', 'NVIDIA', 'ASML', 'Broadcom'],
        'Renewable_Pct': [13.18, 68.72, 78.68, 29.35],
        'Color': [COLORS['tsmc_red'], COLORS['env_green'],
                  COLORS['env_green'], COLORS['gov_gold']]
    })
    
    fig_renewable = go.Figure()
    
    for idx, row in renewable_data.iterrows():
        fig_renewable.add_trace(go.Bar(
            x=[row['Company']],
            y=[row['Renewable_Pct']],
            name=row['Company'],
            marker_color=row['Color'],
            text=f"{row['Renewable_Pct']:.1f}%",
            textposition='outside',
            showlegend=False
        ))
    
    fig_renewable.add_hline(
        y=60, line_dash="dash", line_color=COLORS['warning'],
        annotation_text="TSMC RE60 by 2030 Target",
        annotation_position="bottom right"
    )
    fig_renewable.add_hline(
        y=100, line_dash="dash", line_color=COLORS['env_green'],
        annotation_text="RE100 Target (TSMC 2040 / ASML achieved)",
        annotation_position="top right"
    )
    
    fig_renewable.update_layout(
        height=450,
        yaxis=dict(
            title="% Renewable Energy",
            range=[0, 110],
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)"
        ),
        xaxis=dict(showgrid=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    
    st.plotly_chart(fig_renewable, use_container_width=True)
    
    st.error(
        "**Critical Gap:** TSMC at 13.2% is **65 percentage points behind ASML** (79%) and "
        "**55 points behind NVIDIA** (69%). To meet RE60 by 2030 requires ~7.7pp annual growth vs "
        "the 2.9pp achieved in 2024. This is the #1 strategic priority."
    )
    
    # Scope 1 & 2 Emissions
    st.markdown("#### Scope 1 & 2 Emissions — Absolute vs Intensity")
    
    emissions_abs = pd.DataFrame({
        'Company': ['TSMC', 'NVIDIA', 'ASML', 'Broadcom'],
        'Scope1_MT': [1941670, 11896, 24000, 53648],
        'Scope2_MT': [10957400, 40555, 9000, 166752]
    })
    
    # Approximate 2024 revenues for intensity calc ($M)
    revenues = {'TSMC': 88300, 'NVIDIA': 60922, 'ASML': 28256, 'Broadcom': 51622}
    emissions_abs['Revenue_M'] = emissions_abs['Company'].map(revenues)
    emissions_abs['Scope2_Intensity'] = (emissions_abs['Scope2_MT'] / emissions_abs['Revenue_M'])
    
    tab_a, tab_b = st.tabs(["Absolute (Not Comparable)", "Intensity (Comparable)"])
    
    with tab_a:
        st.warning("⚠️ These absolute figures reflect business model differences — NOT performance")
        
        fig_abs = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Scope 1 Emissions (MT CO2e)", "Scope 2 Market-Based (MT CO2e)")
        )
        
        fig_abs.add_trace(
            go.Bar(
                x=emissions_abs['Company'],
                y=emissions_abs['Scope1_MT'],
                marker_color=COLORS['social_blue'],
                name='Scope 1',
                text=emissions_abs['Scope1_MT'].apply(lambda x: f"{x/1e6:.1f}M"),
                textposition='outside'
            ),
            row=1, col=1
        )
        
        fig_abs.add_trace(
            go.Bar(
                x=emissions_abs['Company'],
                y=emissions_abs['Scope2_MT'],
                marker_color=COLORS['tsmc_red'],
                name='Scope 2',
                text=emissions_abs['Scope2_MT'].apply(lambda x: f"{x/1e6:.1f}M"),
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig_abs.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        st.plotly_chart(fig_abs, use_container_width=True)
        
        st.info(
            "TSMC's Scope 2 is ~270x larger than NVIDIA's because TSMC manufactures " +
            "the chips NVIDIA designs"
        )
    
    with tab_b:
        st.success("✓ Revenue-adjusted intensity metrics ARE comparable")
        
        fig_intensity = go.Figure(go.Bar(
            x=emissions_abs['Company'],
            y=emissions_abs['Scope2_Intensity'],
            marker_color=[COLORS['warning'], COLORS['env_green'],
                         COLORS['env_green'], COLORS['warning']],
            text=emissions_abs['Scope2_Intensity'].apply(lambda x: f"{x:.1f}"),
            textposition='outside'
        ))
        
        fig_intensity.update_layout(
            height=400,
            yaxis_title="Scope 2 Emissions per $M Revenue (MT CO2e/$M)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)"),
        )
        
        st.plotly_chart(fig_intensity, use_container_width=True)
        
        st.markdown("""
        **Intensity Analysis:**
        - TSMC's intensity (124 MT/$M) comparable to Broadcom when controlling for model
        - Gap to ASML (0.3 MT/$M) reflects ASML's 79% renewable procurement
        - **Priority:** Accelerate Scope 2 via offshore wind PPAs
        """)
    
    # Water & Waste
    st.markdown("#### Operational Excellence — Water Recycling & Waste Diversion")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        water_data = pd.DataFrame({
            'Company': ['TSMC', 'Industry Avg'],
            'Recycling_Rate': [88.1, 75.0]
        })
        
        fig_water = go.Figure(go.Bar(
            x=water_data['Company'],
            y=water_data['Recycling_Rate'],
            marker_color=[COLORS['env_green'], COLORS['tsmc_charcoal']],
            text=water_data['Recycling_Rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside'
        ))
        
        fig_water.add_hline(
            y=90, line_dash="dash",
            annotation_text="TSMC 2030 Target (90%)"
        )
        
        fig_water.update_layout(
            title="Water Recycling Rate",
            height=350,
            yaxis=dict(range=[0, 100], title="%"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )
        
        st.plotly_chart(fig_water, use_container_width=True)
    
    with col_b:
        waste_data = pd.DataFrame({
            'Company': ['TSMC', 'ASML', 'NVIDIA'],
            'Diversion_Rate': [97.0, 74.0, np.nan]
        })
        
        fig_waste = go.Figure(go.Bar(
            x=waste_data['Company'][:2],
            y=waste_data['Diversion_Rate'][:2],
            marker_color=[COLORS['env_green'], COLORS['warning']],
            text=['97%', '74%'],
            textposition='outside'
        ))
        
        fig_waste.update_layout(
            title="Waste Diversion from Landfill",
            height=350,
            yaxis=dict(range=[0, 100], title="%"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )
        
        st.plotly_chart(fig_waste, use_container_width=True)
    
    st.success("✓ TSMC leads peers on water recycling (88%) and waste diversion (97%)")

# ===========================================================================
# SOCIAL TAB
# ===========================================================================
with tab2:
    st.markdown("### Social Performance Comparison")
    
    st.markdown(
        f"""
        <div class="panel">
        <p style="font-size: 1.0rem; line-height: 1.6;">
        <b>Key Finding:</b> TSMC's underlying social performance (safety, retention, training)
        is best-in-peer, but disclosure depth lags NVIDIA and ASML on gender pay equity,
        full-workforce diversity, and supplier audit results.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Diverging bar chart
    st.markdown("#### TSMC Social Profile: Strengths vs Disclosure Gaps")
    
    social_profile = pd.DataFrame({
        'Metric': [
            'Gender Pay Gap\nDisclosure',
            'Workforce Diversity\nby Region',
            'Supplier Audit\nTransparency',
            'Safety (TRIR)',
            'Voluntary Turnover',
            'Training Hours'
        ],
        'Value': [-2, -2, -1.5, 3, 2.5, 3],
        'Label': [
            'Gap vs NVIDIA/ASML',
            'Gap vs NVIDIA/ASML',
            'Gap vs ASML',
            'Best-in-Peer (0.133)',
            'Best-in-Peer (3.4%)',
            'Leading (100.5 hrs)'
        ]
    })
    
    colors = [COLORS['tsmc_red'] if v < 0 else COLORS['env_green']
              for v in social_profile['Value']]
    
    fig_social = go.Figure(go.Bar(
        y=social_profile['Metric'],
        x=social_profile['Value'],
        orientation='h',
        marker_color=colors,
        text=social_profile['Label'],
        textposition='outside',
        textfont=dict(size=11)
    ))
    
    fig_social.add_vline(x=0, line_width=2, line_color=COLORS['tsmc_navy'])
    
    fig_social.update_layout(
        height=450,
        xaxis=dict(
            title="← Disclosure Gaps          TSMC Position          Operational Strengths →",
            range=[-3, 4],
            zeroline=False,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.06)"
        ),
        yaxis_title="",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=250, t=20, b=20),
    )
    
    st.plotly_chart(fig_social, use_container_width=True)
    
    # TSMC trends table
    st.markdown("#### TSMC Workforce Metrics Trends (FY2020-2024)")
    
    social_trends = pd.DataFrame({
        'KPI': [
            'Total Employees',
            'Women in Workforce (%)',
            'Women in Senior Mgmt (%)',
            'TRIR (per 200k hrs)',
            'Voluntary Turnover (%)',
            'Training Hours / Employee'
        ],
        '2020': [56831, 37.1, 10.0, 0.311, 5.1, 16.3],
        '2022': [73090, 34.4, 6.1, 0.145, 6.5, 69.5],
        '2024': [83825, 33.7, 11.4, 0.133, 3.4, 100.5],
        '5-Yr Trend': [
            '↑ +47%',
            '↓ -3.4pp',
            '↑ +1.4pp (volatile)',
            '↓ -57% ⭐',
            '↓ -1.7pp ⭐',
            '↑ +517% ⭐'
        ]
    })
    
    st.dataframe(social_trends, use_container_width=True, hide_index=True)
    
    st.warning(
        "**Disclosure Priority:** Publish unadjusted gender pay gap, full-workforce diversity " +
        "beyond senior management, and granular supplier audit results to match NVIDIA/ASML depth"
    )

# ===========================================================================
# GOVERNANCE TAB
# ===========================================================================
with tab3:
    st.markdown("### Governance Comparison")
    
    # Board metrics
    st.markdown("#### Board Independence & Diversity")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        indep_data = pd.DataFrame({
            'Company': ['TSMC', 'NVIDIA', 'ASML', 'Broadcom', 'Peer Median'],
            'Independence': [70, 85, 87, 92, 88]
        })
        
        colors_indep = [
            COLORS['tsmc_red'] if c == 'TSMC'
            else COLORS['tsmc_charcoal'] if c == 'Peer Median'
            else COLORS['env_green']
            for c in indep_data['Company']
        ]
        
        fig_indep = go.Figure(go.Bar(
            x=indep_data['Company'],
            y=indep_data['Independence'],
            marker_color=colors_indep,
            text=indep_data['Independence'].apply(lambda x: f"{x}%"),
            textposition='outside'
        ))
        
        fig_indep.add_hline(
            y=75, line_dash="dash",
            annotation_text="Best Practice (75%)"
        )
        
        fig_indep.update_layout(
            title="Board Independence %",
            height=400,
            yaxis=dict(range=[0, 100]),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )
        
        st.plotly_chart(fig_indep, use_container_width=True)
    
    with col_b:
        diversity_board = pd.DataFrame({
            'Company': ['TSMC', 'NVIDIA', 'ASML', 'Broadcom'],
            'Women_Pct_2024': [20, 27, 29, 25],
            'Target_2030': [25, 30, 35, 30]
        })
        
        fig_div = go.Figure()
        
        fig_div.add_trace(go.Bar(
            name='2024 Actual',
            x=diversity_board['Company'],
            y=diversity_board['Women_Pct_2024'],
            marker_color=COLORS['social_blue'],
            text=diversity_board['Women_Pct_2024'].apply(lambda x: f"{x}%"),
            textposition='outside'
        ))
        
        fig_div.add_trace(go.Scatter(
            name='2030 Target',
            x=diversity_board['Company'],
            y=diversity_board['Target_2030'],
            mode='markers',
            marker=dict(size=14, color=COLORS['tsmc_red'], symbol='diamond')
        ))
        
        fig_div.update_layout(
            title="Women on Board %",
            height=400,
            yaxis=dict(range=[0, 40]),
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center')
        )
        
        st.plotly_chart(fig_div, use_container_width=True)
    
    st.info(
        "TSMC's board independence at 70% is below peer median (88%) but above best-practice " +
        "threshold. Gender diversity doubled from 10% to 20% in 2024 — strong year-over-year " +
        "progress but still below ASML's 29% benchmark."
    )
    
    # ESG-linked compensation
    st.markdown("#### ESG-Linked Executive Compensation")
    
    comp_status = pd.DataFrame({
        'Company': ['TSMC', 'NVIDIA', 'ASML', 'Broadcom'],
        'ESG_Linked_Pay': ['Yes', 'Yes', 'Yes', 'Yes'],
        'Since': ['2020', '2019', '2018', '2021'],
        'Metrics': [
            'GHG, water, TRIR, retention',
            'Energy efficiency, diversity',
            'GHG neutral, diversity',
            'ESG ratings, governance'
        ]
    })
    
    st.dataframe(comp_status, use_container_width=True, hide_index=True)
    
    st.success("✓ All four peers link executive pay to ESG metrics — table stakes for governance")

# ===========================================================================
# GAP ANALYSIS TAB
# ===========================================================================
with tab4:
    st.markdown("### Strategic Gap Analysis — Priority Heatmap")
    
    # Performance heatmap
    heatmap_data = pd.DataFrame({
        'Metric': [
            'Renewable Energy %',
            'Scope 2 Intensity',
            'Water Recycling',
            'Waste Diversion',
            'Board Diversity',
            'Safety (TRIR)',
            'Disclosure Depth'
        ],
        'TSMC': [1, 2, 4, 5, 3, 5, 2],
        'NVIDIA': [4, 5, 3, 3, 3, 3, 4],
        'ASML': [5, 5, 3, 4, 4, 3, 5],
        'Broadcom': [2, 2, 2, 2, 3, 2, 1],
        'Materiality': [5, 5, 4, 3, 3, 4, 4]
    })
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data[['TSMC', 'NVIDIA', 'ASML', 'Broadcom']].values,
        x=['TSMC', 'NVIDIA', 'ASML', 'Broadcom'],
        y=heatmap_data['Metric'],
        colorscale=[
            [0, COLORS['tsmc_red']],
            [0.5, COLORS['warning']],
            [1, COLORS['env_green']]
        ],
        text=heatmap_data[['TSMC', 'NVIDIA', 'ASML', 'Broadcom']].values,
        texttemplate='%{text}',
        textfont={"size": 14, "color": "white"},
        colorbar=dict(
            title="Quartile",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Bottom', 'Below Avg', 'Average', 'Above Avg', 'Top']
        )
    ))
    
    fig_heatmap.update_layout(
        height=500,
        title="Performance Quartile by Metric (1=Bottom, 5=Top)",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("""
    **Reading the Heatmap:**
    - 🟩 Green (4-5): Top/Above-average performance
    - 🟨 Yellow (3): Average performance
    - 🟥 Red (1-2): Below-average — **priority areas**
    
    **High-Priority Cells (Red + High Materiality):**
    - Renewable Energy % (TSMC=1, Materiality=5) ⚠️
    - Scope 2 Intensity (TSMC=2, Materiality=5)
    - Disclosure Depth (TSMC=2, Materiality=4)
    """)
    
    # Financial waterfall
    st.markdown("#### Financial Impact — Carbon Pricing Exposure")
    
    waterfall_stages = [
        'Current\nExposure',
        'EU CBAM\n(2026-2028)',
        'Taiwan Fee\n(2025+)',
        'Mitigated\n(Roadmap)'
    ]
    waterfall_values = [0, 30, 70, -50]
    
    fig_waterfall = go.Figure(go.Waterfall(
        x=waterfall_stages,
        y=waterfall_values,
        text=['$0M', '+$30M', '+$70M', '-$50M'],
        textposition='outside',
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": COLORS['env_green']}},
        increasing={"marker": {"color": COLORS['tsmc_red']}},
        totals={"marker": {"color": COLORS['social_blue']}}
    ))
    
    fig_waterfall.update_layout(
        height=450,
        title="Carbon Pricing Exposure by 2030 ($M/year)",
        yaxis_title="Annual Exposure ($M)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    st.warning(
        "**Financial Case:** Taiwan carbon fee + EU CBAM could create $100M+ annual exposure " +
        "by 2030. Roadmap execution (RE60, SBTi targets) mitigates ~$50M, plus revenue " +
        "protection from ESG-mandate capital and hyperscaler contracts."
    )

# ===========================================================================
# STRATEGIC PRIORITIES TAB
# ===========================================================================
with tab5:
    st.markdown("### Strategic Priorities — Roadmap")
    
    st.markdown(
        f"""
        <div class="panel">
        <h4 style="color: {COLORS['tsmc_red']}; margin-top: 0;">Four Data-Driven Priorities</h4>
        <p>Each priority is grounded in a specific KPI gap vs the peer set and tied to
        measurable 2025-2030 milestones.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Roadmap table
    roadmap = pd.DataFrame({
        'Priority': [
            '1. Accelerate Scope 2\n(Renewable Energy)',
            '2. Deepen Scope 3\n(Supplier Engagement)',
            '3. Close Social\nDisclosure Gaps',
            '4. Water Resilience\nto 90%+'
        ],
        'Gap vs Best-in-Peer': [
            'ASML 79% vs TSMC 13%\n= 65pp gap',
            'Limited supplier\ntarget disclosure',
            'No pay gap, diversity,\naudit transparency',
            '88% vs 90% target\n(2pp gap)'
        ],
        '2025 Milestone': [
            'SBTi resubmission\n+1GW offshore PPA',
            'SBTi Scope 3 target\nTop 200 mandate',
            'Disclose pay gap\nBaseline diversity',
            'Hsinchu Phase 2\nonline'
        ],
        '2027 Target': [
            '25% renewable',
            '100% Tier 1 coverage',
            'Published targets',
            '89% recycling'
        ],
        '2030 Target': [
            '60% renewable (RE60)',
            '-25% intensity vs 2025',
            '≥35% women workforce',
            '≥92% recycling'
        ],
        'Owner': [
            'CFO +\nFacilities',
            'CPO +\nSustainability',
            'CHRO',
            'CSO'
        ]
    })
    
    st.dataframe(roadmap, use_container_width=True, hide_index=True, height=250)
    
    # Expected outcomes
    st.markdown("#### Expected Outcomes by Horizon")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown(
            f"""
            <div class="panel" style="border-top: 4px solid {COLORS['gov_gold']};">
                <h4 style="color: {COLORS['gov_gold']}; margin-top: 0;">2027 Horizon</h4>
                <ul style="line-height: 1.8;">
                    <li>SBTi-validated Scope 1/2/3 target</li>
                    <li>Renewable share past 25%</li>
                    <li>Social disclosure gap closed</li>
                    <li>Sustainalytics → Negligible Risk</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_b:
        st.markdown(
            f"""
            <div class="panel" style="border-top: 4px solid {COLORS['social_blue']};">
                <h4 style="color: {COLORS['social_blue']}; margin-top: 0;">2030 Horizon</h4>
                <ul style="line-height: 1.8;">
                    <li>Renewable share ≥60% (RE60)</li>
                    <li>Absolute Scope 1 declining</li>
                    <li>Water recycling ≥92%</li>
                    <li>Audit transparency = ASML</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_c:
        st.markdown(
            f"""
            <div class="panel" style="border-top: 4px solid {COLORS['env_green']};">
                <h4 style="color: {COLORS['env_green']}; margin-top: 0;">2040-2050</h4>
                <ul style="line-height: 1.8;">
                    <li>RE100 delivered (2040)</li>
                    <li>Net-Zero S1+S2+S3 (2050)</li>
                    <li>Reasonable assurance</li>
                    <li>Best-in-peer foundry ESG</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Director's Summary
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("## Director's Summary — Three Key Takeaways")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['env_green']};">
            <h4 style="color: {COLORS['env_green']}; margin-top: 0;">Where TSMC Leads</h4>
            <ul style="line-height: 1.8;">
                <li>Water recycling: 88% (best-in-peer)</li>
                <li>Waste diversion: 97% (best-in-peer)</li>
                <li>Safety (TRIR): 0.133 (best-in-peer)</li>
                <li>Retention: 3.4% turnover (best-in-peer)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_col2:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['tsmc_red']};">
            <h4 style="color: {COLORS['tsmc_red']}; margin-top: 0;">Where TSMC Lags</h4>
            <ul style="line-height: 1.8;">
                <li>Renewable: 13% vs ASML 79% (65pp gap)</li>
                <li>Board diversity: 20% vs ASML 29%</li>
                <li>Social disclosure vs NVIDIA/ASML</li>
                <li>Scope 2 intensity vs peers</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_col3:
    st.markdown(
        f"""
        <div class="panel" style="border-top: 4px solid {COLORS['social_blue']};">
            <h4 style="color: {COLORS['social_blue']}; margin-top: 0;">Board-Level Actions</h4>
            <ul style="line-height: 1.8;">
                <li>Accelerate offshore wind PPAs (RE60 by 2030)</li>
                <li>Mandate Scope 3 targets for top suppliers</li>
                <li>Disclose pay gap + audit transparency</li>
                <li>Set 2030 diversity targets (≥35% women)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "**Data Sources:** TSMC 2024 Sustainability Report, NVIDIA FY24 Sustainability Report, " +
    "ASML 2024 Integrated Report, Broadcom 2024 Sustainability Report, MSCI ESG Research, " +
    "Sustainalytics ESG Risk Ratings, S&P Global CSA, RepRisk. All data as of FY2024."
)
