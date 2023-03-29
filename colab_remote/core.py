import requests
import json


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
            response = requests.post(self.colab_api_url, json=data)
            results = response.json()
            return results
        except Exception as e:
            return {'error': str(e)}