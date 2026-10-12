

import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ============================================================
# SMARTTRIP - SMART TRAVEL PLANNER
# Initial version: trip planning, budget, itinerary, expenses
# ============================================================

st.set_page_config(
    page_title="SmartTrip | Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- SESSION DATA --------------------

if "trip" not in st.session_state:
    st.session_state.trip = None

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "itinerary_notes" not in st.session_state:
    st.session_state.itinerary_notes = {}

# -------------------- DESIGN --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #f4f7fb;
    }

    [data-testid="stSidebar"] {
        background: #10213b;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .hero {
        background: linear-gradient(120deg, #10213b, #176b83);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #e0f2fe;
        margin: 0;
        font-size: 16px;
    }

    .eyebrow {
        color: #7dd3fc;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e4eaf2;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e4eaf2;
        border-radius: 13px;
        padding: 16px;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #087e8b;
        border: 1px solid #087e8b;
        color: #ffffff;
        border-radius: 9px;
        font-weight: 600;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 9px;
    }

    h1, h2, h3 {
        letter-spacing: -0.3px;
    }

    .small-note {
        color: #64748b;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HELPER FUNCTIONS --------------------

def format_inr(amount):
    """Format a number as Indian rupees."""
    return f"₹{amount:,.0f}"


def calculate_budget(
    days,
    travelers,
    travel_mode,
    accommodation,
    travel_style,
):
    """
    Create illustrative planning estimates.
    These values are NOT live travel prices.
    """

    transport_rates = {
        "Flight": 12000,
        "Train": 2500,
        "Bus": 1500,
        "Car / Road trip": 3500,
    }

    hotel_rates = {
        "Budget": 1800,
        "3-star": 3500,
        "4-star": 6500,
        "5-star": 12000,
    }

    style_multipliers = {
        "Budget saver": 0.75,
        "Balanced": 1.00,
        "Comfort": 1.35,
    }

    multiplier = style_multipliers[travel_style]

    # Basic estimate for transport
    transport = transport_rates[travel_mode] * travelers

    # Assumes approximately two travelers per hotel room
    rooms = max(1, (travelers + 1) // 2)
    hotel = hotel_rates[accommodation] * days * rooms

    # Approximate daily expenses per traveler
    food = 900 * days * travelers
    activities = 600 * days * travelers
    local_transport = 400 * days * travelers

    subtotal = transport + hotel + food + activities + local_transport
    emergency_buffer = subtotal * 0.10

    return {
        "Transport": round(transport * multiplier),
        "Accommodation": round(hotel * multiplier),
        "Food": round(food * multiplier),
        "Activities": round(activities * multiplier),
        "Local transport": round(local_transport * multiplier),
        "Emergency buffer": round(emergency_buffer * multiplier),
    }


def get_trip_days(start_date, end_date):
    """Calculate the number of nights between two dates."""
    return (end_date - start_date).days


def get_trip_total(trip):
    return sum(trip["budget"].values())


def expenses_dataframe():
    columns = [
        "Date",
        "Description",
        "Category",
        "Amount",
        "Paid by",
    ]

    if not st.session_state.expenses:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(st.session_state.expenses, columns=columns)


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">✈️ SmartTrip</div>',
        unsafe_allow_html=True,
    )
    st.caption("Your journey, intelligently planned.")
    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Trip Planner",
            "My Itinerary",
            "Expense Tracker",
            "Trip Report",
        ],
        label_visibility="visible",
    )

    st.divider()

    if st.session_state.trip:
        st.markdown("**CURRENT TRIP**")
        st.write(st.session_state.trip["destination"])
        st.caption(
            f'{st.session_state.trip["start_date"].strftime("%d %b")} '
            f'– {st.session_state.trip["end_date"].strftime("%d %b %Y")}'
        )
    else:
        st.caption("No trip created yet.")

    st.divider()
    st.caption("SMARTTRIP • DEVELOPMENT VERSION")

