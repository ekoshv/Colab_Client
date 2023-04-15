import requests
import pickle

class ColabRemote:
    def __init__(self, colab_api_url):
        """Initialize the ColabRemote class with the given Colab API URL."""
        self.colab_api_url = colab_api_url

    def execute(self, code, input_data=None):
        if input_data is None:
            input_data = {}

        pickled_input_data = pickle.dumps(input_data)
        base64_input_data = base64.b64encode(pickled_input_data)

        data = {
            'input_data': base64_input_data.decode('utf-8'),
            'code': code
        }

        try:
            response = requests.post(self.colab_api_url, json=data)
            base64_results = response.json()['result']
            pickled_results = base64.b64decode(base64_results)
            results = pickle.loads(pickled_results)
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
