import streamlit as st
import pandas as pd

from ui.layout import prime_layout
from core.api import list_leads, create_lead, update_lead

prime_layout(title="👥 Leads")

# ----------------------------
# UI: Dialog size (Streamlit 1.41 supports st.dialog)
# ----------------------------
st.markdown(
    """
    <style>
    /* Dialog'u genişlet */
    div[role="dialog"] {
        width: 92vw !important;
        max-width: 1200px !important;
    }
    div[role="dialog"] > div {
        padding: 1.5rem 2rem !important;
    }

    /* Firma link butonu gibi görünmesin */
    button[data-testid="baseButton-secondary"] {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Modal state
# ----------------------------
if "lead_modal_open" not in st.session_state:
    st.session_state["lead_modal_open"] = False
if "lead_modal_id" not in st.session_state:
    st.session_state["lead_modal_id"] = None
if "leads_refresh" not in st.session_state:
    st.session_state["leads_refresh"] = 0


def open_lead_modal(lead_id: int):
    st.session_state["lead_modal_open"] = True
    st.session_state["lead_modal_id"] = lead_id


def close_lead_modal():
    st.session_state["lead_modal_open"] = False
    st.session_state["lead_modal_id"] = None


def refresh():
    st.session_state["leads_refresh"] += 1


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
    search = st.text_input("Search (Company / Contact / Email)", placeholder="Company, Contact, info@...")

st.divider()

# ----------------------------
# Create Lead (compact form)
# ----------------------------
with st.expander("➕ Add New Lead", expanded=False):
    c1, c2, c3 = st.columns(3)

    with c1:
        company_name = st.text_input("Company Name*", key="new_company")
        source = st.text_input("Source", key="new_source", placeholder="LinkedIn / Referral / Web / ...")

    with c2:
        contact_name = st.text_input("Contact Person*", key="new_contact")
        title = st.text_input("Title", key="new_title")

    with c3:
        email = st.text_input("Email*", key="new_email")
        phone = st.text_input("Phone", key="new_phone", placeholder="+90... veya 05xx...")

    notes = st.text_area("Not", key="new_notes", height=80)

    btn_col1, btn_col2 = st.columns([1, 3])
    with btn_col1:
        if st.button("Save", type="primary", use_container_width=True):
            if not company_name.strip() or not contact_name.strip() or not email.strip():
                st.error("Company Name, Contact Person and Email are required.")
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
                    st.success("Lead created successfully.")
                    refresh()
                    st.rerun()
                except Exception as e:
                    st.error(f"Lead could not be created: {e}")

st.divider()

# ----------------------------
# Load data
# ----------------------------
try:
    leads = list_leads()
except Exception as e:
    st.error(f"Lead data could not be loaded from API: {e}")
    st.stop()

# Client-side filters
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
    st.info("Results not found.")
    st.stop()

df = pd.DataFrame(filtered)
df = df.sort_values(by="id", ascending=True)

st.markdown("### List")

# Header row
h1, h2, h3, h4, h5 = st.columns([1, 3, 3, 2, 1])
with h1:
    st.write("**ID**")
with h2:
    st.write("**Company**")
with h3:
    st.write("**Contact Person**")
with h4:
    st.write("**Email**")
with h5:
    st.write("**Active**")
st.divider()


# Rows
for l in df.to_dict(orient="records"):
    r1, r2, r3, r4, r5 = st.columns([1, 3, 3, 2, 1], gap="small")

    with r1:
        st.write(str(l.get("id", "")))  

    with r2:
        # Firma adı tıklanabilir + ikon
        if st.button(
            f"{safe_str(l.get('company_name'))}  🔗",
            key=f"open_company_{l['id']}",
            help="Detayı aç",
            use_container_width=False,
        ):
            open_lead_modal(int(l["id"]))
            st.rerun()

    with r3:
        st.write(safe_str(l.get("contact_name")))

    with r4:
        st.write(safe_str(l.get("email")))

    with r5:
        st.write("✅" if bool(l.get("is_active", True)) else "—")

    st.divider()

# ----------------------------
# Modal contents
# ----------------------------
def render_lead_edit_form(lead: dict):
    st.markdown("### ✏️ Lead Details")

    e1, e2, e3 = st.columns(3)
    with e1:
        e_company = st.text_input("Company Name", value=safe_str(lead.get("company_name")), key=f"edit_company_{lead['id']}")
        e_source = st.text_input("Source", value=safe_str(lead.get("source")), key=f"edit_source_{lead['id']}")
    with e2:
        e_contact = st.text_input("Contact Person", value=safe_str(lead.get("contact_name")), key=f"edit_contact_{lead['id']}")
        e_title = st.text_input("Title", value=safe_str(lead.get("title")), key=f"edit_title_{lead['id']}")
    with e3:
        e_email = st.text_input("Email", value=safe_str(lead.get("email")), key=f"edit_email_{lead['id']}")
        e_phone = st.text_input("Phone", value=safe_str(lead.get("phone")), key=f"edit_phone_{lead['id']}")

    e_notes = st.text_area("Notes", value=safe_str(lead.get("notes")), height=120, key=f"edit_notes_{lead['id']}")
    e_active = st.toggle("Active", value=bool(lead.get("is_active", True)), key=f"edit_active_{lead['id']}")
    b1, b2, b3 = st.columns([1, 1, 1])

    with b1:
        if st.button("💾 Update", type="primary", use_container_width=True, key=f"btn_update_{lead['id']}"):
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
            try:
                update_lead(int(lead["id"]), payload)
                st.success("Güncellendi.")
                refresh()
                close_lead_modal()
                st.rerun()
            except Exception as e:
                st.error(f"Güncellenemedi: {e}")

    with b2:
        if st.button("🧊 Pasife al", use_container_width=True, key=f"btn_deactivate_{lead['id']}"):
            try:
                update_lead(int(lead["id"]), {"is_active": False})
                st.success("Pasife alındı.")
                refresh()
                close_lead_modal()
                st.rerun()
            except Exception as e:
                st.error(f"Pasife alınamadı: {e}")

    with b3:
        if st.button("Kapat", use_container_width=True, key=f"btn_close_{lead['id']}"):
            close_lead_modal()
            st.rerun()


# ----------------------------
# Modal open
# ----------------------------
if st.session_state.get("lead_modal_open") and st.session_state.get("lead_modal_id"):
    lead_id = int(st.session_state["lead_modal_id"])
    selected = next((x for x in filtered if int(x.get("id")) == lead_id), None)

    if not selected:
        st.warning("Seçilen kayıt bulunamadı.")
        close_lead_modal()
    else:
        @st.dialog("Lead Detayı")
        def _dlg():
            render_lead_edit_form(selected)

        _dlg()
