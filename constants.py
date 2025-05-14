from re import compile

TOKENIZATION_REGEX = compile(r"\b\w+\b")
PREFIX_REGEX = compile(r"^(counter|circum|contra|hetero|pseudo|extra|hyper|infra|inter|intra|macro|micro|milli|multi|quasi|retro|super|supra|trans|ultra|under|ante|anti|auto|down|fore|hemi|homo|mega|meta|mini|mono|omni|over|para|peri|poly|post|semi|tele|abs|bio|com|con|dia|dis|eco|geo|mal|mid|mis|neo|non|out|pan|pre|pro|sub|syn|tri|uni|ab|ad|af|ag|al|an|ap|ar|as|at|be|bi|by|co|de|ef|en|ex|il|im|in|ir|re|un|up|a|e)")
SUFFIX_REGEX = compile(r"(izations|ization|ables|ibles|ances|ences|ettes|hoods|icals|ments|ships|sions|somes|tions|tives|ulars|wards|wises|able|ible|ance|ants|arys|ates|bles|doms|ence|ents|ests|ette|fuls|hood|ians|ical|ifys|ings|ions|ishs|isms|ists|itys|ives|izes|less|lets|ment|ness|ship|sion|some|tion|tive|ular|ures|ward|wise|acs|als|ans|ant|ary|ate|ble|cys|dom|eds|ees|ens|ent|ers|est|ful|ian|ics|ify|ing|ion|ish|ism|ist|ity|ive|ize|let|lys|ors|ous|rys|ths|tys|ure|ac|al|an|cy|ed|ee|en|er|es|ic|ly|or|ry|ts|th|ty|ys|t|y|s)$")
STOPWORDS_REGEX = compile(r"^(the|is|to|of|for|on|at|in|with|this|that|by|as|be|if|it|but|from)$")
HTTP_REMOVAL_REGEX = compile(r"^https://en\.wikipedia\.org/wiki\?curid=")
HTTP_GET_ID_REGEX = compile(r"^\d+")

FILEPATH = "wiki2022/"
DICTIONARY_FILENAME = "dictionary.txt"
INDEX_FILE_PREFIX = "index0000"

PICKLE_PATH_INVERTED_INDEX = "inverted_index.pkl"
PICKLE_PATH_VECTORS = "vectors.pkl"
PICKLE_PATH_DOC_LENGTHS = "doc_lengths.pkl"

ALPHA = 0.85

TOTAL_DOCUMENT_COUNT = 50000
BM25_K_PARAM = 1.2
BM25_B_PARAM = 0.75
PREPROCESSED_AVG_DOC_LENGTH = 1725 #1724.92478

DAMPING_FACTOR = 0.85
OUT_DEGREE = 10
MAX_ITERATIONS = 50

CONSONANTS = "bcdfghjklmnpqrstvwxz"
VOWELS = "aeiou"
SPECIAL = "y"

# For original Porter stemmer implementation, please ignore
PAIRS_S2 = [('ational','ate'), ('tional','tion'), ('enci','ence'), ('anci','ance'), ('izer', 'ize'), ('abli','able'), ('alli','al'), ('entli', 'ent'), ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'), ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'), ('ousness', 'ous'), ('aliti','al'), ('ivit', 'ive'), ('biliti','ble')]
PAIRS_S3_S4 = [('icate','ic'), ('ative',''), ('alize','al'), ('iciti','ic'), ('ical','ic'), ('ful',''), ('ness','')]
SUFFIXES_1_S4 = ['al','ance','ence','er','ic','able','ible','ant','ement','ment','ent']
SUFFIXES_2_S4 = ['ou','ism','ate','iti','ous','ive','ize']
SPECIAL_S4 = "ion"