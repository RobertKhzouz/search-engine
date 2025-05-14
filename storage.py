import os
import pickle
from copy import deepcopy
from constants import PICKLE_PATH_DOC_LENGTHS, PICKLE_PATH_INVERTED_INDEX, PICKLE_PATH_VECTORS
from FreqDict import FreqDict

def load_inverted_index() -> dict[str, FreqDict]:
    """Finds inverted index pickle if it exists, loading and decompressing it"""

    if os.path.exists(PICKLE_PATH_INVERTED_INDEX):
        print("Loading Inverted Index...")
        with open(PICKLE_PATH_INVERTED_INDEX, "rb") as pickler_ii:

            compressed_inverted_index: dict[str, FreqDict] = pickle.load(pickler_ii)

            for term in compressed_inverted_index:
                compressed_inverted_index[term].decompress_data()
            
            # Returns the decompressed inverted index (return variable name is misleading)
            return compressed_inverted_index

    else:
        return dict()
    

def save_inverted_index(inverted_index: dict[str, FreqDict]) -> None:
    """Compresses and pickles inverted index, saving it to disk for reuse. 
    
    Compression is done on a deep copy to prevent modification of the original index, which might still be needed for immediate use after this function runs
    """
    inverted_index_copy = deepcopy(inverted_index)

    for freq_dict in inverted_index_copy.values():
        freq_dict.compress_data()

    with open(PICKLE_PATH_INVERTED_INDEX, "wb") as pickle_ii:
        pickle.dump(inverted_index_copy, pickle_ii)

    
def load_vectors():
    """Finds vectors pickle if it exists and loads it"""

    if os.path.exists(PICKLE_PATH_VECTORS):
        print("Loading Vectors...")
        with open(PICKLE_PATH_VECTORS, "rb") as pickler_v:
            return pickle.load(pickler_v)
    else:
        return dict()
    

def save_vectors(vectors) -> None:
    """Pickles vectors and saves it to disk for reuse"""

    with open(PICKLE_PATH_VECTORS, "wb") as pickle_v:
        pickle.dump(vectors, pickle_v)
    

def load_doc_lengths():
    """Finds document lengths pickle if it exists and loads it"""

    if os.path.exists(PICKLE_PATH_DOC_LENGTHS):
        print("Loading Document Lengths...")
        with open(PICKLE_PATH_DOC_LENGTHS, "rb") as pickler_dl:
            return pickle.load(pickler_dl)
    else:
        return dict()
    

def save_doc_lengths(doc_lengths) -> None:
    """Pickles document lengths and saves it to disk for reuse"""
    
    with open(PICKLE_PATH_DOC_LENGTHS, "wb") as pickle_dl:
        pickle.dump(doc_lengths, pickle_dl)