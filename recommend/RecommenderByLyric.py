import math

import hazm
import tomotopy as tp


class RecommenderNLP:
    topic_counts = 3
    word_topic_show = 15
    model_path="../recommend/lda_model.bin"
    mdl = tp.LDAModel.load("/home/koalamin/1.Programming/df/recommend/lda_model.bin")

    topic_map = {0: "گنگ",
                 1: "غمگین",
                 2: "شاد"}

    def distance_two_lyric_statics(self, lyric1: str, lyric2: str):
        normalizer = hazm.Normalizer()
        lyric1 = normalizer.normalize(lyric1)
        lyric2 = normalizer.normalize(lyric2)
        static_lyric1 = self.test(lyric1)
        static_lyric2 = self.test(lyric2)
        distance = math.dist(static_lyric1, static_lyric2)
        print(distance)
        return distance

    def test(self, lyric: str):
        doc = []
        lyric = lyric.split("\n")
        for line in lyric:
            for word in line.strip().split():
                doc.append(word)

        doc_inst = self.mdl.make_doc(doc)
        topic_dist, ll = self.mdl.infer(doc_inst)
        return list(topic_dist)
