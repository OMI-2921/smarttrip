import math
from datetime import date, timedelta
from html import escape

import pandas as pd
import streamlit as st

# ============================================================
# SMARTTRIP — responsive travel planning & expense management
# Requirements: streamlit, pandas
# ============================================================

st.set_page_config(
    page_title="SmartTrip | Plan. Explore. Enjoy.",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Public image URLs are decorative and can be replaced with your own assets.
HERO_IMAGE = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=2000&q=85"
BALI_IMAGE = "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1100&q=85"
MOUNTAIN_IMAGE = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1100&q=85"
CITY_IMAGE = "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1100&q=85"
BEACH_IMAGE = "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1100&q=85"

PAGES = [
    "🏡 Home",
    "🧭 Plan Trip",
    "🗺️ Itinerary",
    "💳 Expenses",
    "📊 Trip Report",
]

# -------------------- Session defaults --------------------
defaults = {
    "trip": None,
    "expenses": [],
    "navigation": PAGES[0],
    "trip_counter": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- CSS / responsive design --------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        --st-blue: #087cf0;
        --st-blue-dark: #075ec2;
        --st-teal: #16b8a6;
        --st-navy: #122d4b;
        --st-muted: #6b7c90;
        --st-border: #e5edf6;
        --st-panel: #ffffff;
    }}
    html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
    .stApp {{
        color: var(--st-navy);
        background: radial-gradient(ellipse at 0% 0%, #e8f5ff 0%, transparent 34%), #f5f8fc;
    }}
    #MainMenu, footer, [data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
    [data-testid="stSidebar"] {{ display: none; }}
    .block-container {{ max-width: 1440px; padding: 0.85rem 2.25rem 3rem; }}

    .brand-row {{ display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.3rem; }}
    .brand {{ display:flex; align-items:center; gap:.65rem; color:#122d4b; font-size:1.6rem; font-weight:800; letter-spacing:-.8px; }}
    .brand-mark {{ width:42px; height:42px; display:flex; align-items:center; justify-content:center; color:white; border-radius:14px; background:linear-gradient(135deg,#087cf0,#15b9a8); box-shadow:0 7px 18px #087cf02d; font-size:1.25rem; }}
    .brand-blue {{ color:var(--st-blue); }}
    .brand-tag {{ color:#7b8ca0; font-size:.78rem; margin-top:-7px; margin-left:52px; }}
    .top-note {{ color:#6c7e92; font-size:.82rem; text-align:right; }}

    /* Icon-first navigation. Each label below is a real Streamlit button. */
    .st-key-navigation_bar [data-testid="stHorizontalBlock"] {{
        display:flex !important; flex-direction:row !important; flex-wrap:wrap !important;
        gap:.55rem !important; align-items:stretch !important;
    }}
    .st-key-navigation_bar [data-testid="column"] {{
        flex:1 1 calc(20% - .55rem) !important; width:calc(20% - .55rem) !important;
        max-width:none !important; min-width:0 !important; padding:0 !important;
    }}
    .nav-icon {{
        width:62px; height:62px; margin:0 auto .38rem; display:flex;
        align-items:center; justify-content:center; border-radius:19px;
        background:linear-gradient(145deg,#eaf5ff,#f2fbff); border:1px solid #dcecff;
        box-shadow:0 7px 18px #0b65b510; font-size:2.05rem;
        transition:transform .22s ease, box-shadow .22s ease, background .22s ease;
        animation:iconFloat 3.8s ease-in-out infinite;
    }}
    .nav-icon.active {{
        background:linear-gradient(145deg,#d8ecff,#dffbf5); border-color:#b6dafb;
        box-shadow:0 8px 22px #087cf026;
    }}
    .st-key-navigation_bar [data-testid="stButton"] {{ width:100%; }}
    .st-key-navigation_bar [data-testid="stButton"] button {{
        width:100%; min-height:47px; padding:.52rem .35rem !important;
        white-space:normal !important; text-align:center !important;
        border-radius:12px !important; font-size:.88rem !important;
        font-weight:750 !important; line-height:1.25 !important;
        transition:transform .2s ease, box-shadow .2s ease, background .2s ease !important;
    }}
    .st-key-navigation_bar [data-testid="stButton"] button:hover {{
        transform:translateY(-2px); box-shadow:0 8px 18px #087cf020;
    }}
    .st-key-navigation_bar [data-testid="stButton"] button[kind="primary"] {{
        background:linear-gradient(135deg,#087cf0,#0c9be7) !important;
        border-color:#087cf0 !important; color:white !important;
    }}
    .st-key-navigation_bar [data-testid="stButton"] button[kind="secondary"] {{
        background:#ffffff !important; border-color:#e2eaf4 !important; color:#344d67 !important;
    }}
    .st-key-navigation_bar [data-testid="stButton"] button:focus-visible {{
        outline:3px solid #7fc6ff !important; outline-offset:2px !important;
    }}

    .hero {{
        position:relative; overflow:hidden; min-height:265px; display:flex; align-items:center;
        border-radius:25px; padding:2.2rem 2.5rem; margin:.8rem 0 1.35rem;
        background-image:linear-gradient(90deg,rgba(4,45,82,.88) 0%,rgba(7,74,121,.68) 47%,rgba(5,55,90,.05) 100%),url('{HERO_IMAGE}');
        background-size:cover; background-position:center 55%; box-shadow:0 15px 35px #0e548f19;
        animation:fadeUp .55s ease both;
    }}
    .hero-copy {{ max-width:610px; color:#fff; position:relative; z-index:1; }}
    .eyebrow {{ display:inline-flex; align-items:center; gap:.4rem; font-size:.78rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#d8f6ff; background:#ffffff20; border:1px solid #ffffff35; padding:.4rem .7rem; border-radius:999px; }}
    .hero h1 {{ color:white !important; font-size:clamp(2rem,4vw,3.15rem) !important; line-height:1.08 !important; letter-spacing:-1.6px; margin:.85rem 0 .55rem !important; }}
    .hero p {{ color:#eef8ff !important; font-size:1.03rem; max-width:520px; margin:0 !important; }}
    .hero-small {{ color:#d7ecfc; font-size:.78rem; margin-top:1.15rem; }}

    .section-title {{ color:#122d4b; font-size:1.42rem; font-weight:800; letter-spacing:-.5px; margin:.35rem 0 .15rem; }}
    .section-subtitle {{ color:#74849a; font-size:.91rem; margin:0 0 1rem; }}
    .mini-label {{ color:#8291a3; text-transform:uppercase; font-weight:700; font-size:.72rem; letter-spacing:.07em; }}
    .big-value {{ color:#122d4b; font-size:1.62rem; font-weight:800; letter-spacing:-.7px; margin:.15rem 0; }}
    .tiny-copy {{ color:#77889b; font-size:.8rem; }}
    .soft-card {{ background:white; border:1px solid var(--st-border); border-radius:19px; padding:1.05rem 1.15rem; box-shadow:0 5px 18px #1b436b08; height:100%; transition:transform .18s ease,box-shadow .18s ease; }}
    .soft-card:hover {{ transform:translateY(-2px); box-shadow:0 10px 26px #1b436b11; }}
    .card-top {{ display:flex; justify-content:space-between; align-items:center; gap:.5rem; }}
    .icon-tile {{ width:43px; height:43px; display:flex; justify-content:center; align-items:center; border-radius:14px; font-size:1.25rem; background:#e9f4ff; }}
    .tile-blue {{ background:#e7f2ff; }} .tile-teal {{ background:#e2faf5; }} .tile-orange {{ background:#fff0df; }} .tile-purple {{ background:#f0eaff; }}
    .pill {{ display:inline-block; border-radius:999px; padding:.28rem .6rem; background:#e6faf3; color:#09876f; font-size:.72rem; font-weight:750; }}
    .notice {{ background:#edf8ff; border:1px solid #d9ecfb; border-radius:15px; padding:.9rem 1rem; color:#41627f; font-size:.86rem; }}
    .destination-card {{ overflow:hidden; background:white; border:1px solid var(--st-border); border-radius:18px; box-shadow:0 6px 20px #1b436b09; }}
    .destination-card img {{ width:100%; height:145px; object-fit:cover; display:block; transition:transform .45s ease, filter .45s ease; }}
    .destination-card:hover img {{ transform:scale(1.045); filter:saturate(1.08); }}
    .destination-copy {{ padding:.85rem .95rem 1rem; }}
    .destination-copy strong {{ color:#122d4b; font-size:1rem; }}
    .destination-copy p {{ color:#718399; font-size:.82rem; margin:.25rem 0 0; }}
    .step-card {{ border:1px solid #e3edf8; background:#fff; border-radius:17px; padding:1rem; }}
    .step-number {{ display:inline-flex; width:30px; height:30px; align-items:center; justify-content:center; color:#087cf0; background:#e8f4ff; border-radius:10px; font-weight:800; margin-bottom:.5rem; }}
    .footer {{ text-align:center; color:#94a2b3; padding:2.2rem .5rem .3rem; font-size:.77rem; }}

    .stButton > button, .stDownloadButton > button {{
        border-radius:12px; border:1px solid #087cf0; background:#087cf0; color:#fff;
        padding:.62rem 1rem; font-weight:750; transition:all .18s ease; min-height:43px;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{ background:#075ec2; color:white; border-color:#075ec2; transform:translateY(-1px); box-shadow:0 6px 16px #087cf02c; }}
    div[data-testid="stForm"] {{ background:#fff; border:1px solid #e5edf6; border-radius:20px; padding:1.1rem 1.2rem; }}
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {{ border-radius:11px; }}
    .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label, .stTextArea label {{ color:#42576e; font-weight:650; }}
    div[data-testid="stMetric"] {{ background:#fff; border:1px solid #e5edf6; border-radius:16px; padding:1rem; box-shadow:0 4px 15px #16385b05; }}
    div[data-testid="stMetricLabel"] {{ color:#6b7d90; }}
    div[data-testid="stMetricValue"] {{ color:#122d4b; font-weight:800; }}
    hr {{ border-color:#e6edf5; }}
    @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(12px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes screenSlideIn {{ from {{ opacity:0; transform:translateX(28px); }} to {{ opacity:1; transform:translateX(0); }} }}
    @keyframes iconFloat {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-3px); }} }}
    @keyframes softGlow {{ 0%,100% {{ box-shadow:0 7px 18px #0b65b510; }} 50% {{ box-shadow:0 10px 24px #087cf022; }} }}

    @media (max-width: 760px) {{
        .block-container {{ padding:.5rem .8rem 2rem; }}
        .brand {{ font-size:1.35rem; }} .brand-mark {{ width:37px; height:37px; }}
        .brand-tag {{ margin-left:46px; }} .top-note {{ display:none; }}
        .hero {{ min-height:275px; padding:1.45rem 1.2rem; border-radius:19px; background-position:62% center; }}
        .hero h1 {{ font-size:2.05rem !important; }} .hero p {{ font-size:.92rem; }}
        .st-key-navigation_bar [data-testid="stHorizontalBlock"] {{
            flex-direction:row !important; flex-wrap:wrap !important; gap:.45rem !important;
        }}
        .st-key-navigation_bar [data-testid="column"] {{
            flex:1 1 calc(33.333% - .45rem) !important; width:calc(33.333% - .45rem) !important;
            max-width:none !important; min-width:0 !important;
        }}
        .nav-icon {{ width:54px; height:54px; border-radius:17px; font-size:1.85rem; }}
        .st-key-navigation_bar [data-testid="stButton"] button {{ min-height:43px; font-size:.81rem !important; }}
        .soft-card {{ padding:.9rem; }} .big-value {{ font-size:1.35rem; }}
        .destination-card img {{ height:125px; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation:none !important; transition:none !important; scroll-behavior:auto !important; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Helpers --------------------
def go_to_page(page):
    """Change page and animate only when navigation actually changes."""
    if st.session_state.get("navigation") != page:
        st.session_state.nav_transition = True
    st.session_state.navigation = page


def inr(value):
    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return "₹0"


def show_section(title, subtitle=None):
    st.markdown(f'<div class="section-title">{escape(title)}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{escape(subtitle)}</div>', unsafe_allow_html=True)


def render_hero(title, subtitle, tag="YOUR NEXT ADVENTURE STARTS HERE"):
    st.markdown(
        f"""
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow">✦ {escape(tag)}</div>
            <h1>{escape(title)}</h1>
            <p>{escape(subtitle)}</p>
            <div class="hero-small">✈ Plan smarter &nbsp; · &nbsp; Explore more &nbsp; · &nbsp; Spend mindfully</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def calculate_budget(trip):
    nights = max(1, (trip["end_date"] - trip["start_date"]).days)
    days = nights + 1
    people = trip["travelers"]

    transport_rates = {
        "Domestic": {"Flight": 8000, "Train": 2500, "Car": 3500, "Bus": 1500},
        "International": {"Flight": 45000, "Train": 12000, "Car": 15000, "Bus": 9000},
    }
    hotel_rates = {"2-star": 2200, "3-star": 3500, "4-star": 6500, "5-star": 12000}
    style_factor = {"Economy": 0.78, "Balanced": 1.0, "Comfort": 1.22, "Premium": 1.65}
    food_rates = {"Economy": 550, "Balanced": 950, "Comfort": 1500, "Premium": 2600}
    activity_rates = {"Economy": 350, "Balanced": 750, "Comfort": 1300, "Premium": 2200}
    local_rates = {"Economy": 200, "Balanced": 350, "Comfort": 550, "Premium": 900}

    factor = style_factor[trip["budget_style"]]
    rooms = math.ceil(people / 2)
    transport = transport_rates[trip["travel_type"]][trip["transport"]] * people * factor
    accommodation = hotel_rates[trip["hotel"]] * rooms * nights * factor
    food = food_rates[trip["budget_style"]] * people * days
    activities = activity_rates[trip["budget_style"]] * people * days
    local = local_rates[trip["budget_style"]] * people * days
    subtotal = transport + accommodation + food + activities + local
    emergency = subtotal * 0.08
    values = {
        "Transport": round(transport),
        "Accommodation": round(accommodation),
        "Food": round(food),
        "Activities": round(activities),
        "Local travel": round(local),
        "Emergency buffer": round(emergency),
    }
    return values, round(sum(values.values())), days, nights, rooms


def create_day_plan(day_number, destination, interests):
    chosen = set(interests or [])
    morning = "Explore a popular local landmark and get to know the destination."
    afternoon = "Enjoy a relaxed lunch and explore a nearby neighbourhood."
    evening = "Take a scenic walk and enjoy dinner at a well-reviewed local spot."
    if "Nature" in chosen:
        morning = "Start with a nature trail, viewpoint, garden or scenic outdoor spot."
    if "Culture & history" in chosen:
        afternoon = "Visit a cultural attraction, museum, historic site or local market."
    if "Food" in chosen:
        evening = "Try a local food experience and discover regional specialities."
    if "Beaches" in chosen:
        evening = "Enjoy beach time, sunset views and a relaxed dinner nearby."
    if "Adventure" in chosen:
        morning = "Choose an outdoor activity or guided adventure suitable for the group."
    if "Relaxation" in chosen:
        afternoon = "Keep the pace flexible with downtime, a café stop or a wellness break."
    if day_number == 1:
        morning = "Arrive, transfer to your accommodation and settle in."
        afternoon = "Take an easy orientation walk close to your stay."
    return f"Morning\n{morning}\n\nAfternoon\n{afternoon}\n\nEvening\n{evening}\n\nNotes\nKeep transport time and opening hours in mind; confirm details before visiting."


def prepare_new_trip(data):
    budget, total, days, nights, rooms = calculate_budget(data)
    data["budget_breakdown"] = budget
    data["estimated_total"] = total
    data["days"] = days
    data["nights"] = nights
    data["rooms"] = rooms
    data["created_on"] = date.today().isoformat()
    return data


def build_settlement(expenses, traveler_names):
    if not traveler_names:
        return pd.DataFrame(columns=["Traveler", "Paid", "Equal share", "Net"])
    total = sum(float(x["amount"]) for x in expenses)
    per_person_share = total / len(traveler_names) if traveler_names else 0
    rows = []
    for name in traveler_names:
        paid = sum(float(x["amount"]) for x in expenses if x["paid_by"] == name)
        rows.append({
            "Traveler": name,
            "Paid": round(paid, 2),
            "Equal share": round(per_person_share, 2),
            "Net": round(paid - per_person_share, 2),
        })
    return pd.DataFrame(rows)


def export_expenses():
    columns = ["Date", "Description", "Category", "Amount (INR)", "Paid by"]
    df = pd.DataFrame(st.session_state.expenses)
    if df.empty:
        df = pd.DataFrame(columns=columns)
    else:
        df = df.rename(columns={"amount": "Amount (INR)", "date": "Date", "description": "Description", "category": "Category", "paid_by": "Paid by"})
        df = df[["Date", "Description", "Category", "Amount (INR)", "Paid by"]]
    return df.to_csv(index=False).encode("utf-8-sig")


def destination_image(destination):
    text = (destination or "").lower()
    if any(word in text for word in ["bali", "phuket", "goa", "beach", "maldives", "island"]):
        return BALI_IMAGE
    if any(word in text for word in ["mountain", "manali", "shimla", "leh", "alps", "himalaya"]):
        return MOUNTAIN_IMAGE
    if any(word in text for word in ["city", "tokyo", "singapore", "new york", "london", "paris"]):
        return CITY_IMAGE
    return BEACH_IMAGE

# -------------------- Header and top navigation --------------------
head_left, head_right = st.columns([2.2, 1])
with head_left:
    st.markdown(
        '<div class="brand-row"><div class="brand"><span class="brand-mark">✈</span><span>Smart<span class="brand-blue">Trip</span></span></div></div><div class="brand-tag">Plan · Explore · Enjoy</div>',
        unsafe_allow_html=True,
    )
with head_right:
    st.markdown('<div class="top-note">Your next great story is one trip away. 🌍</div>', unsafe_allow_html=True)

# Five icon tiles with clickable text buttons underneath. On small screens,
# CSS wraps them into a 3 + 2 grid so labels remain readable.
if st.session_state.navigation not in PAGES:
    st.session_state.navigation = PAGES[0]
with st.container(key="navigation_bar"):
    nav_columns = st.columns(5, gap="small")
    for idx, page in enumerate(PAGES):
        icon, label = page.split(" ", 1)
        active = st.session_state.navigation == page
        with nav_columns[idx]:
            icon_class = "nav-icon active" if active else "nav-icon"
            st.markdown(f'<div class="{icon_class}">{icon}</div>', unsafe_allow_html=True)
            st.button(
                label,
                key=f"nav_{idx}",
                type="primary" if active else "secondary",
                use_container_width=True,
                on_click=go_to_page,
                args=(page,),
            )

selected_page = st.session_state.navigation
animate_transition = st.session_state.pop("nav_transition", False)
if animate_transition:
    st.markdown(
        """<style>
        @keyframes smartTripSlideIn { from { opacity:0; transform:translateX(30px); } to { opacity:1; transform:translateX(0); } }
        .main .block-container { animation:smartTripSlideIn .42s cubic-bezier(.2,.7,.2,1) both; }
        .hero { animation:fadeUp .52s ease both; }
        .soft-card, .destination-card, .step-card { animation:fadeUp .48s ease both; }
        </style>""",
        unsafe_allow_html=True,
    )
st.markdown("<hr style='margin:.8rem 0 1.1rem;border-color:#e6edf5'>", unsafe_allow_html=True)

trip = st.session_state.trip

# ============================================================
# HOME
# ============================================================
if selected_page == "🏡 Home":
    render_hero(
        "Good trips begin with a great plan.",
        "Bring your ideas together with a clear budget, a flexible itinerary and simple expense tracking.",
        "HELLO, TRAVELER",
    )

    if trip:
        budget_total = trip["estimated_total"]
        actual_total = sum(float(e["amount"]) for e in st.session_state.expenses)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="soft-card"><div class="card-top"><span class="mini-label">Your destination</span><span class="icon-tile tile-blue">📍</span></div><div class="big-value">{escape(trip["destination"])}</div><div class="tiny-copy">{trip["start_date"].strftime("%d %b")} – {trip["end_date"].strftime("%d %b %Y")}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="soft-card"><div class="card-top"><span class="mini-label">Estimated budget</span><span class="icon-tile tile-purple">💰</span></div><div class="big-value">{inr(budget_total)}</div><div class="tiny-copy">{inr(budget_total / trip["travelers"])} per traveler</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="soft-card"><div class="card-top"><span class="mini-label">Recorded expenses</span><span class="icon-tile tile-teal">🧾</span></div><div class="big-value">{inr(actual_total)}</div><div class="tiny-copy">{(actual_total / budget_total * 100 if budget_total else 0):.0f}% of estimate used</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="soft-card"><div class="card-top"><span class="mini-label">Travel party</span><span class="icon-tile tile-orange">🧳</span></div><div class="big-value">{trip["travelers"]} traveler(s)</div><div class="tiny-copy">{trip["travel_type"]} · {trip["budget_style"]} style</div></div>', unsafe_allow_html=True)

        st.write("")
        left, right = st.columns([1.05, 1])
        with left:
            show_section("Your budget at a glance", "Illustrative estimate in Indian rupees — not live supplier pricing.")
            budget_df = pd.DataFrame({"Category": list(trip["budget_breakdown"].keys()), "Amount": list(trip["budget_breakdown"].values())}).set_index("Category")
            st.bar_chart(budget_df, y="Amount", use_container_width=True)
            st.caption("Estimates vary by dates, destination, availability, exchange rates and personal choices.")
        with right:
            show_section("Quick actions", "Pick up where you left off.")
            qa1, qa2 = st.columns(2)
            with qa1:
                st.markdown('<div class="step-card"><div style="font-size:1.6rem">🧭</div><b>Trip details</b><div class="tiny-copy">Review your travel plan</div></div>', unsafe_allow_html=True)
                st.button("Edit trip", use_container_width=True, on_click=go_to_page, args=("🧭 Plan Trip",))
            with qa2:
                st.markdown('<div class="step-card"><div style="font-size:1.6rem">🗺️</div><b>Day-by-day</b><div class="tiny-copy">Open your itinerary</div></div>', unsafe_allow_html=True)
                st.button("View itinerary", use_container_width=True, on_click=go_to_page, args=("🗺️ Itinerary",))
            qa3, qa4 = st.columns(2)
            with qa3:
                st.markdown('<div class="step-card"><div style="font-size:1.6rem">💳</div><b>Track spending</b><div class="tiny-copy">Log trip expenses</div></div>', unsafe_allow_html=True)
                st.button("Add expense", use_container_width=True, on_click=go_to_page, args=("💳 Expenses",))
            with qa4:
                st.markdown('<div class="step-card"><div style="font-size:1.6rem">📊</div><b>Trip summary</b><div class="tiny-copy">Compare planned vs actual</div></div>', unsafe_allow_html=True)
                st.button("See report", use_container_width=True, on_click=go_to_page, args=("📊 Trip Report",))
    else:
        st.markdown("<div class='notice'>✨ <b>Your travel space is ready.</b> Create a trip to get a budget estimate, a flexible day-by-day itinerary and an expense tracker in one place.</div>", unsafe_allow_html=True)
        st.write("")
        st.button("🧭  Plan my first trip", type="primary", use_container_width=True, on_click=go_to_page, args=("🧭 Plan Trip",))
        show_section("A little inspiration", "A few ideas to get your next adventure started.")
        d1, d2, d3 = st.columns(3)
        for col, image_url, title, sub in [
            (d1, BALI_IMAGE, "Island escapes", "Slow mornings, blue water and sunset walks."),
            (d2, MOUNTAIN_IMAGE, "Mountain air", "Fresh views and a little room to breathe."),
            (d3, CITY_IMAGE, "City discoveries", "Food, culture and hidden neighbourhood gems."),
        ]:
            with col:
                st.markdown(f'<div class="destination-card"><img src="{image_url}" alt="Travel inspiration"><div class="destination-copy"><strong>{title}</strong><p>{sub}</p></div></div>', unsafe_allow_html=True)
        st.write("")
        show_section("How SmartTrip helps", "Simple tools for a more organised trip.")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown('<div class="soft-card"><div class="icon-tile tile-blue">🧭</div><h4>Plan confidently</h4><p class="tiny-copy">Gather dates, travel preferences and an illustrative budget in one place.</p></div>', unsafe_allow_html=True)
        with s2:
            st.markdown('<div class="soft-card"><div class="icon-tile tile-teal">🗺️</div><h4>Keep days flexible</h4><p class="tiny-copy">Start with a suggested daily outline, then edit it to suit your group.</p></div>', unsafe_allow_html=True)
        with s3:
            st.markdown('<div class="soft-card"><div class="icon-tile tile-orange">💳</div><h4>Know where money goes</h4><p class="tiny-copy">Record actual spending and view a simple shared-cost estimate.</p></div>', unsafe_allow_html=True)

# ============================================================
# PLAN TRIP
# ============================================================
elif selected_page == "🧭 Plan Trip":
    render_hero("Let's plan something wonderful.", "Tell us a little about the trip. SmartTrip will prepare a starter budget and a flexible itinerary outline.", "YOUR JOURNEY, YOUR WAY")
    show_section("Plan your trip", "Fields marked with a star are needed to create your plan.")
    existing = st.session_state.trip or {}
    start_default = existing.get("start_date", date.today() + timedelta(days=14))
    if start_default < date.today():
        start_default = date.today() + timedelta(days=14)
    end_default = existing.get("end_date", start_default + timedelta(days=5))
    if end_default <= start_default:
        end_default = start_default + timedelta(days=5)
    with st.form("trip_planner_form", clear_on_submit=False):
        st.markdown("#### 📍 Your journey")
        a, b = st.columns(2)
        with a:
            origin = st.text_input("Starting from *", value=existing.get("origin", "Pune, India"), placeholder="e.g. Pune, India")
            start_date = st.date_input("Departure date *", value=start_default, min_value=date.today())
            travelers = st.number_input("Number of travelers *", min_value=1, max_value=30, value=int(existing.get("travelers", 2)), step=1)
        with b:
            destination = st.text_input("Destination *", value=existing.get("destination", "Bali, Indonesia"), placeholder="e.g. Bali, Indonesia")
            end_date = st.date_input("Return date *", value=end_default, min_value=date.today())
            travel_type = st.selectbox("Trip type", ["Domestic", "International"], index=["Domestic", "International"].index(existing.get("travel_type", "International")))

        st.markdown("#### ✨ Travel preferences")
        c, d, e = st.columns(3)
        with c:
            transport = st.selectbox("Main transport", ["Flight", "Train", "Car", "Bus"], index=["Flight", "Train", "Car", "Bus"].index(existing.get("transport", "Flight")))
        with d:
            hotels = ["2-star", "3-star", "4-star", "5-star"]
            hotel = st.selectbox("Hotel preference", hotels, index=hotels.index(existing.get("hotel", "4-star")))
        with e:
            styles = ["Economy", "Balanced", "Comfort", "Premium"]
            budget_style = st.selectbox("Budget style", styles, index=styles.index(existing.get("budget_style", "Balanced")))

        interest_options = ["Beaches", "Nature", "Food", "Culture & history", "Adventure", "Shopping", "Relaxation", "Family-friendly"]
        interests = st.multiselect("What are you interested in?", interest_options, default=existing.get("interests", ["Food", "Nature", "Relaxation"]))
        trip_notes = st.text_area("Anything else to consider? (optional)", value=existing.get("trip_notes", ""), placeholder="e.g. travelling with children, accessible activities, vegetarian food…", height=85)
        submitted = st.form_submit_button("✨  Create / update my trip", use_container_width=True, type="primary")

    if submitted:
        if not origin.strip() or not destination.strip():
            st.error("Please enter both a starting point and a destination.")
        elif end_date <= start_date:
            st.error("Your return date must be after your departure date.")
        else:
            old_trip = st.session_state.trip
            new_trip = {
                "origin": origin.strip(),
                "destination": destination.strip(),
                "start_date": start_date,
                "end_date": end_date,
                "travelers": int(travelers),
                "travel_type": travel_type,
                "transport": transport,
                "hotel": hotel,
                "budget_style": budget_style,
                "interests": interests,
                "trip_notes": trip_notes.strip(),
            }
            new_trip = prepare_new_trip(new_trip)
            st.session_state.trip = new_trip
            # Preserve personal edits unless the destination/interests changed.
            regenerate_itinerary = (
                not old_trip
                or old_trip.get("destination") != new_trip["destination"]
                or old_trip.get("interests") != new_trip["interests"]
            )
            for day_no in range(1, new_trip["days"] + 1):
                key = f"itinerary_day_{day_no}"
                if regenerate_itinerary or key not in st.session_state:
                    st.session_state[key] = create_day_plan(day_no, destination, interests)
            # Clear notes for days beyond the new trip length.
            for key in list(st.session_state.keys()):
                if key.startswith("itinerary_day_"):
                    try:
                        if int(key.rsplit("_", 1)[1]) > new_trip["days"]:
                            del st.session_state[key]
                    except ValueError:
                        pass
            st.success("Your trip plan is ready! The budget is an illustrative planning estimate, not a live quote.")
            st.rerun()

    if st.session_state.trip:
        trip = st.session_state.trip
        show_section("Your current estimate", f"{trip['days']} days · {trip['nights']} nights · {trip['travelers']} traveler(s)")
        q1, q2, q3 = st.columns(3)
        q1.metric("Estimated trip total", inr(trip["estimated_total"]))
        q2.metric("Estimated per traveler", inr(trip["estimated_total"] / trip["travelers"]))
        q3.metric("Estimated accommodation", inr(trip["budget_breakdown"]["Accommodation"]))
        budget_df = pd.DataFrame({"Category": list(trip["budget_breakdown"].keys()), "Estimated amount": list(trip["budget_breakdown"].values())})
        st.dataframe(budget_df.style.format({"Estimated amount": "₹{:,.0f}"}), use_container_width=True, hide_index=True)

# ============================================================
# ITINERARY
# ============================================================
elif selected_page == "🗺️ Itinerary":
    if not trip:
        render_hero("Your story, day by day.", "Create a trip first and your editable itinerary will appear here.", "YOUR TRAVEL STORY")
        st.info("Start by adding your destination, dates and interests in Plan Trip.")
        st.button("Open Trip Planner", type="primary", on_click=go_to_page, args=("🧭 Plan Trip",))
    else:
        render_hero(f"Explore {trip['destination']}.", "A starter itinerary you can change as your plans take shape. Confirm opening hours, tickets and transport before setting off.", "YOUR ITINERARY")
        st.markdown(f"<div class='notice'>📅 <b>{trip['start_date'].strftime('%d %b %Y')} – {trip['end_date'].strftime('%d %b %Y')}</b> &nbsp; · &nbsp; {trip['days']} days &nbsp; · &nbsp; {trip['travelers']} traveler(s)<br><span class='tiny-copy'>This is a locally generated starter outline, not an AI-verified schedule or a reservation.</span></div>", unsafe_allow_html=True)
        st.write("")
        for day_no in range(1, trip["days"] + 1):
            day_date = trip["start_date"] + timedelta(days=day_no - 1)
            with st.expander(f"Day {day_no}  ·  {day_date.strftime('%A, %d %b')}", expanded=(day_no == 1)):
                left, right = st.columns([1, 2.3])
                with left:
                    image_url = destination_image(trip["destination"])
                    st.image(image_url, use_container_width=True)
                    st.markdown(f"**{escape(trip['destination'])}**")
                    st.caption("Suggested day outline")
                with right:
                    key = f"itinerary_day_{day_no}"
                    if key not in st.session_state:
                        st.session_state[key] = create_day_plan(day_no, trip["destination"], trip["interests"])
                    st.text_area("Edit your plan", key=key, height=215, help="You can edit this text whenever your plans change.")
        itinerary_rows = []
        for day_no in range(1, trip["days"] + 1):
            itinerary_rows.append({"Day": day_no, "Date": (trip["start_date"] + timedelta(days=day_no - 1)).isoformat(), "Destination": trip["destination"], "Plan": st.session_state.get(f"itinerary_day_{day_no}", "")})
        itinerary_csv = pd.DataFrame(itinerary_rows).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Download itinerary (CSV)", itinerary_csv, file_name="smarttrip_itinerary.csv", mime="text/csv")

# ============================================================
# EXPENSES
# ============================================================
elif selected_page == "💳 Expenses":
    render_hero("Spend mindfully, enjoy more.", "Log what you spend, see where it goes and estimate a fair split across your travel group.", "YOUR TRIP, UNDER CONTROL")
    if not trip:
        st.info("Create a trip first to set the travel group and budget estimate. You can still explore the app in the meantime.")
        st.button("Create a trip", type="primary", on_click=go_to_page, args=("🧭 Plan Trip",))
    else:
        total_budget = trip["estimated_total"]
        total_actual = sum(float(x["amount"]) for x in st.session_state.expenses)
        a, b, c = st.columns(3)
        a.metric("Budget estimate", inr(total_budget))
        b.metric("Recorded expenses", inr(total_actual))
        c.metric("Budget remaining", inr(total_budget - total_actual), delta=f"{(total_actual / total_budget * 100 if total_budget else 0):.0f}% used", delta_color="inverse")
        st.progress(min(1.0, total_actual / total_budget) if total_budget else 0.0)

        show_section("Add an expense", "Record paid amounts in INR. Your entries stay in this active app session.")
        traveler_names = [f"Traveler {i}" for i in range(1, trip["travelers"] + 1)]
        with st.form("add_expense_form", clear_on_submit=True):
            a, b, c = st.columns([1.5, 1, 1])
            with a:
                description = st.text_input("Expense description *", placeholder="e.g. airport transfer")
            with b:
                amount = st.number_input("Amount (₹) *", min_value=0.0, max_value=100000000.0, value=0.0, step=100.0)
            with c:
                expense_date = st.date_input("Date", value=date.today())
            d, e = st.columns(2)
            with d:
                category = st.selectbox("Category", ["Transport", "Accommodation", "Food", "Activities", "Shopping", "Local travel", "Other"])
            with e:
                paid_by = st.selectbox("Paid by", traveler_names)
            add_expense = st.form_submit_button("＋  Add expense", type="primary", use_container_width=True)
        if add_expense:
            if not description.strip():
                st.error("Please enter a short description for the expense.")
            elif amount <= 0:
                st.error("Enter an amount greater than zero.")
            else:
                st.session_state.expenses.append({"date": expense_date.isoformat(), "description": description.strip(), "category": category, "amount": round(float(amount), 2), "paid_by": paid_by})
                st.success("Expense added.")
                st.rerun()

        st.write("")
        show_section("Recent expenses", "The list updates whenever you add a new entry.")
        if st.session_state.expenses:
            exp_df = pd.DataFrame(st.session_state.expenses).rename(columns={"date": "Date", "description": "Description", "category": "Category", "amount": "Amount (INR)", "paid_by": "Paid by"})
            st.dataframe(exp_df, use_container_width=True, hide_index=True, column_config={"Amount (INR)": st.column_config.NumberColumn(format="₹%.2f")})
            eleft, eright = st.columns([1.2, 1])
            with eleft:
                category_totals = exp_df.groupby("Category")["Amount (INR)"].sum().sort_values(ascending=False)
                st.markdown("**Spending by category**")
                st.bar_chart(category_totals, use_container_width=True)
            with eright:
                st.markdown("**Group split estimate**")
                settle_df = build_settlement(st.session_state.expenses, traveler_names)
                st.dataframe(settle_df, use_container_width=True, hide_index=True, column_config={"Paid": st.column_config.NumberColumn(format="₹%.2f"), "Equal share": st.column_config.NumberColumn(format="₹%.2f"), "Net": st.column_config.NumberColumn(format="₹%.2f")})
                st.caption("Positive net means the traveler paid more than their equal share; negative means less. This is an estimate, not a transfer instruction.")
            st.download_button("⬇️ Download expenses (CSV)", export_expenses(), file_name="smarttrip_expenses.csv", mime="text/csv")
            with st.expander("Remove all recorded expenses"):
                st.warning("This removes all expense entries from the current session. This cannot be undone.")
                if st.button("Clear all expenses", key="clear_expenses"):
                    st.session_state.expenses = []
                    st.rerun()
        else:
            st.markdown("<div class='soft-card'><div style='font-size:2rem'>🧾</div><b>No expenses recorded yet</b><p class='tiny-copy'>Add your first expense above and your spending chart and group split will appear here.</p></div>", unsafe_allow_html=True)

# ============================================================
# TRIP REPORT
# ============================================================
elif selected_page == "📊 Trip Report":
    render_hero("Your trip, all in one snapshot.", "Compare your original estimate with the expenses you record along the way.", "THE BIG PICTURE")
    if not trip:
        st.info("Create a trip first to generate a trip report.")
        st.button("Go to Plan Trip", type="primary", on_click=go_to_page, args=("🧭 Plan Trip",))
    else:
        total_budget = trip["estimated_total"]
        total_actual = sum(float(x["amount"]) for x in st.session_state.expenses)
        difference = total_budget - total_actual
        m1, m2, m3 = st.columns(3)
        m1.metric("Estimated budget", inr(total_budget))
        m2.metric("Actual expenses logged", inr(total_actual))
        m3.metric("Estimate minus spending", inr(difference), delta="Under estimate" if difference >= 0 else "Over estimate", delta_color="normal" if difference >= 0 else "inverse")
        st.write("")
        show_section("Trip details", "Your current planning assumptions.")
        detail1, detail2 = st.columns(2)
        with detail1:
            st.markdown(f"""
            <div class="soft-card">
              <div class="mini-label">Destination</div><div class="big-value">{escape(trip['destination'])}</div>
              <p class="tiny-copy">From {escape(trip['origin'])}</p><hr>
              <b>Travel dates</b><p class="tiny-copy">{trip['start_date'].strftime('%d %b %Y')} – {trip['end_date'].strftime('%d %b %Y')}</p>
              <b>Travel party</b><p class="tiny-copy">{trip['travelers']} traveler(s) · {trip['travel_type']} · {trip['transport']}</p>
              <b>Stay & style</b><p class="tiny-copy">{trip['hotel']} · {trip['budget_style']} budget style</p>
            </div>""", unsafe_allow_html=True)
        with detail2:
            st.markdown("**Estimated vs recorded expenses**")
            comparison = pd.DataFrame({"Amount (INR)": [total_budget, total_actual]}, index=["Estimated budget", "Actual expenses"])
            st.bar_chart(comparison, use_container_width=True)
            if total_budget:
                st.progress(min(1.0, total_actual / total_budget))
                st.caption(f"{total_actual / total_budget * 100:.1f}% of the estimate has been recorded as spent.")
        st.write("")
        show_section("Budget breakdown", "Planning estimates are not quotes or booked rates.")
        break_df = pd.DataFrame({"Category": list(trip["budget_breakdown"].keys()), "Estimated amount (INR)": list(trip["budget_breakdown"].values())})
        st.dataframe(break_df, use_container_width=True, hide_index=True, column_config={"Estimated amount (INR)": st.column_config.NumberColumn(format="₹%.0f")})

        report = {
            "Destination": trip["destination"],
            "Origin": trip["origin"],
            "Departure": trip["start_date"].isoformat(),
            "Return": trip["end_date"].isoformat(),
            "Travelers": trip["travelers"],
            "Trip type": trip["travel_type"],
            "Transport": trip["transport"],
            "Hotel preference": trip["hotel"],
            "Budget style": trip["budget_style"],
            "Estimated budget (INR)": total_budget,
            "Actual expenses logged (INR)": round(total_actual, 2),
            "Budget remaining (INR)": round(difference, 2),
        }
        report_csv = pd.DataFrame([report]).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Download trip summary (CSV)", report_csv, file_name="smarttrip_report.csv", mime="text/csv", type="primary")

# -------------------- Footer / transparent limitations --------------------
st.markdown("<div class='footer'>✈️ <b>SmartTrip</b> · Plan · Explore · Enjoy<br>Planning estimates only. No bookings are made and prices are not live.<br>Current prototype data lives in the active Streamlit session and may reset when the session restarts.</div>", unsafe_allow_html=True)
