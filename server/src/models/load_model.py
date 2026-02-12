from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
from peft import PeftModel

from server.src.constants import DEVICE

def load_peft_model(base_model_name: str, adapter_name: str, model_type: str):

    if model_type.lower() == "causal":
        model_class = AutoModelForCausalLM
    elif model_type.lower() == "seq2seq":
        model_class = AutoModelForSeq2SeqLM
    else:
        raise ValueError("model_type must be 'causal' or 'seq2seq'")

    tokenizer = AutoTokenizer.from_pretrained(adapter_name)

    base_model = model_class.from_pretrained(
        base_model_name,
        device_map=DEVICE,
        torch_dtype="auto",
    )

    model = PeftModel.from_pretrained(base_model, adapter_name)

    return model, tokenizer