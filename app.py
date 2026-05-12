from flask import Flask, jsonify, render_template, request

from ShopGenie.data_ingestion import data_ingestion
from ShopGenie.retrieval_generation import generation

app = Flask(__name__)

chain = None
chain_boot_error = None


def _boot_chain():
    """Initialize vector store + conversational chain once at startup."""
    global chain, chain_boot_error
    try:
        vstore, _ = data_ingestion(load_existing=True)
        chain = generation(vstore)
        chain_boot_error = None
    except Exception as exc:  # pragma: no cover - defensive startup guard
        chain = None
        chain_boot_error = str(exc)


def _invoke_chain(user_input: str, session_id: str) -> str:
    if chain is None:
        raise RuntimeError(
            "Chat engine is not ready. "
            f"Startup error: {chain_boot_error or 'Unknown error'}"
        )

    result = chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )
    return result["answer"] if isinstance(result, dict) else str(result)


_boot_chain()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok" if chain is not None else "degraded",
            "chain_ready": chain is not None,
            "error": chain_boot_error,
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat_api():
    payload = request.get_json(silent=True) or {}
    user_msg = (payload.get("message") or "").strip()
    session_id = (payload.get("session_id") or "shopgenie_web_user").strip()

    if not user_msg:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        answer = _invoke_chain(user_msg, session_id)
        return jsonify({"answer": answer})
    except Exception as exc:  # pragma: no cover - runtime safety for UI
        return jsonify({"error": str(exc)}), 500


@app.route("/get", methods=["POST"])
def chat_form_compat():
    """Backward-compatible endpoint for simple form posts."""
    user_msg = (request.form.get("msg") or "").strip()
    if not user_msg:
        return "Message cannot be empty.", 400

    try:
        return _invoke_chain(user_msg, "shopgenie_form_user")
    except Exception as exc:  # pragma: no cover - runtime safety for UI
        return f"Error: {exc}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
