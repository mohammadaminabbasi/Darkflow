import re
from ast import literal_eval

import hazm
from hazm import Lemmatizer

from songsapi.models import DFSong
from tools.StopWords import StopWords

import tomotopy as tp


class LDAModelTraining:
    topic_counts = 4
    word_topic_show = 25

    def __init__(self):
        self.model_path = "./AI/lda_model.bin"
        self.mdl = tp.LDAModel.load(self.model_path)

    def train(self, songs: [DFSong]):
        mdl = tp.LDAModel(k=self.topic_counts)

        for song in songs:
            mdl.add_doc(song.tokens)

        for i in range(0, 1000, 1):
            mdl.train(10)
            print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

        for k in range(mdl.k):
            print('Top 10 words of topic #{}'.format(k))
            print(self.get_words_of_topic(mdl.get_topic_words(k, top_n=self.word_topic_show)))

        mdl.summary()

        self.save_model(mdl)

    def test(self, title: str, lyric: str):
        doc = []
        lyric = lyric.split("\n")
        for line in lyric:
            for word in line.strip().split():
                doc.append(word)

        doc_inst = self.mdl.make_doc(doc)
        topic_dist, ll = self.mdl.infer(doc_inst)
        best_topic_index = list(topic_dist).index(max(topic_dist))
        best_topic_word_list = self.mdl.get_topic_words(best_topic_index, top_n=self.word_topic_show)
        print(title)
        print(f"Best Topic: {self.get_words_of_topic(best_topic_word_list)}")
        print(f"topic: {best_topic_index}")
        print(f"percentage: {round(max(topic_dist), 2)}")
        print("---------------------------------------------------------------------------------")

    def save_model(self, mdl):
        mdl.save(self.model_path)

    def get_words_of_topic(self, topic_words):
        words = []
        for map in topic_words:
            words.append(map[0])

        return words

    def print_topics(self):
        for i in range(0, self.topic_counts):
            print(i, LDAModelTraining().get_words_of_topic(self.mdl.get_topic_words(i, top_n=self.word_topic_show)))

    def delete_all_puncs(self, str):
        res = re.sub(r'[^\w\s]', '', str)
        return res

    def start(self):
        # lyric = ""
        # self.print_topics()
        # self.test("ashvan", lyric)

        songs = DFSong.objects.filter().order_by('-id')
        for i, song in enumerate(songs):
            if song.tokens != '':
                song.tokens = [token for token in literal_eval(str(song.tokens)) if token is not '']
                song.tokens = str(song.tokens)
                song.save()
            """
            if song.lyric != "" and song.tokens == '':
                tokens = []
                lyric = self.delete_all_puncs(song.lyric)
                stop_words = StopWords()
                lyric = stop_words.remove_stop_words_of_sentences(lyric)
                normalizer = hazm.Normalizer()
                lyric = normalizer.normalize(lyric)
                lemmatizer = Lemmatizer()
                for sent in hazm.sent_tokenize(lyric):
                    for word in hazm.word_tokenize(sent):
                        word = word.strip()
                        word = ''.join([i for i in word if not i.isdigit()])
                        if lemmatizer.lemmatize(word).__contains__("#"):
                            tokens.append(lemmatizer.lemmatize(word).split("#")[0])
                        else:
                            tokens.append(word)

                song.tokens = str(tokens)
                song.save()
                """
            print(song.id)
            print(f"{i}/{len(songs)}")

        # lda_model_training = LDAModelTraining()
        # lda_model_training.train(songs)
