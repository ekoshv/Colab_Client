import requests
import pickle

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

        pickled_input_data = pickle.dumps(input_data)
        files = {
            'input_data': ('input_data.pkl', pickled_input_data),
            'code': ('code.py', code)
        }

        try:
            response = requests.post(self.colab_api_url, files=files)
            print(f"Response status code: {response.status_code}")  # Debugging print
            print(f"Response content: {response.content}")  # Debugging print
            results = pickle.loads(response.content)
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
