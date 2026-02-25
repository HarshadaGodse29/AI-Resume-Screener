from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load once (very important)
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_score(job_desc, resume_text):

    if not job_desc.strip() or not resume_text.strip():
        return 0.0

    embeddings = model.encode([job_desc, resume_text])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)