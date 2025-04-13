# canadian_gov_bond_dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from rateslib.curves import Curve
from rateslib.instruments import FixedRateBond
from datetime import date

st.set_page_config(page_title="Canadian Government Bonds Market Dashboard", layout="wide")
st.title("🇨🇦 Canadian Government Bonds Market Dashboard")
st.markdown("""
This dashboard provides a Bloomberg-style fixed income interface for Canadian Government Bonds.  
It uses `rateslib` to model and analyze government yield curves and bond valuations.
""")

# --- Sample Bond Market Data (can be replaced with live data)
st.sidebar.header("Upload Your Bond Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload CSV with bond data", type=["csv"])

if uploaded_file:
    bond_data = pd.read_csv(uploaded_file)
else:
    # Sample Canada Gov Bond Data (Maturities & Yields)
    bond_data = pd.DataFrame({
        "Maturity (Years)": [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30],
        "Yield": [0.045, 0.046, 0.047, 0.0485, 0.049, 0.05, 0.051, 0.052, 0.053, 0.054]
    })

# --- Plot Yield Curve
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=bond_data["Maturity (Years)"],
    y=bond_data["Yield"] * 100,
    mode="lines+markers",
    line=dict(color="dodgerblue", width=3),
    marker=dict(size=8),
    name="Yield Curve"
))
fig.update_layout(
    title="📉 Canadian Yield Curve",
    xaxis_title="Maturity (Years)",
    yaxis_title="Yield (%)",
    template="plotly_white",
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# --- Build Discount Curve
curve = Curve(
    nodes=bond_data["Maturity (Years)"].tolist(),
    values=bond_data["Yield"].tolist(),
    convention="annual",  # assume annual compounding
    id="CAD"
)

# --- Bond Pricing Section
st.markdown("### 💵 Price a Canadian Government Bond")
col1, col2, col3 = st.columns(3)

with col1:
    coupon = st.number_input("Annual Coupon Rate (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1) / 100

with col2:
    maturity_years = st.number_input("Maturity (Years)", min_value=0.5, max_value=30.0, value=5.0, step=0.5)

with col3:
    frequency = st.selectbox("Coupon Frequency", ["annual", "semi-annual", "quarterly"])

# --- Price the bond using rateslib
bond = FixedRateBond(
    effective=date.today(),
    termination=date.today().replace(year=date.today().year + int(maturity_years)),
    coupon=coupon,
    frequency=frequency,
    curves={"disc": curve}
)
price = bond.npv()

st.metric(label="📌 Estimated Bond Price", value=f"${price:.2f}")

# --- Footer
st.markdown("---")
st.markdown("📈 Built with `rateslib`, `Plotly`, and `Streamlit` | Author: Bebongnchu")


