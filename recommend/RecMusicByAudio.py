import itertools
import json
import os

import requests
from pydub import AudioSegment
from annoy import AnnoyIndex
from radiojavanapi import Client
from embedding.core import ModelPredictAPI
from recommend.models import SongEmbedding


class RecMusicByAudio:
    def __init__(self):
        self.audio_dim = 128 * 177
        self.root_path = "musics_rj"
        self.graph_name = "graph_rec.ann"

    def __download_mp3(self, song_id):
        print("__download_mp3")
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        file_path = f"{self.root_path}/{song_id}.mp3"
        client = Client()
        r = requests.get(client.get_song_by_id(song_id).link, allow_redirects=True)
        open(f"{file_path}", 'wb').write(r.content)
        return file_path

    def __convert_to_wav(self, mp3_file):
        print("__convert_to_wav")
        three_micro_second = 3 * 60 * 1000
        sound = AudioSegment.from_mp3(mp3_file)
        wav_file_path = mp3_file.replace(".mp3", ".wav")

        if len(sound) < three_micro_second:
            sec_silence = AudioSegment.silent(duration=(three_micro_second - len(sound)))
            sound = sound + sec_silence

        sound = sound[10 * 1000:three_micro_second]
        print(len(sound))
        sound.export(wav_file_path, format="wav")
        os.remove(mp3_file)
        return wav_file_path

    def __convert_to_embedding(self, wav_path):
        print("convert_to_embedding")
        predict_api = ModelPredictAPI()
        result = predict_api.create_embedding(wav_path)
        current_embedding = result['embedding']
        merged_embedding = list(itertools.chain(*current_embedding))
        return merged_embedding

    def __create_annoy_rec_system(self, music_models: [SongEmbedding]):
        print("create_annoy_rec_system")
        print(len(music_models))
        annoy_index = AnnoyIndex(self.audio_dim, 'angular')  # Length of item vector that will be indexed
        for index, music_model in enumerate(music_models):
            vector = music_model.embedding
            annoy_index.add_item(index, vector)

        annoy_index.build(50)  # 50 trees
        annoy_index.save(self.root_path + "/" + self.graph_name)
        return annoy_index

    def __load_annoy_model(self):
        annoy_index = AnnoyIndex(self.audio_dim, 'angular')
        annoy_index.load(self.root_path + "/" + self.graph_name)
        return annoy_index

    def __get_recommended_musics(self, annoy_model, index):
        nns_index = annoy_model.get_nns_by_item(int(index), 10)
        return nns_index

    def recommend_by_embedding(self, song_id):
        if not SongEmbedding.objects.all().filter(pk=song_id).exists():
            mp3_file_path = self.__download_mp3(song_id)
            wav_file_path = self.__convert_to_wav(mp3_file_path)
            merged_embedding_result = self.__convert_to_embedding(wav_file_path)
            SongEmbedding(SongEmbedding.objects.count(), song_id, merged_embedding_result).save()


        annoy_model = self.__create_annoy_rec_system(SongEmbedding.objects.all())
        predicted_ids = self.__get_recommended_musics(annoy_model, SongEmbedding.objects.get(pk=song_id).row_number)
        return predicted_ids
