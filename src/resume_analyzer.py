from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (outside function)
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_score(job_desc, resume_text):
    
    if not job_desc.strip() or not resume_text.strip():
        return 0.0

    # Generate embeddings
    embeddings = model.encode(
        [job_desc, resume_text],
        convert_to_numpy=True,
        normalize_embeddings=True  # Important!
    )

    # Cosine similarity manually (faster)
    similarity = np.dot(embeddings[0], embeddings[1])

    return float(similarity)