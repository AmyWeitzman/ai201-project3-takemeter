import os
import json
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

MODEL_DIR = os.path.join(os.path.dirname(__file__), "takemeter-model")

# ---------------------------------------------------------------------------
# Load the fine-tuned model if available; fall back to Groq API otherwise.
# ---------------------------------------------------------------------------
classifier = None
MODEL_SOURCE = None

try:
    from transformers import pipeline
    classifier = pipeline(
        "text-classification",
        model=MODEL_DIR,
        return_all_scores=True,
        device=-1,  # CPU
    )
    MODEL_SOURCE = "fine-tuned DistilBERT (local)"
    print(f"Loaded fine-tuned model from {MODEL_DIR}")
except Exception as exc:
    print(f"Could not load fine-tuned model: {exc}")
    print("Will use Groq API fallback (requires GROQ_API_KEY env var).")
    MODEL_SOURCE = "Groq llama-3.3-70b-versatile (baseline fallback)"

GROQ_SYSTEM_PROMPT = """You are classifying posts from the TopChef community in Reddit (r/TopChef).
Assign each post to exactly one of the following categories.

analysis: The post makes a specific claim and backs it up with concrete evidence (ex: episode details, statistics, cross-season comparisons, or domain expertise) such that the reader can point to the supporting material in the text. Self-reported counts ("I tallied it across 4 seasons") qualify as evidence if the methodology is described, since the reader could in theory replicate it. Posts that present data without stating a conclusion are `discussion`, not `analysis`.

opinion: The post expresses a clear viewpoint or take but asserts rather than argues, the claim is present but little to no concrete evidence is offered to support it.

discussion: The post is not primarily making a claim, it is inviting community participation through a question, hypothetical prompt, or personal experience shared with the group. Posts that build a full argument and then ask "does anyone agree?" are `opinion` — the question must be the point, not a wrapper around a take.

Respond with JSON only, in this exact format:
{"label": "<label>", "confidence": <0.0-1.0>}
Where label is one of: analysis, opinion, discussion
Do not include any other text outside the JSON."""

LABEL_DESCRIPTIONS = {
    "analysis": "Makes a specific claim backed by concrete evidence",
    "opinion": "Expresses a viewpoint without concrete supporting evidence",
    "discussion": "Invites community participation via question or prompt",
}


def classify_with_model(text):
    results = classifier(text[:512])[0]  # list of {label, score} dicts
    best = max(results, key=lambda x: x["score"])
    label = best["label"].lower()
    confidence = best["score"]
    all_scores = {r["label"].lower(): r["score"] for r in results}
    return label, confidence, all_scores


def classify_with_groq(text):
    from groq import Groq
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable not set.")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": GROQ_SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()},
        ],
        temperature=0,
        max_tokens=60,
    )
    raw = response.choices[0].message.content.strip()
    result = json.loads(raw)
    label = result["label"].lower()
    confidence = float(result["confidence"])
    return label, confidence, {}


def classify_post(post_text):
    if not post_text.strip():
        return "—", "—", "—", "Enter a post above and click Classify."

    try:
        if classifier is not None:
            label, confidence, all_scores = classify_with_model(post_text)
            scores_str = "  |  ".join(
                f"{lbl}: {sc:.0%}" for lbl, sc in sorted(all_scores.items())
            )
            detail = f"All scores — {scores_str}"
        else:
            label, confidence, _ = classify_with_groq(post_text)
            detail = f"Using {MODEL_SOURCE}"

        if label not in LABEL_DESCRIPTIONS:
            return "Error", "—", "—", f"Unexpected label: {label}"

        return label, f"{confidence:.0%}", LABEL_DESCRIPTIONS[label], detail

    except Exception as exc:
        return "Error", "—", "—", str(exc)


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------
with gr.Blocks(title="TakeMeter") as demo:
    gr.Markdown(
        "# TakeMeter\n"
        "Classify r/TopChef posts as **analysis**, **opinion**, or **discussion**.\n\n"
    )

    post_input = gr.Textbox(
        label="Post text",
        placeholder="Paste a r/TopChef post here...",
        lines=7,
    )

    classify_btn = gr.Button("Classify", variant="primary")

    with gr.Row():
        label_output = gr.Textbox(label="Label")
        confidence_output = gr.Textbox(label="Confidence")

    classify_btn.click(
        fn=classify_post,
        inputs=post_input,
        outputs=[label_output, confidence_output],
    )

if __name__ == "__main__":
    demo.launch()
