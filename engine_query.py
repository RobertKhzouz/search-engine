from FreqDict import FreqDict
from constants import TOKENIZATION_REGEX, SUFFIX_REGEX, PREFIX_REGEX, STOPWORDS_REGEX, OUT_DEGREE, MAX_ITERATIONS, ALPHA
from okapibm25 import bm25
from pagerank import calculate_cosine_sims, pagerank
from storage import load_doc_lengths, load_inverted_index, load_vectors, save_doc_lengths, save_inverted_index, save_vectors

inverted_index: dict[str, FreqDict] = {}
doc_lengths: dict[int, int] = {}
vectors: dict[int, dict[str, float]] = {}

def main():
    global vectors, inverted_index, doc_lengths
    vectors = {}
    inverted_index = {}
    doc_lengths = {}

    with open("tiny_wikipedia.txt", "r") as file:

        # Either load all of them, or reset all of them
        inverted_index = load_inverted_index()
        vectors = load_vectors()
        doc_lengths = load_doc_lengths()

        # First preprocess run
        if not inverted_index or not vectors or not doc_lengths:
            print("First Run, Preprocessing...")

            # Reset all before preprocessing just in case one of them does in fact exist
            inverted_index = {}
            vectors = {}
            doc_lengths = {}

            documents = file.readlines()
            doc_index = 0
            for doc in documents:
                vectors[doc_index] = {}
                doc_lengths[doc_index] = len(doc)

                # Skip http link
                index = 0
                while True:
                    if doc[index] == " ":
                        break
                    index += 1

                tokenized_sentence = TOKENIZATION_REGEX.findall(doc[index:])

                word_pos = 0
                for token in tokenized_sentence:

                    tokenl = token.lower()

                    # Remove prefix and suffix as long as the new modified token isn't empty
                    mod_tokenl = PREFIX_REGEX.sub("", tokenl)
                    mod_tokenl = SUFFIX_REGEX.sub("", mod_tokenl)
                    if mod_tokenl == "":
                        mod_tokenl = tokenl
                    tokenl = mod_tokenl

                    if STOPWORDS_REGEX.fullmatch(tokenl):
                        word_pos += 1
                        continue

                    weight = 1

                    # Term hasn't been found before at all
                    if tokenl not in inverted_index:
                        inverted_index[tokenl] = FreqDict(1, 1, {doc_index : [[word_pos], weight]})
                        vectors[doc_index][tokenl] = 1
                        word_pos += 1
                        continue

                    # Term has been found but not in this document
                    elif doc_index not in inverted_index[tokenl].data:
                        inverted_index[tokenl].add_data(doc_index, word_pos, weight)
                        vectors[doc_index][tokenl] = 1
                        continue

                    # Term has been found in this document before
                    weight = len(inverted_index[tokenl].data[doc_index][0]) + 1
                    inverted_index[tokenl].add_data(doc_index, word_pos, weight)
                    vectors[doc_index][tokenl] += 1

                    word_pos += 1
                
                doc_index += 1


            # If there is no preprocessed inverted index stored, then it is serialized
            save_inverted_index(inverted_index)

            # If there is no preprocessed vectors stored, then it is serialized
            save_vectors(vectors)

            # If there is no preprocessed doc lengths stored, then it is serialized
            save_doc_lengths(doc_lengths)


    while True:
        query_terms = input("QUERY (type ~escape to quit): ").strip().lower().split()

        if query_terms[0] == "~escape":
            break


        scores: dict[int, float] = {}
        for term in query_terms:

            mod_term = PREFIX_REGEX.sub("", term)
            mod_term = SUFFIX_REGEX.sub("", mod_term)
            if mod_term == "":
                mod_term = term
                term = mod_term
            term = mod_term
            
            if term not in inverted_index:
                continue
            for doc_id in inverted_index[term].data:
                score = bm25(inverted_index, doc_lengths, doc_id, term)
                if doc_id not in scores:
                    scores[doc_id] = score
                else:
                    scores[doc_id] += score

        if not scores:
            print("No results found")
            continue

        # Get the top BM25 documents
        top_k_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:MAX_ITERATIONS]

        # Get all the doc ids
        doc_ids = [doc for doc, _ in top_k_docs]
        
        # Each doc id maps to its vector
        subset_vectors = {doc: vectors[doc] for doc in doc_ids}

        # PageRank and Cosine Similarity calculations
        cosine_sim_graph = calculate_cosine_sims(subset_vectors, k=OUT_DEGREE)
        pr_scores = pagerank(cosine_sim_graph)

        # Get the best BM25 score
        max_bm25 = max(scores[doc] for doc in doc_ids)

        # Normalize scores by dividing each by the best
        normalized_bm25 = {doc: scores[doc] / max_bm25 for doc in doc_ids}

        # Final combined output
        # a * bm25 + (1 - a) * pagerank
        combined_scores = {}
        for doc in doc_ids:
            if doc in normalized_bm25:
                bm25_score = normalized_bm25[doc]
            else:
                bm25_score = 0
            
            if doc in pr_scores:
                pr = pr_scores[doc]
            else:
                pr = 0
            combined_scores[doc] = ALPHA * bm25_score + (1 - ALPHA) * pr

        best_doc = max(combined_scores, key=combined_scores.get, default="EMPTY")
        with open("tiny_wikipedia.txt", "r", encoding="utf-8") as file:
            for current_line_num, line in enumerate(file):
                if current_line_num == best_doc:
                    print(f"LINE [{best_doc}]: {line.strip()}")
                    break

if __name__ == "__main__":
    main()