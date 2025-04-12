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
    st.subheader("📋 Room Check-In Status (by Range)")

    # Define fixed blocks for each column
    room_blocks = {
        "100–139": range(100, 140),
        "200–239": range(200, 240),
        "300–339": range(300, 340),
        "400–439": range(400, 440),
        "500–539": range(500, 540),
        "600–639": range(600, 640),
    }

    columns = st.columns(6)
