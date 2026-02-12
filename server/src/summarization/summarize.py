import torch
from pathlib import Path

from server.src.constants import DEVICE, TRANSCRIPT_FILE, SUMMARY_FILE
from server.src.models.load_model import load_peft_model

model, tokenizer = load_peft_model("google/long-t5-tglobal-base", "nightfury2986/longt5-dnd-finetuned", "seq2seq")


def summarize(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_length=1024,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            early_stopping=True
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
    for chunk in chunks:
        prompt = "summarize: " + chunk
        summary = summarize(prompt)
        chunk_summaries.append(summary)

    return chunk_summaries

def summarize_transcript() -> None:
    transcript = Path(TRANSCRIPT_FILE).read_text()
    chunked_summaries = summarize_document(transcript)
    combined_prompt = "summarize: " + "\n".join(chunked_summaries)
    summary = summarize(combined_prompt)
    Path(SUMMARY_FILE).write_text(summary)