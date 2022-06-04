import hazm


class StopWords:
    stopwords_list = []

    def __init__(self):
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = BASE_DIR + "/tools/stopwords_all.txt"
        stopword_file = open(file_path, 'r')

        for stop_word in stopword_file:
            self.stopwords_list.append(str(stop_word))

    def is_stop_word(self, word):
        for stop_word in self.stopwords_list:
            if str(stop_word).strip() == str(word).strip():
                return True
        return False

    def remove_stop_words_of_sentences(self, sentences: str):
        words = []
        for sent in hazm.sent_tokenize(sentences):
            for word in hazm.word_tokenize(sent):
                if not self.is_stop_word(word):
                    words.append(word)
        return " ".join(words)
