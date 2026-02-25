import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ---------------- NAME ----------------
def extract_name(text):
    doc = nlp(text[:1000])  # Only first part
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return "Not Found"


# ---------------- EMAIL & PHONE ----------------
def extract_contact(text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"\+?\d[\d\s\-().]{8,}\d"

    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)

    email = email[0] if email else "Not Found"
    phone = phone[0] if phone else "Not Found"

    return email, phone


# ---------------- EDUCATION (Section Based) ----------------
def extract_education(text):

    degrees_keywords = [
        "b.tech", "m.tech", "bachelor", "master",
        "b.e", "m.e", "bsc", "msc", "mba",
        "phd", "doctorate"
    ]

    education_section = ""
    match = re.search(r"(education[\s\S]*?)(experience|skills|projects|certifications|$)", text, re.IGNORECASE)
    
    if match:
        education_section = match.group(1)

    found_degrees = []

    for degree in degrees_keywords:
        if degree.lower() in education_section.lower():
            found_degrees.append(degree.upper())

    return list(set(found_degrees)) if found_degrees else ["Not Found"]


# ---------------- SKILLS (STRICT SECTION BASED) ----------------
def extract_skills(text):

    skills_section = ""

    # Extract only skills section
    match = re.search(r"(skills[\s\S]*?)(experience|education|projects|certifications|$)", text, re.IGNORECASE)
    
    if match:
        skills_section = match.group(1)
    else:
        return ["Not Found"]

    # Clean bullets & special chars
    skills_section = re.sub(r"[^a-zA-Z0-9,+#.\s]", " ", skills_section)

    # Split by comma or newline
    raw_skills = re.split(r",|\n", skills_section)

    cleaned_skills = []
    stopwords = {
        "skills", "experience", "education", "years",
        "professional", "summary", "location", "email",
        "phone", "project"
    }

    for skill in raw_skills:
        skill = skill.strip()

        # Remove numbers
        if any(char.isdigit() for char in skill):
            continue

        # Remove small words
        if len(skill) < 3:
            continue

        # Remove stopwords
        if skill.lower() in stopwords:
            continue

        # Remove if it contains too many words (junk sentence)
        if len(skill.split()) > 3:
            continue

        cleaned_skills.append(skill.title())

    # Remove duplicates
    cleaned_skills = list(set(cleaned_skills))

    return cleaned_skills if cleaned_skills else ["Not Found"]