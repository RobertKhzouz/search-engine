from math import sqrt
from constants import MAX_ITERATIONS, DAMPING_FACTOR as D

def dot_product(v1: dict[str, float], v2: dict[str, float]) -> float:
    """Computes dot product between two sparse vectors, only multiplying their identical values"""
    return sum(v1[term] * v2[term] for term in v1 if term in v2)


def norm_calculation(v: dict[str, float]) -> float:
    """Computes norm calculation for a vector. Needed for cosine similarity calculation"""
    return sqrt(sum(weight * weight for weight in v.values()))


def cosine_sim(v1: dict[int, float], v2: dict[int, float]) -> float:
    """Computes cosine similarity between two vectors"""
    return dot_product(v1, v2) / (norm_calculation(v1) * norm_calculation(v2) + 1e-8)
    

def calculate_cosine_sims(vectors: dict[int, dict[str, float]], k: int) -> dict[int, list[tuple[int, float]]]:
    """Stores only the top k highest cosine-sim scores for each document"""

    top_k = {}

    doc_ids = list(vectors.keys())

    for i in doc_ids:
        sims = []
        for j in doc_ids:
            if i == j:
                continue
            sim = cosine_sim(vectors[i], vectors[j])
            sims.append((j, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        top_k[i] = sims[:k]

    return top_k


def pagerank(cosine_similarities, max_iter=MAX_ITERATIONS, tol=1e-6):
    """Computes PageRank of documents"""
    docs = list(cosine_similarities.keys())
    N = len(docs)
    ranks = {doc: 1.0 / N for doc in docs}

    for _ in range(max_iter):
        new_ranks = {}
        for doc in docs:
            incoming_sum = 0
            for other_doc in docs:
                neighbors = cosine_similarities.get(other_doc, [])
                weight_sum = sum(score for _, score in neighbors) or 1
                for neighbor, score in neighbors:
                    if neighbor == doc:
                        incoming_sum += (ranks[other_doc] * score) / weight_sum
            new_ranks[doc] = (1 - D) / N + D * incoming_sum

        # Check convergence
        if all(abs(new_ranks[doc] - ranks[doc]) < tol for doc in docs):
            break
        ranks = new_ranks

    return ranks