# Search Engine (Python)

> ⚠️ **Academic Integrity Notice**  
> This repository contains only a very small subset of the full text corpus originally used, in order to comply with university academic integrity policies.

---

## Overview

This is a custom-built information retrieval engine that processes a corpus of documents and ranks them based on query relevance. It implements several key IR techniques including:

- **Inverted Index construction**
- **Okapi BM25** scoring
- **Cosine-Similarity-based PageRank**
- **Delta Compression via Gamma Encoding**
- **Lightweight Stemming using Regex**
- **Serialization via Pickle for reuse across sessions**

The engine is optimized for document scoring accuracy and indexing efficiency, and supports query-time ranking using a hybrid BM25-PageRank approach.

---

## Features

- 🔍 **Fast and accurate querying** using Okapi BM25  
- 📈 **PageRank simulation** based on document cosine similarity  
- 📦 **Delta-Gamma Compression** for space-efficient disk storage  
- 🧠 **TF-IDF vectorization** for similarity modeling  
- 🔁 **Persistent storage** via Pickle to avoid repeated preprocessing  
- 🧹 **Custom Regex-based stemming** (no external NLP libraries)

---

## Installation

```bash
git clone https://github.com/RobertKhzouz/search-engine.git
cd search-engine
python3 -m venv .venv
source .venv/bin/activate
```

---

## Usage
To launch the query engine, run:
```python
python engine_query.py
```
You will be prompted with:
```bash
QUERY:
```
🕒 First run will trigger preprocessing (~30–50 seconds). All future runs will load from serialized .pkl files if present.

---

## Known Issues
❗ Post-Deserialization Query Accuracy Drop

After decompressing serialized .pkl files, query precision may drop. This appears to be related to how document gaps or position gaps are encoded/decoded in the FreqDict class. Results remain functional but slightly less precise. A fix is under investigation.

---

## 🧠 Technical Highlights
BM25 Scoring
BM25 is used to rank query-document matches using:

```bash
score(D,Q) = ∑ IDF(qi) * ((f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D| / avgdl)))
```
Where:
```bash
f(qi, D) = frequency of term qi in document D
|D| = document length
avgdl = average document length
k1 = 1.2, b = 0.75 (tunables)
```

Cosine Similarity PageRank
Cosine similarity is used to build a semantic graph of documents (top-K neighbors per doc). PageRank is applied to this graph:
```bash
R(t+1) = d * M * R(t) + (1 - d)/N
M = cosine similarity matrix
d = damping factor (0.85 default)
```

Top-ranked document adjusted as:

```bash
score(doc) = α * BM25 + (1 - α) * PageRank
```

---

## 📂 File Structure
```text
├── engine_query.py                  # Main driver script
├── FreqDict.py                      # Custom inverted index entry class
├── okapibm25.py                     # Okapi BM25 scoring logic
├── pagerank.py                      # Cosine similarity + PageRank implementation
├── compressions.py                  # Gamma encoding/decoding functions
├── storage.py                       # Handles saving/loading large IR data
├── constants.py                     # Shared constants (tunable)
├── tiny_wikipedia.txt               # Sample corpus (limited subset)
├── preprocessed_inverted_index.pkl  # Serialized inverted index
├── vectors.pkl                      # Document TF-IDF vectors
├── doc_lengths.pkl                  # Document length mapping
```

---

## 🧪 Requirements
Python 3.13+

RAM: 8 GB recommended

IDE: Visual Studio Code (recommended)

Platform: MacBook M1 (tested)

---

## 💡 Tuning
You may customize relevance scoring in constants.py:

ALPHA – balance BM25 vs PageRank (0.0–1.0)

BM25_K_PARAM, BM25_B_PARAM – control BM25 aggressiveness

OUT_DEGREE – top-K cosine similarity edges for PageRank (higher = slower)

---

## 🔐 License & Usage
This project is provided for academic demonstration only. Please do not copy or redistribute without permission.
If you are an instructor or evaluator reviewing this work, feel free to reach out via email for clarification or demonstration.

---
