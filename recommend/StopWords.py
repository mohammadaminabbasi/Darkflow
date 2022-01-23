import hazm


class StopWords:
    stopwords_list = []

    def __init__(self):
        file_path = "stopwords_all.txt"
        stopword_file = open(file_path, 'r')

        for stop_word in stopword_file:
            self.stopwords_list.append(str(stop_word))

    def is_stop_word(self, word):
        for stop_word in self.stopwords_list:
            if str(stop_word).strip() == str(word).strip():
                return True
        return False
