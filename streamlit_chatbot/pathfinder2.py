
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PathFinder Malaysia 🇲🇾", layout="centered")

st.markdown("<h1 style='text-align:center; color:#4A90E2;'>🎓 PathFinder Malaysia</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Your personalized guide to future careers & study pathways</h4>", unsafe_allow_html=True)

# Quiz Form
st.header("📝 Career Match Quiz - Dive Deeper!")
with st.form("career_form"):
    name = st.text_input("Your name")
    
    fav_sub = st.selectbox("Favourite subject", ["Math", "Science", "Literature", "Art", "ICT"])
    work_style = st.selectbox("Preferred work style", ["Solo", "Teamwork", "Balanced"])
    dream_task = st.selectbox("Dream task", ["Build things", "Help people", "Create/write", "Solve problems"])
    mindset = st.radio("You are more...", ["Logical", "Creative", "Both"])

    skills = st.multiselect(
        "Which skills do you have? (Select all that apply)",
        ["Problem Solving", "Communication", "Creativity", "Analytical Thinking", "Leadership"]
    )
    
    interests = st.multiselect(
        "What are you interested in?",
        ["Technology", "Healthcare", "Arts & Media", "Engineering", "Data & Science"]
    )
    
    personality = st.radio(
        "Choose the personality trait that fits you best:",
        ["Detail-oriented", "Empathetic", "Innovative", "Practical", "Collaborative"]
    )

    experience = st.slider("How much experience do you have in your interests?", 0, 10, 0)
    submit = st.form_submit_button("🎯 Show My Results")

career_score = {
    "Engineer": 0,
    "Doctor/Nurse": 0,
    "Writer/Media": 0,
    "Software Developer/Data Scientist": 0,
    "Designer/Artist": 0
}

