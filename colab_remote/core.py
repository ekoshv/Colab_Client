import requests
import json
from tqdm import tqdm
from io import BytesIO


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

        data = {
            'input_data': input_data,
            'code': code
        }

        try:
            # Wrap the data in a BytesIO buffer for tqdm
            buffer = BytesIO(json.dumps(data).encode())
            total_size = len(buffer.getvalue())

            def progress_bar(bytes_sent):
                nonlocal total_size
                tqdm.write(f"Uploaded: {bytes_sent}/{total_size} bytes")
                return bytes_sent

            # Use the progress bar with the tqdm library
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="Uploading data") as pbar:
                response = requests.post(self.colab_api_url, data=buffer, headers={'Content-Type': 'application/json'}, hooks={'response': [progress_bar]})
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
