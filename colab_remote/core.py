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

    def execute(self, code, input_data=None):
        """
        Execute code on the Colab API and return the result.
        :param code: The code to be executed on the Colab API.
        :param input_data: The input data for the code execution.
        :return: The result of the code execution.
        """
        if input_data is None:
            input_data = {}

        input_data_buffer = self.save_input_data_to_file(input_data)

        files = {
            'input_data': ('input_data.pickle', input_data_buffer, 'application/octet-stream')
        }

        with tqdm(total=input_data_buffer.getbuffer().nbytes, unit='B', unit_scale=True, desc="Uploading data") as pbar:
            response = requests.post(self.colab_api_url, data={'code': code}, files=files, stream=True, hooks={'response': partial(self.progress_bar(pbar))})
            
            if response.status_code == 200:
                result = pickle.load(BytesIO(response.content))
                return result
            else:
                return {'error': f'Request failed with status code {response.status_code}'}

    def save_input_data_to_file(self, input_data):
        """
        Save input data as a pickle file.
        :param input_data: The input data to be saved.
        :return: A BytesIO buffer containing the input data file.
        """
        input_data_buffer = BytesIO()
        pickle.dump(input_data, input_data_buffer)
        input_data_buffer.seek(0)
        return input_data_buffer

    def progress_bar(self, pbar):
        """
        Create a progress bar callback for the requests library.
        :param pbar: The tqdm progress bar instance.
        :return: The update_to callback function for the progress bar.
        """
        def update_to(num_bytes):
            nonlocal pbar
            pbar.update(num_bytes)

        return update_to

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
