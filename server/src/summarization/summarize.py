import torch
from pathlib import Path

from server.src.constants import TRANSCRIPT_FILE, SUMMARY_FILE, T5_MAX_TOKENS, DEVICE
from server.src.models.load_model import load_peft_model

model, tokenizer = load_peft_model("google/long-t5-tglobal-base", "nightfury2986/longt5-dnd-finetuned", "seq2seq")

def get_token_length(document):
    all_tokens = tokenizer.encode(document, add_special_tokens=False)
    return len(all_tokens)

def summarize(prompt, max_new_tokens):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=T5_MAX_TOKENS
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            num_beams=4,
            length_penalty=2.0,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary

def summarize_document(document,
                       max_input_tokens=2048,
                       chunk_overlap=200):
    tokenizer.padding_side = "left"
    tokenizer.truncation_side = "right"

    all_tokens = tokenizer.encode(document, add_special_tokens=False)
    chunks = []

    start = end = 0
    while end < len(all_tokens):
        end = min(start + max_input_tokens, len(all_tokens))
        chunk_tokens = all_tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - chunk_overlap  # overlap to avoid splitting sentences

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"{i}/{len(chunks)}: {get_token_length(chunk)} tokens")
        prompt = "summarize: " + chunk
        summary = summarize(prompt, T5_MAX_TOKENS // 8)
        chunk_summaries.append(summary)

    return chunk_summaries

def summarize_transcript() -> None:
    summaries = Path(TRANSCRIPT_FILE).read_text()
    while get_token_length(summaries) > T5_MAX_TOKENS:
        summaries = "\n".join(summarize_document(summaries))

    combined_prompt = "summarize: " + "\n".join(summaries)
    summary = summarize(combined_prompt, T5_MAX_TOKENS // 4)
    Path(SUMMARY_FILE).write_text(summary)