import streamlit as st
from ui.layout import prime_layout
from core import api

prime_layout(title="🏠 Dashboard")

st.markdown("### Hoş geldin 👋")
st.info("Bu sayfa v1'de özet gösterecek. (Lead sayısı, aktif deal'lar, bu haftaki activity vb.)")

api.health("api ok")