# -------------------- TOP BANNER --------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">YOUR PERSONAL TRAVEL COMPANION</div>
        <h1>Make every journey smarter.</h1>
        <p>
            Plan your next adventure, understand your budget,
            organize your days, and keep your expenses together.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    trip = st.session_state.trip
    expenses = expenses_dataframe()

    st.subheader("Your travel dashboard")
    st.write("Your trip planning and spending overview.")

    if trip:
        estimated_total = get_trip_total(trip)
        actual_total = float(expenses["Amount"].sum()) if not expenses.empty else 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Destination", trip["destination"])
        col2.metric("Estimated budget", format_inr(estimated_total))
        col3.metric("Recorded expenses", format_inr(actual_total))
        col4.metric("Travelers", trip["travelers"])

        st.markdown("### Your current trip")

        left, right = st.columns([1.2, 0.8])

        with left:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="eyebrow">UPCOMING ADVENTURE</div>
                    <h3>{trip["start_location"]} → {trip["destination"]}</h3>
                    <p>{trip["start_date"].strftime("%d %B %Y")}
                    to {trip["end_date"].strftime("%d %B %Y")}</p>
                    <p>{trip["days"]} night(s) · {trip["travelers"]} traveler(s)</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            st.markdown("#### Budget overview")
            budget_df = pd.DataFrame(
                {
                    "Category": list(trip["budget"].keys()),
                    "Estimated cost": list(trip["budget"].values()),
                }
            )
            st.bar_chart(
                budget_df,
                x="Category",
                y="Estimated cost",
            )

        st.caption(
            "Budget values are planning estimates, not confirmed travel prices."
        )

    else:
        st.info(
            "Welcome to SmartTrip! Create your first trip to populate "
            "your dashboard."
        )

        st.markdown("### What you can do with SmartTrip")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("#### 🧭 Plan a trip")
            st.write(
                "Enter your destination, dates, group size, "
                "transport preference, and travel style."
            )

        with c2:
            st.markdown("#### 💰 Manage your budget")
            st.write(
                "View an estimated cost breakdown and record "
                "your actual spending."
            )

        with c3:
            st.markdown("#### 🗓️ Organize your days")
            st.write(
                "Create a day-by-day outline and keep personal "
                "notes for your journey."
            )

    st.divider()
    st.markdown("### SmartTrip development roadmap")

    roadmap1, roadmap2, roadmap3 = st.columns(3)

    with roadmap1:
        st.markdown("**01 · Planning**")
        st.caption("Trip details, budget estimates, and expenses.")

    with roadmap2:
        st.markdown("**02 · Intelligence**")
        st.caption("AI itineraries and a conversational travel assistant.")

    with roadmap3:
        st.markdown("**03 · Live information**")
        st.caption("Maps, weather, exchange rates, and supported travel searches.")

# ============================================================
# TRIP PLANNER
# ============================================================

elif page == "Trip Planner":

    st.subheader("Plan a new trip")
    st.write(
        "Tell us about your journey. SmartTrip will prepare an initial "
        "budget estimate and trip summary."
    )

    existing_trip = st.session_state.trip

    default_start = date.today() + timedelta(days=14)
    default_end = default_start + timedelta(days=3)

    with st.form("trip_planner_form"):

        st.markdown("### 1. Your journey")

        col1, col2 = st.columns(2)

        with col1:
            start_location = st.text_input(
                "Starting location",
                value=existing_trip["start_location"] if existing_trip else "",
                placeholder="e.g. Pune, India",
            )

            destination = st.text_input(
                "Destination",
                value=existing_trip["destination"] if existing_trip else "",
                placeholder="e.g. Goa, India",
            )

            start_date = st.date_input(
                "Departure date",
                value=existing_trip["start_date"] if existing_trip else default_start,
                min_value=date.today(),
            )

        with col2:
            end_date = st.date_input(
                "Return date",
                value=existing_trip["end_date"] if existing_trip else default_end,
                min_value=date.today() + timedelta(days=1),
            )

            travelers = st.number_input(
                "Number of travelers",
                min_value=1,
                max_value=50,
                value=existing_trip["travelers"] if existing_trip else 2,
                step=1,
            )

            travel_mode = st.selectbox(
                "Preferred transport",
                ["Flight", "Train", "Bus", "Car / Road trip"],
                index=(
                    ["Flight", "Train", "Bus", "Car / Road trip"].index(
                        existing_trip["travel_mode"]
                    )
                    if existing_trip
                    else 0
                ),
            )

        st.divider()
        st.markdown("### 2. Your travel style")

        col3, col4 = st.columns(2)

        with col3:
            accommodation_options = ["Budget", "3-star", "4-star", "5-star"]

            accommodation = st.selectbox(
                "Accommodation preference",
                accommodation_options,
                index=(
                    accommodation_options.index(existing_trip["accommodation"])
                    if existing_trip
                    else 1
                ),
            )

            travel_style_options = ["Budget saver", "Balanced", "Comfort"]

            travel_style = st.selectbox(
                "Budget style",
                travel_style_options,
                index=(
                    travel_style_options.index(existing_trip["travel_style"])
                    if existing_trip
                    else 1
                ),
            )

        with col4:
            interest_options = [
                "Nature",
                "Beaches",
                "Food",
                "History & culture",
                "Shopping",
                "Adventure",
                "Family activities",
                "Nightlife",
            ]

            interests = st.multiselect(
                "What interests you?",
                interest_options,
                default=(
                    existing_trip["interests"]
                    if existing_trip
                    else ["Nature", "Food"]
                ),
            )

        submitted = st.form_submit_button(
            "Create My Trip Plan",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not start_location.strip():
            st.error("Please enter your starting location.")

        elif not destination.strip():
            st.error("Please enter your destination.")

        elif end_date <= start_date:
            st.error("Your return date must be after your departure date.")

        else:
            days = get_trip_days(start_date, end_date)

            budget = calculate_budget(
                days=days,
                travelers=int(travelers),
                travel_mode=travel_mode,
                accommodation=accommodation,
                travel_style=travel_style,
            )

            st.session_state.trip = {
                "start_location": start_location.strip(),
                "destination": destination.strip(),
                "start_date": start_date,
                "end_date": end_date,
                "travelers": int(travelers),
                "travel_mode": travel_mode,
                "accommodation": accommodation,
                "travel_style": travel_style,
                "interests": interests,
                "days": days,
                "budget": budget,
            }

            st.session_state.itinerary_notes = {}

            st.success("Your trip plan has been created!")
            st.rerun()

    trip = st.session_state.trip

    if trip:
        st.divider()
        st.markdown("### Your estimated trip budget")

        total = get_trip_total(trip)
        per_person = total / trip["travelers"]

        m1, m2, m3 = st.columns(3)

        m1.metric("Estimated total", format_inr(total))
        m2.metric("Estimated per person", format_inr(per_person))
        m3.metric("Duration", f'{trip["days"]} night(s)')

        budget_df = pd.DataFrame(
            [
                {"Category": category, "Estimated cost": amount}
                for category, amount in trip["budget"].items()
            ]
        )

        st.bar_chart(budget_df, x="Category", y="Estimated cost")

        display_df = budget_df.copy()
        display_df["Estimated cost"] = display_df["Estimated cost"].apply(format_inr)

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
        )

        st.warning(
            "These are illustrative estimates in INR. They are not live "
            "flight fares, hotel rates, or confirmed booking prices."
        )

