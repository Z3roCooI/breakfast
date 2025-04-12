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
    # Read and decode uploaded file
    expected_rooms = set(
        line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines()
        if line.strip().isdigit()
    )
    st.success("Room list loaded.")
    st.markdown(f"**🛏️ Expected rooms:** {len(expected_rooms)} total")

    # Initialize session state
    if "checked_in" not in st.session_state:
        st.session_state.checked_in = set()
    if "unexpected_guests" not in st.session_state:
        st.session_state.unexpected_guests = set()

    # Check-in input
    st.subheader("🎫 Check-In")
    room_input = st.text_input("Enter room number:")

    if st.button("Check-In"):
        room = room_input.strip()
        if not room:
            st.warning("Please enter a room number.")
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

    # Define room range (100-639)
    full_range = list(range(100, 640))

    # Collect all rooms that should be shown (expected + unexpected + checked-in)
    display_rooms = sorted(set(
        full_range
    ).intersection(expected_rooms.union(st.session_state.unexpected_guests)))

    # Split display_rooms evenly into 6 chunks for columns
    col_count = 6
    chunk_size = max(1, (len(display_rooms) + col_count - 1) // col_count)
    room_chunks = [display_rooms[i:i + chunk_size] for i in range(0, len(display_rooms), chunk_size)]

    # Make 6 columns
    columns = st.columns(col_count)

    for col, chunk in zip(columns, room_chunks):
        for room in chunk:
            room_str = str(room)
            if room_str in st.session_state.checked_in:
                col.markdown(f"<div style='font-size: 14px; color: green;'>✅ {room}</div>", unsafe_allow_html=True)
