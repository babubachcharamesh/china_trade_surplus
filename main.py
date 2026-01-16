import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression
from streamlit_option_menu import option_menu
import altair as alt
from streamlit_echarts import st_echarts
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# ───────────────────────────────────────────────
# Page Configuration & Custom Styling
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="China Trade Dashboard 1950–2025",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    :root {
        --primary: #FF4B4B;
        --bg: #0E1117;
        --bg-secondary: #161B22;
        --text: #FAFAFA;
        --accent: #00FFFF;
        --glow: rgba(0, 255, 255, 0.5);
    }
    .stApp {
        background: linear-gradient(135deg, var(--bg), #1F2937);
        color: var(--text);
    }
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    h1, h2, h3 {
        color: var(--accent);
        text-shadow: 0 0 10px var(--glow);
        animation: glow 2s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 5px var(--glow); }
        to   { text-shadow: 0 0 15px var(--glow); }
    }
    .stButton > button {
        background: linear-gradient(45deg, var(--primary), #FF6B6B);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 1.4rem;
        box-shadow: 0 0 12px var(--glow);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px var(--glow);
    }
    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# Data
# ───────────────────────────────────────────────
data = {
    'Year': list(range(1950, 2026)),
    'Exports': [None]*10 + [1.88,1.51,1.51,1.67,1.94,2.25,2.37,2.16,2.11,2.21,2.27,2.71,3.54,5.96,7.21,7.97,7.44,8.27,10.80,13.96,19.41,24.37,22.60,21.96,24.76,25.80,26.20,34.07,44.92,41.19,49.13,55.54,66.85,74.28,104.61,131.86,154.81,187.45,188.75,198.70,253.09,272.06,333.00,447.96,607.36,773.34,991.73,1258.00,1498.00,1263.00,1655.00,2006.00,2175.00,2354.00,2463.00,2362.00,2200.00,2424.00,2656.00,2629.00,2730.00,3554.00,3718.00,3513.00,3573.00,3770.00],
    'Imports': [None]*10 + [1.89,1.41,1.13,1.21,1.48,1.92,2.19,1.92,1.85,1.73,2.20,2.23,2.92,5.26,7.72,8.36,7.35,8.06,12.26,15.54,21.84,22.22,17.79,19.39,24.71,38.30,33.59,33.78,48.98,46.12,38.46,43.94,61.85,86.07,97.25,119.90,137.26,144.62,144.91,168.06,224.31,243.97,295.62,412.14,556.18,648.71,782.81,950.02,1149.00,1043.00,1432.00,1825.00,1943.00,2119.00,2241.00,2003.00,1944.00,2209.00,2564.00,2496.00,2375.00,3093.00,3140.00,3127.00,2581.00,2580.00],
    'Trade Balance': [None]*10 + [-0.01,0.10,0.38,0.46,0.46,0.33,0.18,0.24,0.26,0.48,0.07,0.48,0.62,0.70,-0.51,-0.39,0.09,0.21,-1.46,-1.58,-2.43,2.15,4.81,2.57,0.05,-12.50,-7.39,0.29,-4.06,-4.93,10.67,11.60,5.00,-11.79,7.36,11.96,17.55,42.83,43.84,30.64,28.78,28.09,37.38,35.82,51.18,124.63,208.92,307.98,349.00,220.00,223.00,181.00,232.00,235.00,222.00,359.00,256.00,215.00,92.00,133.00,355.00,461.00,578.00,386.00,992.00,1190.00]
}

df = pd.DataFrame(data).dropna()
df['Year'] = df['Year'].astype(int)

# ───────────────────────────────────────────────
# Global Key Statistics (used in multiple tabs & PDF)
# ───────────────────────────────────────────────
max_surplus = df['Trade Balance'].max()
max_surplus_year = int(df.loc[df['Trade Balance'].idxmax(), 'Year'])
max_exports = df['Exports'].max()
max_exports_year = int(df.loc[df['Exports'].idxmax(), 'Year'])
max_imports = df['Imports'].max()
max_imports_year = int(df.loc[df['Imports'].idxmax(), 'Year'])
avg_positive_surplus = df[df['Trade Balance'] > 0]['Trade Balance'].mean() if (df['Trade Balance'] > 0).any() else 0

# ───────────────────────────────────────────────
# Sidebar Navigation
# ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg", width=90)
    st.title("China Trade Explorer")
    selected = option_menu(
        None,
        ["Dashboard", "Interactive Charts", "Forecasting", "Insights", "Data Export"],
        icons=["house", "graph-up", "robot", "lightbulb", "download"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#161B22"},
            "icon": {"color": "#00FFFF", "font-size": "22px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px 0px"},
            "nav-link-selected": {"background-color": "#FF4B4B"},
        }
    )

# ───────────────────────────────────────────────
# PAGES
# ───────────────────────────────────────────────
if selected == "Dashboard":
    st.title("🌟 China Trade Surplus/Deficit Dashboard 1950–2025")
    st.caption("Values in Billions USD")

    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Surplus", f"${max_surplus:,.2f}B", f"Year: {max_surplus_year}")
    col2.metric("Highest Exports", f"${max_exports:,.2f}B", f"Year: {max_exports_year}")
    col3.metric("Avg Positive Surplus", f"${avg_positive_surplus:,.2f}B")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Exports'], name="Exports", line=dict(color="#00FF9D", width=3)), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Imports'], name="Imports", line=dict(color="#FF6B6B", width=3)), secondary_y=False)
    fig.add_trace(go.Bar(x=df['Year'], y=df['Trade Balance'], name="Balance", marker_color=np.where(df['Trade Balance']>=0, '#00FFFF', '#FF6B6B'), opacity=0.65), secondary_y=True)

    fig.update_layout(
        title="Trade Evolution Over Time", height=550,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e0e0", hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("3D Trade Relationship Explorer"):
        fig3d = px.scatter_3d(df, x='Exports', y='Imports', z='Trade Balance', color='Year',
                              size='Exports', hover_name='Year', color_continuous_scale='Plasma_r')
        fig3d.update_layout(scene=dict(bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3d, use_container_width=True)

elif selected == "Interactive Charts":
    st.title("🔍 Interactive Visualizations")

    min_y, max_y = st.slider("Year Range", int(df['Year'].min()), int(df['Year'].max()), (1960, 2025))
    filtered = df[(df['Year'] >= min_y) & (df['Year'] <= max_y)]

    metrics = st.multiselect("Metrics", ['Exports','Imports','Trade Balance'], default=['Exports','Imports','Trade Balance'])

    base = alt.Chart(filtered).encode(x='Year:Q').interactive()
    layers = []
    if 'Exports' in metrics: layers.append(base.mark_line(color='#00FF9D').encode(y='Exports:Q'))
    if 'Imports' in metrics: layers.append(base.mark_line(color='#FF6B6B').encode(y='Imports:Q'))
    if 'Trade Balance' in metrics: layers.append(base.mark_bar(color='#00FFFF', opacity=0.7).encode(y='Trade Balance:Q'))

    st.altair_chart(alt.layer(*layers).resolve_scale(y='independent'), use_container_width=True)

elif selected == "Forecasting":
    st.title("🤖 Linear Regression Trade Forecast")

    years_ahead = st.slider("Forecast years ahead", 1, 15, 5)

    X = df['Year'].values.reshape(-1, 1)
    future_X = np.array(range(int(df['Year'].max())+1, int(df['Year'].max())+1+years_ahead)).reshape(-1, 1)

    def forecast(series):
        model = LinearRegression().fit(X, series)
        return model.predict(future_X)

    with st.spinner("Calculating forecast..."):
        fut_exp = forecast(df['Exports'])
        fut_imp = forecast(df['Imports'])
        fut_bal = fut_exp - fut_imp

        future_df = pd.DataFrame({
            'Year': range(int(df['Year'].max())+1, int(df['Year'].max())+1+years_ahead),
            'Exports': fut_exp,
            'Imports': fut_imp,
            'Trade Balance': fut_bal
        })

    st.dataframe(future_df.style.format("{:,.2f}").background_gradient(cmap='viridis'), use_container_width=True)

    opt = {
        "title": {"text": f"Forecast {years_ahead} Years Ahead", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Exports", "Imports", "Balance"], "textStyle": {"color": "white"}},
        "xAxis": {"type": "category", "data": future_df['Year'].astype(str).tolist()},
        "yAxis": {"type": "value"},
        "series": [
            {"name": "Exports", "type": "line", "data": future_df['Exports'].tolist(), "itemStyle": {"color": "#00FF9D"}},
            {"name": "Imports", "type": "line", "data": future_df['Imports'].tolist(), "itemStyle": {"color": "#FF6B6B"}},
            {"name": "Balance", "type": "bar", "data": future_df['Trade Balance'].tolist(), "itemStyle": {"color": "#00FFFF"}}
        ],
        "backgroundColor": "transparent"
    }
    st_echarts(options=opt, height=500)

elif selected == "Insights":
    st.title("💡 Key Insights")

    st.metric("Average Surplus (positive years)", f"${avg_positive_surplus:,.2f}B")
    st.markdown(f"**Years with deficit:** {len(df[df['Trade Balance'] < 0])}")
    st.markdown(f"**Strongest surplus growth period:** 2000–2025")

    # Simple sankey
    sankey_opt = {
        "series": [{
            "type": "sankey",
            "data": [{"name": "Exports"}, {"name": "Imports"}, {"name": "Surplus"}, {"name": "Deficit"}],
            "links": [
                {"source": "Exports", "target": "Surplus", "value": df[df['Trade Balance']>0]['Trade Balance'].sum()},
                {"source": "Imports", "target": "Deficit", "value": abs(df[df['Trade Balance']<0]['Trade Balance'].sum())}
            ],
            "lineStyle": {"color": "gradient"}
        }],
        "backgroundColor": "transparent"
    }
    st_echarts(sankey_opt, height=400)

elif selected == "Data Export":
    st.title("📥 Export & Reports")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("CSV Download", df.to_csv(index=False).encode('utf-8'), "china_trade_1950_2025.csv", "text/csv")
    with col2:
        st.download_button("JSON Download", df.to_json(orient='records'), "china_trade_1950_2025.json", "application/json")

    st.divider()

    if st.button("Generate & Download PDF Report", type="primary"):
        with st.spinner("Creating PDF..."):
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            
            c.setFont("Helvetica-Bold", 18)
            c.drawString(100, 750, "China Trade Report 1950–2025")
            
            c.setFont("Helvetica", 12)
            y = 700
            c.drawString(100, y, "From near-zero trade in 1960s to historic surpluses")
            y -= 20
            c.drawString(100, y, "exceeding 1 trillion USD in recent years.")
            y -= 50

            c.setFont("Helvetica-Bold", 13)
            c.drawString(100, y, "Key Figures:")
            y -= 25
            c.setFont("Helvetica", 12)
            c.drawString(120, y, f"• Highest Surplus: ${max_surplus:,.2f}B  ({max_surplus_year})")
            y -= 22
            c.drawString(120, y, f"• Highest Exports: ${max_exports:,.2f}B  ({max_exports_year})")
            y -= 22
            c.drawString(120, y, f"• Average Positive Surplus: ${avg_positive_surplus:,.2f}B")
            y -= 50

            c.drawString(100, y, "Data: Historical records & official statistics")
            c.showPage()
            c.save()

            buffer.seek(0)

            st.download_button(
                "⬇️ Download PDF Report",
                data=buffer,
                file_name="China_Trade_Report_1950-2025.pdf",
                mime="application/pdf"
            )
            st.success("PDF ready! Click above to download.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Data: historical records • © 2026")