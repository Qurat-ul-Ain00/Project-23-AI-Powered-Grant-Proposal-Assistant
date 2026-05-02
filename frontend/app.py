import streamlit as st
import requests

st.title("📄 AI Grant Proposal Assistant")

topic = st.text_input("Enter Topic")
goals = st.text_area("Enter Goals")
agency = st.text_input("Funding Agency")

if st.button("Generate Proposal"):
    response = requests.post(
        "http://localhost:8000/generate/",
        json={
            "topic": topic,
            "goals": goals,
            "agency": agency
        }
    )

    data = response.json()

    st.subheader("📑 Proposal Outline")
    st.write(data["outline"])

    st.subheader("💰 Budget Estimate")
    st.write(data["budget"])

    st.subheader("🧪 Reviewer Feedback")
    st.write(data["review"])


# -------- MEMORY VIEW -------- #

st.divider()
st.header("📜 Version History")

search_topic = st.text_input("Enter topic to view history")

if st.button("Load History"):
    res = requests.get(f"http://localhost:8000/memory/{search_topic}")
    history = res.json()

    for version in history:
        st.subheader(f"Version {version['version']}")
        st.write(version["result"])
        st.caption(f"Rationale: {version['rationale']}")
