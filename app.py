import streamlit as st

st.set_page_config(page_title="Breakfast Check-In", page_icon="🥐", layout="wide")
st.title("🥐 Breakfast Check-In Tool")

# Sidebar: upload + reset
with st.sidebar:
    st.header("📤 Upload Room List")
    uploaded_file = st.file_uploader("expected_rooms.txt", type="txt")
    if st.button("🔄 Reset Session"):
        st.session_state.checked_in = set()
        st.session_state.unexpected_guests = set()
        st.success("Session reset successfully!")

# Main logic
if uploaded_file:
    # Decode and load room list
    expected_rooms = set(
        line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines()
        if line.strip().isdigit() and 100 <= int(line.strip()) <= 639
    )
    st.success("Room list loaded.")
    st.markdown(f"**🛏️ Expected rooms:** {len(expected_rooms)} total")

    # Initialize session state
    if "checked_in" not in st.session_state:
        st.session_state.checked_in = set()
    if "unexpected_guests" not in st.session_state:
        st.session_state.unexpected_guests = set()

    # Check-in UI
    st.subheader("🎫 Check-In")
    room_input = st.text_input("Enter room number:")

    if st.button("Check-In"):
        room = room_input.strip()
        if not room.isdigit():
            st.warning("Please enter a valid room number.")
        else:
            room_num = int(room)
            if room_num < 100 or room_num > 639:
                st.warning("Room number must be between 100 and 639.")
            elif room in st.session_state.checked_in:
                st.info(f"⚠️ Room {room} already checked in.")
            elif room in expected_rooms:
                st.session_state.checked_in.add(room)
                st.success(f"✅ Room {room} checked in.")
            else:
                st.session_state.unexpected_guests.add(room)
                st.error(f"❌ Room {room} is NOT on the list!")

    st.divider()
    st.subheader("📋 Room Check-In Status")

    # Define room ranges for columns
    column_ranges = {
        0: range(100, 140),
        1: range(200, 240),
        2: range(300, 340),
        3: range(400, 440),
        4: range(500, 540),
        5: range(600, 640),
    }

    columns = st.columns(6)

    # Go through each column and only display rooms in that column's range
    for idx, col in enumerate(columns):
        for room_num in column_ranges[idx]:
            room = str(room_num)

            # Skip if room has never been uploaded or interacted with
            if (
                room not in expected_rooms
                and room not in st.session_state.checked_in
                and room not in st.session_state.unexpected_guests
            ):
                continue

            if room in st.session_state.checked_in:
                col.markdown(f"<div style='font-size: 14px; color: green;'>✅ {room}</div>", unsafe_allow_html=True)
            elif room in st.session_state.unexpected_guests:
                col.markdown(f"<div style='font-size: 14px; color: red;'>❗ {room}</div>", unsafe_allow_html=True)
            elif room in expected_rooms:
                col.markdown(f"<div style='font-size: 14px;'>🔲 {room}</div>", unsafe_allow_html=True)

else:
    st.info("⬅️ Please upload a text file with expected room numbers.")
