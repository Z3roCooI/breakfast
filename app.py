import streamlit as st

st.set_page_config(page_title="Breakfast Check-In", page_icon="🥐", layout="wide")
st.title("🥐 Breakfast Check-In Tool")

# Sidebar upload and reset
with st.sidebar:
    st.header("📤 Upload Room List")
    uploaded_file = st.file_uploader("expected_rooms.txt", type="txt")
    if st.button("🔄 Reset Session"):
        st.session_state.checked_in = set()
        st.session_state.unexpected_guests = set()
        st.success("Session reset successfully!")

# If file is uploaded
if uploaded_file:
    # Decode file and load room numbers
    expected_rooms = set(
        line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines()
        if line.strip().isdigit()
    )
    st.success("Room list loaded.")
    st.markdown(f"**🛏️ Expected rooms:** {len(expected_rooms)} total")

    # Initialize session storage
    if "checked_in" not in st.session_state:
        st.session_state.checked_in = set()
    if "unexpected_guests" not in st.session_state:
        st.session_state.unexpected_guests = set()

    # Room input
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

    # Divider
    st.divider()
    st.subheader("📋 Room Status (100–139 and 200–239)")

    # Organize rooms
    def display_room_grid():
        columns = st.columns(6)
        for block in [100, 200]:
            for i in range(40):
                room = str(block + i)
                col = columns[i % 6]
                if room in st.session_state.checked_in:
                    col.markdown(f"✅ **{room}**")
                elif room in st.session_state.unexpected_guests:
                    col.markdown(f"<span style='color:red'>❗{room}</span>", unsafe_allow_html=True)
                elif room in expected_rooms:
                    col.markdown(f"🔲 {room}")
                else:
                    # Room outside of expected range, skip it
                    continue

        # Show extra unexpected guests not in 100–139 / 200–239
        extra = [
            room for room in st.session_state.unexpected_guests
            if not (100 <= int(room) <= 139 or 200 <= int(room) <= 239)
        ]
        if extra:
            st.subheader("🚨 Extra Unexpected Guests (outside range):")
            st.markdown(", ".join(extra))

    display_room_grid()

else:
    st.info("⬅️ Upload a .txt file with expected room numbers to begin.")
