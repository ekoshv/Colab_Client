import json
import os
import tempfile
from contextlib import ExitStack
from functools import partial

import pandas as pd
import requests
from tqdm import tqdm

class ColabRemote:
    def __init__(self, colab_api_url):
        self.colab_api_url = colab_api_url

    def progress_bar(self, pbar):
        def update_to(value, total):
            if total is not None and pbar.total != total:
                pbar.total = total
            pbar.update(value)

        def update_hook(response, *args, **kwargs):
            total_size = response.headers.get('Content-Length', 0)
            if total_size:
                total_size = int(total_size)
            pbar.total = total_size
            response.raw.read = partial(response.raw.read, hooks={'response': partial(update_to, total=total_size)})
            return response

        return update_hook

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
            with tqdm(total=0, unit='B', unit_scale=True, desc="Uploading data") as pbar:
                with ExitStack() as stack:
                    files = [("input_data", (os.path.basename(file_path), stack.enter_context(open(file_path, "rb")))) for file_path in file_paths]
                    response = requests.post(self.colab_api_url, data={'code': code}, files=files, stream=True)
                results = json.loads(''.join(map(lambda x: x.decode(), self.progress_bar(pbar)(response))))
                return results
