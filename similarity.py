from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(job_description, resume_text):
    """
    Calculate semantic similarity between
    Job Description and Resume.

    Returns:
        float (0 - 100)
    """

    # Generate embeddings
    embeddings = model.encode([job_description, resume_text])

    # Cosine similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Convert to percentage
    score = float(round(similarity * 100, 2))

    return score