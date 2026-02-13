import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

from server.src.constants import CHUNKS_FILE, DEVICE
from server.src.models.causal_inference import generate
from server.src.models.load_model import load_peft_model

model, tokenizer = load_peft_model("meta-llama/Llama-3.2-3B-Instruct", "nightfury2986/llama323-dnd-finetuned", "causal")

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

system_prompt = """
# Context
You are an expert in dungeons and dragons. You will be given excerpts from a transcript of a previous dungeons and dragons session
Not all excerpts may be relevant, you must decide which are most relevant and discard the rest
Excerpts will be delimited by === and a newline

# Objective
Answer the user’s question using **only**:
- The provided excerpts
- General Dungeons & Dragons rules or mechanics when needed for clarification

Expand on the response by describing any rules, spells, or mechanics mentioned in the answer

Do not introduce events, facts, or interpretations not supported by the excerpts.
If the answer is not in the excerpts, say 'Not specified in the session'

# Style
Write a short succinct answer.

# Tone
Neutral and matter-of-fact.

# Audience
Someone who participated in or watched the session, and is inquiring about specifics of the session

# Response format
Respond in a few short sentences, with clarifications on rules or mechanics where necessary.
"""

class RAGModel:
    def __init__(self, summarized_chunks: dict[str, list[str]]):
        self.summarized_chunks = summarized_chunks
        self.transformer = SentenceTransformer("all-MiniLM-L6-v2")
        self.keys = list(summarized_chunks.keys())
        embedded_keys = self.transformer.encode(self.keys)
        dim = embedded_keys.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embedded_keys))


    def __to_text(self, index):
        key = self.keys[index]
        chunk = self.summarized_chunks.get(key)
        return "\n".join(chunk)


    def __rag_query(self, query, k=20):
        query_embedding = self.transformer.encode([query])
        _, indices_list = self.index.search(query_embedding, k)
        indices_list = indices_list.tolist()
        return [self.__to_text(index) for indices in indices_list for index in indices]


    def chat(self, query):
        excerpts = self.__rag_query(query)
        conversation = [{
            "role": "system",
            "content": system_prompt
        }, {
            "role": "system",
            "content": "Excerpts:\n" + "\n===\n".join(excerpts)
        }, {
            "role": "user",
            "content": query
        }]
        return generate(conversation)

def get_rag_model() -> RAGModel:
    summarized_chunks = json.loads(Path(CHUNKS_FILE).read_text())
    return RAGModel(summarized_chunks)