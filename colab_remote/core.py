import requests
import json
import os
import tempfile
from io import BytesIO
from tqdm import tqdm
from functools import partial

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def progress_bar(self, pbar):
        """
        Create a progress bar callback for the requests library.
        :param pbar: The tqdm progress bar instance.
        :return: The custom hook function for the progress bar.
        """
        def hook(response, *args, **kwargs):
            nonlocal pbar
            total_size = int(response.headers.get("Content-Length", 0))
            pbar.total = total_size
            pbar.refresh()

            for chunk in response.iter_content(chunk_size=8192):
                pbar.update(len(chunk))
                yield chunk

        return hook

    def execute(self, code, input_data=None):
        """
        Execute code on the Colab API and return the result.
        :param code: The code to be executed on the Colab API.
        :param input_data: The input data for the code execution.
        :return: The result of the code execution.
        """
        if input_data is None:
            input_data = {}

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Save input_data to temporary files
            file_paths = []
            for key, value in input_data.items():
                file_name = f"{key}.parquet" if isinstance(value, pd.DataFrame) else f"{key}.json"
                file_path = os.path.join(tmp_dir, file_name)

                if isinstance(value, pd.DataFrame):
                    value.to_parquet(file_path)
                else:
                    with open(file_path, "w") as f:
                        json.dump(value, f)

                file_paths.append(file_path)

            # Upload the files to the Colab API
            files = [("input_data", (os.path.basename(file_path), open(file_path, "rb"))) for file_path in file_paths]

            with tqdm(total=0, unit='B', unit_scale=True, desc="Uploading data") as pbar:
                response = requests.post(self.colab_api_url, data={'code': code}, files=files, stream=True)
                results = json.loads(''.join(map(lambda x: x.decode(), self.progress_bar(pbar)(response))))
                return results
