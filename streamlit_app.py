import streamlit as st
import ollama
import json

# Load Scholarship Data 
scholarships = [
    {"name": "UNICEF Education Grant", "eligibility": "High school students, low-income", "apply": "https://www.unicef.org/"},
    {"name": "Google Scholarship", "eligibility": "Students in STEM", "apply": "https://buildyourfuture.withgoogle.com/scholarships"},
    {"name": "Local Aid", "eligibility": "Residents of rural areas", "apply": "https://example.com"},
    {"name": "Fund for Education Abroad", "eligibility": "Collage", "apply": "https://fundforeducationabroad.org/"},
    {"name": "Golden Key Scholarships", "eligibility": "Collage", "apply": "https://www.goldenkey.org/scholarships/"},
    {"name": "Rotary Foundation Global Scholarship Grants", "eligibility": "Collage", "apply": "https://www.rotary.org/en/our-programs/scholarships"},
    {"name": "The NextGen Scholarship", "eligibility": "High school students, low-income", "apply": "https://www.perkconsulting.net/about/nextgen/"}
]


# Title
st.title("🎓 Edunity - AI Mentor for Students")

# Sidebar
menu = ["AI Career Mentor", "Free Learning", "Scholarship Matcher", "AI Resume Builder", "AI-Powered Personalized Learning", "Micro-Jobs & Support"]
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


# AI-Powered Personalized Learning
elif choice == "AI-Powered Personalized Learning":
    st.subheader("🧠 Personalized AI Learning")
    
    study_hours = st.slider("Select available daily study time (in hours):", 1, 5, 2)
    st.write(f"📚 AI will generate a study plan for {study_hours} hours per day.")
    
    if st.button("Generate Study Plan"):
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": f"Create a study plan for a student with only {study_hours} hours per day."}])
        st.write("📖 Study Plan:")
        st.write(response["message"]["content"])
    
# Free Learning Resources
elif choice == "Free Learning":
    st.subheader("📚 Free Learning Resources")
    
    subjects = {
        "Programming": [
            ("CS50, Harvard", "https://cs50.harvard.edu/"),
            ("Python.org", "https://www.python.org/"),
            ("freeCodeCamp", "https://www.freecodecamp.org/")
            
        ],
        "Math": [
            ("Khan Academy", "https://www.khanacademy.org/"),
            ("Harvard University", "https://pll.harvard.edu/subject/mathematics/free"),
            ("The Open University", "https://www.open.edu/openlearn/science-maths-technology/free-courses")
        ],
        "Science": [
            ("Stanford University(link is external)", "https://ughb.stanford.edu/courses/approved-courses/science-courses-2024-25"),
            ("Yale College", "https://science.yalecollege.yale.edu/academics/faculty-resources/science-courses-without-prerequisite"),
            
        ]
    }

    sub = st.selectbox("Choose a subject", list(subjects.keys()))

    for name, link in subjects[sub]:
        st.markdown(f"🔗 [{name}]({link})")

# Micro-Jobs & Support
elif choice == "Micro-Jobs & Support":
    st.subheader("🛠️ Financial & Accessibility Support")
    
    # Micro-jobs section
    st.write("💼 **Skill-Based Micro-Jobs**")
    st.write("Find small remote jobs to earn money while studying!")
    st.markdown("🔗 [Browse Jobs](https://www.freelancer.com/)https://www.mastersportal.com/articles/3139/work-from-dorm-12-online-jobs-for-students-around-the-world.html")

    # Location-based free education centers
    st.write("📍 **Find Local Learning Centers**")
    
    user_location = st.text_input("Enter your city or area (e.g., 'New Delhi, India')")
    
    if user_location:
        maps_url = f"https://www.google.com/maps/search/free+tuition+center+near+{user_location.replace(' ', '+')}"
        st.markdown(f"🔗 [Find Nearby Free Education Centers]({maps_url})")
    else:
        st.write("Enter a location to search for free education centers.")

# Smart Scholarship Matcher
elif choice == "Scholarship Matcher":
    st.subheader("🎓 Find the Right Scholarship")
    criteria = st.text_input("Enter your study level (e.g., High School, STEM, Collage, Rural)")
    matches = [s for s in scholarships if criteria.lower() in s["eligibility"].lower()]
    if matches:
        for s in matches:
            st.write(f"**{s['name']}** - Apply: [Link]({s['apply']})")
    else:
        st.write("❌ No matching scholarships found.")

# AI Resume Builder
elif choice == "AI Resume Builder":
    st.subheader("📄 AI Resume Builder")
    st.write("🛠️ This feature will generate resumes based on your skills & achievements!")

    def generate_resume(name, education, skills, experience, projects):
        """Generate a professional resume using Llama 3 AI."""
        prompt = f"""
        Create a professional resume for the following details:
        - Name: {name}
        - Education: {education}
        - Skills: {skills}
        - Experience: {experience}
        - Projects: {projects}

        Format it as a well-structured resume with sections and proper formatting.
        """
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

    # User Inputs
    name = st.text_input("Full Name")
    education = st.text_area("Education (Degrees, Certifications)")
    skills = st.text_area("Key Skills (Comma-separated)")
    experience = st.text_area("Work Experience (Job Titles, Companies, Years)")
    projects = st.text_area("Projects (Describe major projects)")

    if st.button("Generate Resume"):
        if name and education and skills:
            with st.spinner("Generating Resume..."):
                resume_text = generate_resume(name, education, skills, experience, projects)
                st.success("✅ Resume Generated!")
                st.text_area("Your AI-Generated Resume:", resume_text, height=300)
        else:
            st.error("❌ Please fill in at least Name, Education, and Skills!")
