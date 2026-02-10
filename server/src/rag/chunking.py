import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from server.src.constants import SUMMARIZATION_MODEL, DEVICE, TRANSCRIPT_FILE, CHUNKS_FILE
from server.src.summarization.summarize import summarize

tokenizer = AutoTokenizer.from_pretrained(SUMMARIZATION_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZATION_MODEL).to(DEVICE)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def token_length(tokens) -> int:
    return len(tokens.input_ids)

def chunk_text(lines: list[str], max_tokens: int =128, min_overlap: int =64) -> list[list[str]]:
    tokens = [tokenizer(line) for line in lines]
    for token in tokens:
        if token_length(token) > max_tokens:
            raise ValueError("Line has more tokens than max tokens")

    chunks = []
    start = next_start = end = curr_length = 0

    while end < len(tokens):
        while end < len(tokens) and (curr_length + token_length(tokens[end])) <= max_tokens:
            curr_length = curr_length + token_length(tokens[end])
            end += 1
            if max_tokens - curr_length >= min_overlap:
                next_start = end
        chunks.append([tokenizer.decode(token.input_ids, skip_special_tokens=True) for token in tokens[start:end]])
        start = end = next_start
        curr_length = 0

    return chunks

def generate_chunks() -> None:
    transcript = Path(TRANSCRIPT_FILE).read_text().split("\n")
    chunks = chunk_text(transcript)
    summarized_chunks = {
        summarize("\n".join(chunk)): chunk
        for chunk in chunks
    }
    Path(CHUNKS_FILE).write_text(json.dumps(summarized_chunks))