import streamlit as st

# Set page title and layout
st.set_page_config(page_title="PathFinder", layout="centered")
st.title("🎯 PathFinder - Discover Your Career")

st.markdown("Welcome to **PathFinder**, your personal guide to finding the perfect career path! 💼💡")
st.markdown("Answer a few quick questions and we'll suggest careers that match your interests, skills, and personality.")

st.header("📝 Quick Career Quiz")

# Quiz Questions
questions = {
    "q1": st.radio("1. Which subject do you enjoy the most?", 
                   ["Math", "Biology", "Literature", "Art", "ICT"]),
    "q2": st.radio("2. How do you like working?", 
                   ["Alone", "In a team", "Both"]),
    "q3": st.radio("3. What type of tasks do you enjoy?", 
                   ["Building or designing things", "Helping people", 
                    "Writing or expressing ideas", "Solving problems"]),
    "q4": st.radio("4. Pick a dream activity:", 
                   ["Create an app", "Design a bridge", "Write a novel", "Run a lab"]),
    "q5": st.radio("5. Do you like logic or creativity more?", 
                   ["Logic", "Creativity", "Both"]),
}

# Recommendation Engine
if st.button("🔍 Show My Career Matches"):
    score = {
        "Engineer": 0,
        "Doctor/Nurse": 0,
        "Writer/Media": 0,
        "Software Developer/Data Scientist": 0,
        "Designer/Artist": 0
    }

    # Question-based scoring
    if questions["q1"] == "Math":
        score["Engineer"] += 1
        score["Software Developer/Data Scientist"] += 1
    elif questions["q1"] == "Biology":
        score["Doctor/Nurse"] += 2
    elif questions["q1"] == "Literature":
        score["Writer/Media"] += 2
    elif questions["q1"] == "Art":
        score["Designer/Artist"] += 2
    elif questions["q1"] == "ICT":
        score["Software Developer/Data Scientist"] += 2

    if questions["q3"] == "Building or designing things":
        score["Engineer"] += 2
    elif questions["q3"] == "Helping people":
        score["Doctor/Nurse"] += 2
    elif questions["q3"] == "Writing or expressing ideas":
        score["Writer/Media"] += 2
    elif questions["q3"] == "Solving problems":
        score["Software Developer/Data Scientist"] += 2

    if questions["q4"] == "Create an app":
        score["Software Developer/Data Scientist"] += 2
    elif questions["q4"] == "Design a bridge":
        score["Engineer"] += 2
    elif questions["q4"] == "Write a novel":
        score["Writer/Media"] += 2
    elif questions["q4"] == "Run a lab":
        score["Doctor/Nurse"] += 2

    if questions["q5"] == "Logic":
        score["Engineer"] += 1
        score["Software Developer/Data Scientist"] += 1
    elif questions["q5"] == "Creativity":
        score["Designer/Artist"] += 2
        score["Writer/Media"] += 1
    elif questions["q5"] == "Both":
        for k in score: score[k] += 1

    # Get Top 2 Careers
    top_matches = sorted(score.items(), key=lambda x: x[1], reverse=True)[:2]

    # Show results
    st.success("✨ Your Top Career Matches:")
    for match in top_matches:
        st.markdown(f"- **{match[0]}**")

    st.info("Want to learn more about these careers? Scroll down for details!")

# Career Info Section
st.header("📚 Career Info")

careers = {
    "Engineer": "🔧 **Engineer** - Design, build, and maintain infrastructure and technology. Includes fields like civil, mechanical, and electrical engineering.",
    "Doctor/Nurse": "🩺 **Doctor/Nurse** - Healthcare heroes who diagnose, treat, and care for patients. Involves science, compassion, and critical thinking.",
    "Writer/Media": "📝 **Writer/Media** - Creative communicators who tell stories, report news, or create content through writing, journalism, or media.",
    "Software Developer/Data Scientist": "💻 **Software Developer / Data Scientist** - Tech-savvy minds who create apps or use data to solve real-world problems and predict outcomes.",
    "Designer/Artist": "🎨 **Designer/Artist** - Creative thinkers who work in visual design, branding, fashion, or digital art to create stunning experiences."
}

for career, desc in careers.items():
    with st.expander(career):
        st.markdown(desc)

# Footer
st.markdown("---")
st.markdown("Built with 💖 by the future of tech and civil brilliance — **YOU**.")

