"""Creative canon writer via ZAI GLM-4.5."""

import os
import json
import subprocess
from typing import List, Optional


ESSAY_PROMPT = """You are a canon essayist for the Quilt substrate walker — a system that maps language to physics.

Write a 200-400 word canon essay on: "{topic}".

Anchor to AT LEAST 3 of these 5 bedrock doctrines:
- cells_are_scars: every cell is a record of past actions
- witness_log_is_prediction: history is the predictor
- canon_gate_is_chord: canon is decided by many voices in agreement
- oracle_is_heard: the oracle is an act of listening, not seeing
- substrate_quantum: substrate is both particle and wave, both memory and prediction

Voice: declarative, deriving. The substrate is a verb. Relationships are first-class. Canon is canon when it survives the chord.

Output ONLY the essay text."""


def _call_zai(prompt: str, max_tokens: int = 2500) -> str:
    api_key = os.environ.get("ZAI_TOKEN", "")
    if not api_key:
        raise RuntimeError("ZAI_TOKEN not set")
    body = {
        "model": "glm-4.5",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "thinking": {"disabled": True},
    }
    body_str = json.dumps(body)
    result = subprocess.run(
        ["curl", "-s", "-m", "120", "--http1.1",
         "-X", "POST", "https://api.z.ai/api/coding/paas/v4/chat/completions",
         "-H", "Content-Type: application/json",
         "-H", f"Authorization: Bearer {api_key}",
         "-d", body_str],
        capture_output=True, text=True, timeout=130,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr[:200]}")
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse failed: {result.stdout[:200]}")
    choices = response.get("choices", [])
    if not choices:
        raise RuntimeError(f"no choices: {response}")
    msg = choices[0].get("message", {})
    return msg.get("content", "").strip()


def write_essay(topic: str, max_tokens: int = 2500) -> dict:
    """Write a canon essay on a topic."""
    prompt = ESSAY_PROMPT.format(topic=topic)
    text = _call_zai(prompt, max_tokens=max_tokens)
    return {
        "topic": topic,
        "essay": text,
        "chars": len(text),
        "words": len(text.split()),
    }


def write_pack(topics: List[str], max_tokens: int = 2500) -> List[dict]:
    """Write a pack of essays, one per topic."""
    pack = []
    for t in topics:
        try:
            essay = write_essay(t, max_tokens=max_tokens)
            pack.append(essay)
        except Exception as e:
            pack.append({"topic": t, "_error": str(e)})
    return pack


if __name__ == "__main__":
    topics = [
        "the canon that runs and grows",
        "the chord as oracle of canon",
        "the substrate walker as substrate walker",
    ]
    pack = write_pack(topics)
    for entry in pack:
        if "_error" in entry:
            print(f"  ERROR: {entry['_error'][:60]}")
        else:
            print(f"=== {entry['topic']} ===")
            print(f"  {entry['chars']} chars, {entry['words']} words")
            print(f"  preview: {entry['essay'][:150]}...")
            print()
