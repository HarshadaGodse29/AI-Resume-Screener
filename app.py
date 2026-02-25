import streamlit as st
import pandas as pd
import plotly.express as px
from src.pdf_parser import extract_text
from src.extract_info import extract_name, extract_contact, extract_education, extract_skills
from src.resume_analyzer import match_score

# ---------------- Page Config ----------------
st.set_page_config(page_title="AI Resume Screener", layout="wide", initial_sidebar_state="expanded")
st.title("🚀 AI Resume Screener & Analyzer")

# ---------------- Job Description ----------------
job_desc = st.text_area("Paste Job Description Here", height=200)

# ---------------- Upload Resumes ----------------
uploaded_files = st.file_uploader("Upload Resumes (PDF, DOCX, TXT)", accept_multiple_files=True)

# ---------------- Analyze Button ----------------
if st.button("Analyze") and uploaded_files:

    results = []

    for f in uploaded_files:
        text = extract_text(f)
        score = match_score(job_desc, text) * 100
        name = extract_name(text)
        email, phone = extract_contact(text)
        edu = extract_education(text)
        skills = extract_skills(text)

        # Updated Threshold
        if score >= 60:
            relevance = "Highly Relevant"
        elif score >= 40:
            relevance = "Partially Relevant"
        else:
            relevance = "Irrelevant"

        results.append({
            "file": f.name,
            "name": name,
            "email": email,
            "phone": phone,
            "education": ', '.join(edu),
            "skills": ', '.join(skills),
            "score": round(score, 2),
            "relevance": relevance
        })

    df = pd.DataFrame(results).sort_values(by="score", ascending=False).reset_index(drop=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Resumes Uploaded", len(uploaded_files))
    col2.metric("⚡ Average Score", f"{df['score'].mean():.2f}%")
    col3.metric("🏆 Top Score", f"{df['score'].max():.2f}%")
    st.markdown("---")

    st.subheader("🏅 Resume Ranking")
    for i, row in df.iterrows():
        color = "green" if row['relevance']=="Highly Relevant" else "orange" if row['relevance']=="Partially Relevant" else "red"
        st.markdown(f"### {i+1}. {row['name']} ({row['file']})")
        st.write(f"**Email:** {row['email']} | **Phone:** {row['phone']}")
        st.write(f"**Education:** {row['education']} | **Skills:** {row['skills']}")
        st.progress(row['score']/100)
        st.markdown(f"**Relevance Score:** {row['score']}%")
        st.markdown(f"**Relevance:** <span style='color:{color}; font-weight:bold'>{row['relevance']}</span>", unsafe_allow_html=True)
        st.markdown("---")

    st.subheader("📊 Resume Summary Table")
    st.dataframe(df[['file','name','email','phone','education','skills','score','relevance']])

    st.subheader("📈 Summary Visualizations")
    c1, c2 = st.columns(2)

    fig1 = px.bar(df, x='name', y='score', color='relevance',
                  color_discrete_map={'Highly Relevant':'green','Partially Relevant':'orange','Irrelevant':'red'},
                  text='score', title="Resume Match Scores")
    fig1.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig1.update_layout(height=400, yaxis=dict(range=[0,100]))
    c1.plotly_chart(fig1, use_container_width=True)

    relevance_counts = df['relevance'].value_counts().reset_index()
    relevance_counts.columns = ['Relevance','Count']
    fig2 = px.pie(relevance_counts, names='Relevance', values='Count',
                  color='Relevance',
                  color_discrete_map={'Highly Relevant':'green','Partially Relevant':'orange','Irrelevant':'red'},
                  title="Relevance Distribution")
    fig2.update_layout(height=400)
    c2.plotly_chart(fig2, use_container_width=True)

    st.success("✅ Analysis Completed!")