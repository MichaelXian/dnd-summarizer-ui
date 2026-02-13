from pathlib import Path

from huggingface_hub import login
from server.src.constants import HF_TOKEN, TRANSCRIPT_FILE, CHUNKS_FILE, REFINED_SUMMARY_FILE
from server.src.rag.inference import get_rag_model
from server.src.state import state, Status


def init():
    state.status = Status.AWAITING_DATA
    login(HF_TOKEN)
    if Path(TRANSCRIPT_FILE).exists() and Path(REFINED_SUMMARY_FILE).exists() and Path(CHUNKS_FILE).exists():
        state.status = Status.READY
        state.rag_model = get_rag_model()