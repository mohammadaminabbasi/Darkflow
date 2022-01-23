#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from werkzeug.datastructures import FileStorage
from .model import ModelWrapper


class ModelPredictAPI:
    model_wrapper = ModelWrapper()

    def create_embedding(self, wav_path):
        """Generate audio embedding from input data"""
        result = {'status': 'error'}

        fp = open(wav_path, 'rb')
        file = FileStorage(fp)

        audio_data = file.read()
        print("audio_data")

        # Getting the predictions
        preds = self.model_wrapper.predict(audio_data)

        # Aligning the predictions to the required API format
        result['embedding'] = preds.tolist()
        result['status'] = 'ok'

        return result
