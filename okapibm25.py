from math import log
from constants import TOTAL_DOCUMENT_COUNT, BM25_K_PARAM, BM25_B_PARAM, PREPROCESSED_AVG_DOC_LENGTH
from FreqDict import FreqDict

def idf(term: str, global_term_freq: int) -> float:
    """
    Computes the inverse document frequency (IDF) score for a given term using BM25 formulation.

    Parameters:
        term (str): The term for which to calculate IDF.
        global_term_freq (int): The number of documents containing the term.

    Returns:
        float: The IDF score for the term.
    """
    numerator = TOTAL_DOCUMENT_COUNT - global_term_freq + 0.5
    denominator = global_term_freq + 0.5
    return log((numerator / denominator) + 1)

def bm25(inverted_index: dict[str, FreqDict], doc_lengths: dict[int, int], document_id: int, term: str) -> float:
    """
    Computes the BM25 relevance score for a given document and query term.

    Parameters:
        inverted_index (dict[str, FreqDict]): Inverted index mapping terms to their statistics.
        doc_lengths (dict[int, int]): Mapping of document IDs to their respective lengths.
        document_id (int): ID of the document being scored.
        term (str): The (stemmed) term for which to compute the score.

    Returns:
        float: The BM25 score of the term in the specified document.
    """
    term_idf = idf(term, inverted_index[term].globaL_doc_freq)
    term_count_in_doc = sum(inverted_index[term].data[document_id][0])

    numerator = term_count_in_doc * (BM25_K_PARAM + 1)
    denominator = term_count_in_doc + BM25_K_PARAM * (1 - BM25_B_PARAM + BM25_B_PARAM * (doc_lengths[document_id] / PREPROCESSED_AVG_DOC_LENGTH))

    return term_idf * (numerator / denominator)