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
st.title("🎓 EduBridge - AI Mentor for Students")

# Sidebar Menu
menu = ["AI Career Mentor", "AI Resume Builder"]
choice = st.sidebar.selectbox("Choose a Feature", menu)

# AI Career Mentor with Chat History
if choice == "AI Career Mentor":
    st.subheader("🤖 AI Career Mentor (Powered by Llama 3)")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you today?"}]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖").write(msg["content"])

    # AI Response Generator
    def generate_response():
        response = ollama.chat(model="llama3", stream=True, messages=st.session_state.messages)
        for partial_resp in response:
            yield partial_resp["message"]["content"]

    # User Input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="👤").write(prompt)
        full_message = "".join(generate_response())
        st.chat_message("assistant", avatar="🤖").write(full_message)
        st.session_state.messages.append({"role": "assistant", "content": full_message})


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
