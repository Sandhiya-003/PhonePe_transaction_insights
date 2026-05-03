import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0a1e;
    color: #e8e0f5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0f35 0%, #0f0a1e 100%);
    border-right: 1px solid #3d2a6e;
}
[data-testid="stSidebar"] * { color: #c9b8f0 !important; }

/* Main headings */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #1e1040 0%, #2d1b5e 100%);
    border: 1px solid #4a2d8a;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(111,66,193,0.15);
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-title {
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #9d7fd4;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #c084fc;
    line-height: 1.2;
}
.kpi-sub {
    font-size: 11px;
    color: #6b5fa0;
    margin-top: 4px;
}

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8e0f5;
    border-left: 4px solid #7c3aed;
    padding-left: 12px;
    margin: 32px 0 16px 0;
}

/* Tag badge */
.badge {
    display: inline-block;
    background: #2d1b5e;
    border: 1px solid #5b3fa0;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    color: #a78bfa;
    margin: 2px;
}

/* Streamlit overrides */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e1040, #2d1b5e);
    border: 1px solid #4a2d8a;
    border-radius: 12px;
    padding: 16px;
}
.stSelectbox > div > div {
    background: #1e1040 !important;
    border: 1px solid #4a2d8a !important;
    color: #e8e0f5 !important;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# Plotly dark theme template
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c9b8f0"),
    colorway=["#7c3aed","#a78bfa","#c084fc","#e879f9","#f0abfc",
               "#818cf8","#38bdf8","#34d399","#fb923c","#f87171"],
)

PURPLE_SEQ = px.colors.sequential.Purples


# ─────────────────────────────────────────────
#  DB HELPERS
# ─────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH  = ROOT_DIR / "phonepe.db"

@st.cache_data(show_spinner=False)
def query(sql: str) -> pd.DataFrame:
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

def fmt_billions(val): return f"₹{val/1e9:.2f}B"
def fmt_crore(val):    return f"₹{val/1e7:.1f}Cr"
def fmt_lakh(val):     return f"{val/1e5:.1f}L"


# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 30px 0;'>
        <div style='font-size:40px'>💜</div>
        <div style='font-family:Syne,sans-serif; font-size:18px;
                    font-weight:800; color:#c084fc; margin-top:8px;'>
            PhonePe Insights
        </div>
        <div style='font-size:11px; color:#6b5fa0; margin-top:4px;'>
            Transaction Analytics Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Overview",
         "📊 Transactions",
         "🗺️ Map View",
         "👤 Users",
         "🏆 Top Performers",
         "🛡️ Insurance",
         "🔍 Business Insights"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Global year filter
    years_df = query("SELECT DISTINCT Year FROM aggregated_transaction ORDER BY Year")
    all_years = years_df["Year"].tolist() if not years_df.empty else [2018,2019,2020,2021,2022]
    selected_years = st.multiselect("Filter by Year", all_years, default=all_years)
    year_filter = ",".join(str(y) for y in selected_years) if selected_years else ",".join(str(y) for y in all_years)

    st.markdown(f"""
    <div style='margin-top:40px; font-size:10px; color:#3d2a6e; text-align:center;'>
        Data: PhonePe Pulse GitHub<br>
        Built with Streamlit + Plotly
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("""
    <h1 style='margin-bottom:4px;'>PhonePe Transaction Insights</h1>
    <p style='color:#6b5fa0; font-size:15px; margin-bottom:32px;'>
        Aggregated view of payments, users & insurance across India
    </p>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    kpi_sql = f"""
        SELECT
            SUM(Transaction_Count)  AS txn_count,
            SUM(Transaction_Amount) AS txn_amount
        FROM aggregated_transaction
        WHERE Year IN ({year_filter})
    """
    user_sql = f"""
        SELECT SUM(Registered_Users) AS users, SUM(App_Opens) AS opens
        FROM aggregated_user WHERE Year IN ({year_filter})
    """
    ins_sql = f"""
        SELECT SUM(Insurance_Amount) AS ins_amount
        FROM aggregated_insurance WHERE Year IN ({year_filter})
    """

    kpi   = query(kpi_sql).iloc[0]
    ukpi  = query(user_sql).iloc[0]
    ikpi  = query(ins_sql).iloc[0]

    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, "Total Transactions",    f"{kpi['txn_count']/1e9:.2f}B",   "billions of payments"),
        (c2, "Total Amount",          fmt_crore(kpi['txn_amount']),      "transacted"),
        (c3, "Registered Users",      fmt_lakh(ukpi['users']),           "across all states"),
        (c4, "App Opens",             fmt_lakh(ukpi['opens']),           "total sessions"),
        (c5, "Insurance Value",       fmt_crore(ikpi['ins_amount']),     "policies transacted"),
    ]
    for col, title, val, sub in cards:
        col.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>{title}</div>
            <div class='kpi-value'>{val}</div>
            <div class='kpi-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Yearly Trend ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Transaction Volume by Year</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Year, SUM(Transaction_Count) AS Count,
                   ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY Year ORDER BY Year
        """)
        if not df.empty:
            fig = go.Figure()
            fig.add_bar(x=df["Year"], y=df["Count"]/1e9, name="Count (B)",
                        marker_color="#7c3aed")
            fig.add_scatter(x=df["Year"], y=df["Amount_B"], name="Amount (₹B)",
                            mode="lines+markers", line=dict(color="#e879f9", width=3),
                            yaxis="y2")
            fig.update_layout(**PLOTLY_THEME, height=300,
                              yaxis2=dict(overlaying="y", side="right"),
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Transaction Type Share</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Transaction_Type, SUM(Transaction_Count) AS Count
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY Transaction_Type ORDER BY Count DESC
        """)
        if not df.empty:
            fig = px.pie(df, names="Transaction_Type", values="Count",
                         hole=0.55, color_discrete_sequence=PLOTLY_THEME["colorway"])
            fig.update_layout(**PLOTLY_THEME, height=300,
                              showlegend=True,
                              legend=dict(orientation="h", y=-0.2))
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

    # ── State Heatmap ──
    st.markdown("<div class='section-header'>State-wise Transaction Amount</div>", unsafe_allow_html=True)
    df = query(f"""
        SELECT State, ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B
        FROM aggregated_transaction WHERE Year IN ({year_filter})
        GROUP BY State ORDER BY Amount_B DESC
    """)
    if not df.empty:
        fig = px.bar(df, x="State", y="Amount_B",
                     color="Amount_B", color_continuous_scale="Purples",
                     labels={"Amount_B": "Amount (₹B)"})
        fig.update_layout(**PLOTLY_THEME, height=350,
                          xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 2 — TRANSACTIONS
# ══════════════════════════════════════════════════════════════
elif page == "📊 Transactions":
    st.markdown("<h1>Transaction Analysis</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🏦 By Type", "📍 By State"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-header'>Quarterly Trend</div>", unsafe_allow_html=True)
            df = query(f"""
                SELECT Year, Quarter,
                       SUM(Transaction_Count)  AS Count,
                       ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY Year, Quarter ORDER BY Year, Quarter
            """)
            if not df.empty:
                df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
                fig = px.line(df, x="Period", y="Amount_B",
                              markers=True, color_discrete_sequence=["#7c3aed"])
                fig.update_layout(**PLOTLY_THEME, height=320,
                                  xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>Quarter Comparison</div>", unsafe_allow_html=True)
            df = query(f"""
                SELECT Quarter, SUM(Transaction_Count) AS Count,
                       ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY Quarter
            """)
            if not df.empty:
                fig = px.bar(df, x="Quarter", y="Amount_B",
                             color="Quarter", color_discrete_sequence=PLOTLY_THEME["colorway"],
                             text_auto=".1f")
                fig.update_layout(**PLOTLY_THEME, height=320, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        # Average transaction value trend
        st.markdown("<div class='section-header'>Average Transaction Value Over Time</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Year, Quarter,
                   ROUND(SUM(Transaction_Amount)/NULLIF(SUM(Transaction_Count),0),2) AS Avg_Value
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY Year, Quarter ORDER BY Year, Quarter
        """)
        if not df.empty:
            df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
            fig = px.area(df, x="Period", y="Avg_Value",
                          color_discrete_sequence=["#a78bfa"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(124,58,237,0.15)")
            fig.update_layout(**PLOTLY_THEME, height=280, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-header'>Transaction Count by Type</div>", unsafe_allow_html=True)
            df = query(f"""
                SELECT Transaction_Type,
                       SUM(Transaction_Count) AS Count,
                       ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY Transaction_Type ORDER BY Count DESC
            """)
            if not df.empty:
                fig = px.bar(df, x="Count", y="Transaction_Type",
                             orientation="h", color="Amount_B",
                             color_continuous_scale="Purples",
                             labels={"Count":"Transaction Count","Amount_B":"Amount ₹B"})
                fig.update_layout(**PLOTLY_THEME, height=350, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>Amount Share by Type</div>", unsafe_allow_html=True)
            if not df.empty:
                fig = px.pie(df, names="Transaction_Type", values="Amount_B",
                             hole=0.5, color_discrete_sequence=PLOTLY_THEME["colorway"])
                fig.update_layout(**PLOTLY_THEME, height=350)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>Type Performance by Year</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Year, Transaction_Type,
                   SUM(Transaction_Count) AS Count
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY Year, Transaction_Type ORDER BY Year
        """)
        if not df.empty:
            fig = px.bar(df, x="Year", y="Count", color="Transaction_Type",
                         barmode="group",
                         color_discrete_sequence=PLOTLY_THEME["colorway"])
            fig.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("<div class='section-header'>Top 15 States by Transaction Amount</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT State,
                   ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
                   SUM(Transaction_Count) AS Count
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY State ORDER BY Amount_B DESC LIMIT 15
        """)
        if not df.empty:
            fig = px.bar(df, x="Amount_B", y="State", orientation="h",
                         color="Amount_B", color_continuous_scale="Purples",
                         text_auto=".1f")
            fig.update_layout(**PLOTLY_THEME, height=500,
                              yaxis=dict(autorange="reversed"),
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div class='section-header'>State Data Table</div>", unsafe_allow_html=True)
        st.dataframe(df.style.background_gradient(cmap="Purples"), use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 3 — MAP VIEW
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Map View":
    st.markdown("<h1>Geographic Distribution</h1>", unsafe_allow_html=True)

    metric = st.selectbox("Select Metric", ["Transaction Amount", "Transaction Count", "Registered Users"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Top 10 States</div>", unsafe_allow_html=True)
        if metric == "Transaction Amount":
            df = query(f"""
                SELECT State, ROUND(SUM(Transaction_Amount)/1e9,2) AS Value
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY State ORDER BY Value DESC LIMIT 10
            """)
            unit = "₹B"
        elif metric == "Transaction Count":
            df = query(f"""
                SELECT State, SUM(Transaction_Count) AS Value
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY State ORDER BY Value DESC LIMIT 10
            """)
            unit = "Transactions"
        else:
            df = query(f"""
                SELECT State, SUM(Registered_Users) AS Value
                FROM aggregated_user WHERE Year IN ({year_filter})
                GROUP BY State ORDER BY Value DESC LIMIT 10
            """)
            unit = "Users"

        if not df.empty:
            fig = px.bar(df, x="Value", y="State", orientation="h",
                         color="Value", color_continuous_scale="Purples",
                         labels={"Value": unit})
            fig.update_layout(**PLOTLY_THEME, height=400,
                              yaxis=dict(autorange="reversed"),
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Top 10 Districts</div>", unsafe_allow_html=True)
        if metric in ["Transaction Amount", "Transaction Count"]:
            df2 = query(f"""
                SELECT State, District,
                       ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
                       SUM(Transaction_Count) AS Count
                FROM map_transaction
                GROUP BY State, District ORDER BY Amount_B DESC LIMIT 10
            """)
            if not df2.empty:
                df2["Label"] = df2["District"] + ", " + df2["State"]
                fig = px.bar(df2, x="Amount_B", y="Label", orientation="h",
                             color="Amount_B", color_continuous_scale="Purples",
                             labels={"Amount_B":"Amount ₹B"})
                fig.update_layout(**PLOTLY_THEME, height=400,
                                  yaxis=dict(autorange="reversed"),
                                  coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            df2 = query("""
                SELECT State, District, SUM(Registered_Users) AS Users
                FROM map_user GROUP BY State, District
                ORDER BY Users DESC LIMIT 10
            """)
            if not df2.empty:
                df2["Label"] = df2["District"] + ", " + df2["State"]
                fig = px.bar(df2, x="Users", y="Label", orientation="h",
                             color="Users", color_continuous_scale="Purples")
                fig.update_layout(**PLOTLY_THEME, height=400,
                                  yaxis=dict(autorange="reversed"),
                                  coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

    # State treemap
    st.markdown("<div class='section-header'>State Treemap — Transaction Amount</div>", unsafe_allow_html=True)
    df3 = query(f"""
        SELECT State, ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
               SUM(Transaction_Count) AS Count
        FROM aggregated_transaction WHERE Year IN ({year_filter})
        GROUP BY State
    """)
    if not df3.empty:
        fig = px.treemap(df3, path=["State"], values="Amount_B",
                         color="Amount_B", color_continuous_scale="Purples",
                         hover_data={"Count": True})
        fig.update_layout(**PLOTLY_THEME, height=450)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 4 — USERS
# ══════════════════════════════════════════════════════════════
elif page == "👤 Users":
    st.markdown("<h1>User Analytics</h1>", unsafe_allow_html=True)

    # KPIs
    ukpi = query(f"""
        SELECT SUM(Registered_Users) AS users, SUM(App_Opens) AS opens
        FROM aggregated_user WHERE Year IN ({year_filter})
    """).iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Registered Users</div><div class='kpi-value'>{fmt_lakh(ukpi['users'])}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-title'>App Opens</div><div class='kpi-value'>{fmt_lakh(ukpi['opens'])}</div></div>", unsafe_allow_html=True)
    ratio = ukpi['opens'] / ukpi['users'] if ukpi['users'] else 0
    c3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Opens per User</div><div class='kpi-value'>{ratio:.1f}x</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>User Growth by Year</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Year, SUM(Registered_Users) AS Users, SUM(App_Opens) AS Opens
            FROM aggregated_user WHERE Year IN ({year_filter})
            GROUP BY Year ORDER BY Year
        """)
        if not df.empty:
            fig = go.Figure()
            fig.add_bar(x=df["Year"], y=df["Users"], name="Registered Users",
                        marker_color="#7c3aed")
            fig.add_scatter(x=df["Year"], y=df["Opens"], name="App Opens",
                            mode="lines+markers",
                            line=dict(color="#e879f9", width=3), yaxis="y2")
            fig.update_layout(**PLOTLY_THEME, height=320,
                              yaxis2=dict(overlaying="y", side="right"),
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Quarterly User Engagement</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Quarter, SUM(Registered_Users) AS Users
            FROM aggregated_user WHERE Year IN ({year_filter})
            GROUP BY Quarter ORDER BY Quarter
        """)
        if not df.empty:
            fig = px.bar(df, x="Quarter", y="Users",
                         color="Quarter", color_discrete_sequence=PLOTLY_THEME["colorway"],
                         text_auto=True)
            fig.update_layout(**PLOTLY_THEME, height=320, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # Top states by users
    st.markdown("<div class='section-header'>Top States by Registered Users</div>", unsafe_allow_html=True)
    df = query(f"""
        SELECT State, SUM(Registered_Users) AS Users,
               SUM(App_Opens) AS Opens
        FROM aggregated_user WHERE Year IN ({year_filter})
        GROUP BY State ORDER BY Users DESC LIMIT 15
    """)
    if not df.empty:
        fig = px.bar(df, x="State", y="Users",
                     color="Opens", color_continuous_scale="Purples",
                     labels={"Users": "Registered Users", "Opens": "App Opens"})
        fig.update_layout(**PLOTLY_THEME, height=380, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # Top districts
    st.markdown("<div class='section-header'>Top 10 Districts by Users</div>", unsafe_allow_html=True)
    df = query("""
        SELECT State, District, SUM(Registered_Users) AS Users
        FROM map_user GROUP BY State, District
        ORDER BY Users DESC LIMIT 10
    """)
    if not df.empty:
        df["Label"] = df["District"] + " (" + df["State"] + ")"
        fig = px.bar(df, x="Label", y="Users",
                     color="Users", color_continuous_scale="Purples",
                     text_auto=True)
        fig.update_layout(**PLOTLY_THEME, height=350,
                          xaxis_tickangle=-35, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 5 — TOP PERFORMERS
# ══════════════════════════════════════════════════════════════
elif page == "🏆 Top Performers":
    st.markdown("<h1>Top Performers</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏛️ States", "🌆 Districts", "📮 Pincodes"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='section-header'>Top 10 States — Transactions</div>", unsafe_allow_html=True)
            df = query(f"""
                SELECT State, ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
                       SUM(Transaction_Count) AS Count
                FROM aggregated_transaction WHERE Year IN ({year_filter})
                GROUP BY State ORDER BY Amount_B DESC LIMIT 10
            """)
            if not df.empty:
                for i, row in df.iterrows():
                    medal = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
                    st.markdown(f"""
                    <div style='display:flex; justify-content:space-between; align-items:center;
                                background:#1e1040; border:1px solid #3d2a6e; border-radius:10px;
                                padding:10px 16px; margin-bottom:6px;'>
                        <span>{medal} {row['State']}</span>
                        <span style='color:#c084fc; font-weight:700;'>₹{row['Amount_B']}B</span>
                    </div>
                    """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-header'>Top 10 States — Users</div>", unsafe_allow_html=True)
            df2 = query(f"""
                SELECT State, SUM(Registered_Users) AS Users
                FROM aggregated_user WHERE Year IN ({year_filter})
                GROUP BY State ORDER BY Users DESC LIMIT 10
            """)
            if not df2.empty:
                for i, row in df2.iterrows():
                    medal = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
                    st.markdown(f"""
                    <div style='display:flex; justify-content:space-between; align-items:center;
                                background:#1e1040; border:1px solid #3d2a6e; border-radius:10px;
                                padding:10px 16px; margin-bottom:6px;'>
                        <span>{medal} {row['State']}</span>
                        <span style='color:#a78bfa; font-weight:700;'>{row['Users']:,}</span>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-header'>Top 15 Districts by Transaction Amount</div>", unsafe_allow_html=True)
        df = query("""
            SELECT State, District,
                   ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
                   SUM(Transaction_Count) AS Count
            FROM map_transaction
            GROUP BY State, District ORDER BY Amount_B DESC LIMIT 15
        """)
        if not df.empty:
            df["District_State"] = df["District"] + ", " + df["State"]
            fig = px.bar(df, x="Amount_B", y="District_State", orientation="h",
                         color="Count", color_continuous_scale="Purples",
                         labels={"Amount_B":"Amount ₹B","Count":"Txn Count"})
            fig.update_layout(**PLOTLY_THEME, height=500,
                              yaxis=dict(autorange="reversed"),
                              coloraxis_showscale=True)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='section-header'>Top 10 Pincodes — Transactions</div>", unsafe_allow_html=True)
            df = query(f"""
                SELECT Pincode, State,
                       ROUND(SUM(Transaction_Amount)/1e9,2) AS Amount_B,
                       SUM(Transaction_Count) AS Count
                FROM top_transaction WHERE Year IN ({year_filter})
                GROUP BY Pincode, State ORDER BY Amount_B DESC LIMIT 10
            """)
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("<div class='section-header'>Top 10 Pincodes — Users</div>", unsafe_allow_html=True)
            df2 = query(f"""
                SELECT Pincode, State, SUM(Registered_Users) AS Users
                FROM top_user WHERE Year IN ({year_filter})
                GROUP BY Pincode, State ORDER BY Users DESC LIMIT 10
            """)
            if not df2.empty:
                st.dataframe(df2, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 6 — INSURANCE
# ══════════════════════════════════════════════════════════════
elif page == "🛡️ Insurance":
    st.markdown("<h1>Insurance Analytics</h1>", unsafe_allow_html=True)

    # KPIs
    ikpi = query(f"""
        SELECT SUM(Insurance_Count) AS cnt,
               ROUND(SUM(Insurance_Amount)/1e9,2) AS amt
        FROM aggregated_insurance WHERE Year IN ({year_filter})
    """).iloc[0]

    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Policies</div><div class='kpi-value'>{ikpi['cnt']:,}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Premium Value</div><div class='kpi-value'>₹{ikpi['amt']}B</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Insurance Growth by Year</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT Year, SUM(Insurance_Count) AS Policies,
                   ROUND(SUM(Insurance_Amount)/1e9,2) AS Amount_B
            FROM aggregated_insurance WHERE Year IN ({year_filter})
            GROUP BY Year ORDER BY Year
        """)
        if not df.empty:
            fig = go.Figure()
            fig.add_bar(x=df["Year"], y=df["Policies"], name="Policies",
                        marker_color="#7c3aed")
            fig.add_scatter(x=df["Year"], y=df["Amount_B"], name="Amount ₹B",
                            mode="lines+markers",
                            line=dict(color="#34d399", width=3), yaxis="y2")
            fig.update_layout(**PLOTLY_THEME, height=320,
                              yaxis2=dict(overlaying="y", side="right"),
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Top 10 States by Insurance</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT State, ROUND(SUM(Insurance_Amount)/1e9,2) AS Amount_B
            FROM aggregated_insurance WHERE Year IN ({year_filter})
            GROUP BY State ORDER BY Amount_B DESC LIMIT 10
        """)
        if not df.empty:
            fig = px.bar(df, x="State", y="Amount_B",
                         color="Amount_B", color_continuous_scale="Greens",
                         text_auto=".1f")
            fig.update_layout(**PLOTLY_THEME, height=320,
                              xaxis_tickangle=-35, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    # Insurance penetration
    st.markdown("<div class='section-header'>Insurance Penetration Rate by State</div>", unsafe_allow_html=True)
    df = query(f"""
        SELECT i.State,
               ROUND(SUM(i.Insurance_Count)*100.0/NULLIF(SUM(t.Transaction_Count),0),4) AS Penetration_Pct
        FROM aggregated_insurance i
        JOIN aggregated_transaction t
            ON i.State=t.State AND i.Year=t.Year AND i.Quarter=t.Quarter
        WHERE i.Year IN ({year_filter})
        GROUP BY i.State ORDER BY Penetration_Pct DESC
    """)
    if not df.empty:
        fig = px.bar(df, x="State", y="Penetration_Pct",
                     color="Penetration_Pct", color_continuous_scale="Teal",
                     labels={"Penetration_Pct": "Penetration %"}, text_auto=".3f")
        fig.update_layout(**PLOTLY_THEME, height=380,
                          xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # Top districts
    st.markdown("<div class='section-header'>Top 10 Districts by Insurance Amount</div>", unsafe_allow_html=True)
    df = query("""
        SELECT State, District,
               ROUND(SUM(Insurance_Amount)/1e9,2) AS Amount_B,
               SUM(Insurance_Count) AS Policies
        FROM map_insurance GROUP BY State, District
        ORDER BY Amount_B DESC LIMIT 10
    """)
    if not df.empty:
        df["Label"] = df["District"] + " (" + df["State"] + ")"
        fig = px.bar(df, x="Amount_B", y="Label", orientation="h",
                     color="Policies", color_continuous_scale="Greens",
                     text_auto=".1f")
        fig.update_layout(**PLOTLY_THEME, height=380,
                          yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 7 — BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "🔍 Business Insights":
    st.markdown("<h1>Business Case Insights</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Segmentation", "⚠️ Fraud Proxy",
        "📈 Growth Rate", "🎯 Opportunities"
    ])

    with tab1:
        st.markdown("<div class='section-header'>Customer Segmentation by Avg Transaction Value</div>", unsafe_allow_html=True)
        df = query(f"""
            SELECT State,
                   ROUND(SUM(Transaction_Amount)/NULLIF(SUM(Transaction_Count),0),2) AS Avg_Value,
                   SUM(Transaction_Count) AS Total_Txns,
                   CASE
                       WHEN SUM(Transaction_Amount)/NULLIF(SUM(Transaction_Count),0) > 5000 THEN 'High Value'
                       WHEN SUM(Transaction_Amount)/NULLIF(SUM(Transaction_Count),0) > 1000 THEN 'Mid Value'
                       ELSE 'Low Value'
                   END AS Segment
            FROM aggregated_transaction WHERE Year IN ({year_filter})
            GROUP BY State ORDER BY Avg_Value DESC
        """)
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.scatter(df, x="Total_Txns", y="Avg_Value",
                                 color="Segment", size="Total_Txns",
                                 hover_name="State", text="State",
                                 color_discrete_map={
                                     "High Value": "#c084fc",
                                     "Mid Value":  "#7c3aed",
                                     "Low Value":  "#4a2d8a"
                                 })
                fig.update_layout(**PLOTLY_THEME, height=420)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                seg_counts = df["Segment"].value_counts().reset_index()
                seg_counts.columns = ["Segment","Count"]
                fig2 = px.pie(seg_counts, names="Segment", values="Count",
                              hole=0.5, color_discrete_sequence=["#c084fc","#7c3aed","#4a2d8a"])
                fig2.update_layout(**PLOTLY_THEME, height=420)
                st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(df.style.background_gradient(subset=["Avg_Value"], cmap="Purples"),
                         use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("<div class='section-header'>Fraud Detection Proxy — Abnormal Transaction Values</div>", unsafe_allow_html=True)
        st.caption("States/quarters where avg transaction value is 3× the overall average — potential anomaly signals.")
        df = query(f"""
            SELECT State, Year, Quarter, Transaction_Type,
                   ROUND(Transaction_Amount/NULLIF(Transaction_Count,0),2) AS Avg_Txn_Value
            FROM aggregated_transaction
            WHERE Year IN ({year_filter})
              AND (Transaction_Amount/NULLIF(Transaction_Count,0)) >
                  (SELECT AVG(Transaction_Amount/NULLIF(Transaction_Count,0))*3
                   FROM aggregated_transaction)
            ORDER BY Avg_Txn_Value DESC LIMIT 20
        """)
        if df.empty:
            st.success("✅ No anomalous transactions detected in selected years.")
        else:
            fig = px.bar(df, x="State", y="Avg_Txn_Value",
                         color="Transaction_Type",
                         barmode="group",
                         color_discrete_sequence=PLOTLY_THEME["colorway"])
            fig.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("<div class='section-header'>Payment Type Growth Rate</div>", unsafe_allow_html=True)
        df = query("""
            SELECT Transaction_Type,
                   SUM(CASE WHEN Year=(SELECT MIN(Year) FROM aggregated_transaction)
                       THEN Transaction_Count ELSE 0 END) AS First_Year,
                   SUM(CASE WHEN Year=(SELECT MAX(Year) FROM aggregated_transaction)
                       THEN Transaction_Count ELSE 0 END) AS Last_Year,
                   ROUND(
                       (SUM(CASE WHEN Year=(SELECT MAX(Year) FROM aggregated_transaction)
                            THEN Transaction_Count ELSE 0 END) -
                        SUM(CASE WHEN Year=(SELECT MIN(Year) FROM aggregated_transaction)
                            THEN Transaction_Count ELSE 0 END))
                       * 100.0 /
                       NULLIF(SUM(CASE WHEN Year=(SELECT MIN(Year) FROM aggregated_transaction)
                            THEN Transaction_Count ELSE 0 END),0)
                   ,2) AS Growth_Pct
            FROM aggregated_transaction
            GROUP BY Transaction_Type ORDER BY Growth_Pct DESC
        """)
        if not df.empty:
            fig = px.bar(df, x="Transaction_Type", y="Growth_Pct",
                         color="Growth_Pct",
                         color_continuous_scale="RdYlGn",
                         text_auto=".1f",
                         labels={"Growth_Pct": "Growth %"})
            fig.update_layout(**PLOTLY_THEME, height=380, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("<div class='section-header'>Opportunity Markets — Bottom 10 States</div>", unsafe_allow_html=True)
        st.caption("Low transaction volume states with growth potential for targeted marketing.")
        df = query(f"""
            SELECT t.State,
                   SUM(t.Transaction_Count) AS Transactions,
                   ROUND(SUM(t.Transaction_Amount)/1e6,2) AS Amount_M,
                   SUM(u.Registered_Users) AS Users
            FROM aggregated_transaction t
            LEFT JOIN aggregated_user u
                ON t.State=u.State AND t.Year=u.Year AND t.Quarter=u.Quarter
            WHERE t.Year IN ({year_filter})
            GROUP BY t.State ORDER BY Transactions ASC LIMIT 10
        """)
        if not df.empty:
            fig = px.scatter(df, x="Users", y="Transactions",
                             size="Amount_M", color="Amount_M",
                             hover_name="State", text="State",
                             color_continuous_scale="Purples",
                             labels={"Amount_M":"Amount ₹M"})
            fig.update_traces(textposition="top center")
            fig.update_layout(**PLOTLY_THEME, height=420)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