if submit:
    # Base scoring weights (adjust for effectiveness)
    subject_weights = {
        "Math": {"Engineer": 3, "Software Developer/Data Scientist": 3},
        "Science": {"Doctor/Nurse": 4},
        "Literature": {"Writer/Media": 4},
        "Art": {"Designer/Artist": 4},
        "ICT": {"Software Developer/Data Scientist": 4},
    }
    
    task_weights = {
        "Build things": {"Engineer": 4},
        "Help people": {"Doctor/Nurse": 4},
        "Create/write": {"Writer/Media": 4},
        "Solve problems": {"Software Developer/Data Scientist": 4}
    }
    
    mindset_weights = {
        "Logical": {"Engineer": 2, "Software Developer/Data Scientist": 2},
        "Creative": {"Writer/Media": 2, "Designer/Artist": 3},
        "Both": {c:1 for c in career_score}
    }
    
    skills_weights = {
        "Problem Solving": {"Engineer": 3, "Software Developer/Data Scientist": 3},
        "Communication": {"Doctor/Nurse": 2, "Writer/Media": 3},
        "Creativity": {"Designer/Artist": 4, "Writer/Media": 2},
        "Analytical Thinking": {"Engineer": 3, "Software Developer/Data Scientist": 3},
        "Leadership": {c: 2 for c in career_score}
    }
    
    interests_weights = {
        "Technology": {"Software Developer/Data Scientist": 4, "Engineer": 2},
        "Healthcare": {"Doctor/Nurse": 4},
        "Arts & Media": {"Designer/Artist": 3, "Writer/Media": 3},
        "Engineering": {"Engineer": 4},
        "Data & Science": {"Software Developer/Data Scientist": 4}
    }
    
    personality_weights = {
        "Detail-oriented": {"Engineer": 3, "Software Developer/Data Scientist": 3},
        "Empathetic": {"Doctor/Nurse": 4},
        "Innovative": {"Designer/Artist": 3, "Software Developer/Data Scientist": 2},
        "Practical": {"Engineer": 3, "Doctor/Nurse": 2},
        "Collaborative": {c: 2 for c in career_score}
    }
    
    # Apply weights
    def add_scores(weight_map, answer):
        for career, weight in weight_map.get(answer, {}).items():
            career_score[career] += weight
    
    # Subjects
    add_scores(subject_weights, fav_sub)
    
    # Tasks
    add_scores(task_weights, dream_task)
    
    # Mindset
    for career, weight in mindset_weights.get(mindset, {}).items():
        career_score[career] += weight
    
    # Skills
    for skill in skills:
        for career, weight in skills_weights.get(skill, {}).items():
            career_score[career] += weight
    
    # Interests
    for interest in interests:
        for career, weight in interests_weights.get(interest, {}).items():
            career_score[career] += weight
    
    # Personality
    for career, weight in personality_weights.get(personality, {}).items():
        career_score[career] += weight
    
    # Experience bonus: add half a point per year to related careers
    if "Technology" in interests or "Data & Science" in interests:
        career_score["Software Developer/Data Scientist"] += experience * 0.5
    if "Engineering" in interests:
        career_score["Engineer"] += experience * 0.5
    if "Healthcare" in interests:
        career_score["Doctor/Nurse"] += experience * 0.5
    if "Arts & Media" in interests:
        career_score["Designer/Artist"] += experience * 0.5

    # Show results summary
    top = sorted(career_score.items(), key=lambda x: x[1], reverse=True)[:3]
    
    st.success(f"🎉 Hey {name if name else 'there'}, based on your answers, your top career matches are:")
    for idx, (career, score) in enumerate(top, 1):
        st.markdown(f"**{idx}. {career}** (Score: {score:.1f})")

    # Visualize
    df = pd.DataFrame.from_dict(career_score, orient='index', columns=['Score']).reset_index()
    df = df.rename(columns={"index": "Career"})
    fig = px.bar(df, x='Career', y='Score', color='Score', color_continuous_scale='Viridis',
                 title="Career Match Scores")
    st.plotly_chart(fig, use_container_width=True)

    # University recommendations with pros/cons
    st.header("🏫 University Suggestions & Study Paths")

    uni_info = {
        "Engineer": {
            "Government": ["UTM", "UM", "USM", "UKM"],
            "Private": ["Taylor’s", "Limkokwing", "Sunway"],
            "Pros": "Strong engineering faculties, affordable fees in government unis.",
            "Cons": "Highly competitive entry, limited seats."
        },
        "Doctor/Nurse": {
            "Government": ["UKM", "UM", "UiTM", "USM"],
            "Private": ["IMU", "Taylor’s", "Sunway"],
            "Pros": "Well-established medical programs in government universities.",
            "Cons": "Long study duration and tough entrance exams."
        },
        "Writer/Media": {
            "Government": ["UM", "UUM", "UKM"],
            "Private": ["Taylor’s", "Sunway", "HELP University"],
            "Pros": "Good practical exposure and industry links.",
            "Cons": "Smaller intake and less specialized courses in government."
        },
        "Software Developer/Data Scientist": {
            "Government": ["MMU", "UTM", "USM", "UM"],
            "Private": ["Taylor’s", "Multimedia University", "Sunway"],
            "Pros": "Cutting-edge tech courses with good internship opportunities.",
            "Cons": "Fast-changing field requiring constant upskilling."
        },
        "Designer/Artist": {
            "Government": ["UiTM", "USM"],
            "Private": ["Limkokwing", "UCSI", "Taylor’s"],
            "Pros": "Strong portfolios and creative environments.",
            "Cons": "Limited spots in government universities."
        }
    }

    path_info = {
        "Engineer": "SPM → Foundation in Engineering / Matrikulasi → Engineering Degree",
        "Doctor/Nurse": "SPM → Foundation in Science / Matrikulasi → MBBS / Nursing Degree",
        "Writer/Media": "SPM → Diploma / Foundation in Mass Comm → Media Degree",
        "Software Developer/Data Scientist": "SPM → Foundation in IT / Diploma in CS → CS/Data Science Degree",
        "Designer/Artist": "SPM → Diploma in Design / Foundation in Arts → Design Degree"
    }

    for career, score in top:
        st.subheader(f"{career}")
        uni = uni_info.get(career, {})
        if uni:
            st.markdown(f"**Government Universities:** {', '.join(uni['Government'])}")
            st.markdown(f"**Private Universities:** {', '.join(uni['Private'])}")
            st.markdown(f"**Pros:** {uni['Pros']}")
            st.markdown(f"**Cons:** {uni['Cons']}")
        st.markdown(f"**Suggested Study Path:** {path_info.get(career, 'N/A')}")

    # Download result
    result_text = f"Career Matches for {name if name else 'Student'}:\n\n"
    for idx, (career, score) in enumerate(top, 1):
        result_text += f"{idx}. {career} (Score: {score:.1f})\n"
        uni = uni_info.get(career, {})
        if uni:
            result_text += f"Government Universities: {', '.join(uni['Government'])}\n"
            result_text += f"Private Universities: {', '.join(uni['Private'])}\n"
            result_text += f"Pros: {uni['Pros']}\nCons: {uni['Cons']}\n"
        result_text += f"Study Path: {path_info.get(career, 'N/A')}\n\n"

    st.download_button("📄 Download My Career Report", result_text, "career_report.txt")

st.markdown("---")
st.markdown("<p style='text-align:center;'>💖 Built for Malaysian students with love</p>", unsafe_allow_html=True)
