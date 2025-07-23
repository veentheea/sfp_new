import streamlit as st
from datetime import datetime, timedelta
import pydeck as pdk

# ----- SESSION STATE INIT -----
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "events" not in st.session_state:
    st.session_state.events = []

# ----- LOGIN & REGISTER -----
st.title("🎉 Event Planner App")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])
if not st.session_state.logged_in:
    if menu == "Login":
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"You're logged in as: {username}")
            else:
                st.error("Invalid username or password")
    else:
        st.subheader("📝 Register")
        new_user = st.text_input("Choose a username")
        new_pass = st.text_input("Choose a password", type="password")
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.warning("Username already exists.")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Registered! Please login.")
else:
    st.success(f"You're logged in as: {st.session_state.username}")
    st.sidebar.success("✅ Logged In")

    # ----- REMINDER SYSTEM -----
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    upcoming = []
    for event in st.session_state.events:
        if event["creator"] == st.session_state.username or st.session_state.username in event["guests"]:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            if event_date == today:
                upcoming.append((event["name"], "📅 Today"))
            elif event_date == tomorrow:
                upcoming.append((event["name"], "📆 Tomorrow"))

    if upcoming:
        st.warning("🔔 Upcoming Events:")
        for name, when in upcoming:
            st.write(f"- **{name}** → {when}")

    # ----- EVENT CREATION -----
    st.header("📌 Create New Event")
    with st.form("create_event_form"):
        name = st.text_input("Event Name")
        date = st.date_input("Event Date")
        location = st.text_input("Location")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        description = st.text_area("Description")
        timeline = st.text_area("Timeline / Agenda", placeholder="e.g.\n10:00am - Opening\n11:00am - Games\n12:00pm - Lunch")
        submit = st.form_submit_button("Create Event")

        if submit:
            event = {
                "name": name,
                "date": str(date),
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "description": description,
                "creator": st.session_state.username,
                "guests": [],
                "budget": [],
                "tasks": [],
                "timeline": timeline
            }
            st.session_state.events.append(event)
            st.success(f"Event '{name}' created!")

    # ----- SHOW EVENTS -----
    st.header("📨 All Events (Join One!)")

    for i, event in enumerate(st.session_state.events):
        st.subheader(event["name"])
        st.write(f"📅 Date: {event['date']}")
        st.write(f"📍 Location: {event['location']}")
        st.write(f"📝 {event['description']}")
        st.write(f"👤 Created by: {event['creator']}")

        # RSVP
        if st.session_state.username not in event["guests"]:
            if st.button(f"RSVP to {event['name']}", key=f"rsvp_{i}"):
                event["guests"].append(st.session_state.username)
                st.success("RSVP Confirmed ✅")
        else:
            st.info("You’ve already RSVPed! 🙌")

        # Guest List
        with st.expander("👥 View Guest List"):
            st.write(", ".join(event["guests"]) or "No guests yet!")

        # Budget Tracker
        with st.expander("💸 Budget Tracker"):
            expense = st.text_input(f"Add Expense for {event['name']}", key=f"item_{i}")
            amount = st.number_input("Amount (RM)", min_value=0.0, key=f"amt_{i}")
            if st.button("Add Expense", key=f"add_exp_{i}"):
                if expense:
                    event["budget"].append({"item": expense, "amount": amount, "by": st.session_state.username})
                    st.success("Expense added!")
            total = sum(e["amount"] for e in event["budget"])
            st.write(f"💰 Total Spent: RM{total:.2f}")
            for b in event["budget"]:
                st.write(f"- {b['item']} (RM{b['amount']}) — by {b['by']}")

        # Task Manager
        with st.expander("✅ Task Manager"):
            task = st.text_input("New Task", key=f"task_{i}")
            if st.button("Add Task", key=f"task_btn_{i}"):
                if task:
                    event["tasks"].append({"task": task, "done": False})
                    st.success("Task added!")
            for idx, t in enumerate(event["tasks"]):
                checked = st.checkbox(t["task"], value=t["done"], key=f"task_chk_{i}_{idx}")
                t["done"] = checked

        # Timeline / Agenda
        with st.expander("🗓️ Timeline & Agenda"):
            st.text(event["timeline"])

        # Map Location
        with st.expander("🗺️ Event Map"):
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/streets-v11',
                initial_view_state=pdk.ViewState(
                    latitude=event["latitude"],
                    longitude=event["longitude"],
                    zoom=12,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=[{"lat": event["latitude"], "lon": event["longitude"]}],
                        get_position='[lon, lat]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=200,
                    ),
                ],
            ))
        st.markdown("---")







