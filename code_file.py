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