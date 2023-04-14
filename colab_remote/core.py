import requests
import json
from tqdm import tqdm
import io
import pandas as pd
import tempfile
import os


class ProgressBytesIO(io.BytesIO):
    def __init__(self, data, progress_bar):
        super().__init__(data)
        self.progress_bar = progress_bar

    def read(self, n=-1):
        chunk = super().read(n)
        self.progress_bar.update(len(chunk))
        return chunk


class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def save_input_data_to_file(self, input_data):
        temp_dir = tempfile.mkdtemp()
        file_paths = {}

        for key, value in input_data.items():
            if isinstance(value, pd.DataFrame):
                file_path = os.path.join(temp_dir, f"{key}.parquet")
                value.to_parquet(file_path)
                file_paths[key] = file_path
            else:
                file_path = os.path.join(temp_dir, f"{key}.json")
                with open(file_path, 'w') as f:
                    json.dump(value, f)
                file_paths[key] = file_path

        return file_paths

    def send_files(self, file_paths):
        with tqdm(desc="Uploading files", unit="file") as pbar:
            for key, file_path in file_paths.items():
                with open(file_path, 'rb') as f:
                    buffer = ProgressBytesIO(f.read(), pbar)
                    response = requests.post(f"{self.colab_api_url}/upload/{key}", data=buffer)
                    if response.status_code != 200:
                        raise Exception(f"Error uploading file {key}: {response.text}")

    def execute(self, code, input_data=None):
        if input_data is None:
            input_data = {}

        # Save input_data to temporary files
        file_paths = self.save_input_data_to_file(input_data)

        # Send the files to the server
        self.send_files(file_paths)

        # Execute the code
        data = {'code': code}
        try:
            response = requests.post(f"{self.colab_api_url}/execute", json=data)
            results = response.json()
            return results
        except Exception as e:
            return {'error': str(e)}

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

