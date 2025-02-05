import streamlit as st
import ollama


# Load Scholarship Data (Demo)
scholarships = [
    {"name": "UNICEF Education Grant", "eligibility": "High school students, low-income", "apply": "https://www.unicef.org/"},
    {"name": "Google Scholarship", "eligibility": "Students in STEM", "apply": "https://buildyourfuture.withgoogle.com/scholarships"},
    {"name": "Local Aid", "eligibility": "Residents of rural areas", "apply": "https://example.com"}
]

# Title
st.title("🎓 Edunity - AI Mentor for Students")

# Sidebar
menu = ["AI Career Mentor", "Free Learning", "Scholarship Matcher", "AI Resume Builder", "Find a Mentor"]
choice = st.sidebar.selectbox("Choose a Feature", menu)

# AI Career Mentor with Chat History
if choice == "AI Career Mentor":
    st.subheader("🤖 AI Career Mentor")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask about *careers*, _skills_, or _study plans_:"}]
    
    # Display message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="👤").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])
    
    # Token generator
    def generate_response():
        response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            st.session_state["full_message"] += token
            yield token
    
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="👤").write(prompt)
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})

# Free Learning Resources
elif choice == "Free Learning":
    st.subheader("📚 Free Learning Resources")
    subjects = {"Programming": ["CS50, Harvard", "Python.org"], "Math": ["Khan Academy"], "English": ["BBC Learning"]}
    sub = st.selectbox("Choose a subject", list(subjects.keys()))
    st.write("🔗", subjects[sub])

# Smart Scholarship Matcher
elif choice == "Scholarship Matcher":
    st.subheader("🎓 Find the Right Scholarship")
    criteria = st.text_input("Enter your study level (e.g., High School, STEM, Rural)")
    matches = [s for s in scholarships if criteria.lower() in s["eligibility"].lower()]
    if matches:
        for s in matches:
            st.write(f"**{s['name']}** - Apply: [Link]({s['apply']})")
    else:
        st.write("❌ No matching scholarships found.")

# AI Resume Builder
elif choice == "AI Resume Builder":
    st.subheader("📄 AI-Powered Resume Generator (Coming Soon!)")
    st.write("🛠️ This feature will generate resumes based on your skills & achievements!")

# Find a Mentor
elif choice == "Find a Mentor":
    st.subheader("🤝 AI Mentor Matching (Coming Soon!)")
    st.write("🚀 This feature will connect you with real mentors!")

st.sidebar.write("🚀 Empowering Underprivileged Students! 🌍")
