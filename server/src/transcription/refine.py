from server.src.constants import SUMMARY_FILE, REFINED_SUMMARY_FILE
from server.src.models.causal_inference import generate

system_prompt = """
# Context
You are an expert in dungeons and dragons. You will be given a summary of a session by an LLM. It may contain some incoherent utterances or sentence structures which may not fit together properly. The summary was based on a transcript, so "I" may refer to different characters.

# Objective
You will edit the summary to be more coherent.
You will include as much information as possible, but not include any facts or events not supported by the summary.
Try to determine who "I" refers to in each part of the summary, and rewrite accordingly.

You will expand on parts of the summary by describing any rules, spells, or mechanics mentioned 

# Style
Write a detailed summary

# Tone
Neutral and matter-of-fact.

# Audience
Someone who missed out on the session, and would like the to learn the most relevant plot points

# Response format
Respond in a few paragraphs.
"""

from pathlib import Path

def refine():
    summary = Path(SUMMARY_FILE).read_text()
    conversation = [{
        "role": "system",
        "content": system_prompt
    }, {
        "role": "user",
        "content": summary
    }]
    refined = generate(conversation,
        do_sample = True,
        temperature = 0.3,
        top_p = 0.9,
        repetition_penalty = 1.15,
        min_new_tokens=200
    )
    Path(REFINED_SUMMARY_FILE).write_text(refined)
