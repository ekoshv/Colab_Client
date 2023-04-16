import base64
import io
import json
import requests
import tensorflow as tf

class ColabRemote:
    def __init__(self, colab_api_url):
        self.colab_api_url = colab_api_url

    def execute(self, code, input_data=None):
        if input_data is None:
            input_data = {}

        data = {
            'input_data': input_data,
            'code': code
        }

        try:
            response = requests.post(self.colab_api_url, json=data)
            results = response.json()
            if 'result' in results and results['result'] is not None:
                model_buffer = io.BytesIO(base64.b64decode(results['result'].encode('utf-8')))
                results['result'] = tf.keras.models.load_model(model_buffer)
            return results
        except Exception as e:
            return {'error': str(e)}

    def execute_from_file(self, file_path, input_data=None):
        with open(file_path, 'r') as code_file:
            code = code_file.read()

        if input_data is None:
            input_data = {}

        return self.execute(code, input_data)
