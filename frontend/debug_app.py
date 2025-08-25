import streamlit as st

# Simple debug app to test if Streamlit is working
st.set_page_config(page_title="Debug App", page_icon="🐛")

st.title("🐛 Debug App")
st.write("If you can see this, Streamlit is working!")

# Test basic Streamlit components
st.header("Basic Components Test")

# Text
st.write("This is a text component")

# Button
if st.button("Click me"):
    st.write("Button clicked!")

# Input
user_input = st.text_input("Enter some text:")
if user_input:
    st.write(f"You entered: {user_input}")

# Sidebar
st.sidebar.title("Sidebar Test")
st.sidebar.write("Sidebar is working!")

# Success message
st.success("✅ All basic components are working!")

st.write("---")
st.write("If you can see all of the above, the issue is in the main app configuration.")
