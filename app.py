import streamlit as st
import joblib
import pandas as pd

# لود مدل
@st.cache_resource
def load_model():
    model = joblib.load("linear_model.pkl")
    columns = joblib.load("columns.pkl")
    return model, columns

model, columns = load_model()

# عنوان
st.title("🏠 پیش‌بینی قیمت آپارتمان مشهد")
st.markdown("---")

# ورودی کاربر
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("📐 متراژ", min_value=10, max_value=500, value=80)
    floor = st.number_input("🏢 طبقه", min_value=0, max_value=30, value=3)

with col2:
    elevator = st.checkbox("🛗 آسانسور", value=True)
    parking = st.checkbox("🅿️ پارکینگ", value=True)
    warehouse = st.checkbox("📦 انباری", value=True)

# مناطق
neighborhoods = [c.replace("neighborhood_", "") for c in columns if c.startswith("neighborhood_")]
neighborhood = st.selectbox("📍 منطقه", neighborhoods)

# پیش‌بینی
if st.button("💰 پیش‌بینی قیمت", type="primary"):
    input_data = pd.DataFrame(0, index=[0], columns=columns)
    input_data["area"] = area
    input_data["floor"] = floor
    input_data["has_elevator"] = int(elevator)
    input_data["has_parking"] = int(parking)
    input_data["has_warehouse"] = int(warehouse)
    
    col_name = f"neighborhood_{neighborhood}"
    if col_name in input_data.columns:
        input_data[col_name] = 1
    
    prediction = model.predict(input_data)[0]
    st.success(f"💰 قیمت پیش‌بینی: **{prediction:,.0f} تومان**")
    st.info(f"≈ **{prediction/1e9:.2f} میلیارد تومان**")
