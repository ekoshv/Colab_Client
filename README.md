# Colab Remote

Colab Remote is a Python library that allows users to execute code remotely on Google Colab instances from their local machines. It simplifies the process of sending input data and code to Colab, where the code is executed and the results are returned to the local machine.

## Installation

There are two methods to install the `colab_remote` library:

### 1. From a Git Repository

pip install --upgrade --no-cache-dir git+https://github.com/ekoshv/Colab_Client.git

### 2. From Source
To install the library from the source, first clone the repository or download the source code, then navigate to the root directory of the library and run:

bash
pip install .

## Usage
To use the colab_remote library, first, set up a Colab instance with the REST API in the Colab side library (other library). Once the API is running, follow these steps indicated in the example. The example uses the colab_remote library to execute a simple TensorFlow model on Google Colab. The model takes random input data and produces random outputs. The TensorFlow code and input data are sent to the Colab API, and the model's output is returned and printed on the local machine.
