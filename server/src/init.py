from torch import login
from server.src.constants import HF_TOKEN


def init():
    login(HF_TOKEN)