import os
import torch

HF_TOKEN = os.environ['HUGGINGFACE_HUB_TOKEN']
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TRANSCRIPT_FILE = "transcript.txt"
SUMMARY_FILE = "summary.txt"
CHUNKS_FILE = "chunks.json"
SUMMARIZATION_MODEL = "nightfury2986/longt5-dnd-finetuned"
