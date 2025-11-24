# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------ PAGE CONFIG ------------
st.set_page_config(
    page_title="Sellers Liquid Dashboard",
    page_icon="💧",
    layout="wide"
)

# ------------ HIDE STREAMLIT DEFAULT HEADER / FOOTER / MENU ------------
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ------------ GLOBAL CSS (LIQUID, LIMPIO) ------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 0% 0%, #E0F2FE 0%, #CBD5E1 30%, #A5B4FC 55%, #818CF8 100%);
        color: #0F172A;
        font-family: "Segoe UI", "SF Pro Text", -apple-system, system-ui, sans-serif;
    }

    body {
        margin: 0;
    }

    .block-container {
        padding-top: 1.3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background: radial-gradient(circle at 0% 0%, #E0F2FE 0%, #CBD5E1 40%, #A5B4FC 90%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.3rem;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.60);
        border-radius: 24px;
        padding: 1.2rem 1.6rem;
        border: 1px solid rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.15);
    }

    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        opacity: 0.7;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-top: .1rem;
        margin-bottom: .1rem;
    }

    .metric-sub {
        font-size: 0.85rem;
        opacity: 0.8;
    }

    .badge-pill {
        border-radius: 999px;
        padding: 0.17rem 0.7rem;
        font-size: 0.73rem;
        background: rgba(15, 23, 42, 0.07);
        display: inline-block;
        margin-top: 0.45rem;
    }

    .pill-green {
        background: rgba(22, 163, 74, 0.15);
        color: #166534;
        border: 1px solid rgba(22, 163, 74, 0.4);
    }

    .pill-blue {
        background: rgba(59, 130, 246, 0.15);
        color: #1D4ED8;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }

    .pill-orange {
        background: rgba(234, 179, 8, 0.15);
        color: #B45309;
        border: 1px solid rgba(234, 179, 8, 0.4);
    }

    .header-title {
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .header-sub {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .avatar-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(145deg, #E0F2FE 0%, #C7D2FE 45%, #A5B4FC 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1rem;
        color: #0F172A;
        margin-right: 0.5rem;
    }

    .user-name {
        font-weight: 600;
        font-size: 0.95rem;
    }

    .user-role {
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .plotly-chart {
        border-radius: 24px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------ LOAD DATA ------------
file_path = r"/Users/davidlerma/Desktop/testing streamlit/sellers.xlsx"
df_raw = pd.read_excel(file_path)
df = df_raw.rename(columns=lambda x: x.strip())

# Column mappings
col_region = "REGION"
col_units = "SOLD UNITS"
col_total = "TOTAL SALES"
col_avg = "SALES AVERAGE"

# Create vendor column (NAME + LASTNAME)
df["VENDOR"] = df["NAME"].str.strip() + " " + df["LASTNAME"].str.strip()
col_vendor = "VENDOR"

# ------------ SIDEBAR FILTERS ------------
st.sidebar.title("Filters")  # sin gota

regions = ["All"] + sorted(df[col_region].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions, index=0)

vendors_all = sorted(df[col_vendor].dropna().unique().tolist())
selected_vendor = st.sidebar.selectbox("Vendor (optional)", ["All"] + vendors_all, index=0)

metrics_selected = st.sidebar.multiselect(
    "Metrics on chart",
    ["Units Sold", "Total Sales", "Average Sales"],
    default=["Total Sales", "Units Sold"]
)

# Apply filters
df_filtered = df.copy()
if selected_region != "All":
    df_filtered = df_filtered[df_filtered[col_region] == selected_region]

if selected_vendor != "All":
    df_filtered = df_filtered[df_filtered[col_vendor] == selected_vendor]

# ------------ KPIs ------------
total_sales = df_filtered[col_total].sum()
total_units = df_filtered[col_units].sum()
avg_sales_overall = df_filtered[col_avg].mean()
num_vendors = df_filtered[col_vendor].nunique()

# ------------ HEADER ------------
col_h1, col_h2 = st.columns([3, 1])

with col_h1:
    st.markdown(
        """
        <div class="glass-card">
            <div class="header-title">Sellers Dashboard</div>
            <div class="header-sub">Liquid glass UI · Based on sellers.xlsx</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_h2:
    st.markdown(
        f"""
        <div class="glass-card" style="display:flex; align-items:center; gap:0.5rem;">
            <div class="avatar-circle">DL</div>
            <div>
                <div class="user-name">David Lerma</div>
                <div class="user-role">Sales Analytics</div>
                <div style="font-size:0.76rem; opacity:0.7; margin-top:0.1rem;">
                    Region: {selected_region if selected_region != 'All' else 'All'}<br/>
                    Vendor: {selected_vendor if selected_vendor != 'All' else 'All'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")

# ------------ KPI CARDS ------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">Total Sales</div>
            <div class="metric-value">${total_sales:,.0f}</div>
            <div class="metric-sub">Sum of {col_total}</div>
            <span class="badge-pill pill-green">Revenue</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">Units Sold</div>
            <div class="metric-value">{total_units:,.0f}</div>
            <div class="metric-sub">Total units across filtered data</div>
            <span class="badge-pill pill-blue">Volume</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">Avg Sales</div>
            <div class="metric-value">${avg_sales_overall:,.0f}</div>
            <div class="metric-sub">Mean {col_avg}</div>
            <span class="badge-pill pill-orange">Ticket promedio</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">Active Vendors</div>
            <div class="metric-value">{num_vendors}</div>
            <div class="metric-sub">Unique {col_vendor} in selection</div>
            <span class="badge-pill">Coverage</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")

# ------------ TABS ------------
tab_overview, tab_vendors, tab_regions = st.tabs(["Overview", "Vendors", "Regions"])

# ===================== OVERVIEW TAB =====================
with tab_overview:
    st.markdown("")

    col1, col2 = st.columns([1.6, 1.4])

    # --- Total Sales by Region (bar) ---
    with col1:
        df_region = (
            df_filtered
            .groupby(col_region, as_index=False)[col_total]
            .sum()
            .sort_values(col_total, ascending=False)
        )

        fig_region = px.bar(
            df_region,
            x=col_region,
            y=col_total,
            template="plotly_white"
        )
        fig_region.update_layout(
            title="Total Sales by Region",
            margin=dict(l=20, r=20, t=50, b=40),
            xaxis_title="Region",
            yaxis_title="Total Sales",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_region, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Bubble Chart global ---
    with col2:
        if not df_filtered.empty:
            fig_bubble = px.scatter(
                df_filtered,
                x=col_units,
                y=col_total,
                size=col_avg,
                color=col_region,
                hover_name=col_vendor,
                size_max=30,
                template="plotly_white"
            )
            fig_bubble.update_layout(
                title="Bubble Chart: Units vs Sales vs Avg",
                xaxis_title="Units Sold",
                yaxis_title="Total Sales",
                margin=dict(l=20, r=20, t=50, b=40),
                legend=dict(title="Region", orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        else:
            fig_bubble = px.scatter(x=[], y=[], template="plotly_white")
            fig_bubble.update_layout(
                title="Bubble Chart: Units vs Sales vs Avg",
                margin=dict(l=20, r=20, t=50, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_bubble, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")

    # --- Heatmap + Table ---
    heat_col, table_col = st.columns([1.1, 1.9])

    with heat_col:
        if not df_filtered.empty:
            df_heatmap = df_filtered.pivot_table(
                index=col_region,
                columns=col_vendor,
                values=col_total,
                aggfunc="sum",
                fill_value=0
            )
            fig_heat = px.imshow(
                df_heatmap,
                labels=dict(x="Vendor", y="Region", color="Total Sales"),
                color_continuous_scale="Blues",
            )
            fig_heat.update_layout(
                title="Heatmap: Total Sales by Region & Vendor",
                margin=dict(l=20, r=20, t=50, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        else:
            fig_heat = px.imshow([[0]], labels=dict(x="", y="", color="Total Sales"))
            fig_heat.update_layout(
                title="Heatmap: Total Sales by Region & Vendor",
                margin=dict(l=20, r=20, t=50, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_heat, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with table_col:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Data table</div>
                <div class="metric-sub" style="margin-bottom:0.6rem;">
                    Filtered view from <b>sellers.xlsx</b>. Use the sidebar filters to refine region or vendor.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_filtered, use_container_width=True)

# ===================== VENDORS TAB =====================
with tab_vendors:
    st.markdown("")

    # --- Metrics by Vendor (bar grouped) ---
    metric_cols_map = {
        "Units Sold": col_units,
        "Total Sales": col_total,
        "Average Sales": col_avg,
    }
    metrics_real = [metric_cols_map[m] for m in metrics_selected]

    df_plot = df_filtered[[col_vendor] + metrics_real].copy()
    df_long = df_plot.melt(id_vars=col_vendor, var_name="Metric", value_name="Value")
    inv_map = {v: k for k, v in metric_cols_map.items()}
    df_long["Metric"] = df_long["Metric"].map(inv_map)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    fig_vendor = px.bar(
        df_long,
        x=col_vendor,
        y="Value",
        color="Metric",
        barmode="group",
        template="plotly_white"
    )
    fig_vendor.update_layout(
        title="Vendor Performance by Metric",
        margin=dict(l=20, r=20, t=50, b=40),
        xaxis_title="Vendor",
        yaxis_title="Value",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_vendor, use_container_width=True, theme=None)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")

    # --- Vendor focus + vendor table ---
    left, right = st.columns([1.1, 1.9])

    with left:
        if selected_vendor != "All":
            df_vendor = df[df[col_vendor] == selected_vendor]
            total_vendor_sales = df_vendor[col_total].sum()
            total_vendor_units = df_vendor[col_units].sum()
            avg_vendor_sale = df_vendor[col_avg].mean()

            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="metric-label">Vendor focus</div>
                    <div class="metric-value" style="font-size:1.5rem;">{selected_vendor}</div>
                    <div class="metric-sub">
                        Total Sales: <b>${total_vendor_sales:,.0f}</b><br/>
                        Units Sold: <b>{total_vendor_units:,.0f}</b><br/>
                        Avg Sales: <b>${avg_vendor_sale:,.0f}</b>
                    </div>
                    <span class="badge-pill pill-blue">Detail view</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="metric-label">Vendor focus</div>
                    <div class="metric-sub">
                        Select a specific vendor on the left sidebar to see a detailed summary here.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Vendors data</div>
                <div class="metric-sub" style="margin-bottom:0.6rem;">
                    Filtered vendor records (after applying Region and Vendor filters).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_filtered[[col_vendor, col_region, col_units, col_total, col_avg]], use_container_width=True)

# ===================== REGIONS TAB =====================
with tab_regions:
    st.markdown("")

    # --- Region summary table ---
    df_region_summary = (
        df_filtered
        .groupby(col_region, as_index=False)
        .agg(
            Total_Sales=(col_total, "sum"),
            Units_Sold=(col_units, "sum"),
            Avg_Sales=(col_avg, "mean"),
            Vendors_Count=(col_vendor, "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    reg_top, reg_bottom = st.columns([1.5, 1.5])

    with reg_top:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Region summary</div>
                <div class="metric-sub" style="margin-bottom:0.6rem;">
                    Aggregated KPIs per region (based on current filters).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_region_summary, use_container_width=True)

    with reg_bottom:
        fig_region2 = px.bar(
            df_region_summary,
            x=col_region,
            y="Total_Sales",
            hover_data=["Units_Sold", "Avg_Sales", "Vendors_Count"],
            template="plotly_white"
        )
        fig_region2.update_layout(
            title="Total Sales & Context per Region",
            margin=dict(l=20, r=20, t=50, b=40),
            xaxis_title="Region",
            yaxis_title="Total Sales",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_region2, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------ INSIGHTS / EXPLANACIÓN ------------
with st.expander("What each section is useful for"):
    st.markdown(
        """
        ### Overview
        - **Total Sales by Region**: Te dice qué región domina en revenue y cuál está débil.
        - **Bubble Chart (Units vs Sales vs Avg)**: Cada burbuja es un vendedor; ves volumen, revenue y ticket en una sola vista.
        - **Heatmap**: Cruza región y vendedor para ver hotspots donde hay mucha o poca venta.

        ### Vendors
        - **Vendor Performance by Metric**: Compara a los vendedores en las métricas clave (unidades, ventas, promedio).
        - **Vendor focus**: Tarjeta que resume el desempeño del vendedor seleccionado.
        - **Vendors data table**: Tabla limpia para revisar filas específicas de vendedores.

        ### Regions
        - **Region summary table**: KPIs por región (ventas totales, unidades, ticket promedio, # de vendors).
        - **Total Sales & Context per Region**: Gráfico para ver rápido qué región aporta más y su contexto.
        """
    )
