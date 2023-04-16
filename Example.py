import numpy as np
from colab_remote import ColabRemote

# Replace this with the public URL of your Colab API
colab_api_url = 'http://0c5e-34-68-99-166.ngrok.io/execute'
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

# Save the model as a complex object
result = model
'''

# Execute the TensorFlow code on Colab and get the output
results = colabuser.execute(code, input_data, complex_input=None)
print("Results:", results)

# Load the returned model
model = results['result']

# Use the model to make predictions on new data
new_input_data = np.random.rand(5, 3)
output_data = model.predict(new_input_data)
print("Predictions on new data:", output_data)

# Save the TensorFlow code in a file
with open('code_file.py', 'w') as code_file:
    code_file.write(code)

# Execute the code from the file and get the output
results_from_file = colabuser.execute_from_file('code_file.py', input_data, complex_input=None)
print("Results from file:", results_from_file)

# Load the returned model from the file
model_from_file = results_from_file['result']

# Use the model from the file to make predictions on new data
new_input_data_from_file = np.random.rand(5, 3)
output_data_from_file = model_from_file.predict(new_input_data_from_file)
print("Predictions on new data from file:", output_data_from_file)
