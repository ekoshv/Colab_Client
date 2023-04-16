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

# Save the model for serialization
result = model
'''

# Execute the TensorFlow code on Colab and get the output
results = colabuser.execute(code, input_data)

if 'error' in results:
    print("Error:", results['error'])
else:
    # Load the returned model
    model = results['result']

    # Use the model to make predictions on new data
    new_input_data = np.random.rand(5, 3)
    output_data = model.predict(new_input_data)
    print("Predictions on new data:", output_data)
