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

    # Define room blocks for vertical columns
    room_blocks = {
        "100–139": range(100, 140),
        "200–239": range(200, 240),
        "300–339": range(300, 340),
        "400–439": range(400, 440),
        "500–539": range(500, 540),
        "600–639": range(600, 640),
    }

    columns = st.columns(6)

    for col, (block_name, room_range) in zip(columns, room_blocks.items()):
        col.subheader(f"🚪 {block_name}")
        for room in room_range:
            room_str = str(room)
            if room_str in st.session_state.checked_in:
                col.markdown(f"<span style='color:green'>✅ {room}</span>", unsafe_allow_html=True)
            elif room_str in st.session_state.unexpected_guests:
                col.markdown(f"<span style='color:red'>❗ {room}</span>", unsafe_allow_html=True)
            elif room_str in expected_rooms:
                col.markdown(f"🔲 {room}")
            else:
                col.markdown(f"<span style='color:gray'>—</span>", unsafe_allow_html=True)

    # Unexpected rooms outside displayed blocks
    known_range = set()
    for rng in room_blocks.values():
        known_range.update(str(num) for num in rng)

    extra_unexpected = [
        room for room in st.session_state.unexpected_guests if room not in known_range
    ]
    if extra_unexpected:
        st.subheader("🚨 Unexpected Guests Outside Displayed Blocks")
        st.markdown(", ".join(extra_unexpected))

else:
    st.info("⬅️ Please upload a text file with expected room numbers.")
