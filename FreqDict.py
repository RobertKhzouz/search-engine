from compressions import gamma_decode, gamma_encode

class FreqDict:
    """
    FreqDict tracks statistics for a specific term across a corpus.

    Attributes:
        global_doc_freq (int): Number of documents in which the term appears at least once.
        global_term_freq (int): Total number of times the term appears across all documents.
        data (dict[int, list]): A mapping from document ID to a list where:
            - The first element is a list of positional indices where the term appears in the document.
            - The second element is the term frequency in that document (currently unused).
    """
    
    def __init__(self, global_doc_freq, global_term_freq, data=None, word_code=-1):
        self._global_doc_freq = global_doc_freq
        self._global_term_freq = global_term_freq
        self._data = data if data is not None else {}
        self._word_code = word_code

    def __getstate__(self):
        return {
            "_global_doc_freq": self._global_doc_freq,
            "_global_term_freq": self._global_term_freq,
            "_data": self._data,
            "_word_code": self._word_code
        }

    def __setstate__(self, state):
        self._global_doc_freq = state["_global_doc_freq"]
        self._global_term_freq = state["_global_term_freq"]
        self._data = state["_data"]
        self._word_code = state["_word_code"]

    @property
    def globaL_doc_freq(self):
        return self._global_doc_freq

    @property
    def global_term_freq(self):
        return self._global_term_freq
    
    @property
    def data(self):
        return self._data
    
    @property
    def word_code(self):
        return self._word_code
    
    @globaL_doc_freq.setter
    def global_doc_freq(self, val):
        """ Not type safe, only pass int """
        self._global_doc_freq = val
    
    @global_term_freq.setter
    def global_term_freq(self, val):
        """ Not type safe, only pass int """
        self._global_term_freq = val

    @word_code.setter
    def word_code(self, val):
        """ Not type safe, only pass int """
        self._word_code = val

    def add_data(self, doc, index, weight=0):
        if doc not in self._data:
            self._data[doc] = [[index], weight]
            self.increment_global_doc_freq()
        else:
            self._data[doc][0].append(index)
            self._data[doc][1] = weight
        self.increment_global_term_freq()

    def increment_global_term_freq(self, amount=1):
        self.global_term_freq += amount

    def increment_global_doc_freq(self, amount=1):
        self.global_doc_freq += amount

    def compress_data(self):
        """Compress the term's doc_ids and indexes before pickling"""
        
        compressed_data = {}

        # Compress doc_ids
        prev_doc = 0
        for doc_id in sorted(self._data):
            doc_gap = (doc_id - prev_doc) + 1
            prev_doc = doc_id

            weight = self._data[doc_id][1]

            # Compress indexes
            gap_indexes = []
            prev_index = 0
            for index in sorted(self._data[doc_id][0]):
                index_gap = (index - prev_index) + 1
                prev_index = index
                
                gap_indexes.append(index_gap)
            
            # Gamma encode indexes and doc gaps
            gamma_positions = []
            for gap_i in gap_indexes:
                gamma_positions.append(gamma_encode(gap_i))

            compressed_data[gamma_encode(doc_gap)] = [gamma_positions, weight]
    
        self._data = compressed_data

    def decompress_data(self):
        """Decompress the doc_ids and indexes after loading pickle"""
        decompressed_data = {}

        prev_doc = 0
        for gamma_doc, (gamma_positions, weight) in self._data.items():
            doc_gap = gamma_decode(gamma_doc)
            doc_id = (prev_doc + doc_gap) - 1
            prev_doc = doc_id

            positions = []
            prev_pos = 0
            for gamma_pos in gamma_positions:
                pos_gap = gamma_decode(gamma_pos)
                pos = (prev_pos + pos_gap) - 1
                positions.append(pos)
                prev_pos = pos

            decompressed_data[doc_id] = [positions, weight]

        self._data = decompressed_data