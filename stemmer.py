# NOTE: This file/stemmer isn't being used. It was created initially for improved stemming but was a poor implementation

import constants

class Stemmer:

    def stem(self, term):
        """ Term should be passed in as lowercase """
        stem = self._porter_S1(term)
        stem = self._porter_S2(stem)
        stem = self._porter_S3(stem)
        stem = self._porter_S4(stem)
        return self._porter_S5(stem)

    def _letter_grouping(self, term):
        """ Term should be passed in as lowercase """
        groups = []
        prev = ""
        end_index = len(term) - 1

        i = 0
        for letter in term:
            # First letter
            if not prev:
                prev = letter
            else:
                # Vowel-vowel or consonant-consonant
                if self._same_lettertype(prev, letter):
                    prev += letter
                    if i == end_index:
                        groups.append(prev)
                else:
                    groups.append(prev)
                    prev = letter
                    if i == end_index:
                        groups.append(letter)
            i += 1
        return groups

    def _same_lettertype(self, let1, let2):
        consonants = constants.CONSONANTS
        vowels = constants.VOWELS
        if let1 in consonants and let2 in consonants:
            return True
        elif let1 in vowels and let2 in vowels:
            return True
        return False
    
    def _get_lettertype(self, group): 
        return "V" if group[0] in constants.VOWELS else "C"
    
    # Converts each letter group to corresponding group type (either "C" or "V")
    def _encode(self, word) -> list:
        groups = self._letter_grouping(word)
        return [self._get_lettertype(group) for group in groups]
    
    def _get_measure(self, word):
        types = self._encode(word)
        if len(types) <= 1:
            return 0
        
        # ignores optional beginning consonant
        if types[0] == "C":
            types = types[1:]
        
        # ignores optional ending vowel
        if types[-1] == "V":
            types = types[:len(types)-1]

        return len(types) // 2 if (len(types) / 2) >= 1 else 0

    def _condition_s(self, stemmed_word, letter_str):
        for letter in letter_str:
            if stemmed_word.endswith(letter):
                return True
        return False
    
    def _condiition_v(self, stemmed_word):
        for letter in stemmed_word:
            if letter in constants.VOWELS:
                return True
        return False
    
    def _condition_d(self, stemmed_word):
        if stemmed_word[-1] in constants.CONSONANTS and stemmed_word[-2] in constants.CONSONANTS:
            return True
        return False
    
    def _condition_o(self, stemmed_word):
        if len(stemmed_word) <= 2:
            return False
        
        # String ends in CVC Pattern except W, X, and Y
        if (stemmed_word[-3] in constants.CONSONANTS) and (stemmed_word[-2] in constants.VOWELS) and (stemmed_word[-1] in constants.CONSONANTS) and (stemmed_word[-1] not in "wxy"):
            return True
        else:
            return False
        
    def _porter_S1(self, word):
        stemmed_word = word
        stepb2 = False

        if stemmed_word.endswith("sses"):
            stemmed_word = stemmed_word[:-2]
        elif stemmed_word.endswith("ies"):
            stemmed_word = stemmed_word[:-2]
        elif not stemmed_word.endswith("ss") and stemmed_word.endswith("s"):
            stemmed_word = stemmed_word[:-1]
        
        if len(stemmed_word) >= 5:
            if stemmed_word.endswith("eed") and self._get_measure(stemmed_word) > 0:
                stemmed_word = stemmed_word[:-1]
            elif stemmed_word.endswith("ed"):
                stemmed_word = stemmed_word[:-2]
                if not self._condiition_v(stemmed_word):
                    stemmed_word = word
                else:
                    stepb2 = True
            elif stemmed_word.endswith("ing"):
                stemmed_word = stemmed_word[:-3]
                if not self._condiition_v(stemmed_word):
                    stemmed_word = word
                else:
                    stepb2 = True
        
        if stepb2:
            if stemmed_word.endswith("at") or stemmed_word.endswith("bl") or stemmed_word.endswith("iz"):
                stemmed_word += "e"
            elif self._condition_d(stemmed_word) and not (self._condition_s(stemmed_word, "lsz")):
                stemmed_word = stemmed_word[:-1]
            elif self._get_measure(stemmed_word)==1 and self._condition_o(stemmed_word):
                stemmed_word += "e"

        if self._condiition_v(stemmed_word) and stemmed_word.endswith("y"):
            stemmed_word = stemmed_word[:-1] + "i"

        return stemmed_word

    def _porter_S2(self, stemmed_word):
        if self._get_measure(stemmed_word) >= 1:
            for term, stm in constants.PAIRS_S2:
                if stemmed_word.endswith(term):
                    return stemmed_word[:-len(term)] + stm
        return stemmed_word

    def _porter_S3(self, stemmed_word):
        if self._get_measure(stemmed_word) >= 1:
            for term, stm in constants.PAIRS_S3_S4:
                if stemmed_word.endswith(term):
                    return stemmed_word[:-len(term)] + stm
        return stemmed_word

    def _porter_S4(self, stemmed_word):
        if self._get_measure(stemmed_word) > 1:

            for suf in constants.SUFFIXES_1_S4:
                if stemmed_word.endswith(suf):
                    return stemmed_word[:-len(suf)]
                
            if stemmed_word.endswith(constants.SPECIAL_S4):
                tmp = stemmed_word[:-len(constants.SPECIAL_S4)]
                if self._condition_s(tmp, "st"):
                    return tmp
                
            for suf in constants.SUFFIXES_2_S4:
                if stemmed_word.endswith(suf):
                    return stemmed_word[:-len(suf)]

        return stemmed_word

    def _porter_S5(self, stemmed_word):
        tmp = stemmed_word
        if self._get_measure(tmp) >= 2 and tmp.endswith("e"):
            tmp = tmp[:-1]
        elif self._get_measure(tmp) == 1 and (not self._condition_o(tmp)) and tmp.endswith("e") and len(tmp) >= 5:
            tmp = tmp[:-1]
        if self._get_measure(tmp) >= 2 and self._condition_d(tmp) and self._condition_s(tmp, "l"):
            tmp = tmp[:-1]
        return tmp