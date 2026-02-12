from pathlib import Path

from huggingface_hub import login
from server.src.constants import HF_TOKEN, TRANSCRIPT_FILE, SUMMARY_FILE, CHUNKS_FILE
from server.src.rag.inference import get_rag_model
from server.src.state import state, Status


def init():
    state.status = Status.AWAITING_DATA
    login(HF_TOKEN)
    if Path(TRANSCRIPT_FILE).exists() and Path(SUMMARY_FILE).exists() and Path(CHUNKS_FILE).exists():
        state.status = Status.READY
        state.rag_model = get_rag_model()