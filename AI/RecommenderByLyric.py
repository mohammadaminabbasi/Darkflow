import json
import math
from ast import literal_eval

import hazm
import tomotopy as tp

from songsapi.models import DFSong


class RecommenderByLyric:
    topic_counts = 4
    word_topic_show = 15
    model_path = "/home/koalamin/DarkFlow/Darkflow-Django-df/AI/lda_model.bin"
    mdl = tp.LDAModel.load(model_path)

    topic_map = {0: "گنگ",
                 1: "غمگین",
                 2: "شاد"}

    def distance_two_lyric_statics(self, lyric1: str, lyric2: str):
        static_lyric1 = self.test(lyric1)
        static_lyric2 = self.test(lyric2)
        distance = math.dist(static_lyric1, static_lyric2)
        return distance

    def test(self, lyric):
        doc = []
        lyric = lyric.split("\n")
        for line in lyric:
            for word in line.strip().split():
                doc.append(word)

        doc_inst = self.mdl.make_doc(doc)
        topic_dist, ll = self.mdl.infer(doc_inst)
        return list(topic_dist)

    def calculate_distance_lyrical(self, song_ids):
        distance_maps = []
        main_song = DFSong.objects.filter(pk=song_ids[0])[0]
        for suggested_song_df in song_ids:
            second_song = DFSong.objects.filter(pk=suggested_song_df)[0]
            if second_song.lyric is not "" and main_song.lyric is not "":
                distance_two_lyrics = self.distance_two_lyric_statics(str(' '.join(literal_eval(main_song.tokens))),
                                                                      str(' '.join(literal_eval(second_song.tokens))))
                distance_map = {"song": suggested_song_df, "distance": distance_two_lyrics}
                distance_maps.append(distance_map)
            else:
                distance_map = {"song": suggested_song_df, "distance": 100}
                distance_maps.append(distance_map)
        sorted_distance_maps = sorted(distance_maps, key=lambda d: d["distance"])
        sorted_songs = [d["song"] for d in sorted_distance_maps]
        return sorted_songs
