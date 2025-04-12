import streamlit as st

st.title("🍳 Breakfast Check-In Tool")

# Upload file
uploaded_file = st.file_uploader("Upload expected_rooms.txt", type="txt")

if uploaded_file:
    expected_rooms = set(line.strip() for line in uploaded_file if line.strip().isdigit())
    if "checked_in" not in st.session_state:
        st.session_state.checked_in = set()
    if "unexpected_guests" not in st.session_state:
        st.session_state.unexpected_guests = set()

    room_input = st.text_input("Enter Room Number")

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

    st.subheader("✔️ Checked-in Rooms")
    st.write(", ".join(sorted(st.session_state.checked_in)) or "None")

    st.subheader("❗ Unexpected Guests")
    st.write(", ".join(sorted(st.session_state.unexpected_guests)) or "None")
else:
    st.info("⬆️ Please upload a text file with expected room numbers.")

