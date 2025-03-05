import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from transformers import TFAutoModelForCausalLM, AutoTokenizer
import tensorflow as tf
with tf.device('/GPU:1'):
# Load the tokenizer and model using TensorFlow
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForCausalLM.from_pretrained(model_name)

# Encode input text
prompt = "Once upon a time, in a land far away"
input_ids = tokenizer(prompt, return_tensors="tf").input_ids

# Generate text
output = model.generate(input_ids, max_length=50)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_text)
