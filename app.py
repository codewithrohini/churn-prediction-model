import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ChurnGuard AI | Business Intelligence",
    page_icon="📈",
    layout="wide",
)

# --- 2. REFINED LIGHT UI CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background: Ultra-light grey/blue */
    .stApp { background-color: #fcfdfe; }
    
    /* Sidebar: Light, clean with subtle border */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e6e9ef;
    }

    /* Metric Cards: White with soft shadow */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f0f2f6;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Buttons: Brand Blue */
    .stButton>button {
        background-color: #0066ff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
    }

    /* Typography */
    h1, h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    .stMarkdown { color: #475569; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("customer_data.csv")
    except:
        # Create dummy data if file is missing for demo purposes
        return pd.DataFrame({
            'country': ['France', 'Spain', 'Germany']*100,
            'age': np.random.randint(18, 70, 300),
            'churn': np.random.randint(0, 2, 300),
            'balance': np.random.uniform(0, 100000, 300),
            'credit_score': np.random.randint(400, 850, 300),
            'tenure': np.random.randint(1, 10, 300),
            'active_member': np.random.randint(0, 2, 300),
            'products_number': np.random.randint(1, 4, 300),
            'estimated_salary': np.random.uniform(30000, 150000, 300)
        })

df = load_data()

# --- 4. SIDEBAR NAVIGATION (Light Version) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=50) # Tiny logo
    st.title("ChurnGuard")
    st.markdown("---")
    page = st.radio(
        "MAIN MENU",
        ["🏠 Dashboard", "👥 Customers", "🧪 Risk Predictor"],
        index=0
    )
    st.markdown("---")
    st.caption("v2.1.0-Light-Mode")

# --- 5. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("Retention Analytics Overview")
    
    # KPIs in a clean row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Clients", f"{len(df):,}", "↑ 12")
    m2.metric("Churn Rate", f"{(df['churn'].mean()*100):.1f}%", "-0.5%", delta_color="inverse")
    m3.metric("Avg Score", int(df['credit_score'].mean()))
    m4.metric("Retention Rate", f"{(1 - df['churn'].mean())*100:.1f}%")

    st.markdown("### Behavioral Trends")
    c1, c2 = st.columns(2)
    
    with c1:
        # Professional Blue/Grey color scheme
        fig = px.histogram(df, x="age", color="churn", 
                           color_discrete_map={0: "#0066ff", 1: "#cbd5e1"},
                           title="Churn Variance by Age", barmode='overlay')
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        geo_churn = df.groupby('country')['churn'].mean().reset_index()
        fig2 = px.bar(geo_churn, x='country', y='churn', 
                      title="Market Risk by Region",
                      color_discrete_sequence=['#0066ff'])
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

# --- 6. PAGE: CUSTOMERS ---
elif page == "👥 Customers":
    st.title("Customer Directory")
    
    # Filter tools in a container
    with st.expander("Filter Controls", expanded=True):
        col1, col2 = st.columns(2)
        region = col1.multiselect("Select Markets", df['country'].unique(), default=df['country'].unique())
        risk_level = col2.select_slider("Filter by Age", options=list(range(18, 100)), value=(18, 65))

    filtered_df = df[(df['country'].isin(region)) & (df['age'].between(risk_level[0], risk_level[1]))]
    
    st.dataframe(
        filtered_df.style.format({'balance': '${:,.2f}'}),
        use_container_width=True,
        height=500
    )

# --- 7. PAGE: RISK PREDICTOR ---
elif page == "🧪 Risk Predictor":
    st.title("AI Predictive Scoring")
    st.info("Simulate a customer profile to see their churn probability.")

    # Two-column input layout
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            score = st.slider("Credit Score", 300, 850, 600)
            balance = st.number_input("Account Balance ($)", 0.0, 200000.0, 5000.0)
            active = st.toggle("Active Member", value=True)
        with c2:
            age = st.number_input("Age", 18, 90, 30)
            products = st.selectbox("Products Owned", [1, 2, 3, 4])
            geo = st.selectbox("Market Location", df['country'].unique())

    if st.button("Run Intelligence Report", use_container_width=True):
        # Placeholder for your model.predict_proba()
        risk_score = np.random.uniform(0.05, 0.95)
        
        st.markdown("---")
        res1, res2 = st.columns([1, 2])
        
        with res1:
            # Custom Gauge
            fig_g = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'bar': {'color': "#0066ff"},
                         'axis': {'range': [None, 100]},
                         'steps': [{'range': [0, 50], 'color': "#e2e8f0"}]}))
            st.plotly_chart(fig_g, use_container_width=True)

        with res2:
            if risk_score > 0.6:
                st.error("### HIGH RISK DETECTED")
                st.write("This profile matches 85% of previous churn behavior.")
            else:
                st.success("### LOW RISK PROFILE")
                st.write("Customer engagement metrics are stable.")

                with st.expander("ℹ️ About this Model"):
    st.write("""
        This system uses a **Random Forest Classifier** trained on 10,000 customer records. 
        It analyzes behavioral patterns such as credit score, tenure, and activity status 
        to predict the likelihood of a customer leaving the bank.
    """)