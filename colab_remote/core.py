import requests
import json
import base64

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def execute(self, code, input_data=None, complex_input=None):
        """
        Execute code on the Colab API and return the result.
        :param code: The code to be executed on the Colab API.
        :param input_data: The input data for the code execution.
        :param complex_input: The keys of complex input data in the results.
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

            if complex_input:
                for key in complex_input:
                    results[key] = base64.b64decode(results[key].encode())

            return results
        except Exception as e:
            return {'error': str(e)}

    def execute_from_file(self, file_path, input_data=None, complex_input=None):
        """
        Execute code from a file on the remote Google Colab instance.
        :param file_path: The path to the file containing the code.
        :param input_data: Optional input data to be used in the code execution.
        :param complex_input: The keys of complex input data in the results.
        :return: The result of the code execution.
        """
        with open(file_path, 'r') as code_file:
            code = code_file.read()

        if input_data is None:
            input_data = {}

        return self.execute(code, input_data, complex_input)
