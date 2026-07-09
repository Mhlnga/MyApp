import streamlit as st
import pandas as pd
import base64

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Flight Ticket Booking",
    page_icon="✈️",
    layout="centered"
)

# -------------------------------------------------
# Background Image Function
# -------------------------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("images/airplane.png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* White transparent container */
        [data-testid="stVerticalBlock"] {{
            background: rgba(255,255,255,0.88);
            padding: 25px;
            border-radius: 15px;
        }}

        h1, h2, h3 {{
            color: #003366;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# Add background
add_bg_from_local("images/airplane.png")

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("✈️ Flight Ticket Booking System")
st.write("Please complete the booking form below.")

# -------------------------------------------------
# Passenger Details
# -------------------------------------------------
name = st.text_input("Passenger Name")

departure = st.selectbox(
    "Departure City",
    [
        "Johannesburg",
        "Cape Town",
        "Durban",
        "Pretoria"
    ]
)

destination = st.selectbox(
    "Destination",
    [
        "Johannesburg",
        "Cape Town",
        "Durban",
        "Pretoria"
    ]
)

travel_date = st.date_input("Departure Date")

flight_class = st.selectbox(
    "Flight Class",
    [
        "Economy",
        "Business",
        "First Class"
    ]
)

passengers = st.number_input(
    "Number of Passengers",
    min_value=1,
    max_value=10,
    value=1
)

# -------------------------------------------------
# Distance Between Cities (km)
# -------------------------------------------------
distances = {
    ("Johannesburg", "Cape Town"): 1400,
    ("Cape Town", "Johannesburg"): 1400,

    ("Johannesburg", "Durban"): 570,
    ("Durban", "Johannesburg"): 570,

    ("Johannesburg", "Pretoria"): 60,
    ("Pretoria", "Johannesburg"): 60,

    ("Cape Town", "Durban"): 1630,
    ("Durban", "Cape Town"): 1630,

    ("Cape Town", "Pretoria"): 1460,
    ("Pretoria", "Cape Town"): 1460,

    ("Durban", "Pretoria"): 630,
    ("Pretoria", "Durban"): 630,
}

# -------------------------------------------------
# Calculate Distance
# -------------------------------------------------
if departure == destination:
    distance = 0
else:
    distance = distances.get((departure, destination), 0)

# -------------------------------------------------
# Ticket Price
# -------------------------------------------------
price_per_km = 2.50
base_price = distance * price_per_km

# -------------------------------------------------
# Flight Class Multiplier
# -------------------------------------------------
if flight_class == "Economy":
    multiplier = 1.0
elif flight_class == "Business":
    multiplier = 1.5
else:
    multiplier = 2.0

ticket_price = base_price * multiplier
total = ticket_price * passengers

# -------------------------------------------------
# Ticket Price Display
# -------------------------------------------------
st.divider()

st.subheader("💰 Ticket Price")

if departure == destination:
    st.error("Departure and destination cannot be the same.")
else:
    st.write(f"**Distance:** {distance} km")
    st.write(f"**Price per km:** R{price_per_km:.2f}")
    st.write(f"**Flight Class:** {flight_class}")
    st.write(f"**Passengers:** {passengers}")

    st.success(f"Total Ticket Price: R{total:,.2f}")

# -------------------------------------------------
# Book Flight
# -------------------------------------------------
if st.button("✈️ Book Flight"):

    if name.strip() == "":
        st.error("Please enter the passenger name.")

    elif departure == destination:
        st.error("Please choose different departure and destination cities.")

    else:

        booking = pd.DataFrame({
            "Passenger": [name],
            "Departure": [departure],
            "Destination": [destination],
            "Distance (km)": [distance],
            "Departure Date": [travel_date],
            "Flight Class": [flight_class],
            "Passengers": [passengers],
            "Total Price": [f"R{total:,.2f}"]
        })

        # Save booking details
        st.session_state["name"] = name
        st.session_state["departure"] = departure
        st.session_state["destination"] = destination
        st.session_state["travel_date"] = str(travel_date)
        st.session_state["flight_class"] = flight_class
        st.session_state["passengers"] = passengers
        st.session_state["distance"] = distance
        st.session_state["total_price"] = total

        st.success("✅ Flight Booked Successfully!")

        st.subheader("Booking Summary")

        st.dataframe(booking, use_container_width=True)

        csv = booking.to_csv(index=False)

        st.download_button(
            label="📥 Download Ticket",
            data=csv,
            file_name="FlightTicket.csv",
            mime="text/csv"
        )

# -------------------------------------------------
# Online Check-in
# -------------------------------------------------
st.divider()

st.subheader("🧳 Online Check-in")

st.write(
    "If you have completed your booking, continue to the luggage check."
)

if st.button("🧳 Check In Luggage"):
    st.switch_page("pages/Luggage_Check.py")