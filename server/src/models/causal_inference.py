from server.src.constants import DEVICE
from server.src.models.load_model import load_peft_model

model, tokenizer = load_peft_model("meta-llama/Llama-3.2-3B-Instruct", "nightfury2986/llama323-dnd-finetuned", "causal")

def generate(conversation, **kwargs):
    inputs = tokenizer.apply_chat_template(
        conversation,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    ).to(DEVICE)

    input_length = len(inputs[0])
    outputs = model.generate(
        inputs=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=2048,
        pad_token_id=tokenizer.eos_token_id,
        **kwargs
    )
    generated_tokens = outputs[0][input_length:]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)
