import requests
import json
import pickle
from io import BytesIO
from functools import partial
from tqdm import tqdm

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def save_input_data_to_file(self, input_data):
        buffer = BytesIO()
        pickle.dump(input_data, buffer)
        buffer.seek(0)
        return buffer

    def execute(self, code, input_data=None):
        if input_data is None:
            input_data = {}

        input_data_buffer = self.save_input_data_to_file(input_data)

        files = {
            'input_data': ('input_data.pickle', input_data_buffer, 'application/octet-stream')
        }

        with tqdm(total=input_data_buffer.getbuffer().nbytes, unit='B', unit_scale=True, desc="Uploading data") as pbar:
            response = requests.post(self.colab_api_url, data={'code': code}, files=files, stream=True, hooks={'response': partial(self.progress_bar(pbar))})
            results = response.json()
            return results

    def progress_bar(self, pbar):
        def update_to(r, **kwargs):
            if r.headers.get('content-length'):
                pbar.total = int(r.headers['content-length'])
            pbar.update(len(r.content))
        return update_to

    def execute_from_file(self, file_path, input_data=None):
        with open(file_path, 'r') as code_file:
            code = code_file.read()

        if input_data is None:
            input_data = {}

        return self.execute(code, input_data)
