import requests
import json
import pickle
import os
from tqdm import tqdm
from functools import partial

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def save_input_data_to_file(self, input_data):
        file_path = 'input_data.pkl'
        with open(file_path, 'wb') as f:
            pickle.dump(input_data, f)
        return file_path

    def progress_bar(self, pbar):
        def update_to(total_read_len, total_to_read_len):
            pbar.update(total_read_len)
        return update_to

    def execute(self, code, input_data=None):
        """
        Execute code on the Colab API and return the result.
        :param code: The code to be executed on the Colab API.
        :param input_data: The input data for the code execution.
        :return: The result of the code execution.
        """
        if input_data is None:
            input_data = {}

        file_path = self.save_input_data_to_file(input_data)

        with open(file_path, 'rb') as f:
            files = {'input_data': f}
            file_size = os.path.getsize(file_path)
            
            with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="Uploading data") as pbar:
                response = requests.post(self.colab_api_url, data={'code': code}, files=files, stream=True, hooks={'response': partial(self.progress_bar(pbar))})
                results = response.json()
                return results

    def execute_from_file(self, file_path, input_data=None):
        """
        Execute code from a file on the remote Google Colab instance.
        :param file_path: The path to the file containing the code.
        :param input_data: Optional input data to be used in the code execution.
        :return: The result of the code execution.
        """
        with open(file_path, 'r') as code_file:
            code = code_file.read()

        if input_data is None:
            input_data = {}

        return self.execute(code, input_data)
