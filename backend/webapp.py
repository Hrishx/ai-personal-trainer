import streamlit as st
import subprocess

st.title("AI Fitness Coach")

st.write("Real-time AI exercise analysis system")

if st.button("Start Workout Analysis"):
    subprocess.run(["python", "main.py"])

st.write("Features:")
st.write("- Pose detection")
st.write("- Rep counting")
st.write("- Form correction")
st.write("- Fatigue detection")
st.write("- AI coaching report")