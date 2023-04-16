import base64
import pickle
import requests
import json

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def serialize_data(self, data):
        """Serialize data using pickle and encode it with base64."""
        serialized_data = pickle.dumps(data)
        return base64.b64encode(serialized_data).decode('utf-8')

    def deserialize_data(self, data_str):
        """Decode base64 data and deserialize it using pickle."""
        decoded_data = base64.b64decode(data_str.encode('utf-8'))
        return pickle.loads(decoded_data)

    def execute(self, code, input_data=None, complex_input=None):
        """
        Execute code on the Colab API and return the result.
        :param code: The code to be executed on the Colab API.
        :param input_data: The input data for the code execution.
        :param complex_input: Complex input data for the code execution.
        :return: The result of the code execution.
        """
        if input_data is None:
            input_data = {}

        if complex_input is not None:
            complex_input_str = self.serialize_data(complex_input)
            input_data['complex_input'] = complex_input_str

        data = {
            'input_data': input_data,
            'code': code
        }

        try:
            response = requests.post(self.colab_api_url, json=data)
            results = response.json()

            if 'complex_result' in results:
                results['result'] = self.deserialize_data(results['complex_result'])

            return results
        except Exception as e:
            return {'error': str(e)}

    def execute_from_file(self, file_path, input_data=None, complex_input=None):
        """
        Execute code from a file on the remote Google Colab instance.
        :param file_path: The path to the file containing the code.
        :param input_data: Optional input data to be used in the code execution.
        :param complex_input: Complex input data for the code execution.
        :return: The result of the code execution.
        """
        with open(file_path, 'r') as code_file:
            code = code_file.read()

        if input_data is None:
            input_data = {}

        return self.execute(code, input_data, complex_input)