# ============================================================
# ITINERARY
# ============================================================

elif page == "My Itinerary":

    st.subheader("My itinerary")

    trip = st.session_state.trip

    if not trip:
        st.info("Create a trip in Trip Planner before preparing your itinerary.")

    else:
        st.markdown(f"### {trip['destination']}")
        st.caption(
            f"{trip['start_date'].strftime('%d %b %Y')} – "
            f"{trip['end_date'].strftime('%d %b %Y')} · "
            f"{trip['days']} night(s)"
        )

        st.info(
            "This is an editable starter itinerary. AI recommendations, "
            "opening hours, route optimization, and live place information "
            "will be integrated in a later phase."
        )

        for day_number in range(1, trip["days"] + 1):

            with st.expander(
                f"Day {day_number}",
                expanded=(day_number == 1),
            ):

                st.markdown("**Morning**")
                st.write("Breakfast and explore the local area.")

                st.markdown("**Afternoon**")
                st.write("Plan a main sightseeing activity or experience.")

                st.markdown("**Evening**")
                st.write("Dinner and relaxed exploration.")

                note_key = f"day_{day_number}"

                note = st.text_area(
                    "Your plans and notes",
                    value=st.session_state.itinerary_notes.get(note_key, ""),
                    key=f"note_input_{day_number}",
                    placeholder="Add places, timings, bookings, or reminders...",
                )

                st.session_state.itinerary_notes[note_key] = note

        itinerary_export = []

        for day_number in range(1, trip["days"] + 1):
            itinerary_export.append(
                {
                    "Day": day_number,
                    "Date": (
                        trip["start_date"] + timedelta(days=day_number - 1)
                    ).isoformat(),
                    "Destination": trip["destination"],
                    "Notes": st.session_state.itinerary_notes.get(
                        f"day_{day_number}", ""
                    ),
                }
            )

        itinerary_df = pd.DataFrame(itinerary_export)

        st.download_button(
            "Download itinerary as CSV",
            data=itinerary_df.to_csv(index=False).encode("utf-8"),
            file_name="smarttrip_itinerary.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ============================================================
# EXPENSE TRACKER
# ============================================================

elif page == "Expense Tracker":

    st.subheader("Expense tracker")
    st.write("Record what you spend during your journey.")

    trip = st.session_state.trip

    if trip:
        st.caption(f"Current trip: {trip['destination']}")

    with st.form("expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            expense_description = st.text_input(
                "Expense description",
                placeholder="e.g. Hotel dinner",
            )

            expense_category = st.selectbox(
                "Expense category",
                [
                    "Transport",
                    "Accommodation",
                    "Food",
                    "Activities",
                    "Shopping",
                    "Other",
                ],
            )

            expense_date = st.date_input(
                "Expense date",
                value=date.today(),
            )

        with col2:
            expense_amount = st.number_input(
                "Amount (INR)",
                min_value=0.0,
                value=0.0,
                step=100.0,
            )

            paid_by = st.text_input(
                "Paid by",
                placeholder="e.g. Traveler 1",
            )

        add_expense = st.form_submit_button(
            "Add Expense",
            type="primary",
            use_container_width=True,
        )

    if add_expense:

        if not expense_description.strip():
            st.error("Please enter an expense description.")

        elif expense_amount <= 0:
            st.error("Please enter an amount greater than zero.")

        else:
            st.session_state.expenses.append(
                {
                    "Date": expense_date.isoformat(),
                    "Description": expense_description.strip(),
                    "Category": expense_category,
                    "Amount": float(expense_amount),
                    "Paid by": paid_by.strip() or "Not specified",
                }
            )

            st.success("Expense added successfully.")
            st.rerun()

    expenses = expenses_dataframe()

    if not expenses.empty:

        total_spent = float(expenses["Amount"].sum())

        col1, col2 = st.columns(2)

        col1.metric("Total recorded spending", format_inr(total_spent))
        col2.metric("Number of expenses", len(expenses))

        st.markdown("### Your expenses")

        display_expenses = expenses.copy()
        display_expenses["Amount"] = display_expenses["Amount"].apply(format_inr)

        st.dataframe(
            display_expenses,
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("### Spending by category")

        category_totals = (
            expenses.groupby("Category", as_index=False)["Amount"]
            .sum()
        )

        st.bar_chart(
            category_totals,
            x="Category",
            y="Amount",
        )

        st.download_button(
            "Download expenses as CSV",
            data=expenses.to_csv(index=False).encode("utf-8"),
            file_name="smarttrip_expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()

        if st.button("Clear all expenses", type="secondary"):
            st.session_state.expenses = []
            st.rerun()

    else:
        st.info("You have not recorded any expenses yet.")

    st.caption(
        "Current limitation: expenses are kept in the active app session. "
        "Permanent database storage will be added in a later phase."
    )

# ============================================================
# TRIP REPORT
# ============================================================

elif page == "Trip Report":

    st.subheader("Trip report")

    trip = st.session_state.trip
    expenses = expenses_dataframe()

    if not trip:
        st.info("Create a trip first to generate your trip report.")

    else:
        estimated_total = get_trip_total(trip)

        actual_total = (
            float(expenses["Amount"].sum())
            if not expenses.empty
            else 0.0
        )

        difference = actual_total - estimated_total

        st.markdown(
            f"### {trip['start_location']} → {trip['destination']}"
        )

        st.caption(
            f"{trip['start_date'].strftime('%d %b %Y')} – "
            f"{trip['end_date'].strftime('%d %b %Y')}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Estimated budget",
            format_inr(estimated_total),
        )

        col2.metric(
            "Recorded spending",
            format_inr(actual_total),
        )

        col3.metric(
            "Actual minus estimate",
            format_inr(difference),
            delta=(
                "Over estimate"
                if difference > 0
                else "Under estimate"
                if difference < 0
                else "Equal to estimate"
            ),
            delta_color="inverse",
        )

        st.markdown("### Trip details")

        details_left, details_right = st.columns(2)

        with details_left:
            st.write(f"**Starting location:** {trip['start_location']}")
            st.write(f"**Destination:** {trip['destination']}")
            st.write(f"**Travelers:** {trip['travelers']}")
            st.write(f"**Duration:** {trip['days']} night(s)")

        with details_right:
            st.write(f"**Transport:** {trip['travel_mode']}")
            st.write(f"**Accommodation:** {trip['accommodation']}")
            st.write(f"**Travel style:** {trip['travel_style']}")
            st.write(
                "**Interests:** "
                + (", ".join(trip["interests"]) or "Not specified")
            )

        report_df = pd.DataFrame(
            [
                {
                    "Metric": "Estimated budget",
                    "Amount_INR": estimated_total,
                },
                {
                    "Metric": "Recorded spending",
                    "Amount_INR": actual_total,
                },
                {
                    "Metric": "Actual minus estimate",
                    "Amount_INR": difference,
                },
            ]
        )

        st.download_button(
            "Download trip report as CSV",
            data=report_df.to_csv(index=False).encode("utf-8"),
            file_name="smarttrip_trip_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "SmartTrip | Early development version | Budget figures are estimates, "
    "not confirmed prices. Keep a separate copy of important trip data."
)
