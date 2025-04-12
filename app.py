import streamlit as st

st.set_page_config(page_title="Breakfast Check-In", page_icon="🥐", layout="wide")
st.title("🥐 Breakfast Check-In Tool")

# Sidebar
with st.sidebar:
    st.header("📤 Upload Room List")
    uploaded_file = st.file_uploader("expected_rooms.txt", type="txt")
    if st.button("🔄 Reset Session"):
        st.session_state.checked_in = set()
        st.session_state.unexpected_guests = set()
        st.success("Session reset successfully!")

# Main section
if uploaded_file:
    # Load and decode room numbers
    expected_rooms = set(
        line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines()
        if line.strip().isdigit()
    )
    st.success("Room list loaded.")
    st.markdown(f"**🛏️ Expected rooms:** {len(expected_rooms)} total")

    if "checked_in" not in st.session_state:
        st.session_state.checked_in = set()
    if "unexpected_guests" not in st.session_state:
        st.session_state.unexpected_guests = set()

    st.subheader("🎫 Check-In")
    room_input = st.text_input("Enter room number:")

    if st.button("Check-In"):
        room = room_input.strip()
        if not room:
            st.warning("Please enter a room number.")
        elif room in st.session_state.checked_in:
            st.info(f"⚠️ Room
