import streamlit as st
import pandas as pd

from ui.layout import prime_layout
from core.api import list_leads, create_lead, update_lead

prime_layout(title="👥 Leads")

# ----------------------------
# Helpers
# ----------------------------
def refresh():
    st.session_state["leads_refresh"] = st.session_state.get("leads_refresh", 0) + 1


def safe_str(x):
    return "" if x is None else str(x)


# ----------------------------
# Top actions
# ----------------------------
col_a, col_b, col_c = st.columns([1, 1, 2])

with col_a:
    st.button("🔄 Refresh", on_click=refresh, use_container_width=True)

with col_b:
    show_inactive = st.toggle("Inactive göster", value=False)

with col_c:
    search = st.text_input("Ara (firma / kişi / email)", placeholder="Firma, İsim, info@...")

st.divider()

# ----------------------------
# Create Lead (compact form)
# ----------------------------
with st.expander("➕ Yeni Lead Ekle", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        company_name = st.text_input("Firma Adı*", key="new_company")
        source = st.text_input("Kaynak", key="new_source", placeholder="LinkedIn / Referral / Web / ...")
    with c2:
        contact_name = st.text_input("İlgili Kişi*", key="new_contact")
        title = st.text_input("Unvan", key="new_title")
    with c3:
        email = st.text_input("Email*", key="new_email")
        phone = st.text_input("Telefon", key="new_phone", placeholder="+90... veya 05xx...")

    notes = st.text_area("Not", key="new_notes", height=80)

    btn_col1, btn_col2 = st.columns([1, 3])
    with btn_col1:
        if st.button("Kaydet", type="primary", use_container_width=True):
            if not company_name.strip() or not contact_name.strip() or not email.strip():
                st.error("Firma Adı, İlgili Kişi ve Email zorunludur.")
            else:
                payload = {
                    "company_name": company_name.strip(),
                    "contact_name": contact_name.strip(),
                    "email": email.strip(),
                    "title": title.strip() or None,
                    "source": source.strip() or None,
                    "phone": phone.strip() or None,
                    "notes": notes.strip() or None,
                    "is_active": True,
                }
                try:
                    create_lead(payload)
                    st.success("Lead oluşturuldu.")
                    refresh()
                except Exception as e:
                    st.error(f"Lead oluşturulamadı: {e}")

st.divider()

# ----------------------------
# Load data
# ----------------------------
_ = st.session_state.get("leads_refresh", 0)  # dependency trigger

try:
    leads = list_leads()
except Exception as e:
    st.error(f"API'den lead verisi alınamadı: {e}")
    st.stop()

# Client-side filters (aktif/pasif + arama)
filtered = []
for l in leads:
    active = bool(l.get("is_active", True))
    if not show_inactive and not active:
        continue

    hay = " ".join(
        [
            safe_str(l.get("company_name")),
            safe_str(l.get("contact_name")),
            safe_str(l.get("email")),
            safe_str(l.get("title")),
            safe_str(l.get("source")),
        ]
    ).lower()

    if search and search.lower() not in hay:
        continue

    filtered.append(l)

if not filtered:
    st.info("Kayıt bulunamadı.")
    st.stop()

df = pd.DataFrame(filtered)

# Make columns nice
preferred_cols = [
    "id",
    "company_name",
    "contact_name",
    "email",
    "title",
    "source",
    "phone",
    "is_active",
    "created_at",
]
cols = [c for c in preferred_cols if c in df.columns] + [c for c in df.columns if c not in preferred_cols]
df = df[cols]

st.caption(f"Toplam kayıt: {len(df)}")

st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ----------------------------
# Edit panel
# ----------------------------
st.markdown("### ✏️ Düzenle")

ids = df["id"].tolist()
selected_id = st.selectbox("Lead seç", options=ids, format_func=lambda x: f"#{x}", key="lead_select")

selected = next((x for x in filtered if x.get("id") == selected_id), None)
if not selected:
    st.warning("Seçilen kayıt bulunamadı.")
    st.stop()

e1, e2, e3 = st.columns(3)
with e1:
    e_company = st.text_input("Firma Adı", value=safe_str(selected.get("company_name")), key="edit_company")
    e_source = st.text_input("Kaynak", value=safe_str(selected.get("source")), key="edit_source")
with e2:
    e_contact = st.text_input("İlgili Kişi", value=safe_str(selected.get("contact_name")), key="edit_contact")
    e_title = st.text_input("Unvan", value=safe_str(selected.get("title")), key="edit_title")
with e3:
    e_email = st.text_input("Email", value=safe_str(selected.get("email")), key="edit_email")
    e_phone = st.text_input("Telefon", value=safe_str(selected.get("phone")), key="edit_phone")

e_notes = st.text_area("Not", value=safe_str(selected.get("notes")), height=90, key="edit_notes")
e_active = st.toggle("Aktif", value=bool(selected.get("is_active", True)), key="edit_active")

btn1, btn2, btn3 = st.columns([1, 1, 3])
with btn1:
    if st.button("💾 Güncelle", type="primary", use_container_width=True):
        payload = {
            "company_name": e_company.strip() or None,
            "contact_name": e_contact.strip() or None,
            "email": e_email.strip() or None,
            "title": e_title.strip() or None,
            "source": e_source.strip() or None,
            "phone": e_phone.strip() or None,
            "notes": e_notes.strip() or None,
            "is_active": bool(e_active),
        }
        # Do not send None for required fields accidentally; backend should validate too.
        try:
            update_lead(selected_id, payload)
            st.success("Güncellendi.")
            refresh()
        except Exception as e:
            st.error(f"Güncellenemedi: {e}")

with btn2:
    if st.button("🧊 Pasife al", use_container_width=True):
        try:
            update_lead(selected_id, {"is_active": False})
            st.success("Pasife alındı.")
            refresh()
        except Exception as e:
            st.error(f"Pasife alınamadı: {e}")
