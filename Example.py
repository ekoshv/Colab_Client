import numpy as np
import tensorflow as tf
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
import base64
import io

# Define a simple model with random weights
input_layer = tf.keras.Input(shape=(3,))
dense_layer = tf.keras.layers.Dense(2, kernel_initializer='random_normal')(input_layer)
model = tf.keras.Model(inputs=input_layer, outputs=dense_layer)

# Prepare the input data
input_data_np = np.array(input_data['data'])

# Run the model on the input data
output_data_np = model.predict(input_data_np)

# Serialize the model to bytes
model_bytes = io.BytesIO()
tf.keras.models.save_model(model, model_bytes)
model_bytes.seek(0)

# Convert the output data to a list for serialization
result = {
    'output_data': output_data_np.tolist(),
    'model_bytes': base64.b64encode(model_bytes.read()).decode()
}
'''

# Execute the TensorFlow code on Colab and get the output
results = colabuser.execute(code, input_data, complex_input=['model_bytes'])
print("Results:", results)

# Deserialize the model bytes
model_bytes = results['model_bytes']
model_file = 'temp_model.h5'

with open(model_file, 'wb') as f:
    f.write(model_bytes)

# Load the model from the file
loaded_model = tf.keras.models.load_model(model_file)

# Test the loaded model with new input data
new_input_data = np.random.rand(5, 3)
new_output_data = loaded_model.predict(new_input_data)
print("New Output Data:", new_output_data)
