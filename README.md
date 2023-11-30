


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sagemaker_huggingface_inference_toolkit import handler, defaults

def model_fn(model_dir):
    tokenizer = AutoTokenizer.from_pretrained("epfl-llm/meditron-70B")
    model = AutoModelForCausalLM.from_pretrained("epfl-llm/meditron-70B")
    return model

def transform_fn(model, input_data, content_type, accept_type):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if content_type == defaults.JSON_CONTENT_TYPE:
        input_data = handler.decode_json_input(input_data, content_type)
    
    inputs = tokenizer(input_data["text"], return_tensors="pt", max_length=512, truncation=True)
    inputs = {key: tensor.to(device) for key, tensor in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    return handler.encode_json_output(outputs)

if __name__ == "__main__":
    handler._initialize()

