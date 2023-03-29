import numpy as np
from colab_remote import ColabRemote

# Replace this with the public URL of your Colab API
colab_api_url = 'http://your-colab-api-url.ngrok.io/execute'
colabuser = ColabRemote(colab_api_url)

# Prepare the input data: a random array of shape (5, 3)
input_data = {
    'data': np.random.rand(5, 3).tolist()
}

# Define the TensorFlow code to be executed on Colab
code = '''
import tensorflow as tf
import numpy as np

# Define a simple model with random weights
input_layer = tf.keras.Input(shape=(3,))
dense_layer = tf.keras.layers.Dense(2, kernel_initializer='random_normal')(input_layer)
model = tf.keras.Model(inputs=input_layer, outputs=dense_layer)

# Prepare the input data
input_data_np = np.array(input_data['data'])

# Run the model on the input data
output_data_np = model.predict(input_data_np)

# Convert the output data to a list for serialization
result = output_data_np.tolist()
'''

# Execute the TensorFlow code on Colab and get the output
results = colabuser.execute(code, input_data)
print("Results:", results)

input_data = {
    # Your input data here
}

file_path = 'code_file.py'

results = colabuser.execute_from_file(file_path, input_data)
print(results)
